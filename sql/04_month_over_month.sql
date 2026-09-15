WITH monthly_rates AS (
    SELECT
        DATE_TRUNC('month', rate_date)::DATE AS month,
        target_currency,
        AVG(rate) AS average_rate
    FROM exchange_rates
    GROUP BY
        DATE_TRUNC('month', rate_date),
        target_currency
),
with_previous AS (
    SELECT
        month,
        target_currency,
        average_rate,
        LAG(average_rate) OVER (
            PARTITION BY target_currency
            ORDER BY month
        ) AS previous_month_rate
    FROM monthly_rates
)
SELECT
    month,
    target_currency,
    ROUND(average_rate, 6) AS average_rate,
    ROUND(previous_month_rate, 6) AS previous_month_rate,
    ROUND(
        ((average_rate - previous_month_rate)
        / previous_month_rate) * 100,
        2
    ) AS percentage_change
FROM with_previous
ORDER BY
    month,
    target_currency;