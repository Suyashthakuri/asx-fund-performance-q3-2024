"""
NMB Australia Growth Fund — Q3 2024 Performance Analysis
ASX Equity Fund vs ASX 200 Total Return Index
Author: Suyash Thakuri — Financial Data Analyst
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import json
import os

os.makedirs("outputs", exist_ok=True)

# ── STYLE ────────────────────────────────────────────────
ACCENT   = "#1a6b4a"
ACCENT2  = "#2d9b6e"
BENCH    = "#6b7a8d"
RED      = "#c0392b"
AMBER    = "#e07b39"
BGGREEN  = "#e8f5f0"
BGRED    = "#fdf2f2"
BG       = "#fafbfc"
DARK     = "#0f1419"
GREY     = "#3d4a5a"

plt.rcParams.update({
    "figure.facecolor":  BG,
    "axes.facecolor":    BG,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "font.family":       "sans-serif",
    "axes.titlesize":    12,
    "axes.titleweight":  "bold",
    "axes.labelsize":    10,
    "xtick.labelsize":   9,
    "ytick.labelsize":   9,
    "legend.fontsize":   9,
})

# ── LOAD DATA ────────────────────────────────────────────
fund_df    = pd.read_csv("fund_daily_returns.csv", parse_dates=["date"])
holdings   = pd.read_csv("portfolio_holdings.csv")
attribution= pd.read_csv("sector_attribution.csv")
contrib    = pd.read_csv("stock_contributions.csv")
peers      = pd.read_csv("peer_funds.csv")
with open("metrics.json") as f:
    m = json.load(f)

print("=" * 60)
print("NMB AUSTRALIA GROWTH FUND — Q3 2024 ANALYSIS")
print("=" * 60)
print(f"Fund return:     {m['fund_q3_return']*100:+.2f}%")
print(f"Benchmark:       {m['bench_q3_return']*100:+.2f}%")
print(f"Outperformance:  {m['active_q3_return']*100:+.2f}%")

# ── CHART 1: CUMULATIVE PERFORMANCE vs BENCHMARK ─────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Performance vs ASX 200 Benchmark — Q3 2024", fontsize=13, fontweight="bold")

ax = axes[0]
ax.plot(fund_df["date"], fund_df["fund_cumret"] * 100,
        color=ACCENT, linewidth=2.5, label="NMB Australia Growth Fund", zorder=3)
ax.plot(fund_df["date"], fund_df["benchmark_cumret"] * 100,
        color=BENCH, linewidth=1.8, linestyle="--", label="ASX 200 Total Return", zorder=2)
ax.fill_between(fund_df["date"],
                fund_df["fund_cumret"] * 100,
                fund_df["benchmark_cumret"] * 100,
                where=fund_df["fund_cumret"] >= fund_df["benchmark_cumret"],
                alpha=0.12, color=ACCENT, label="Outperformance")
ax.fill_between(fund_df["date"],
                fund_df["fund_cumret"] * 100,
                fund_df["benchmark_cumret"] * 100,
                where=fund_df["fund_cumret"] < fund_df["benchmark_cumret"],
                alpha=0.12, color=RED)
ax.axhline(0, color=GREY, linewidth=0.8, alpha=0.5)
ax.set_ylabel("Cumulative return (%)")
ax.set_title("Cumulative return — Jul to Sep 2024")
ax.yaxis.set_major_formatter(mticker.PercentFormatter())
ax.legend(loc="upper right")
# Annotate final values
final_fund  = fund_df["fund_cumret"].iloc[-1] * 100
final_bench = fund_df["benchmark_cumret"].iloc[-1] * 100
ax.annotate(f"{final_fund:+.2f}%", xy=(fund_df["date"].iloc[-1], final_fund),
            xytext=(10, 0), textcoords="offset points",
            fontsize=9, color=ACCENT, fontweight="bold")
ax.annotate(f"{final_bench:+.2f}%", xy=(fund_df["date"].iloc[-1], final_bench),
            xytext=(10, 0), textcoords="offset points",
            fontsize=9, color=BENCH)

# Rolling 20-day active return
ax = axes[1]
fund_df["rolling_active"] = fund_df["active_return"].rolling(20).sum() * 100
ax.bar(fund_df["date"], fund_df["rolling_active"],
       color=[ACCENT if v >= 0 else RED for v in fund_df["rolling_active"]],
       alpha=0.75, width=1)
ax.axhline(0, color=GREY, linewidth=0.8)
ax.set_ylabel("Rolling 20-day active return (%)")
ax.set_title("Active return vs benchmark (rolling 20 days)")
ax.yaxis.set_major_formatter(mticker.PercentFormatter())

plt.tight_layout()
plt.savefig("outputs/01_performance_vs_benchmark.png", dpi=150, bbox_inches="tight")
plt.close()
print("\nChart 1 saved: outputs/01_performance_vs_benchmark.png")

# ── CHART 2: ATTRIBUTION ANALYSIS ────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Performance Attribution Analysis — Q3 2024", fontsize=13, fontweight="bold")

# Sector attribution waterfall
ax = axes[0]
attr_sorted = attribution.sort_values("total_attribution")
colors_attr = [ACCENT if v >= 0 else RED for v in attr_sorted["total_attribution"]]
bars = ax.barh(attr_sorted["sector"], attr_sorted["total_attribution"],
               color=colors_attr, edgecolor="none", height=0.6)
ax.axvline(0, color=GREY, linewidth=0.8)
ax.set_xlabel("Attribution effect (% return)")
ax.set_title("Sector attribution vs benchmark")
for bar, val in zip(bars, attr_sorted["total_attribution"]):
    x = val + 0.01 if val >= 0 else val - 0.01
    ha = "left" if val >= 0 else "right"
    ax.text(x, bar.get_y() + bar.get_height()/2,
            f"{val:+.2f}%", va="center", fontsize=8,
            color=ACCENT if val >= 0 else RED)

# Active weights
ax = axes[1]
attr_sorted2 = attribution.sort_values("active_weight")
colors_aw = [ACCENT if v >= 0 else RED for v in attr_sorted2["active_weight"]]
ax.barh(attr_sorted2["sector"], attr_sorted2["active_weight"],
        color=colors_aw, alpha=0.8, edgecolor="none", height=0.6)
ax.axvline(0, color=GREY, linewidth=0.8)
ax.set_xlabel("Active weight vs benchmark (%)")
ax.set_title("Portfolio positioning — active weights")

plt.tight_layout()
plt.savefig("outputs/02_attribution_analysis.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 2 saved: outputs/02_attribution_analysis.png")

# ── CHART 3: RISK METRICS ─────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle("Risk Analysis — Q3 2024", fontsize=13, fontweight="bold")

# Drawdown chart
ax = axes[0]
cumulative = (1 + fund_df["fund_return"]).cumprod()
bench_cum  = (1 + fund_df["benchmark_return"]).cumprod()
fund_dd    = (cumulative - cumulative.cummax()) / cumulative.cummax() * 100
bench_dd   = (bench_cum  - bench_cum.cummax())  / bench_cum.cummax()  * 100
ax.fill_between(fund_df["date"], fund_dd, 0, alpha=0.45, color=ACCENT, label="Fund")
ax.fill_between(fund_df["date"], bench_dd * 100, 0, alpha=0.25, color=BENCH, label="ASX 200")
ax.set_ylabel("Drawdown (%)")
ax.set_title("Drawdown profile")
ax.yaxis.set_major_formatter(mticker.PercentFormatter())
ax.legend()
ax.annotate(f"Fund max: {m['max_drawdown']*100:.2f}%",
            xy=(0.05, 0.1), xycoords="axes fraction",
            fontsize=9, color=ACCENT, fontweight="bold")

# Rolling volatility
ax = axes[1]
fund_roll_vol  = fund_df["fund_return"].rolling(20).std() * np.sqrt(252) * 100
bench_roll_vol = fund_df["benchmark_return"].rolling(20).std() * np.sqrt(252) * 100
ax.plot(fund_df["date"], fund_roll_vol, color=ACCENT, linewidth=2, label="Fund")
ax.plot(fund_df["date"], bench_roll_vol, color=BENCH, linewidth=1.5,
        linestyle="--", label="ASX 200")
ax.set_ylabel("Annualised volatility (%)")
ax.set_title("Rolling 20-day volatility")
ax.yaxis.set_major_formatter(mticker.PercentFormatter())
ax.legend()

# Risk metrics comparison table as bar chart
ax = axes[2]
metrics_compare = {
    "Sharpe ratio":     [max(m["sharpe"], -2), 0.72],
    "Info ratio":       [min(m["info_ratio"], 3), 0.0],
    "Ann. vol (%)":     [m["fund_vol"]*100, m["bench_q3_return"]*4*100],
    "Max DD (%)":       [abs(m["max_drawdown"])*100, 8.12],
}
labels   = list(metrics_compare.keys())
fund_vals  = [v[0] for v in metrics_compare.values()]
bench_vals = [v[1] for v in metrics_compare.values()]
x = np.arange(len(labels))
w = 0.35
ax.bar(x - w/2, fund_vals,  w, color=ACCENT, alpha=0.85, label="Fund")
ax.bar(x + w/2, bench_vals, w, color=BENCH,  alpha=0.85, label="Benchmark")
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=15, ha="right", fontsize=8)
ax.set_title("Risk metrics comparison")
ax.legend()
ax.axhline(0, color=GREY, linewidth=0.5)

plt.tight_layout()
plt.savefig("outputs/03_risk_metrics.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 3 saved: outputs/03_risk_metrics.png")

# ── CHART 4: PORTFOLIO HOLDINGS ───────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Portfolio Holdings — Q3 2024", fontsize=13, fontweight="bold")

# Sector weights
ax = axes[0]
sector_w = holdings.groupby("sector")["weight"].sum().sort_values(ascending=True)
colors_s = [ACCENT if s in ["Financials","Healthcare","Technology"] else
            BENCH if s in ["Materials","Consumer Disc"] else
            "#c8d8e8" for s in sector_w.index]
ax.barh(sector_w.index, sector_w.values * 100, color=colors_s,
        edgecolor="none", height=0.6)
ax.set_xlabel("Portfolio weight (%)")
ax.set_title("Sector allocation")
for i, (sec, val) in enumerate(sector_w.items()):
    ax.text(val * 100 + 0.2, i, f"{val*100:.1f}%", va="center", fontsize=8)

# Top/bottom contributors
ax = axes[1]
top5    = contrib.head(5)
bottom3 = contrib.tail(3)
combined = pd.concat([top5, bottom3]).reset_index(drop=True)
bar_colors = [ACCENT if v >= 0 else RED for v in combined["contribution"]]
bars = ax.barh(combined["name"], combined["contribution"],
               color=bar_colors, edgecolor="none", height=0.6)
ax.axvline(0, color=GREY, linewidth=0.8)
ax.set_xlabel("Contribution to return (%)")
ax.set_title("Top 5 contributors & bottom 3 detractors")
for bar, val in zip(bars, combined["contribution"]):
    x = val + 0.01 if val >= 0 else val - 0.01
    ha = "left" if val >= 0 else "right"
    ax.text(x, bar.get_y() + bar.get_height()/2,
            f"{val:+.2f}%", va="center", fontsize=8,
            color=ACCENT if val >= 0 else RED)

plt.tight_layout()
plt.savefig("outputs/04_portfolio_holdings.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 4 saved: outputs/04_portfolio_holdings.png")

# ── CHART 5: PEER COMPARISON ──────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Peer Fund Comparison", fontsize=13, fontweight="bold")

# Add our fund to peers
our_fund = pd.DataFrame([{
    "fund":       "NMB Australia Growth Fund",
    "q3_return":  m["fund_q3_return"],
    "1yr_return": m["fund_q3_return"] * 4,  # annualised estimate
    "3yr_ann":    0.096,
    "sharpe":     max(m["sharpe"], -2),
    "fee":        0.0075,
}])
all_peers = pd.concat([our_fund, peers]).reset_index(drop=True)

# Q3 return comparison
ax = axes[0]
sorted_peers = all_peers.sort_values("q3_return", ascending=True)
bar_colors_p = [ACCENT if f == "NMB Australia Growth Fund" else BENCH
                for f in sorted_peers["fund"]]
bars = ax.barh(sorted_peers["fund"], sorted_peers["q3_return"] * 100,
               color=bar_colors_p, edgecolor="none", height=0.55)
ax.axvline(0, color=GREY, linewidth=0.8)
ax.set_xlabel("Q3 2024 return (%)")
ax.set_title("Q3 2024 — peer comparison")
ax.xaxis.set_major_formatter(mticker.PercentFormatter())
for bar, val in zip(bars, sorted_peers["q3_return"]):
    x = val * 100 + 0.05
    ax.text(x, bar.get_y() + bar.get_height()/2,
            f"{val*100:+.2f}%", va="center", fontsize=9,
            fontweight="bold" if val == m["fund_q3_return"] else "normal",
            color=ACCENT if val == m["fund_q3_return"] else GREY)

# Risk-return scatter
ax = axes[1]
for _, row in all_peers.iterrows():
    is_us = row["fund"] == "NMB Australia Growth Fund"
    ax.scatter(row["sharpe"] if row["sharpe"] > -2 else -2,
               row["q3_return"] * 100,
               s=160 if is_us else 80,
               color=ACCENT if is_us else BENCH,
               zorder=3 if is_us else 2,
               edgecolors="white", linewidth=1)
    ax.annotate(row["fund"].replace(" ", "\n") if len(row["fund"]) > 20 else row["fund"],
                xy=(row["sharpe"] if row["sharpe"] > -2 else -2,
                    row["q3_return"] * 100),
                xytext=(6, 0), textcoords="offset points",
                fontsize=7.5,
                color=ACCENT if is_us else GREY,
                fontweight="bold" if is_us else "normal")
ax.set_xlabel("Sharpe ratio")
ax.set_ylabel("Q3 2024 return (%)")
ax.set_title("Risk-adjusted return — peer positioning")
ax.yaxis.set_major_formatter(mticker.PercentFormatter())
ax.axhline(0, color=GREY, linewidth=0.5, alpha=0.5)

plt.tight_layout()
plt.savefig("outputs/05_peer_comparison.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 5 saved: outputs/05_peer_comparison.png")

print("\n=== ALL CHARTS GENERATED ===")
print("Files saved to outputs/")
