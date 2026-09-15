SELECT
    target_currency,
    ROUND(AVG(rate), 6) AS average_rate,
    ROUND(STDDEV(rate), 6) AS standard_deviation,
    ROUND(
        (STDDEV(rate) / AVG(rate)) * 100,
        2
    ) AS coefficient_of_variation_pct
FROM exchange_rates
GROUP BY target_currency
ORDER BY coefficient_of_variation_pct DESC;