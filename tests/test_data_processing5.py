import pandas as pd
from src.data_processing import create_rfm_features, run_kmeans_clustering


# -----------------------------
# Test 1: RFM feature columns
# -----------------------------
def test_create_rfm_features_columns(sample_df):
    rfm = create_rfm_features(sample_df)

    expected_columns = {"CustomerId", "recency", "frequency", "monetary"}

    assert expected_columns.issubset(rfm.columns), \
        "RFM feature engineering did not return expected columns"


# -----------------------------
# Test 2: KMeans clustering output
# -----------------------------
def test_kmeans_creates_cluster_column(sample_rfm):
    clustered = run_kmeans_clustering(sample_rfm)

    assert "cluster" in clustered.columns, \
        "Cluster column not created"

    assert clustered["cluster"].nunique() == 3, \
        "KMeans should produce exactly 3 clusters"