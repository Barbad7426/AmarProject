import pandas as pd

m = pd.read_csv("data/processed/merged.csv")

# --- ساخت متغیرهای اصلی ---
m["SBP"] = m[["BPXOSY1", "BPXOSY2", "BPXOSY3"]].mean(axis=1)
m["DBP"] = m[["BPXODI1", "BPXODI2", "BPXODI3"]].mean(axis=1)
m["SLEEP_WEEK"] = (5 * m["SLD012"] + 2 * m["SLD013"]) / 7

key = ["RIDAGEYR", "RIAGENDR", "SBP", "DBP", "BMXBMI",
       "SLD012", "SLD013", "SLEEP_WEEK", "WTMEC2YR"]

# --- ۱. داده‌ی گمشده ---
print("=== Missing values ===")
miss = m[key].isna().sum()
print(pd.DataFrame({"n_missing": miss,
                    "pct": (miss / len(m) * 100).round(1)}))

# --- ۲. دامنه‌ی مقادیر (برای پیدا کردن مقادیر غیرممکن) ---
print("\n=== Ranges ===")
print(m[key].describe().T[["count", "min", "max"]])

# --- ۳. کدهای ویژه در متغیرهای طبقه‌ای ---
print("\n=== Category counts ===")
for col in ["RIAGENDR", "RIDSTATR", "DMDEDUC2"]:
    print(col, m[col].value_counts(dropna=False).sort_index().to_dict())

# --- ۴. تعداد اندازه‌گیری‌های فشار برای هر فرد ---
print("\n=== Number of SBP readings per person ===")
n_read = m[["BPXOSY1", "BPXOSY2", "BPXOSY3"]].notna().sum(axis=1)
print(n_read.value_counts().sort_index().to_dict())

# --- ۵. فشار صفر یا نامعقول ---
print("\n=== Suspicious BP values ===")
print("DBP == 0:", (m[["BPXODI1", "BPXODI2", "BPXODI3"]] == 0).sum().sum())
print("SBP < 70 or > 250:", ((m["SBP"] < 70) | (m["SBP"] > 250)).sum())