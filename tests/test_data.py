import pandas as pd

def test_no_missing_target(df):
    assert df['is_high_risk'].isna().sum() == 0