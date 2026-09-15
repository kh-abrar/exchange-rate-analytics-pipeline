import pandas as pd

from src.transform import transform_exchange_rates


def sample_api_response():
    return {
        "base": "USD",
        "start_date": "2025-01-01",
        "end_date": "2025-01-03",
        "rates": {
            "2025-01-01": {
                "EUR": 0.95,
                "GBP": 0.78,
                "JPY": 157.20
            },
            "2025-01-02": {
                "EUR": 0.96,
                "GBP": 0.79,
                "JPY": 158.10
            }
        }
    }


def test_transform_returns_dataframe():
    data = sample_api_response()

    df = transform_exchange_rates(data)

    assert isinstance(df, pd.DataFrame)


def test_required_columns_exist():
    data = sample_api_response()

    df = transform_exchange_rates(data)

    expected_columns = {
        "rate_date",
        "base_currency",
        "target_currency",
        "rate"
    }

    assert set(df.columns) == expected_columns


def test_rates_are_positive():
    data = sample_api_response()

    df = transform_exchange_rates(data)

    assert (df["rate"] > 0).all()


def test_no_missing_values():
    data = sample_api_response()

    df = transform_exchange_rates(data)

    assert df.isnull().sum().sum() == 0


def test_no_duplicate_records():
    data = sample_api_response()

    df = transform_exchange_rates(data)

    assert not df.duplicated(
        subset=["rate_date", "base_currency", "target_currency"]
    ).any()


def test_expected_row_count():
    data = sample_api_response()

    df = transform_exchange_rates(data)

    assert len(df) == 6