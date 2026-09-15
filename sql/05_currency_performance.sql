WITH ranked_rates AS (
    SELECT
        target_currency,
        rate_date,
        rate,
        ROW_NUMBER() OVER (
            PARTITION BY target_currency
            ORDER BY rate_date
        ) AS first_row,
        ROW_NUMBER() OVER (
            PARTITION BY target_currency
            ORDER BY rate_date DESC
        ) AS last_row
    FROM exchange_rates
),
first_last AS (
    SELECT
        target_currency,
        MAX(CASE WHEN first_row = 1 THEN rate END) AS starting_rate,
        MAX(CASE WHEN last_row = 1 THEN rate END) AS ending_rate
    FROM ranked_rates
    GROUP BY target_currency
)
SELECT
    target_currency,
    ROUND(starting_rate, 6) AS starting_rate,
    ROUND(ending_rate, 6) AS ending_rate,
    ROUND(
        ((ending_rate - starting_rate) / starting_rate) * 100,
        2
    ) AS percentage_change
FROM first_last
ORDER BY percentage_change DESC;