#Importing libraries
import sys
from datetime import datetime
import pandas as pd

#Defining constants
INPUT_FILE = "device_sustainability.csv"
OUTPUT_FILE = "device_sustainability_deduped.csv"
NUMERIC_COLUMNS = [
    "release_year",
    "cpu_tdp_w",
    "gpu_tdp_w",
    "ram_gb",
    "storage_capacity_gb",
    "battery_capacity_wh",
    "battery_life_hours",
    "display_size_inches",
    "weight_kg",
    "repairability_score",
    "price_usd",
    "reported_age_years_avg",
]
YES_NO_COLUMNS = [
    "battery_replaceable",
    "ram_upgradeable",
    "storage_upgradeable",
]
VALID_GPU_TYPES = {"Dedicated", "Integrated"}
VALID_BOOLEAN = {"Yes", "No"}
LIFESPAN_COLUMN = "reported_age_years_avg"

REQUIRED_COLUMNS = [
    "manufacturer",
    "model",
    "release_year",
    "device_category",
    "cpu_tdp_w",
    "gpu_tdp_w",
    "gpu_type",
    "ram_gb",
    "storage_capacity_gb",
    "storage_type",
    "battery_capacity_wh",
    "battery_life_hours",
    "display_size_inches",
    "weight_kg",
    "repairability_score",
    "price_usd",
    "battery_replaceable",
    "ram_upgradeable",
    "storage_upgradeable",
    "reported_age_years_avg",
    "source_type",
]

print("Loading dataset and running preprocessing checks...")

df = pd.read_csv(INPUT_FILE, keep_default_na=True, na_values=[""])

# Remove leading/trailing spaces from text columns
df = df.apply(
    lambda col: col.str.strip() if col.dtype == "object" else col
)

missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
if missing_columns:
    print("Missing columns:")
    for col in missing_columns:
        print("-", col)
    sys.exit()

# Check for missing manufacturer or model
missing_key = df["manufacturer"].isna() | df["model"].isna()

if missing_key.any():
    print("\nRows with missing manufacturer or model:")
    print(df.loc[missing_key, ["manufacturer", "model"]])
else:
    print("Manufacturer and model columns contain no missing values.")

# Row-wise validation checks
row_validation_errors = []
for idx, row in df.iterrows():
    for col in YES_NO_COLUMNS:
        if pd.notna(row[col]) and row[col] not in VALID_BOOLEAN:
            row_validation_errors.append(
                f"Row {idx + 2}: column '{col}' has invalid Yes/No value ({row[col]})"
            )
    if pd.notna(row["gpu_type"]) and row["gpu_type"] not in VALID_GPU_TYPES:
        row_validation_errors.append(
            f"Row {idx + 2}: column 'gpu_type' has invalid value ({row['gpu_type']})"
        )

if row_validation_errors:
    print("Row validation issues found:")
    for issue in row_validation_errors:
        print(" -", issue)
else:
    print("All rows passed the initial validation checks.")

# Column-level validation for numeric columns
numeric_column_issues = {}
for col in NUMERIC_COLUMNS:
    if col not in df.columns:
        numeric_column_issues[col] = "missing column"
        continue

    coerced = pd.to_numeric(df[col], errors="coerce")
    invalid = df[col].notna() & coerced.isna()
    if invalid.any():
        numeric_column_issues[col] = df.loc[invalid, col].unique().tolist()

    # Keep numeric columns safe for later range checks even when bad values exist.
    df[col] = coerced

if numeric_column_issues:
    print("Numeric column validation issues:")
    for col, values in numeric_column_issues.items():
        print(f" - {col}: invalid values -> {values}")
else:
    print("All numeric columns are numeric.")

# Validate Yes/No columns are text and values
yes_no_issues = {}
for col in YES_NO_COLUMNS:
    if col not in df.columns:
        yes_no_issues[col] = "missing column"
        continue

    invalid = df[col].notna() & ~df[col].isin(VALID_BOOLEAN)
    if invalid.any():
        yes_no_issues[col] = f"{invalid.sum()} invalid values"

if yes_no_issues:
    print("Yes/No column validation issues:")
    for col, issue in yes_no_issues.items():
        print(f" - {col}: {issue}")
else:
    print("Yes/No columns contain only valid values.")

VALID_MANUFACTURERS = {
    "Acer",
    "Apple",
    "ASUS",
    "Dell",
    "Fujitsu",
    "HP",
    "Lenovo",
    "Microsoft",
    "Panasonic",
    "Samsung",
    "Toshiba",
}
invalid = ~df["manufacturer"].isin(VALID_MANUFACTURERS)
if invalid.any():
    print("\nInvalid manufacturers:")
    print(df.loc[invalid, ["manufacturer", "model"]])
else:
    print("Manufacturer values are valid.")

VALID_DEVICE_CATEGORIES = {
    "Business",
    "Chromebook",
    "Consumer",
    "Convertible",
    "Gaming",
    "Premium",
    "Rugged",
    "Ultraportable",
    "Workstation",
}
invalid = ~df["device_category"].isin(VALID_DEVICE_CATEGORIES)
if invalid.any():
    print("\nInvalid device categories:")
    print(df.loc[invalid, ["manufacturer", "model", "device_category"]])
else:
    print("Device category values are valid.")

VALID_STORAGE_TYPES = {
    "PCIe NVMe SSD",
    "HDD",
    "Hybrid",
    "SATA SSD",
    "eMMC",
}
invalid = ~df["storage_type"].isin(VALID_STORAGE_TYPES)
if invalid.any():
    print("\nInvalid storage types:")
    print(df.loc[invalid, ["manufacturer", "model", "storage_type"]])
else:
    print("Storage type values are valid.")

VALID_SOURCE_TYPES = {
    "Dell Community + Forums",
    "Dell Community",
    "Forums",
    "HP Hardware Forums",
    "MacRumors",
    "MacRumors + Forums",
    "MacRumors + r/macbook",
    "NotebookReview Forums",
    "RuggedPCReview Forums",
    "r/acer",
    "r/acer + Forums",
    "r/asus",
    "r/asus + Forums",
    "r/chromebook",
    "r/dell",
    "r/dell + Forums",
    "r/dell7567 + Forums",
    "r/gaminglaptops",
    "r/hp",
    "r/hp + Forums",
    "r/macbook",
    "r/samsung",
    "r/surface",
    "r/surface + Forums",
    "r/sysadmin + Forums",
    "r/thinkpad",
    "r/thinkpad + Forums",
    "r/筆記型電腦 + Forums",
}
invalid = ~df["source_type"].isin(VALID_SOURCE_TYPES)
if invalid.any():
    print("\nInvalid source types:")
    print(df.loc[invalid, ["manufacturer", "model", "source_type"]])
else:
    print("Source type values are valid.")

# Ensure missing lifespan values appear as NaN
if LIFESPAN_COLUMN in df.columns:
    if not pd.api.types.is_numeric_dtype(df[LIFESPAN_COLUMN]):
        df[LIFESPAN_COLUMN] = pd.to_numeric(df[LIFESPAN_COLUMN], errors="coerce")

    missing_lifespan_count = df[LIFESPAN_COLUMN].isna().sum()
    print(
        f"Missing lifespan values in '{LIFESPAN_COLUMN}': {missing_lifespan_count} "
        "(these appear as NaN after preprocessing)."
    )
else:
    print(f"Missing lifespan check skipped: column '{LIFESPAN_COLUMN}' does not exist.")

CURRENT_YEAR = datetime.now().year
RANGES = {
    "release_year": (2010, CURRENT_YEAR),
    "cpu_tdp_w": (1, 150),
    "gpu_tdp_w": (0, 250),
    "ram_gb": (2, 128),
    "storage_capacity_gb": (32, 8000),
    "battery_capacity_wh": (20, 150),
    "battery_life_hours": (1, 30),
    "display_size_inches": (10, 18),
    "weight_kg": (0.5, 5),
    "repairability_score": (0, 10),
    "price_usd": (299, 10000),
    "reported_age_years_avg": (0, 25),
}
range_errors = False
for column, (minimum, maximum) in RANGES.items():
    invalid = (
        df[column].notna()
        & ((df[column] < minimum) | (df[column] > maximum))
    )
    if invalid.any():
        range_errors = True
        print(f"\nInvalid values in {column}")
        print(df.loc[invalid, ["manufacturer", "model", column]])

if not range_errors:
    print("All numeric values are within valid ranges.")

duplicates = df.duplicated(subset=["manufacturer", "model"], keep=False)
if duplicates.any():
    print("\nDuplicate laptops:")
    print(df.loc[duplicates, ["manufacturer", "model"]])
else:
    print("\nNo duplicate laptops found.")

# Remove duplicate rows and save the cleaned dataset
clean_df = df.drop_duplicates(subset=["manufacturer", "model"], keep="first")
removed_duplicates = len(df) - len(clean_df)

if removed_duplicates > 0:
    print(f"\nRemoved {removed_duplicates} duplicate row(s).")
else:
    print("\nNo duplicate rows were removed.")

clean_df = clean_df[REQUIRED_COLUMNS]
clean_df.to_csv(OUTPUT_FILE, index=False)
print(f"Saved cleaned dataset to '{OUTPUT_FILE}'.")

print("\nDataset Summary")
print(f"Rows: {len(clean_df)}")
print(f"Columns: {len(clean_df.columns)}")

print("\nMissing values by column:")
print(clean_df.isnull().sum())

print("Preprocessing checks completed.")
