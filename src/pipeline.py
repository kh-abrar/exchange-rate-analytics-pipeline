from extract import fetch_exchange_rates
from transform import transform_exchange_rates
from load import load_to_postgres


def run_pipeline():
    print("Starting exchange rate pipeline...")

    # Extract
    print("Fetching exchange rate data...")
    data = fetch_exchange_rates()

    # Transform
    print("Transforming data...")
    df = transform_exchange_rates(data)

    print(f"Rows transformed: {len(df)}")

    # Load
    print("Loading data into PostgreSQL...")
    load_to_postgres(df)

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()