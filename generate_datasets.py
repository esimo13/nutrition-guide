import random

import pandas as pd

random.seed(42)

NUM_USERS = 200

DISTRICTS = [
    "Dhaka",
    "Khulna",
    "Sylhet",
    "Rajshahi",
    "Barisal",
    "Chittagong",
    "Rangpur",
    "Mymensingh",
]

SEASONS = ["Monsoon", "Winter", "Summer"]

REGIONAL_DATA = {
    "district": DISTRICTS,
    "maternal_anemia_rate": [38.2, 41.5, 46.0, 32.1, 44.2, 35.4, 49.1, 40.3],
    "newborn_stunting_risk": ["Medium", "High", "High", "Medium", "High", "Medium", "High", "High"],
    "soil_zinc_deficiency": [0, 1, 0, 1, 0, 0, 1, 1],
    "water_salinity_level": ["Low", "High", "Low", "Low", "Medium", "Medium", "Low", "Low"],
}

FOOD_LIBRARY = [
    {
        "food_name_en": "Lal Shak",
        "food_name_bn": "লাল শাক",
        "season": "Monsoon",
        "local_availability": "Abundant",
        "price_tier": "Low",
        "primary_nutrient": "Iron",
        "iron_mg_per_100g": 2.5,
        "caloric_density": "Low",
    },
    {
        "food_name_en": "Mola Fish",
        "food_name_bn": "মলা মাছ",
        "season": "Monsoon",
        "local_availability": "Abundant",
        "price_tier": "Medium",
        "primary_nutrient": "Vitamin A",
        "iron_mg_per_100g": 5.7,
        "caloric_density": "Medium",
    },
    {
        "food_name_en": "Guava",
        "food_name_bn": "পেয়ারা",
        "season": "Monsoon",
        "local_availability": "Abundant",
        "price_tier": "Low",
        "primary_nutrient": "Vitamin C",
        "iron_mg_per_100g": 0.3,
        "caloric_density": "Low",
    },
    {
        "food_name_en": "Bottle Gourd (Lau)",
        "food_name_bn": "লাউ",
        "season": "Monsoon",
        "local_availability": "Abundant",
        "price_tier": "Low",
        "primary_nutrient": "Carbohydrates",
        "iron_mg_per_100g": 0.3,
        "caloric_density": "Low",
    },
    {
        "food_name_en": "Bitter Gourd (Korola)",
        "food_name_bn": "করলা",
        "season": "Monsoon",
        "local_availability": "Abundant",
        "price_tier": "Low",
        "primary_nutrient": "Vitamin C",
        "iron_mg_per_100g": 0.7,
        "caloric_density": "Low",
    },
    {
        "food_name_en": "Okra (Dherosh)",
        "food_name_bn": "ঢেঁড়স",
        "season": "Monsoon",
        "local_availability": "Abundant",
        "price_tier": "Low",
        "primary_nutrient": "Vitamin C",
        "iron_mg_per_100g": 0.6,
        "caloric_density": "Low",
    },
    {
        "food_name_en": "Ridge Gourd (Jhinge)",
        "food_name_bn": "ঝিঙে",
        "season": "Monsoon",
        "local_availability": "Abundant",
        "price_tier": "Low",
        "primary_nutrient": "Vitamin C",
        "iron_mg_per_100g": 0.5,
        "caloric_density": "Low",
    },
    {
        "food_name_en": "Snake Gourd (Chichinga)",
        "food_name_bn": "চিচিঙ্গা",
        "season": "Monsoon",
        "local_availability": "Moderate",
        "price_tier": "Low",
        "primary_nutrient": "Vitamin C",
        "iron_mg_per_100g": 0.4,
        "caloric_density": "Low",
    },
    {
        "food_name_en": "Prawn (Chingri)",
        "food_name_bn": "চিংড়ি",
        "season": "Monsoon",
        "local_availability": "Moderate",
        "price_tier": "High",
        "primary_nutrient": "Protein",
        "iron_mg_per_100g": 1.8,
        "caloric_density": "Medium",
    },
    {
        "food_name_en": "Hilsa (Ilish)",
        "food_name_bn": "ইলিশ",
        "season": "Monsoon",
        "local_availability": "Moderate",
        "price_tier": "High",
        "primary_nutrient": "Protein",
        "iron_mg_per_100g": 2.0,
        "caloric_density": "High",
    },
    {
        "food_name_en": "Taro Stem (Kochu Shak)",
        "food_name_bn": "কচু শাক",
        "season": "Monsoon",
        "local_availability": "Moderate",
        "price_tier": "Low",
        "primary_nutrient": "Iron",
        "iron_mg_per_100g": 1.3,
        "caloric_density": "Low",
    },
    {
        "food_name_en": "Corn (Bhutta)",
        "food_name_bn": "ভুট্টা",
        "season": "Monsoon",
        "local_availability": "Abundant",
        "price_tier": "Low",
        "primary_nutrient": "Carbohydrates",
        "iron_mg_per_100g": 0.6,
        "caloric_density": "Medium",
    },
    {
        "food_name_en": "Papaya (Green)",
        "food_name_bn": "কাঁচা পেঁপে",
        "season": "Monsoon",
        "local_availability": "Abundant",
        "price_tier": "Low",
        "primary_nutrient": "Vitamin C",
        "iron_mg_per_100g": 0.4,
        "caloric_density": "Low",
    },
    {
        "food_name_en": "Lentils (Dal)",
        "food_name_bn": "ডাল",
        "season": "Winter",
        "local_availability": "Abundant",
        "price_tier": "Low",
        "primary_nutrient": "Protein",
        "iron_mg_per_100g": 6.5,
        "caloric_density": "High",
    },
    {
        "food_name_en": "Spinach (Palong Shak)",
        "food_name_bn": "পালং শাক",
        "season": "Winter",
        "local_availability": "Abundant",
        "price_tier": "Low",
        "primary_nutrient": "Iron",
        "iron_mg_per_100g": 2.7,
        "caloric_density": "Low",
    },
    {
        "food_name_en": "Sweet Potato",
        "food_name_bn": "মিষ্টি আলু",
        "season": "Winter",
        "local_availability": "Abundant",
        "price_tier": "Low",
        "primary_nutrient": "Carbohydrates",
        "iron_mg_per_100g": 0.6,
        "caloric_density": "Medium",
    },
    {
        "food_name_en": "Cauliflower (Phulkopi)",
        "food_name_bn": "ফুলকপি",
        "season": "Winter",
        "local_availability": "Abundant",
        "price_tier": "Low",
        "primary_nutrient": "Vitamin C",
        "iron_mg_per_100g": 0.4,
        "caloric_density": "Low",
    },
    {
        "food_name_en": "Cabbage (Bandhakopi)",
        "food_name_bn": "বাঁধাকপি",
        "season": "Winter",
        "local_availability": "Abundant",
        "price_tier": "Low",
        "primary_nutrient": "Vitamin C",
        "iron_mg_per_100g": 0.5,
        "caloric_density": "Low",
    },
    {
        "food_name_en": "Tomato",
        "food_name_bn": "টমেটো",
        "season": "Winter",
        "local_availability": "Abundant",
        "price_tier": "Low",
        "primary_nutrient": "Vitamin C",
        "iron_mg_per_100g": 0.3,
        "caloric_density": "Low",
    },
    {
        "food_name_en": "Carrot (Gajor)",
        "food_name_bn": "গাজর",
        "season": "Winter",
        "local_availability": "Abundant",
        "price_tier": "Low",
        "primary_nutrient": "Vitamin A",
        "iron_mg_per_100g": 0.3,
        "caloric_density": "Low",
    },
    {
        "food_name_en": "Beetroot",
        "food_name_bn": "বিট",
        "season": "Winter",
        "local_availability": "Moderate",
        "price_tier": "Medium",
        "primary_nutrient": "Iron",
        "iron_mg_per_100g": 0.8,
        "caloric_density": "Low",
    },
    {
        "food_name_en": "Green Peas (Motor)",
        "food_name_bn": "মটরশুটি",
        "season": "Winter",
        "local_availability": "Abundant",
        "price_tier": "Low",
        "primary_nutrient": "Protein",
        "iron_mg_per_100g": 1.5,
        "caloric_density": "Medium",
    },
    {
        "food_name_en": "Mustard Greens (Shorisha Shak)",
        "food_name_bn": "সরিষা শাক",
        "season": "Winter",
        "local_availability": "Moderate",
        "price_tier": "Low",
        "primary_nutrient": "Iron",
        "iron_mg_per_100g": 2.0,
        "caloric_density": "Low",
    },
    {
        "food_name_en": "Radish (Mula)",
        "food_name_bn": "মূলা",
        "season": "Winter",
        "local_availability": "Abundant",
        "price_tier": "Low",
        "primary_nutrient": "Vitamin C",
        "iron_mg_per_100g": 0.3,
        "caloric_density": "Low",
    },
    {
        "food_name_en": "Potato (Aloo)",
        "food_name_bn": "আলু",
        "season": "Winter",
        "local_availability": "Abundant",
        "price_tier": "Low",
        "primary_nutrient": "Carbohydrates",
        "iron_mg_per_100g": 0.4,
        "caloric_density": "High",
    },
    {
        "food_name_en": "Chicken (Murgi)",
        "food_name_bn": "মুরগি",
        "season": "Winter",
        "local_availability": "Abundant",
        "price_tier": "Medium",
        "primary_nutrient": "Protein",
        "iron_mg_per_100g": 1.3,
        "caloric_density": "High",
    },
    {
        "food_name_en": "Eggs",
        "food_name_bn": "ডিম",
        "season": "Winter",
        "local_availability": "Abundant",
        "price_tier": "Low",
        "primary_nutrient": "Protein",
        "iron_mg_per_100g": 1.2,
        "caloric_density": "High",
    },
    {
        "food_name_en": "Yogurt (Doi)",
        "food_name_bn": "দই",
        "season": "Winter",
        "local_availability": "Moderate",
        "price_tier": "Medium",
        "primary_nutrient": "Calcium",
        "iron_mg_per_100g": 0.1,
        "caloric_density": "Medium",
    },
    {
        "food_name_en": "Chickpeas (Chola)",
        "food_name_bn": "ছোলা",
        "season": "Winter",
        "local_availability": "Abundant",
        "price_tier": "Low",
        "primary_nutrient": "Protein",
        "iron_mg_per_100g": 2.9,
        "caloric_density": "High",
    },
    {
        "food_name_en": "Mango",
        "food_name_bn": "আম",
        "season": "Summer",
        "local_availability": "Abundant",
        "price_tier": "Medium",
        "primary_nutrient": "Vitamin C",
        "iron_mg_per_100g": 0.2,
        "caloric_density": "Medium",
    },
    {
        "food_name_en": "Beef Liver",
        "food_name_bn": "গরুর কলিজা",
        "season": "Summer",
        "local_availability": "Moderate",
        "price_tier": "High",
        "primary_nutrient": "Iron",
        "iron_mg_per_100g": 9.0,
        "caloric_density": "High",
    },
    {
        "food_name_en": "Milk",
        "food_name_bn": "দুধ",
        "season": "Summer",
        "local_availability": "Moderate",
        "price_tier": "Medium",
        "primary_nutrient": "Calcium",
        "iron_mg_per_100g": 0.1,
        "caloric_density": "Medium",
    },
    {
        "food_name_en": "Watermelon (Tormuj)",
        "food_name_bn": "তরমুজ",
        "season": "Summer",
        "local_availability": "Abundant",
        "price_tier": "Low",
        "primary_nutrient": "Vitamin C",
        "iron_mg_per_100g": 0.1,
        "caloric_density": "Low",
    },
    {
        "food_name_en": "Pineapple (Anarosh)",
        "food_name_bn": "আনারস",
        "season": "Summer",
        "local_availability": "Moderate",
        "price_tier": "Medium",
        "primary_nutrient": "Vitamin C",
        "iron_mg_per_100g": 0.2,
        "caloric_density": "Low",
    },
    {
        "food_name_en": "Coconut (Narikel)",
        "food_name_bn": "নারিকেল",
        "season": "Summer",
        "local_availability": "Moderate",
        "price_tier": "Medium",
        "primary_nutrient": "Carbohydrates",
        "iron_mg_per_100g": 0.4,
        "caloric_density": "Medium",
    },
    {
        "food_name_en": "Banana (Kola)",
        "food_name_bn": "কলা",
        "season": "Summer",
        "local_availability": "Abundant",
        "price_tier": "Low",
        "primary_nutrient": "Carbohydrates",
        "iron_mg_per_100g": 0.3,
        "caloric_density": "Medium",
    },
    {
        "food_name_en": "Litchi (Litchu)",
        "food_name_bn": "লিচু",
        "season": "Summer",
        "local_availability": "Moderate",
        "price_tier": "High",
        "primary_nutrient": "Vitamin C",
        "iron_mg_per_100g": 0.1,
        "caloric_density": "Low",
    },
    {
        "food_name_en": "Cucumber (Shosha)",
        "food_name_bn": "শসা",
        "season": "Summer",
        "local_availability": "Abundant",
        "price_tier": "Low",
        "primary_nutrient": "Vitamin C",
        "iron_mg_per_100g": 0.3,
        "caloric_density": "Low",
    },
    {
        "food_name_en": "Rice (Chal)",
        "food_name_bn": "চাল",
        "season": "Summer",
        "local_availability": "Abundant",
        "price_tier": "Low",
        "primary_nutrient": "Carbohydrates",
        "iron_mg_per_100g": 0.3,
        "caloric_density": "High",
    },
    {
        "food_name_en": "Rui Fish",
        "food_name_bn": "রুই মাছ",
        "season": "Summer",
        "local_availability": "Abundant",
        "price_tier": "Medium",
        "primary_nutrient": "Protein",
        "iron_mg_per_100g": 1.0,
        "caloric_density": "Medium",
    },
]


def clamp(value, low, high):
    return max(low, min(high, value))


def weighted_choice(options, weights):
    total = sum(weights)
    pick = random.uniform(0, total)
    cumulative = 0
    for option, weight in zip(options, weights):
        cumulative += weight
        if pick <= cumulative:
            return option
    return options[-1]


def generate_users():
    rows = []
    for index in range(1, NUM_USERS + 1):
        age = random.randint(18, 40)
        trimester = random.choice([1, 2, 3])
        bmi = round(random.uniform(16.0, 35.0), 1)
        blood_pressure = weighted_choice(["Normal", "High"], [0.78, 0.22])
        history_diabetes = 1 if random.random() < 0.15 else 0
        history_anemia = 1 if random.random() < 0.35 else 0

        rows.append(
            {
                "user_id": f"USR_{index:03d}",
                "age": age,
                "district": random.choice(DISTRICTS),
                "trimester": trimester,
                "bmi": bmi,
                "blood_pressure": blood_pressure,
                "history_diabetes": history_diabetes,
                "history_anemia": history_anemia,
                "current_season": random.choice(SEASONS),
            }
        )
    return pd.DataFrame(rows)


def generate_targets(users_df, regional_df):
    regional_lookup = regional_df.set_index("district")
    targets = []

    for _, row in users_df.iterrows():
        trimester_bonus = (row["trimester"] - 1) * 150
        bmi_adjustment = (row["bmi"] - 21.0) * 20
        base_calories = 2000 + trimester_bonus + bmi_adjustment
        target_calories = int(round(clamp(base_calories, 1800, 2800), -1))

        anemia_rate = regional_lookup.loc[row["district"], "maternal_anemia_rate"]
        high_priority = (
            row["history_anemia"] == 1
            or row["bmi"] < 18.5
            or anemia_rate >= 40
        )
        target_iron_tier = "High Priority" if high_priority else "Standard"

        targets.append(
            {
                "user_id": row["user_id"],
                "target_calories": target_calories,
                "target_iron_tier": target_iron_tier,
                "restrict_sugar": 1 if row["history_diabetes"] == 1 else 0,
                "restrict_sodium": 1 if row["blood_pressure"] == "High" else 0,
            }
        )

    return pd.DataFrame(targets)


def generate_foods():
    foods = []
    for index, item in enumerate(FOOD_LIBRARY, start=1):
        base = item.copy()
        base["food_id"] = f"FOOD_{index:02d}"
        foods.append(base)

    return pd.DataFrame(foods)


df_users = generate_users()
df_users.to_csv("users.csv", index=False)

df_regional = pd.DataFrame(REGIONAL_DATA)
df_regional.to_csv("regional_deficiencies.csv", index=False)

df_foods = generate_foods()
df_foods.to_csv("seasonal_foods.csv", index=False)

df_targets = generate_targets(df_users, df_regional)
df_targets.to_csv("nutrition_targets.csv", index=False)

print("All custom thesis datasets generated successfully in your directory!")