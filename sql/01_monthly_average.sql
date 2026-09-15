SELECT
    DATE_TRUNC('month', rate_date)::DATE AS month,
    target_currency,
    ROUND(AVG(rate), 6) AS average_rate
FROM exchange_rates
GROUP BY
    DATE_TRUNC('month', rate_date),
    target_currency
ORDER BY
    month,
    target_currency;