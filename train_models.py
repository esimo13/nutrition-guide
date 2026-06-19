import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_absolute_error
from sklearn.model_selection import train_test_split

def main():
    data = pd.read_csv("cleaned_features.csv")

    feature_columns = [
        "age",
        "trimester",
        "bmi",
        "history_diabetes",
        "history_anemia",
        "maternal_anemia_rate",
        "blood_pressure",
        "newborn_stunting_risk",
    ]

    X = pd.get_dummies(data[feature_columns])
    y_reg = data["target_calories"]
    y_class = data["target_iron_tier"].astype("category")
    y_class_codes = y_class.cat.codes

    X_train, X_test, y_reg_train, y_reg_test, y_class_train, y_class_test = train_test_split(
        X,
        y_reg,
        y_class_codes,
        test_size=0.2,
        random_state=42,
    )

    regressor = RandomForestRegressor(random_state=42)
    regressor.fit(X_train, y_reg_train)
    reg_preds = regressor.predict(X_test)
    reg_mae = mean_absolute_error(y_reg_test, reg_preds)

    classifier = RandomForestClassifier(random_state=42)
    classifier.fit(X_train, y_class_train)
    class_preds = classifier.predict(X_test)
    class_accuracy = accuracy_score(y_class_test, class_preds)

    print("Regression (target_calories) MAE:", reg_mae)
    print("Classification (target_iron_tier) Accuracy:", class_accuracy)

if __name__ == "__main__":
    main()
