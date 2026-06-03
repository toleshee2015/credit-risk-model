import pytest
import pandas as pd


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "CustomerId": ["A", "A", "B", "B"],
        "TransactionId": [1, 2, 3, 4],
        "TransactionStartTime": pd.to_datetime([
            "2024-01-01",
            "2024-01-05",
            "2024-01-03",
            "2024-01-10"
        ]),
        "Amount": [100, 200, 150, 300]
    })


@pytest.fixture
def sample_rfm():
    return pd.DataFrame({
        "CustomerId": ["A", "B", "C"],
        "recency": [10, 20, 30],
        "frequency": [5, 3, 1],
        "monetary": [1000, 500, 200]
    })