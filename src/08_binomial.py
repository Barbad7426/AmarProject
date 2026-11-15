import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/analytic.csv")
df["B"] = (df["SBP"] >= 130).astype(int)

n_group = 20
p = df["B"].mean()
k_groups = len(df) // n_group


def binom_pmf(k, n, p):
    return math.comb(n, k) * p**k * (1 - p) ** (n - k)


def group_counts(order):
    b = df.loc[order, "B"].to_numpy()[: k_groups * n_group]
    return b.reshape(k_groups, n_group).sum(axis=1)


rng = np.random.default_rng(1405)
random_order = rng.permutation(df.index)
age_order = df.sort_values("RIDAGEYR", kind="stable").index

counts = {
    "random": group_counts(random_order),
    "age_sorted": group_counts(age_order),
}

bin_mean = n_group * p
bin_var = n_group * p * (1 - p)
print(f"p = {p:.4f}   n = {n_group}   groups = {k_groups}")
print(f"Binomial: mean = {bin_mean:.3f}   var = {bin_var:.3f}")

rows = []
for name, c in counts.items():
    rows.append({
        "grouping": name,
        "mean": c.mean(),
        "var": c.var(ddof=1),
        "var_ratio": c.var(ddof=1) / bin_var,
        "min": c.min(),
        "max": c.max(),
    })
summary = pd.DataFrame(rows)
print("\n", summary.round(3).to_string(index=False))

ks = np.arange(n_group + 1)
pmf = np.array([binom_pmf(k, n_group, p) for k in ks])

compare = pd.DataFrame({"k": ks, "binomial": pmf})
for name, c in counts.items():
    compare[name] = np.bincount(c, minlength=n_group + 1) / k_groups
print("\n", compare.round(3).to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
titles = {"random": "Random groups of 20",
          "age_sorted": "Groups of 20 sorted by age"}
for ax, (name, c) in zip(axes, counts.items()):
    ax.bar(ks, compare[name], color="lightsteelblue", label="Observed")
    ax.plot(ks, pmf, "o-", color="darkred", ms=4,
            label=f"Binomial(20, {p:.3f})")
    ax.set_title(titles[name])
    ax.set_xlabel("Number with SBP ≥ 130 mmHg in group")
axes[0].set_ylabel("Proportion of groups")
axes[0].legend()
plt.tight_layout()
plt.savefig("figures/phase2/binomial_groups.png", dpi=150)

summary.to_csv("reports/phase2/binomial_summary.csv", index=False)
compare.to_csv("reports/phase2/binomial_compare.csv", index=False)
