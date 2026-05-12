import pandas as pd
import matplotlib.pyplot as plt
import os

# -----------------------------
# CREATE OUTPUT FOLDERS
# -----------------------------
os.makedirs("output/charts", exist_ok=True)

# -----------------------------
# LOAD DATASET (try multiple paths)
# -----------------------------
possible_paths = [
    "data/healthcare_dataset.csv.zip",
    "healthcare_dataset.csv.zip"
]

csv_path = None
for path in possible_paths:
    if os.path.exists(path):
        csv_path = path
        break

if csv_path is None:
    raise FileNotFoundError("CSV file not found in either 'data/' or current folder.")

df = pd.read_csv(csv_path)
print(f"Dataset Loaded Successfully from: {csv_path}")
print("First 5 rows:")
print(df.head())

# -----------------------------
# DATA CLEANING
# -----------------------------

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# Handle missing values (forward fill)
df.fillna(method='ffill', inplace=True)

# Strip column names
df.columns = df.columns.str.strip()

# Clean text columns (remove spaces & standardize case)
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].astype(str).str.strip().str.title()

# -----------------------------
# SAVE CLEANED DATA
# -----------------------------
df.to_csv("output/cleaned_data.csv", index=False)
print("Cleaned data saved successfully!")

# -----------------------------
# GENERATE REPORT
# -----------------------------
report = df.describe(include='all')

with open("output/report.txt", "w") as f:
    f.write("HEALTHCARE DATA REPORT\n\n")
    f.write(str(report))

print("Report generated successfully!")

# -----------------------------
# VISUALIZATION 1: FIRST NUMERIC COLUMN
# -----------------------------
numeric_cols = df.select_dtypes(include='number').columns

if len(numeric_cols) > 0:
    col = numeric_cols[0]

    plt.figure()
    df[col].hist()

    plt.title(f"{col} Distribution")
    plt.xlabel(col)
    plt.ylabel("Frequency")

    plt.savefig(f"output/charts/{col}_distribution.png")
    plt.close()

    print(f"{col} chart created!")

# -----------------------------
# VISUALIZATION 2: CATEGORY COLUMN (if exists)
# -----------------------------
cat_cols = df.select_dtypes(include='object').columns

if len(cat_cols) > 0:
    col = cat_cols[0]

    plt.figure()
    df[col].value_counts().head(10).plot(kind='bar')

    plt.title(f"{col} Count")
    plt.xlabel(col)
    plt.ylabel("Count")

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(f"output/charts/{col}_bar_chart.png")
    plt.close()

    print(f"{col} bar chart created!")

# -----------------------------
# COMPLETION MESSAGE
# -----------------------------
print("DATA CLEANING & REPORTING AUTOMATION COMPLETED SUCCESSFULLY!")
