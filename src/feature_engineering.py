import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class AggregateFeatures(BaseEstimator, TransformerMixin):
    
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        
        df = X.copy()

        customer_agg = (
    df.groupby('CustomerId')
      .agg(
          TotalTransactionAmount=('Amount', 'sum'),
          AverageTransactionAmount=('Amount', 'mean'),
          TransactionCount=('TransactionId', 'count'),
          StdTransactionAmount=('Amount', 'std'),
          MaxTransactionAmount=('Amount', 'max'),
          MinTransactionAmount=('Amount', 'min')
      )
      .reset_index()
)
        )

        customer_agg['StdTransactionAmount'] = (
            customer_agg['StdTransactionAmount']
            .fillna(0)
        )

        df = df.merge(
            customer_agg,
            on='CustomerId',
            how='left'
        )

        return df