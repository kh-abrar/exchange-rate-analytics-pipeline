import pandas as pd

from src.extract import fetch_exchange_rates


def transform_exchange_rates(data):
    rows = []

    for date, rates in data["rates"].items():
        for currency, rate in rates.items():
            rows.append({
                "rate_date": date,
                "base_currency": data["base"],
                "target_currency": currency,
                "rate": rate
            })

    df = pd.DataFrame(rows)

    # Convert data types
    df["rate_date"] = pd.to_datetime(df["rate_date"])
    df["rate"] = pd.to_numeric(df["rate"])

    # Remove duplicate records
    df = df.drop_duplicates(
        subset=["rate_date", "base_currency", "target_currency"]
    )

    # Remove invalid rates
    df = df[df["rate"] > 0]

    # Sort data
    df = df.sort_values(
        ["rate_date", "target_currency"]
    ).reset_index(drop=True)

    return df


if __name__ == "__main__":
    data = fetch_exchange_rates()

    df = transform_exchange_rates(data)

    print("\nTransformed Data:")
    print(df.head(10))

    print("\nDataFrame Information:")
    print(df.info())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())