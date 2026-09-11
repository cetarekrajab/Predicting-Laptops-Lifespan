import pandas as pd
import joblib

# Load original dataset
original_df = pd.read_csv("device_sustainability_deduped.csv")

# Create a copy for preprocessing
df = original_df.copy()

# Remove the same columns used during training
df = df.drop(
    columns=[
        "model",
        "source_type",
        "manufacturing_emissions_kg_co2e",
        "recycled_material_percentage",
    ],
    errors="ignore",
)

# Remove rows with missing target (same as training)
df = df.dropna(subset=["reported_age_years_avg"])

# Fill missing numeric values
numeric_columns = df.select_dtypes(include=["int64", "float64"]).columns

for col in numeric_columns:
    if col != "reported_age_years_avg":
        df[col] = df[col].fillna(df[col].median())

# Fill missing categorical values
categorical_columns = df.select_dtypes(include="object").columns

for col in categorical_columns:
    df[col] = df[col].fillna(df[col].mode()[0])

# One-hot encode categorical columns
df = pd.get_dummies(
    df,
    columns=categorical_columns,
    drop_first=True
)

# Prepare features
X = df.drop(columns=["reported_age_years_avg"])

# Load scaler and model
scaler = joblib.load("scaler.pkl")
model = joblib.load("best_model.pkl")

# Scale features
X_scaled = scaler.transform(X)

# Predict lifespan
predictions = model.predict(X_scaled)

# Add predictions to the ORIGINAL dataset
original_df.loc[df.index, "predicted_life_span"] = predictions.round(2)

# Save the final dataset
original_df.to_csv("final.csv", index=False)

print("Done! Predictions added.")
print("Saved as final.csv")