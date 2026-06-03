from sklearn.ensemble import RandomForestClassifier

def test_model_fit(X_train, y_train):
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    assert hasattr(model, "predict")