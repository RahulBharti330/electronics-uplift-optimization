import pandas as pd


def simulate_profit(y_true, uplift_scores, treatment,
                    discount_cost=10,
                    product_margin=50,
                    k=0.1):

    df = pd.DataFrame({
        "y": y_true,
        "uplift": uplift_scores,
        "treatment": treatment
    })

    df = df.sort_values("uplift", ascending=False)
    top_k = df.head(int(len(df) * k))

    treat_conv = top_k[top_k["treatment"] == 1]["y"].mean()
    control_conv = top_k[top_k["treatment"] == 0]["y"].mean()

    incremental_conversion = treat_conv - control_conv

    expected_profit = (incremental_conversion * product_margin) - discount_cost

    return expected_profit
