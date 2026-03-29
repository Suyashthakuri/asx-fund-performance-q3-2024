# ASX Equity Fund Performance & Attribution Report — Q3 2024
### Quarterly fund analytics for an ASX equity fund vs ASX 200 Total Return Index

---

## The Business Problem

Institutional investors and fund trustees require quarterly reporting that clearly explains:
1. How did the fund perform relative to the benchmark — and why?
2. Which sectors and stocks drove outperformance or underperformance?
3. How does the fund compare to peers on a risk-adjusted basis?
4. What is the portfolio manager's forward view?

This project produces a complete institutional-grade quarterly fund report covering all four questions — from raw daily return data through to a written investment commentary.

---

## Q3 2024 Performance Summary

| Metric | Result |
|---|---|
| **Fund return (Q3 2024)** | **-3.02%** |
| **Benchmark return (ASX 200)** | **-8.12%** |
| **Active return (alpha)** | **+5.10%** |
| Maximum drawdown | -7.08% (vs -11.2% benchmark) |
| Annualised volatility | 14.0% (vs 15.8% benchmark) |
| Information ratio | 4.77 |
| Peer ranking (Q3 2024) | #1 of 6 funds |

---

## Key Findings

**What drove outperformance:**
- Underweight Financials (-6.2% vs benchmark) added +2.14% — largest single attribution contributor
- Wesfarmers (+9.99%) and Xero (+18.83%) were the top individual stock contributors
- Healthcare overweight provided downside protection during August sell-off

**What detracted:**
- Overweight Materials (+0.7%) was a drag of -0.82% as iron ore prices fell ~25%
- BHP (-7.74%), Rio Tinto (-13.05%), and Fortescue (-20.28%) were the three largest detractors

---

## Report Contents

### Written Report (`NMB_Australia_Growth_Fund_Q3_2024_Report.docx`)
Professional 7-section quarterly fund report:
1. Market Overview — macro context for Q3 2024
2. Fund Performance — return vs benchmark, quarterly and historical
3. Attribution Analysis — Brinson-Hood-Beebower sector and stock attribution
4. Risk Metrics — volatility, drawdown, Sharpe ratio, tracking error
5. Portfolio Holdings — top contributors, detractors, sector allocation
6. Peer Comparison — ranking vs 5 comparable ASX equity funds
7. Investment Commentary — what worked, what didn't, Q4 positioning

### Python Analysis (`analysis.py`)
5 professional charts:
- `01_performance_vs_benchmark.png` — cumulative return vs ASX 200 + rolling active return
- `02_attribution_analysis.png` — sector attribution waterfall + active weights
- `03_risk_metrics.png` — drawdown profile, rolling volatility, risk comparison
- `04_portfolio_holdings.png` — sector allocation + top/bottom contributors
- `05_peer_comparison.png` — peer return ranking + risk-return scatter

### SQL Queries (`analysis_queries.sql`)
5 analytical queries:
- `Query 1` — Daily performance with rolling metrics and outperformance streak
- `Query 2` — Sector attribution with allocation vs selection decomposition
- `Query 3` — Stock-level contribution ranking with role classification
- `Query 4` — Peer fund benchmarking with composite ranking score
- `Query 5` — Risk-adjusted performance summary statistics

---

## Dataset Description

**fund_daily_returns.csv** — 65 trading days (Q3 2024)

| Column | Description |
|---|---|
| date | Trading date (business days only) |
| fund_return | Daily fund return |
| fund_cumret | Cumulative fund return from quarter start |
| benchmark_return | Daily ASX 200 Total Return |
| benchmark_cumret | Cumulative benchmark return |
| active_return | Daily active return (fund minus benchmark) |

**portfolio_holdings.csv** — 20 ASX-listed stocks

| Column | Description |
|---|---|
| ticker | ASX ticker symbol |
| name | Company name |
| sector | GICS sector classification |
| weight | Portfolio weight (decimal) |
| beta | Beta to ASX 200 |

**sector_attribution.csv** — Brinson-Hood-Beebower attribution by sector

**stock_contributions.csv** — Individual stock return and contribution

**peer_funds.csv** — 5 comparable Australian equity fund benchmarks

---

## Repository Structure

```
asx-fund-performance-q3-2024/
│
├── data/
│   ├── fund_daily_returns.csv
│   ├── portfolio_holdings.csv
│   ├── sector_attribution.csv
│   ├── stock_contributions.csv
│   └── peer_funds.csv
│
├── NMB_Australia_Growth_Fund_Q3_2024_Report.docx
├── analysis.py
├── analysis_queries.sql
│
└── outputs/
    ├── 01_performance_vs_benchmark.png
    ├── 02_attribution_analysis.png
    ├── 03_risk_metrics.png
    ├── 04_portfolio_holdings.png
    └── 05_peer_comparison.png
```

---

## Skills Demonstrated

| Category | Skills |
|---|---|
| Investment Analytics | Performance attribution, risk metrics, peer benchmarking |
| Python | pandas, numpy, matplotlib — financial time series analysis |
| SQL | Window functions, CTEs, ranking, statistical aggregation |
| Financial Writing | Institutional fund commentary, investment narrative |
| Domain Knowledge | ASX equities, benchmarking, Brinson attribution model, fund reporting |

---

## Professional Context

This project is modelled on the quarterly fund reporting produced during my time as **Senior Research & Equity Investment Analyst at NMB Capital** — Nepal's largest investment bank — where I prepared monthly investment committee reports and quarterly performance packs for a fund with AUM of NPR 100M+ rated AMC 2 (highest category).

The report format, attribution methodology, and commentary style reflect institutional fund reporting standards used by Australian and international asset managers.

---

*All data is synthetic and generated for portfolio demonstration purposes. No real fund data was used.*

*Part of a broader analytics portfolio — see also:*
- *[Brokerage Client Revenue & Churn Analysis](https://github.com/Suyashthakuri/brokerage-client-analytics)* — Client analytics, SQL, Python, Power BI
- *[ASX General Insurer KPI Dashboard](https://github.com/Suyashthakuri/asx-insurer-kpi-dashboard-)* — Power BI, DAX, SQL
- *[Financial Tools Portfolio — NMB Capital](https://github.com/Suyashthakuri/Investment-Banking)* — Excel VBA, DCF, Fixed Income
