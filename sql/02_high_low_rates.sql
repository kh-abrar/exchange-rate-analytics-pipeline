SELECT
    target_currency,
    ROUND(MIN(rate), 6) AS lowest_rate,
    ROUND(MAX(rate), 6) AS highest_rate,
    ROUND(MAX(rate) - MIN(rate), 6) AS rate_range
FROM exchange_rates
GROUP BY target_currency
ORDER BY rate_range DESC;