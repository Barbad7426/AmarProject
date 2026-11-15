from statistics import NormalDist

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/analytic.csv")
x = df["SBP"]
n = len(x)

# Task 7: expectation and variance
mu = x.mean()
var = x.var(ddof=1)
sd = np.sqrt(var)
print("=== SBP moments ===")
print(f"mean = {mu:.2f}   var = {var:.2f}   sd = {sd:.2f}")
print(f"median = {x.median():.2f}   skew = {x.skew():.3f}")

normal = NormalDist(mu, sd)
std_normal = NormalDist()

# Empirical rule
print("\n=== Within mean ± k·sd ===")
for k in [1, 2, 3]:
    observed = ((x - mu).abs() <= k * sd).mean()
    expected = std_normal.cdf(k) - std_normal.cdf(-k)
    print(f"k={k}: observed = {observed:.4f}   normal = {expected:.4f}")

# Tail probabilities
print("\n=== Tail probabilities ===")
for t in [100, 130, 140, 160]:
    obs = (x >= t).mean()
    nor = 1 - normal.cdf(t)
    print(f"P(SBP >= {t}): observed = {obs:.4f}   normal = {nor:.4f}")

# Outliers (IQR rule)
q1, q3 = x.quantile([0.25, 0.75])
iqr = q3 - q1
lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
print("\n=== Outliers (1.5 IQR) ===")
print(f"Q1 = {q1:.2f}   Q3 = {q3:.2f}   bounds = [{lo:.2f}, {hi:.2f}]")
print(f"below: {(x < lo).sum()}   above: {(x > hi).sum()}")
print(f"min = {x.min():.2f}   max = {x.max():.2f}")

# Log transform
lx = np.log(x)
print("\n=== log(SBP) ===")
print(f"skew of log(SBP) = {lx.skew():.3f}")


def qq_points(values):
    z = np.sort((values - values.mean()) / values.std(ddof=1))
    probs = (np.arange(1, len(z) + 1) - 0.5) / len(z)
    theo = np.array([std_normal.inv_cdf(p) for p in probs])
    return theo, z


fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))

axes[0].hist(x, bins=50, density=True, color="lightsteelblue",
             edgecolor="white")
grid = np.linspace(x.min(), x.max(), 300)
axes[0].plot(grid, [normal.pdf(g) for g in grid], color="darkred",
             label=f"N({mu:.1f}, {sd:.1f}²)")
axes[0].set_title("SBP with fitted normal curve")
axes[0].set_xlabel("SBP (mmHg)")
axes[0].set_ylabel("Density")
axes[0].legend()

for ax, values, title in [(axes[1], x, "Q-Q plot: SBP"),
                          (axes[2], lx, "Q-Q plot: log(SBP)")]:
    theo, z = qq_points(values)
    ax.scatter(theo, z, s=4, alpha=0.4)
    ax.plot([-4, 4], [-4, 4], color="darkred")
    ax.set_title(title)
    ax.set_xlabel("Theoretical normal quantile")
    ax.set_ylabel("Standardized sample quantile")

plt.tight_layout()
plt.savefig("figures/phase2/sbp_normality.png", dpi=150)
# Task 8: two random variables, covariance
print("\n=== Covariance matrix ===")
cols = ["SBP", "SLEEP_WEEK", "RIDAGEYR", "BMXBMI"]
cov = df[cols].cov()
print(cov.round(2))

print("\n=== Quadrant shares (relative to means) ===")
for xcol in ["SLEEP_WEEK", "RIDAGEYR"]:
    dx = df[xcol] - df[xcol].mean()
    dy = df["SBP"] - mu
    same = ((dx * dy) > 0).mean()
    opposite = ((dx * dy) < 0).mean()
    print(f"{xcol}: same-sign = {same:.3f}   opposite-sign = {opposite:.3f}")

fig2, axes2 = plt.subplots(1, 2, figsize=(12, 4.5), sharey=True)
pairs = [("SLEEP_WEEK", "Weekly average sleep (hours)", 0.5),
         ("RIDAGEYR", "Age (years)", 5)]
for ax, (xcol, xlabel, width) in zip(axes2, pairs):
    ax.scatter(df[xcol], df["SBP"], s=4, alpha=0.2, color="steelblue")
    bins = (df[xcol] // width) * width
    binned = df.groupby(bins).agg(x=(xcol, "mean"), mean=("SBP", "mean"),
                                  size=("SBP", "size"))
    binned = binned[binned["size"] >= 30]
    ax.plot(binned["x"], binned["mean"], "o-",
            color="darkred", ms=4, label="Mean SBP per bin")
    ax.axhline(mu, color="gray", ls="--", lw=1)
    ax.axvline(df[xcol].mean(), color="gray", ls="--", lw=1)
    ax.set_xlabel(xlabel)
    ax.set_title(f"SBP vs {xlabel.split(' (')[0]}   "
                 f"Cov = {cov.loc['SBP', xcol]:.2f}")
axes2[0].set_ylabel("SBP (mmHg)")
axes2[0].legend()
plt.tight_layout()
plt.savefig("figures/phase2/scatter_cov.png", dpi=150)

cov.to_csv("reports/phase2/covariance_matrix.csv")
plt.show()