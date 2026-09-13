import requests

API_URL = "https://api.frankfurter.dev/v1"

BASE_CURRENCY = "USD"
TARGET_CURRENCIES = ["EUR", "GBP", "JPY", "CAD", "AUD"]

START_DATE = "2025-01-01"
END_DATE = "2026-09-11"

def fetch_exchange_rates():
    params = {
        "base": BASE_CURRENCY,
        "symbols": ",".join(TARGET_CURRENCIES)
    }

    response = requests.get(
        f"{API_URL}/{START_DATE}..{END_DATE}",
        params=params,
        timeout=10
    )

    response.raise_for_status()
    return  response.json()

if __name__ == "__main__":
    data = fetch_exchange_rates()

    print(f"Base currency: {data['base']}")
    print(f"Start date: {data['start_date']}")
    print(f"End date: {data['end_date']}")
    print(f"Number of observations: {len(data['rates'])}")
