# Exchange Rate Analytics Pipeline

An end-to-end data engineering and analytics project that extracts historical foreign exchange rate data from a public API, transforms it using pandas, loads it into PostgreSQL, and performs analytical queries using SQL.

## Project Overview

This project demonstrates a complete ETL pipeline:

**Frankfurter API → Python → Pandas → PostgreSQL → Analytical SQL**

The pipeline collects historical USD exchange rates for EUR, GBP, JPY, CAD, and AUD.

The project focuses on practical data engineering concepts including:

- REST API integration
- Data extraction and transformation
- Data cleaning with pandas
- PostgreSQL database loading
- Data quality validation
- SQL analytics
- Window functions and CTEs
- Database indexing
- Automated testing
- Environment configuration

## Architecture

```text
┌─────────────────────┐
│   Frankfurter API   │
│ Exchange Rate Data  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     extract.py      │
│    API Extraction   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    transform.py     │
│  Pandas Processing   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│       load.py       │
│ PostgreSQL Loading  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    PostgreSQL DB    │
│   exchange_rates    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    Analytical SQL   │
│    7 SQL Queries    │
└─────────────────────┘
```

## Data Source

This project uses the [Frankfurter API](https://frankfurter.dev/), a free public foreign exchange rates API.

### Configuration

- **Base currency:** USD
- **Target currencies:** EUR, GBP, JPY, CAD, AUD
- **Data type:** Historical exchange rates
- **Storage:** PostgreSQL
- **Transformation:** pandas

The current dataset contains **2,170 records** across **5 currencies**.

## Project Structure

```text
exchange-rate-analytics-pipeline/
│
├── data/
│
├── sql/
│   ├── 01_monthly_average.sql
│   ├── 02_high_low_rates.sql
│   ├── 03_currency_volatility.sql
│   ├── 04_month_over_month.sql
│   ├── 05_currency_performance.sql
│   ├── 06_indexes.sql
│   └── 07_data_quality.sql
│
├── src/
│   ├── __init__.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── pipeline.py
│
├── tests/
│   └── test_transform.py
│
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

## ETL Pipeline

### 1. Extract

`extract.py` connects to the Frankfurter API and retrieves historical exchange rate data.

The API response contains exchange rates grouped by date and currency.

### 2. Transform

`transform.py` converts the nested API response into a structured pandas DataFrame.

The transformation process:

- Converts API JSON into tabular data
- Converts dates to datetime
- Converts exchange rates to numeric values
- Removes duplicate records
- Removes invalid non-positive rates
- Sorts the resulting dataset

The resulting DataFrame contains:

```text
rate_date
base_currency
target_currency
rate
```

### 3. Load

`load.py` loads the transformed data into PostgreSQL.

The database uses a unique constraint on:

```text
rate_date
base_currency
target_currency
```

This prevents duplicate exchange-rate records when the pipeline is run multiple times.

### 4. Pipeline Orchestration

`pipeline.py` combines extraction, transformation, and loading into a single pipeline.

Run the complete pipeline with:

```bash
python -m src.pipeline
```

## Database Schema

The project uses the following PostgreSQL table:

```sql
CREATE TABLE IF NOT EXISTS exchange_rates (
    id SERIAL PRIMARY KEY,
    rate_date DATE NOT NULL,
    base_currency VARCHAR(3) NOT NULL,
    target_currency VARCHAR(3) NOT NULL,
    rate NUMERIC(18, 8) NOT NULL,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_exchange_rate
        UNIQUE (rate_date, base_currency, target_currency),
    CONSTRAINT positive_exchange_rate
        CHECK (rate > 0)
);
```

## SQL Analysis

The project contains seven SQL scripts covering different analytical and database concepts.

### 1. Monthly Average Rates

Calculates the average exchange rate for each currency by month.

**Concepts:** `GROUP BY`, `AVG()`, date aggregation

### 2. High and Low Rates

Identifies the lowest rate, highest rate, and overall rate range for each currency.

**Concepts:** `MIN()`, `MAX()`, aggregation

### 3. Currency Volatility

Measures exchange-rate volatility using standard deviation and coefficient of variation.

**Concepts:** `STDDEV()`, statistical analysis

The coefficient of variation is used to make volatility more comparable across currencies with different rate scales.

### 4. Month-over-Month Changes

Calculates monthly exchange-rate changes compared with the previous month.

**Concepts:** CTEs, `LAG()`, window functions

### 5. Currency Performance

Compares the first and last observed exchange rates and calculates the overall percentage change.

**Concepts:** CTEs, `ROW_NUMBER()`, conditional aggregation

### 6. Database Indexes

Creates indexes on frequently queried columns:

- `rate_date`
- `target_currency`
- `target_currency, rate_date`

### 7. Data Quality Checks

Validates:

- Total number of records
- Unique dates
- Unique currencies
- Null exchange rates
- Invalid exchange rates
- Observation coverage by currency

## Data Quality

Data quality is handled at both the Python and PostgreSQL levels.

### Python Validation

Automated tests verify:

- DataFrame creation
- Required columns
- Positive exchange rates
- Missing values
- Duplicate records
- Expected row count

### PostgreSQL Validation

The database enforces:

- `NOT NULL` constraints
- Positive exchange-rate validation
- Unique exchange-rate records

## Testing

The project uses `pytest` for automated testing.

Run the test suite with:

```bash
pytest
```

The current test suite contains 6 tests covering the transformation process.

Example result:

```text
6 passed
```

## Setup

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd exchange-rate-analytics-pipeline
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example`.

Example:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=exchange_rate_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
```

Do not commit `.env` to GitHub.

### 5. Create the database table

Create the `exchange_rates` table in your PostgreSQL database using the schema provided above.

### 6. Run the pipeline

```bash
python -m src.pipeline
```

### 7. Run tests

```bash
pytest
```

### 8. Run analytical SQL queries

The SQL queries are available in:

```text
sql/
```

They can be executed using PostgreSQL clients such as DBeaver or pgAdmin.

## Technologies Used

- **Python**
- **pandas**
- **Requests**
- **PostgreSQL**
- **SQLAlchemy**
- **psycopg2**
- **pytest**
- **python-dotenv**
- **SQL**
- **Git & GitHub**

## Key Skills Demonstrated

- REST API integration
- ETL pipeline development
- Data transformation with pandas
- Relational database design
- PostgreSQL data loading
- SQL aggregation
- CTEs
- Window functions
- Statistical analysis
- Data quality validation
- Database indexing
- Automated testing
- Environment configuration
- Git-based version control

## Future Improvements

Potential improvements include:

- Parameterizing extraction dates and currencies
- Adding structured logging
- Implementing incremental data loading
- Scheduling automated pipeline runs
- Adding Power BI visualizations
- Adding GitHub Actions for CI
- Expanding the number of currencies
- Adding additional financial analytics

## License

This project is intended for educational and portfolio purposes.
