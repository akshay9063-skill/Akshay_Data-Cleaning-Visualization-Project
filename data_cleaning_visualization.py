"""
Data Cleaning & Visualization Project
Dataset: synthetic sample retail sales data generated for this project.
Run: python data_cleaning_visualization.py
Dependencies: pandas, numpy, matplotlib
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "dataset" / "raw_sales_data.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
CHART_DIR = BASE_DIR / "visualizations"
OUTPUT_DIR.mkdir(exist_ok=True)
CHART_DIR.mkdir(exist_ok=True)

# 1. Load data
df = pd.read_csv(DATA_PATH)
print("Original dataset shape:", df.shape)
print("\\nMissing values before cleaning:\\n", df.isna().sum())
print("Duplicate rows before cleaning:", df.duplicated().sum())

# 2. Remove exact duplicate rows
df = df.drop_duplicates().copy()

# 3. Convert data types and fill missing values
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce")
df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
df["Product"] = df["Product"].fillna("Unknown")
df["Region"] = df["Region"].fillna("Unknown")
df["Quantity"] = df["Quantity"].fillna(df["Quantity"].median())
df["Unit_Price"] = df["Unit_Price"].fillna(df["Unit_Price"].median())

# Recalculate Sales so it is consistent with Quantity * Unit_Price
df["Sales"] = df["Quantity"] * df["Unit_Price"]

# 4. Detect and cap sales outliers using the IQR rule
q1 = df["Sales"].quantile(0.25)
q3 = df["Sales"].quantile(0.75)
iqr = q3 - q1
upper_bound = q3 + 1.5 * iqr
lower_bound = max(0, q1 - 1.5 * iqr)
outlier_count = int(((df["Sales"] < lower_bound) | (df["Sales"] > upper_bound)).sum())
df["Sales"] = df["Sales"].clip(lower=lower_bound, upper=upper_bound)

# 5. Save cleaned data and summary
df["Order_Date"] = df["Order_Date"].dt.strftime("%Y-%m-%d")
clean_path = OUTPUT_DIR / "cleaned_sales_data.csv"
df.to_csv(clean_path, index=False)

summary = df.groupby("Product", dropna=False)["Sales"].agg(["sum", "mean", "count"]).sort_values("sum", ascending=False)
summary.to_csv(OUTPUT_DIR / "product_sales_summary.csv")

print("\\nCleaned dataset shape:", df.shape)
print("Outliers capped using IQR rule:", outlier_count)
print("\\nProduct sales summary:\\n", summary)

# 6. Create visualizations
plot_df = df.copy()
plot_df["Sales"] = pd.to_numeric(plot_df["Sales"])
product_sales = plot_df.groupby("Product")["Sales"].sum().sort_values(ascending=False)
plt.figure(figsize=(9, 5))
product_sales.plot(kind="bar")
plt.title("Total Sales by Product")
plt.xlabel("Product")
plt.ylabel("Sales")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(CHART_DIR / "sales_by_product.png", dpi=150)
plt.close()

region_sales = plot_df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
plt.figure(figsize=(7, 5))
region_sales.plot(kind="bar")
plt.title("Total Sales by Region")
plt.xlabel("Region")
plt.ylabel("Sales")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(CHART_DIR / "sales_by_region.png", dpi=150)
plt.close()

plot_df["Order_Date"] = pd.to_datetime(plot_df["Order_Date"])
daily_sales = plot_df.groupby("Order_Date")["Sales"].sum().sort_index()
plt.figure(figsize=(10, 5))
daily_sales.plot(kind="line", marker="o", markersize=3)
plt.title("Daily Sales Trend")
plt.xlabel("Order Date")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig(CHART_DIR / "daily_sales_trend.png", dpi=150)
plt.close()

print("\\nFiles saved to outputs/ and visualizations/")
