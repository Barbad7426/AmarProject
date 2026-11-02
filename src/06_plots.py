import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/analytic.csv")
FIG = "figures"
os.makedirs(FIG, exist_ok=True)
sleep_order = ["Short (<7h)", "Normal (7-9h)", "Long (>9h)"]
age_order = ["20-39", "40-59", "60+"]

def save(name):
    plt.tight_layout()
    plt.savefig(f"{FIG}/{name}.png", dpi=200)
    plt.close()

# 1. Histogram of SBP
plt.figure(figsize=(7, 4.5))
plt.hist(df["SBP"], bins=40, edgecolor="white")
plt.axvline(df["SBP"].mean(), color="red", linestyle="--", label="Mean")
plt.axvline(df["SBP"].median(), color="black", linestyle=":", label="Median")
plt.title("Distribution of systolic blood pressure (adults 20+)")
plt.xlabel("Systolic blood pressure (mmHg)")
plt.ylabel("Number of participants")
plt.legend()
save("fig1_sbp_hist")

# 2. Histogram of weekly sleep
plt.figure(figsize=(7, 4.5))
plt.hist(df["SLEEP_WEEK"], bins=24, edgecolor="white")
plt.axvline(7, color="gray", linestyle="--")
plt.axvline(9, color="gray", linestyle="--")
plt.title("Distribution of average weekly sleep duration")
plt.xlabel("Sleep duration (hours/night, weekly average)")
plt.ylabel("Number of participants")
save("fig2_sleep_hist")

# 3. Bar chart of sleep categories
counts = df["SLEEP_CAT"].value_counts().reindex(sleep_order)
pct = counts / counts.sum() * 100
plt.figure(figsize=(6, 4.5))
bars = plt.bar(counts.index, pct)
for b, p in zip(bars, pct):
    plt.text(b.get_x() + b.get_width() / 2, p + 1, f"{p:.1f}%", ha="center")
plt.title("Sleep duration categories")
plt.ylabel("Percent of participants (%)")
plt.ylim(0, 100)
save("fig3_sleep_cat_bar")

# 4. Boxplot of SBP by sleep category
plt.figure(figsize=(7, 4.5))
plt.boxplot([df.loc[df["SLEEP_CAT"] == c, "SBP"] for c in sleep_order],
            tick_labels=sleep_order)
plt.title("Systolic blood pressure by sleep category")
plt.xlabel("Sleep category")
plt.ylabel("Systolic blood pressure (mmHg)")
save("fig4_sbp_by_sleep_box")

# 5. Boxplot of SBP by age group
plt.figure(figsize=(7, 4.5))
plt.boxplot([df.loc[df["AGE_GRP"] == a, "SBP"] for a in age_order],
            tick_labels=age_order)
plt.title("Systolic blood pressure by age group")
plt.xlabel("Age group (years)")
plt.ylabel("Systolic blood pressure (mmHg)")
save("fig5_sbp_by_age_box")

print("Saved 5 figures to", FIG)