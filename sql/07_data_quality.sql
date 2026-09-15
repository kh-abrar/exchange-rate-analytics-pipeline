SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT rate_date) AS unique_dates,
    COUNT(DISTINCT target_currency) AS unique_currencies,
    COUNT(*) FILTER (WHERE rate <= 0) AS invalid_rates,
    COUNT(*) FILTER (WHERE rate IS NULL) AS null_rates
FROM exchange_rates;

SELECT
    target_currency,
    COUNT(*) AS observation_count,
    MIN(rate_date) AS first_date,
    MAX(rate_date) AS last_date
FROM exchange_rates
GROUP BY target_currency
ORDER BY target_currency;