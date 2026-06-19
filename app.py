import os

import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

from recommend_food import get_recommendations

FEATURE_COLUMNS = [
    "age",
    "trimester",
    "bmi",
    "history_diabetes",
    "history_anemia",
    "maternal_anemia_rate",
    "blood_pressure",
    "newborn_stunting_risk",
]

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

class UserProfile(BaseModel):
    age: int
    district: str
    trimester: int
    bmi: float
    blood_pressure: str
    history_diabetes: int
    history_anemia: int
    current_season: str


def train_models():
    data = pd.read_csv("cleaned_features.csv")

    X = pd.get_dummies(data[FEATURE_COLUMNS])
    y_reg = data["target_calories"]
    y_class = data["target_iron_tier"].astype("category")
    y_class_codes = y_class.cat.codes

    X_train, _, y_reg_train, _, y_class_train, _ = train_test_split(
        X,
        y_reg,
        y_class_codes,
        test_size=0.2,
        random_state=42,
    )

    regressor = RandomForestRegressor(random_state=42)
    regressor.fit(X_train, y_reg_train)

    classifier = RandomForestClassifier(random_state=42)
    classifier.fit(X_train, y_class_train)

    return regressor, classifier, X.columns, y_class.cat.categories


def load_regional_lookup():
    regional = pd.read_csv("regional_deficiencies.csv")
    return regional.set_index("district")


def generate_llm_prompt(predictions, food_list, season):
    food_names = ", ".join(food_list) if food_list else "recommended seasonal foods"

    prompt = (
        "You are an empathetic Bangladeshi clinical dietitian. "
        "Write a comforting, professional summary in Bangla (বাংলা) for a pregnant mother. "
        "Use the predicted targets below and the recommended foods list. "
        "Explain clearly why the recommended foods are critical for her pregnancy "
        f"based on her high iron needs during the {season} season. "
        "Keep the tone supportive and culturally appropriate.\n\n"
        f"Predicted target calories: {predictions['target_calories']}\n"
        f"Predicted iron tier: {predictions['target_iron_tier']}\n"
        f"Recommended foods: {food_names}\n"
    )

    return prompt


def get_llm_response(prompt_text):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not set")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt_text}],
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"OpenAI API call failed: {exc}")

    return response.choices[0].message.content


REGIONAL_LOOKUP = load_regional_lookup()
REGRESSOR, CLASSIFIER, TRAINING_COLUMNS, CLASS_LABELS = train_models()


def build_feature_row(profile: UserProfile):
    if profile.district not in REGIONAL_LOOKUP.index:
        raise HTTPException(status_code=400, detail="Unknown district")

    regional_row = REGIONAL_LOOKUP.loc[profile.district]

    return {
        "age": profile.age,
        "trimester": profile.trimester,
        "bmi": profile.bmi,
        "history_diabetes": profile.history_diabetes,
        "history_anemia": profile.history_anemia,
        "maternal_anemia_rate": regional_row["maternal_anemia_rate"],
        "blood_pressure": profile.blood_pressure,
        "newborn_stunting_risk": regional_row["newborn_stunting_risk"],
    }


@app.post("/api/recommend")
async def recommend(user: UserProfile):
    feature_row = build_feature_row(user)

    new_user_df = pd.DataFrame([feature_row])
    new_user_encoded = pd.get_dummies(new_user_df[FEATURE_COLUMNS])
    new_user_encoded = new_user_encoded.reindex(columns=TRAINING_COLUMNS, fill_value=0)

    predicted_calories = REGRESSOR.predict(new_user_encoded)[0]
    predicted_class_code = CLASSIFIER.predict(new_user_encoded)[0]
    predicted_iron_tier = CLASS_LABELS[predicted_class_code]

    try:
        top_foods = get_recommendations(
            predicted_calories, predicted_iron_tier, user.current_season
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    food_list = top_foods["food_name_en"].tolist()

    predictions = {
        "target_calories": round(predicted_calories, 2),
        "target_iron_tier": predicted_iron_tier,
    }
    prompt = generate_llm_prompt(predictions, food_list, user.current_season)
    llm_response = get_llm_response(prompt)

    return {
        "response": llm_response,
        "predicted_calories": predictions["target_calories"],
        "predicted_iron_tier": predictions["target_iron_tier"],
        "recommended_foods": food_list,
    }


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
