-- ============================================================
-- Fund Performance Analytics — SQL Queries
-- NMB Australia Growth Fund vs ASX 200 | Q3 2024
-- Author: Suyash Thakuri — Financial Data Analyst
-- ============================================================
-- TABLES:
--   fund_daily_returns  (date, fund_return, fund_cumret,
--                        benchmark_return, benchmark_cumret,
--                        active_return)
--   portfolio_holdings  (ticker, name, sector, weight, beta)
--   sector_attribution  (sector, fund_weight, bench_weight,
--                        active_weight, sector_return,
--                        contribution_pct, allocation_effect,
--                        selection_effect, total_attribution)
--   stock_contributions (ticker, name, sector, weight_pct,
--                        return_pct, contribution)
--   peer_funds          (fund, q3_return, 1yr_return,
--                        3yr_ann, sharpe, fee)
-- ============================================================


-- ============================================================
-- QUERY 1: Daily Performance Summary with Rolling Metrics
-- BUSINESS QUESTION: How did the fund perform day by day
--                    vs benchmark? Where were key events?
-- ============================================================

WITH daily_metrics AS (
    SELECT
        date,
        ROUND(fund_return * 100, 4)             AS fund_return_pct,
        ROUND(benchmark_return * 100, 4)        AS benchmark_return_pct,
        ROUND(active_return * 100, 4)           AS active_return_pct,
        ROUND(fund_cumret * 100, 2)             AS fund_cumulative_pct,
        ROUND(benchmark_cumret * 100, 2)        AS benchmark_cumulative_pct,
        ROUND((fund_cumret - benchmark_cumret)
              * 100, 2)                          AS active_cumulative_pct,
        -- Rolling 20-day active return (approximated with window)
        ROUND(AVG(active_return) OVER (
            ORDER BY date
            ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
        ) * 20 * 100, 2)                        AS rolling_20d_active_pct,
        -- Outperformance flag
        CASE
            WHEN active_return > 0  THEN 'Outperform'
            WHEN active_return < 0  THEN 'Underperform'
            ELSE 'Neutral'
        END                                      AS daily_status
    FROM fund_daily_returns
)
SELECT
    date,
    fund_return_pct,
    benchmark_return_pct,
    active_return_pct,
    fund_cumulative_pct,
    benchmark_cumulative_pct,
    active_cumulative_pct,
    rolling_20d_active_pct,
    daily_status,
    -- Consecutive outperformance streak
    SUM(CASE WHEN daily_status = 'Outperform' THEN 1 ELSE 0 END)
        OVER (ORDER BY date
              ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
                                                 AS cumulative_outperform_days
FROM daily_metrics
ORDER BY date;


-- ============================================================
-- QUERY 2: Sector Attribution Analysis
-- BUSINESS QUESTION: Which sectors drove outperformance
--                    and what was the source — allocation
--                    or stock selection?
-- ============================================================

WITH attribution_ranked AS (
    SELECT
        sector,
        ROUND(fund_weight, 1)                    AS fund_weight_pct,
        ROUND(bench_weight, 1)                   AS bench_weight_pct,
        ROUND(active_weight, 1)                  AS active_weight_pct,
        ROUND(sector_return, 2)                  AS sector_return_pct,
        ROUND(allocation_effect, 3)              AS allocation_effect_pct,
        ROUND(selection_effect, 3)               AS selection_effect_pct,
        ROUND(total_attribution, 3)              AS total_attribution_pct,
        RANK() OVER (ORDER BY total_attribution DESC)
                                                 AS attribution_rank,
        CASE
            WHEN total_attribution > 0.5  THEN 'Strong positive'
            WHEN total_attribution > 0    THEN 'Positive'
            WHEN total_attribution > -0.5 THEN 'Slight drag'
            ELSE                               'Significant drag'
        END                                      AS attribution_flag,
        -- Source of alpha
        CASE
            WHEN ABS(allocation_effect) > ABS(selection_effect)
                THEN 'Allocation-driven'
            ELSE 'Selection-driven'
        END                                      AS alpha_source
    FROM sector_attribution
)
SELECT
    attribution_rank,
    sector,
    fund_weight_pct,
    bench_weight_pct,
    active_weight_pct,
    sector_return_pct,
    allocation_effect_pct,
    selection_effect_pct,
    total_attribution_pct,
    attribution_flag,
    alpha_source
FROM attribution_ranked
ORDER BY attribution_rank;


-- ============================================================
-- QUERY 3: Stock-Level Contribution Analysis
-- BUSINESS QUESTION: Which individual holdings were the
--                    biggest contributors and detractors?
-- ============================================================

WITH stock_ranked AS (
    SELECT
        ticker,
        name,
        sector,
        ROUND(weight_pct, 1)                     AS weight_pct,
        ROUND(return_pct, 2)                     AS return_pct,
        ROUND(contribution, 3)                   AS contribution_pct,
        RANK() OVER (ORDER BY contribution DESC) AS contributor_rank,
        RANK() OVER (ORDER BY contribution ASC)  AS detractor_rank,
        CASE
            WHEN contribution > 0 THEN 'Contributor'
            ELSE 'Detractor'
        END                                      AS role,
        -- Relative performance (return vs avg fund return)
        ROUND(return_pct - AVG(return_pct) OVER (), 2)
                                                 AS vs_fund_avg_pct
    FROM stock_contributions
)
SELECT
    contributor_rank,
    ticker,
    name,
    sector,
    weight_pct,
    return_pct,
    contribution_pct,
    vs_fund_avg_pct,
    role
FROM stock_ranked
ORDER BY contribution_pct DESC;


-- ============================================================
-- QUERY 4: Peer Fund Benchmarking
-- BUSINESS QUESTION: How does our fund rank vs peers
--                    on return, risk, and fees?
-- ============================================================

WITH fund_with_ours AS (
    -- Include our fund in comparison
    SELECT 'NMB Australia Growth Fund' AS fund,
           -0.0302                     AS q3_return,
           -0.0302 * 4                 AS ann_return_est,
           0.096                       AS three_yr_ann,
           -1.17                       AS sharpe,
           0.0075                      AS fee
    UNION ALL
    SELECT fund, q3_return,
           "1yr_return" AS ann_return_est,
           "3yr_ann"    AS three_yr_ann,
           sharpe, fee
    FROM peer_funds
),
ranked AS (
    SELECT *,
        RANK() OVER (ORDER BY q3_return DESC)     AS q3_return_rank,
        RANK() OVER (ORDER BY three_yr_ann DESC)  AS three_yr_rank,
        RANK() OVER (ORDER BY sharpe DESC)        AS sharpe_rank,
        RANK() OVER (ORDER BY fee ASC)            AS fee_rank,
        -- Overall score (lower = better)
        (RANK() OVER (ORDER BY q3_return DESC) +
         RANK() OVER (ORDER BY three_yr_ann DESC) +
         RANK() OVER (ORDER BY sharpe DESC))      AS composite_rank_score
    FROM fund_with_ours
)
SELECT
    composite_rank_score,
    fund,
    ROUND(q3_return * 100, 2)    AS q3_return_pct,
    q3_return_rank,
    ROUND(three_yr_ann * 100, 2) AS three_yr_ann_pct,
    three_yr_rank,
    ROUND(sharpe, 2)              AS sharpe_ratio,
    sharpe_rank,
    ROUND(fee * 100, 3)           AS mgmt_fee_pct,
    fee_rank
FROM ranked
ORDER BY composite_rank_score;


-- ============================================================
-- QUERY 5: Risk-Adjusted Performance Summary
-- BUSINESS QUESTION: What are the key risk metrics and
--                    how do they compare vs benchmark?
-- ============================================================

WITH daily_stats AS (
    SELECT
        COUNT(*)                             AS trading_days,
        ROUND(AVG(fund_return) * 252 * 100, 2)
                                             AS fund_ann_return_pct,
        ROUND(AVG(benchmark_return) * 252 * 100, 2)
                                             AS bench_ann_return_pct,
        -- Annualised volatility
        ROUND(
            SQRT(AVG(fund_return * fund_return) -
                 AVG(fund_return) * AVG(fund_return))
            * SQRT(252) * 100, 2)            AS fund_ann_vol_pct,
        -- Outperformance days
        ROUND(
            SUM(CASE WHEN active_return > 0 THEN 1.0 ELSE 0.0 END)
            / COUNT(*) * 100, 1)             AS outperform_day_pct,
        -- Best/worst days
        ROUND(MAX(fund_return) * 100, 2)     AS best_day_pct,
        ROUND(MIN(fund_return) * 100, 2)     AS worst_day_pct,
        -- Positive days
        ROUND(
            SUM(CASE WHEN fund_return > 0 THEN 1.0 ELSE 0.0 END)
            / COUNT(*) * 100, 1)             AS positive_day_pct
    FROM fund_daily_returns
),
period_stats AS (
    SELECT
        ROUND((MAX(fund_cumret) - MIN(fund_cumret)) * 100, 2)
                                             AS intra_quarter_range_pct,
        ROUND(MIN(fund_cumret) * 100, 2)     AS max_drawdown_approx_pct,
        ROUND(
            (SUM(CASE WHEN active_return > 0
                      THEN active_return ELSE 0 END)) /
            NULLIF(ABS(SUM(CASE WHEN active_return < 0
                               THEN active_return ELSE 0 END)), 0)
        , 2)                                 AS gain_loss_ratio
    FROM fund_daily_returns
)
SELECT
    d.trading_days,
    d.fund_ann_return_pct,
    d.bench_ann_return_pct,
    d.fund_ann_vol_pct,
    d.outperform_day_pct,
    d.best_day_pct,
    d.worst_day_pct,
    d.positive_day_pct,
    p.intra_quarter_range_pct,
    p.max_drawdown_approx_pct,
    p.gain_loss_ratio
FROM daily_stats d, period_stats p;
