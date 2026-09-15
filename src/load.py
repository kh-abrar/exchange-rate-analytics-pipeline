import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from src.extract import fetch_exchange_rates
from src.transform import transform_exchange_rates


load_dotenv()


def get_database_engine():
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    database_url = (
        f"postgresql+psycopg2://{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
    )

    return create_engine(database_url)


def load_to_postgres(df):
    engine = get_database_engine()

    records = df.to_dict(orient="records")

    insert_query = text("""
        INSERT INTO exchange_rates (
            rate_date,
            base_currency,
            target_currency,
            rate
        )
        VALUES (
            :rate_date,
            :base_currency,
            :target_currency,
            :rate
        )
        ON CONFLICT (
            rate_date,
            base_currency,
            target_currency
        )
        DO NOTHING;
    """)

    with engine.begin() as connection:
        connection.execute(insert_query, records)

    engine.dispose()


if __name__ == "__main__":
    data = fetch_exchange_rates()

    df = transform_exchange_rates(data)

    print(f"Rows to load: {len(df)}")

    load_to_postgres(df)

    print("Data loaded successfully.")