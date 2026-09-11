import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt

df = pd.read_csv("device_sustainability_deduped.csv")
print(df.head())

df = df.drop(
    columns=[
        "model",
        "source_type",
        "manufacturing_emissions_kg_co2e",
        "recycled_material_percentage",
    ],
    errors="ignore",
)

print(df.isnull().sum())

df = df.dropna(subset=["reported_age_years_avg"])

numeric_columns = df.select_dtypes(include=["int64", "float64"]).columns

for col in numeric_columns:
    if col != "reported_age_years_avg":
        df[col] = df[col].fillna(df[col].median())

categorical_columns = df.select_dtypes(include="object").columns

for col in categorical_columns:
    df[col] = df[col].fillna(df[col].mode()[0])

print(df.isnull().sum())

df = pd.get_dummies(
    df,
    columns=categorical_columns,
    drop_first=True
)

print(df.head())

X = df.drop(columns=["reported_age_years_avg"])
y = df["reported_age_years_avg"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

linear_model = LinearRegression()
decision_tree = DecisionTreeRegressor(random_state=42)
random_forest = RandomForestRegressor(random_state=42)

for _ in range(10):
    linear_model.fit(X_train, y_train)
    decision_tree.fit(X_train, y_train)
    random_forest.fit(X_train, y_train)

linear_pred = linear_model.predict(X_test)
tree_pred = decision_tree.predict(X_test)
forest_pred = random_forest.predict(X_test)

results = {
    "Linear Regression": {
        "model": linear_model,
        "prediction": linear_pred,
    },
    "Decision Tree": {
        "model": decision_tree,
        "prediction": tree_pred,
    },
    "Random Forest": {
        "model": random_forest,
        "prediction": forest_pred,
    },
}

best_model = None
best_mae = float("inf")
best_name = ""

for name, result in results.items():
    prediction = result["prediction"]

    mae = mean_absolute_error(y_test, prediction)
    rmse = np.sqrt(mean_squared_error(y_test, prediction))
    r2 = r2_score(y_test, prediction)

    print(f"\n{name}")
    print(f"MAE: {mae:.3f}")
    print(f"RMSE: {rmse:.3f}")
    print(f"R²: {r2:.3f}")

    if mae < best_mae:
        best_mae = mae
        best_model = result["model"]
        best_name = name

print(f"\nBest Model: {best_name}")
print(f"Best MAE: {best_mae:.3f}")

joblib.dump(best_model, "best_model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("Best model saved as 'best_model.pkl'")
print("Scaler saved as 'scaler.pkl'")

importance = random_forest.feature_importances_

importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": importance
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

plt.figure(figsize=(10,6))
plt.barh(
    importance_df["Feature"][:10],
    importance_df["Importance"][:10]
)
plt.xlabel("Importance")
plt.title("Top 10 Most Important Features")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

plt.figure(figsize=(6,6))
plt.scatter(y_test, forest_pred)
plt.xlabel("Actual Average Age")
plt.ylabel("Predicted Average Age")
plt.title("Actual vs Predicted Average Age")
plt.plot(
    [y_test.min(), y_test.max()],
    [y_test.min(), y_test.max()],
    "r--"
)
plt.tight_layout()
plt.show()