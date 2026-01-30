from src.data_preprocessing import load_data, preprocess_data, split_data
from src.baseline_model import train_baseline_model, evaluate_baseline
from src.uplift_model import train_two_model, predict_uplift
from src.evaluation import (
    compute_qini_curve,
    compute_auuc,
    uplift_at_k,
    plot_qini_curve
)
from src.profit_simulation import simulate_profit


def main():

    df = load_data("data/raw/data.csv")

    X, y, treatment = preprocess_data(df)

    X_train, X_test, y_train, y_test, treat_train, treat_test = split_data(
        X, y, treatment
    )

    # Baseline
    baseline_model = train_baseline_model(X_train, y_train)
    auc = evaluate_baseline(baseline_model, X_test, y_test)
    print("Baseline ROC-AUC:", round(auc, 4))

    # Uplift
    model_treat, model_control = train_two_model(
        X_train, y_train, treat_train
    )

    uplift_scores = predict_uplift(
        model_treat, model_control, X_test
    )

    lift = uplift_at_k(y_test, uplift_scores, treat_test, k=0.1)
    print("Top 10% Incremental Lift:", round(lift, 4))

    # Qini + AUUC
    qini_df = compute_qini_curve(y_test, uplift_scores, treat_test)
    auuc = compute_auuc(qini_df)
    print("AUUC:", round(auuc, 4))

    plot_qini_curve(qini_df)

    # Profit Simulation
    profit = simulate_profit(
        y_test,
        uplift_scores,
        treat_test,
        discount_cost=10,
        product_margin=50,
        k=0.1
    )

    print("Simulated Profit Impact:", round(profit, 4))


if __name__ == "__main__":
    main()
