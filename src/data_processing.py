import pandas as pd
import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# ===================================================
# 1. CUSTOMER AGGREGATIONS
# ===================================================
class CustomerAggregator(BaseEstimator, TransformerMixin):

    def __init__(self, customer_col="CustomerId", amount_col="Amount"):
        self.customer_col = customer_col
        self.amount_col = amount_col

    def fit(self, X, y=None):
        return self

    def transform(self, X):

        X = X.copy()

        if self.customer_col not in X.columns:
            return X  # safety guard

        agg = X.groupby(self.customer_col).agg(
            TotalTransactionAmount=(self.amount_col, "sum"),
            AverageTransactionAmount=(self.amount_col, "mean"),
            TransactionCount=(self.amount_col, "count"),
            StdTransactionAmount=(self.amount_col, "std")
        ).reset_index()

        agg["StdTransactionAmount"] = agg["StdTransactionAmount"].fillna(0)

        return X.merge(agg, on=self.customer_col, how="left")


# ===================================================
# 2. TIME FEATURES
# ===================================================
class TimeFeatureExtractor(BaseEstimator, TransformerMixin):

    def __init__(self, time_col="TransactionStartTime"):
        self.time_col = time_col

    def fit(self, X, y=None):
        return self

    def transform(self, X):

        X = X.copy()

        if self.time_col not in X.columns:
            return X

        X[self.time_col] = pd.to_datetime(X[self.time_col], errors="coerce")

        X["TransactionHour"] = X[self.time_col].dt.hour
        X["TransactionDay"] = X[self.time_col].dt.day
        X["TransactionMonth"] = X[self.time_col].dt.month
        X["TransactionYear"] = X[self.time_col].dt.year

        return X


# ===================================================
# 3. PREPROCESSOR
# ===================================================
DROP_COLS = [
    "TransactionId",
    "BatchId",
    "AccountId",
    "SubscriptionId",
    "CustomerId",
    "CurrencyCode"
]


def build_preprocessor(X):

    X = X.drop(columns=DROP_COLS, errors="ignore")

    num_cols = X.select_dtypes(include=["int64", "float64"]).columns
    cat_cols = X.select_dtypes(include=["object", "string"]).columns

    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    return ColumnTransformer([
        ("num", numeric_pipeline, num_cols),
        ("cat", categorical_pipeline, cat_cols)
    ])


# ===================================================
# 4. FULL PIPELINE
# ===================================================
class FullPipelineWrapper(BaseEstimator, TransformerMixin):

    def __init__(self):

        self.feature_engineering_steps = [
            CustomerAggregator(),
            TimeFeatureExtractor()
        ]

        self.preprocessor = None

    def fit(self, X, y=None):

        X_fe = X.copy()

        # FEATURE ENGINEERING FIRST
        for step in self.feature_engineering_steps:
            X_fe = step.fit_transform(X_fe, y)

        # DROP ONLY AFTER FEATURE ENGINEERING
        X_fe = X_fe.drop(columns=DROP_COLS, errors="ignore")

        # BUILD + FIT PREPROCESSOR
        self.preprocessor = build_preprocessor(X_fe)
        self.preprocessor.fit(X_fe, y)

        return self

    def transform(self, X):

        X_fe = X.copy()

        # FEATURE ENGINEERING
        for step in self.feature_engineering_steps:
            X_fe = step.transform(X_fe)

        # DROP ONLY AFTER FEATURE ENGINEERING
        X_fe = X_fe.drop(columns=DROP_COLS, errors="ignore")

        return self.preprocessor.transform(X_fe)


# ===================================================
# 5. ENTRY POINT
# ===================================================
def process_data(df):

    pipeline = FullPipelineWrapper()
    X_processed = pipeline.fit_transform(df)

    return X_processed, pipeline