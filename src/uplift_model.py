from xgboost import XGBClassifier
import numpy as np


def train_two_model(X_train, y_train, treatment_train):

    X_treat = X_train[treatment_train == 1]
    y_treat = y_train[treatment_train == 1]

    X_control = X_train[treatment_train == 0]
    y_control = y_train[treatment_train == 0]

    model_treat = XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        use_label_encoder=False,
        eval_metric="logloss"
    )

    model_control = XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        use_label_encoder=False,
        eval_metric="logloss"
    )

    model_treat.fit(X_treat, y_treat)
    model_control.fit(X_control, y_control)

    return model_treat, model_control


def predict_uplift(model_treat, model_control, X):
    p_treat = model_treat.predict_proba(X)[:, 1]
    p_control = model_control.predict_proba(X)[:, 1]

    uplift = p_treat - p_control
    return uplift
