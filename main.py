
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# ==========================================
# 1. PROJECT CONFIGURATION
# ==========================================

os.makedirs("outputs", exist_ok=True)

sns.set_theme(style="whitegrid", context="notebook")

# Professional chart colors
RURAL_COLOR = "#8B5E34"
URBAN_COLOR = "#E6B84A"
INDIA_COLOR = "#E76F51"
BLUE_COLOR = "#3568A8"

print("\n==========================================")
print("       UNEMPLOYMENT ANALYSIS PROJECT")
print("==========================================")

# ==========================================
# 2. LOAD CLEANED DATASETS
# ==========================================

df1 = pd.read_csv("outputs/cleaned_unemployment_india.csv")
df2 = pd.read_csv("outputs/cleaned_unemployment_2020.csv")

df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# Convert dates
df1["Date"] = pd.to_datetime(df1["Date"], errors="coerce")
df2["Date"] = pd.to_datetime(df2["Date"], errors="coerce")

# Convert unemployment rates to numeric
rate_column = "Estimated Unemployment Rate (%)"

df1[rate_column] = pd.to_numeric(df1[rate_column], errors="coerce")
df2[rate_column] = pd.to_numeric(df2[rate_column], errors="coerce")

# Remove invalid records
df1.dropna(subset=["Date", rate_column], inplace=True)
df2.dropna(subset=["Date", rate_column], inplace=True)

print("\nDatasets loaded successfully!")
print("Dataset 1 shape:", df1.shape)
print("Dataset 2 shape:", df2.shape)

# ==========================================
# 3. OVERALL UNEMPLOYMENT TREND
# ==========================================

monthly_trend = (
    df1.groupby("Date")[rate_column]
    .mean()
    .reset_index()
)

plt.figure(figsize=(12, 6))

sns.lineplot(
    data=monthly_trend,
    x="Date",
    y=rate_column,
    marker="o",
    linewidth=2.5,
    color=BLUE_COLOR
)

plt.title(
    "Overall Unemployment Rate Trend in India",
    fontsize=16,
    fontweight="bold",
    pad=15
)

plt.xlabel("Date", fontsize=12)
plt.ylabel("Unemployment Rate (%)", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "outputs/unemployment_trend.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

# ==========================================
# 4. STATE-WISE UNEMPLOYMENT ANALYSIS
# ==========================================

statewise = (
    df1.groupby("Region")[rate_column]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

plt.figure(figsize=(12, 8))

sns.barplot(
    data=statewise,
    x=rate_column,
    y="Region",
    color=BLUE_COLOR
)

plt.title(
    "Average Unemployment Rate by State",
    fontsize=16,
    fontweight="bold",
    pad=15
)

plt.xlabel("Average Unemployment Rate (%)")
plt.ylabel("State")

plt.tight_layout()

plt.savefig(
    "outputs/statewise_unemployment.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

# ==========================================
# 5. RURAL vs URBAN vs INDIA (2020)
# ==========================================

print("\nPreparing Rural vs Urban vs India chart...")

# Use Dataset 1 because it contains the Area column
# with Rural and Urban categories.

df1["Area"] = df1["Area"].astype(str).str.strip().str.title()

# Select March to August 2020
df1["Month"] = df1["Date"].dt.strftime("%b")

month_order = ["Mar", "Apr", "May", "Jun", "Jul", "Aug"]

df_2020 = df1[
    (df1["Date"].dt.year == 2020) &
    (df1["Month"].isin(month_order))
].copy()

# Check available categories
print("\nArea categories found:", df_2020["Area"].unique())

# Monthly Rural and Urban averages
area_monthly = (
    df_2020.groupby(["Month", "Area"])[rate_column]
    .mean()
    .unstack()
)

# Monthly overall India average
india_monthly = (
    df_2020.groupby("Month")[rate_column]
    .mean()
)

# Create comparison table
chart_data = pd.DataFrame(index=month_order)

for area in ["Rural", "Urban"]:
    if area in area_monthly.columns:
        chart_data[area] = area_monthly[area]

chart_data["India"] = india_monthly

print("\nMonthly unemployment comparison:")
print(chart_data.round(2))

# Create grouped bar chart
fig, ax = plt.subplots(figsize=(13, 7))

x = np.arange(len(chart_data.index))
bar_width = 0.24

categories = [
    ("Rural", RURAL_COLOR),
    ("Urban", URBAN_COLOR),
    ("India", INDIA_COLOR)
]

for i, (category, color) in enumerate(categories):

    if category not in chart_data.columns:
        continue

    values = chart_data[category]

    positions = x + (i - 1) * bar_width

    bars = ax.bar(
        positions,
        values,
        width=bar_width,
        label=category,
        color=color,
        edgecolor="white",
        linewidth=1
    )

    # Display values above bars
    ax.bar_label(
        bars,
        fmt="%.2f",
        padding=4,
        fontsize=9,
        fontweight="bold"
    )

ax.set_title(
    "Monthly Rural vs Urban vs India Unemployment Rate (2020)",
    fontsize=16,
    fontweight="bold",
    pad=20
)

ax.set_xlabel("Month", fontsize=12, fontweight="bold")
ax.set_ylabel("Unemployment Rate (%)", fontsize=12, fontweight="bold")

ax.set_xticks(x)
ax.set_xticklabels(chart_data.index)

ax.legend(
    title="Category",
    fontsize=10,
    title_fontsize=11,
    loc="upper right",
    frameon=True
)

ax.grid(axis="y", linestyle="--", alpha=0.4)
ax.set_axisbelow(True)

# Start y-axis at zero
ax.set_ylim(
    0,
    chart_data.max().max() * 1.18
)

plt.tight_layout()

plt.savefig(
    "outputs/rural_urban_india_2020.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

# ==========================================
# 6. COVID-19 UNEMPLOYMENT TREND
# ==========================================

covid_trend = (
    df2.groupby("Date")[rate_column]
    .mean()
    .reset_index()
)

plt.figure(figsize=(12, 6))

sns.lineplot(
    data=covid_trend,
    x="Date",
    y=rate_column,
    marker="o",
    linewidth=2.5,
    color=INDIA_COLOR
)

plt.title(
    "Unemployment Rate During COVID-19 (2020)",
    fontsize=16,
    fontweight="bold",
    pad=15
)

plt.xlabel("Date", fontsize=12)
plt.ylabel("Unemployment Rate (%)", fontsize=12)

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "outputs/covid_unemployment_trend.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

# ==========================================
# 7. IMPORTANT ANALYSIS RESULTS
# ==========================================

print("\n==========================================")
print("             KEY FINDINGS")
print("==========================================")

average_rate = df1[rate_column].mean()

print(
    "\nOverall average unemployment rate:",
    round(average_rate, 2), "%"
)

highest_state = statewise.iloc[0]
lowest_state = statewise.iloc[-1]

print(
    "\nHighest unemployment state:",
    highest_state["Region"],
    "-",
    round(highest_state[rate_column], 2), "%"
)

print(
    "\nLowest unemployment state:",
    lowest_state["Region"],
    "-",
    round(lowest_state[rate_column], 2), "%"
)

print("\nMonthly Rural vs Urban vs India comparison:")
print(chart_data.round(2))

# ==========================================
# 8. PROJECT COMPLETION
# ==========================================

print("\n==========================================")
print("       ANALYSIS COMPLETED SUCCESSFULLY")
print("==========================================")

print("\nGenerated charts:")

print("1. unemployment_trend.png")
print("2. statewise_unemployment.png")
print("3. rural_urban_india_2020.png")
print("4. covid_unemployment_trend.png")

print("\nAll charts are saved in the outputs folder.")
