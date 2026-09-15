CREATE INDEX IF NOT EXISTS idx_exchange_rates_date
ON exchange_rates(rate_date);

CREATE INDEX IF NOT EXISTS idx_exchange_rates_currency
ON exchange_rates(target_currency);

CREATE INDEX IF NOT EXISTS idx_exchange_rates_currency_date
ON exchange_rates(target_currency, rate_date);