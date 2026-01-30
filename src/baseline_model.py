from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score


def train_baseline_model(X_train, y_train):
    model = XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        use_label_encoder=False,
        eval_metric="logloss"
    )
    model.fit(X_train, y_train)
    return model


def evaluate_baseline(model, X_test, y_test):
    preds = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, preds)
    return auc
