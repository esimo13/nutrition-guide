import pandas as pd

def main():
    users = pd.read_csv("users.csv")
    regional = pd.read_csv("regional_deficiencies.csv")
    seasonal = pd.read_csv("seasonal_foods.csv")
    targets = pd.read_csv("nutrition_targets.csv")

    merged = users.merge(regional, on="district", how="inner")
    merged = merged.merge(targets, on="user_id", how="inner")

    print("Merged shape:", merged.shape)
    print("Missing values per column:")
    print(merged.isnull().sum())
    print("Merged head:")
    print(merged.head())

    merged.to_csv("cleaned_features.csv", index=False)

if __name__ == "__main__":
    main()
