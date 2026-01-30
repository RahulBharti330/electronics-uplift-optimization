import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_data(path):
    return pd.read_csv(path)


def preprocess_data(df, target_col="conversion", treatment_col="treatment"):
    df = df.dropna()

    X = df.drop(columns=[target_col, treatment_col])
    y = df[target_col]
    treatment = df[treatment_col]

    # Scale numeric features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y.values, treatment.values


def split_data(X, y, treatment, test_size=0.2, random_state=42):
    return train_test_split(
        X, y, treatment,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )
