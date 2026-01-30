import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def compute_qini_curve(y_true, uplift_scores, treatment):
    df = pd.DataFrame({
        "y": y_true,
        "uplift": uplift_scores,
        "treatment": treatment
    })

    df = df.sort_values("uplift", ascending=False).reset_index(drop=True)

    df["cum_treated"] = (df["treatment"] == 1).cumsum()
    df["cum_control"] = (df["treatment"] == 0).cumsum()

    df["cum_y_treated"] = (df["y"] * (df["treatment"] == 1)).cumsum()
    df["cum_y_control"] = (df["y"] * (df["treatment"] == 0)).cumsum()

    df["qini"] = (
        df["cum_y_treated"] -
        df["cum_y_control"] *
        (df["cum_treated"] / df["cum_control"].replace(0, 1))
    )

    return df


def compute_auuc(qini_df):
    return np.trapz(qini_df["qini"])


def uplift_at_k(y_true, uplift_scores, treatment, k=0.1):
    df = pd.DataFrame({
        "y": y_true,
        "uplift": uplift_scores,
        "treatment": treatment
    })

    df = df.sort_values("uplift", ascending=False)
    top_k = df.head(int(len(df) * k))

    treat_conv = top_k[top_k["treatment"] == 1]["y"].mean()
    control_conv = top_k[top_k["treatment"] == 0]["y"].mean()

    return treat_conv - control_conv


def plot_qini_curve(qini_df):
    plt.figure(figsize=(8, 6))
    plt.plot(qini_df["qini"], label="Model")
    plt.plot(
        [0, len(qini_df)],
        [0, qini_df["qini"].iloc[-1]],
        linestyle="--",
        label="Random Baseline"
    )
    plt.title("Qini Curve")
    plt.xlabel("Population (Sorted by Uplift)")
    plt.ylabel("Incremental Gains")
    plt.legend()
    plt.show()
