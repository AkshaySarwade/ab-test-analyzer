"""
E-commerce Conversion A/B Test Analyzer
========================================
A Streamlit application for analyzing A/B test results on e-commerce
conversion data. Calculates conversion rates, lift, statistical
significance, and provides ship/no-ship recommendations.

Author: Akshay Sarwade
GitHub: https://github.com/AkshaySarwade
"""

import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="A/B Test Analyzer",
    page_icon="📊",
    layout="wide"
)

# ----------------------------------------------------------------------
# STATISTICAL FUNCTIONS
# ----------------------------------------------------------------------

def calculate_conversion_rates(df, group_col, conversion_col):
    """Calculate conversion rate for each group (control vs variant)."""
    summary = df.groupby(group_col)[conversion_col].agg(['count', 'sum'])
    summary.columns = ['users', 'conversions']
    summary['conversion_rate'] = summary['conversions'] / summary['users']
    return summary


def calculate_lift(control_rate, variant_rate):
    """Calculate relative lift of variant over control."""
    if control_rate == 0:
        return 0
    return ((variant_rate - control_rate) / control_rate) * 100


def two_proportion_z_test(control_users, control_conv,
                           variant_users, variant_conv):
    """
    Two-proportion z-test for A/B testing.
    Returns: z_stat, p_value
    """
    p1 = control_conv / control_users
    p2 = variant_conv / variant_users

    # Pooled proportion under null hypothesis
    p_pool = (control_conv + variant_conv) / (control_users + variant_users)

    # Standard error
    se = np.sqrt(p_pool * (1 - p_pool) *
                 (1 / control_users + 1 / variant_users))

    if se == 0:
        return 0, 1.0

    # Z-statistic
    z_stat = (p2 - p1) / se

    # Two-tailed p-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    return z_stat, p_value


def confidence_interval(users, conversions, confidence=0.95):
    """95% confidence interval for a conversion rate."""
    p = conversions / users
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    margin = z * np.sqrt(p * (1 - p) / users)
    return max(0, p - margin), min(1, p + margin)


def make_recommendation(p_value, lift, alpha=0.05, min_lift=2.0):
    """
    Decision rule:
    - SHIP if statistically significant AND lift exceeds minimum threshold
    - DO NOT SHIP otherwise
    """
    if p_value < alpha and lift > min_lift:
        return "SHIP IT", "green", (
            f"Variant is statistically significantly better "
            f"(p < {alpha}) with meaningful lift ({lift:.2f}% > {min_lift}%)."
        )
    elif p_value < alpha and lift <= min_lift:
        return "DO NOT SHIP", "orange", (
            f"Result is statistically significant but the lift "
            f"({lift:.2f}%) is below the minimum business threshold "
            f"({min_lift}%)."
        )
    elif p_value >= alpha and lift > min_lift:
        return "INCONCLUSIVE", "orange", (
            f"Lift looks promising ({lift:.2f}%) but not statistically "
            f"significant (p = {p_value:.4f}). Consider running the test "
            f"longer for more data."
        )
    else:
        return "DO NOT SHIP", "red", (
            f"No significant difference detected "
            f"(p = {p_value:.4f}, lift = {lift:.2f}%)."
        )


# ----------------------------------------------------------------------
# UI
# ----------------------------------------------------------------------

st.title("📊 E-commerce A/B Test Analyzer")
st.markdown(
    "Upload your A/B test data to evaluate conversion lift, statistical "
    "significance, and get a clear ship / no-ship recommendation."
)

# --- Sidebar settings ---
st.sidebar.header("Test Configuration")
alpha = st.sidebar.slider(
    "Significance level (α)", 0.01, 0.10, 0.05, 0.01,
    help="Threshold for statistical significance. 0.05 means 95% confidence."
)
min_lift = st.sidebar.slider(
    "Minimum business lift (%)", 0.0, 20.0, 2.0, 0.5,
    help="The minimum lift you'd ship a feature for."
)

# --- Data input ---
st.header("1. Load Your Data")

input_method = st.radio(
    "How do you want to provide data?",
    ("Use sample data", "Upload CSV"),
    horizontal=True
)

df = None

if input_method == "Upload CSV":
    uploaded = st.file_uploader(
        "Upload A/B test CSV (must have group and conversion columns)",
        type="csv"
    )
    if uploaded:
        df = pd.read_csv(uploaded)
else:
    # Generate sample data for demo purposes
    np.random.seed(42)
    n_control, n_variant = 5000, 5000
    df = pd.DataFrame({
        'user_id': range(n_control + n_variant),
        'group': ['control'] * n_control + ['variant'] * n_variant,
        'converted': (
            list(np.random.binomial(1, 0.10, n_control)) +
            list(np.random.binomial(1, 0.115, n_variant))
        )
    })
    st.info(
        "Using simulated data: 5,000 users per group, control conversion "
        "rate = 10%, variant conversion rate = 11.5%."
    )

if df is not None:
    st.dataframe(df.head(10), use_container_width=True)

    # --- Column selection ---
    st.header("2. Select Columns")
    col1, col2 = st.columns(2)
    with col1:
        group_col = st.selectbox(
            "Group column (control / variant)",
            df.columns,
            index=list(df.columns).index('group') if 'group' in df.columns else 0
        )
    with col2:
        conv_col = st.selectbox(
            "Conversion column (1 / 0)",
            df.columns,
            index=list(df.columns).index('converted')
                  if 'converted' in df.columns else 0
        )

    # --- Analysis ---
    st.header("3. Test Results")

    summary = calculate_conversion_rates(df, group_col, conv_col)
    if len(summary) != 2:
        st.error(
            "The group column must have exactly 2 values "
            "(e.g. 'control' and 'variant')."
        )
    else:
        groups = summary.index.tolist()
        # Heuristic: 'control' first, otherwise alphabetical
        if 'control' in groups:
            control_name = 'control'
            variant_name = [g for g in groups if g != 'control'][0]
        else:
            control_name, variant_name = sorted(groups)

        control = summary.loc[control_name]
        variant = summary.loc[variant_name]

        # Metrics row
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(
            f"{control_name.title()} CR",
            f"{control['conversion_rate']:.2%}",
            f"{int(control['users'])} users"
        )
        m2.metric(
            f"{variant_name.title()} CR",
            f"{variant['conversion_rate']:.2%}",
            f"{int(variant['users'])} users"
        )

        lift = calculate_lift(
            control['conversion_rate'], variant['conversion_rate']
        )
        m3.metric("Relative Lift", f"{lift:+.2f}%")

        z, p_value = two_proportion_z_test(
            int(control['users']), int(control['conversions']),
            int(variant['users']), int(variant['conversions'])
        )
        m4.metric("p-value", f"{p_value:.4f}")

        # Confidence intervals
        st.subheader("95% Confidence Intervals")
        ci_control = confidence_interval(
            int(control['users']), int(control['conversions'])
        )
        ci_variant = confidence_interval(
            int(variant['users']), int(variant['conversions'])
        )
        ci_df = pd.DataFrame({
            'Group': [control_name, variant_name],
            'Conversion Rate': [
                f"{control['conversion_rate']:.2%}",
                f"{variant['conversion_rate']:.2%}"
            ],
            '95% CI Lower': [f"{ci_control[0]:.2%}", f"{ci_variant[0]:.2%}"],
            '95% CI Upper': [f"{ci_control[1]:.2%}", f"{ci_variant[1]:.2%}"],
        })
        st.dataframe(ci_df, use_container_width=True)

        # --- Visualization ---
        st.subheader("Visualization")
        fig, ax = plt.subplots(figsize=(8, 4))
        rates = [control['conversion_rate'], variant['conversion_rate']]
        errors = [
            (ci_control[1] - ci_control[0]) / 2,
            (ci_variant[1] - ci_variant[0]) / 2,
        ]
        bars = ax.bar(
            [control_name, variant_name], rates,
            yerr=errors, capsize=10,
            color=['#4C72B0', '#55A868'], alpha=0.85
        )
        ax.set_ylabel("Conversion Rate")
        ax.set_title("Conversion Rate by Group (with 95% CI)")
        for bar, rate in zip(bars, rates):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.001,
                f"{rate:.2%}", ha='center', va='bottom', fontweight='bold'
            )
        st.pyplot(fig)

        # --- Recommendation ---
        st.header("4. Recommendation")
        decision, color, reasoning = make_recommendation(
            p_value, lift, alpha, min_lift
        )
        st.markdown(
            f"<div style='padding:1rem;border-radius:8px;"
            f"background-color:{color};color:white;font-size:1.5rem;"
            f"font-weight:bold;text-align:center;'>{decision}</div>",
            unsafe_allow_html=True
        )
        st.info(reasoning)

        # Educational notes
        with st.expander("📚 What does this mean?"):
            st.markdown("""
            - **Conversion Rate (CR):** Fraction of users who converted in each group.
            - **Relative Lift:** Percentage improvement of the variant over control.
            - **p-value:** Probability of seeing this result (or more extreme) if there were truly no difference between the groups. Lower = stronger evidence the variant is different.
            - **Confidence Interval:** The range of plausible true conversion rates given the data.
            - **Statistical significance** alone is not enough — the lift also has to be large enough to matter to the business. That is why we check both.
            """)
