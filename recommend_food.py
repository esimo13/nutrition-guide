import pandas as pd

def get_recommendations(predicted_calories, predicted_iron_tier, user_season):
    foods = pd.read_csv("seasonal_foods.csv")

    season_key = str(user_season).strip().casefold()
    foods["_season_key"] = foods["season"].astype(str).str.strip().str.casefold()
    seasonal_foods = foods[foods["_season_key"] == season_key].copy()

    if seasonal_foods.empty:
        raise ValueError(f"No foods found for season: {user_season}")

    if predicted_iron_tier == "High Priority":
        seasonal_foods = seasonal_foods.sort_values(
            by="iron_mg_per_100g", ascending=False
        )

    top_foods = seasonal_foods.head(3)

    print("Recommendations for season:", user_season)
    print("Predicted calories:", predicted_calories)
    print("Predicted iron tier:", predicted_iron_tier)
    print(top_foods[["food_name_en", "season", "iron_mg_per_100g"]])

    return top_foods

if __name__ == "__main__":
    get_recommendations(2400, "High Priority", "Monsoon")
