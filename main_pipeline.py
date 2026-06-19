import os

import pandas as pd
from openai import OpenAI
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

from recommend_food import get_recommendations

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

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

def generate_llm_prompt(predictions, food_list):
    food_names = ", ".join(food_list) if food_list else "recommended seasonal foods"

    prompt = (
        "You are an empathetic Bangladeshi clinical dietitian. "
        "Write a comforting, professional summary in Bangla (বাংলা) for a pregnant mother. "
        "Use the predicted targets below and the recommended foods list. "
        "Explain clearly why Mola Fish, Lal Shak, or Guava are critical for her pregnancy "
        "based on her high iron needs during the Monsoon season. "
        "Keep the tone supportive and culturally appropriate.\n\n"
        f"Predicted target calories: {predictions['target_calories']}\n"
        f"Predicted iron tier: {predictions['target_iron_tier']}\n"
        f"Recommended foods: {food_names}\n"
    )

    return prompt

def get_llm_response(prompt_text):
    if not OPENAI_API_KEY:
        print("OPENAI_API_KEY is not set")
        return None
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt_text}],
        )
    except Exception as exc:
        print("OpenAI API call failed:", exc)
        return None

    return response.choices[0].message.content

def predict_and_recommend_for_user(new_user_data, current_season):
    regressor, classifier, training_columns, class_labels = train_models()

    new_user_df = pd.DataFrame([new_user_data])
    new_user_encoded = pd.get_dummies(new_user_df[FEATURE_COLUMNS])
    new_user_encoded = new_user_encoded.reindex(columns=training_columns, fill_value=0)

    predicted_calories = regressor.predict(new_user_encoded)[0]
    predicted_class_code = classifier.predict(new_user_encoded)[0]
    predicted_iron_tier = class_labels[predicted_class_code]

    print("Predicted calories:", round(predicted_calories, 2))
    print("Predicted iron tier:", predicted_iron_tier)

    top_foods = get_recommendations(predicted_calories, predicted_iron_tier, current_season)
    food_list = top_foods["food_name_en"].tolist()

    predictions = {
        "target_calories": round(predicted_calories, 2),
        "target_iron_tier": predicted_iron_tier,
    }
    prompt = generate_llm_prompt(predictions, food_list)
    print("\nGenerated LLM prompt:\n")
    print(prompt)

    llm_response = get_llm_response(prompt)
    if llm_response:
        print("\nLLM response:\n")
        print(llm_response)

if __name__ == "__main__":
    example_user = {
        "age": 24,
        "trimester": 2,
        "bmi": 21.5,
        "history_diabetes": 0,
        "history_anemia": 1,
        "maternal_anemia_rate": 38.2,
        "blood_pressure": "Normal",
        "newborn_stunting_risk": "Medium",
    }

    predict_and_recommend_for_user(example_user, "Monsoon")
