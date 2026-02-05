import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Financial Inclusion Dashboard", layout="wide")

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/ethiopia_fi_enriched_data.csv")
    return df

df = load_data()

# Clean essentials
df = df[df["record_type"] == "observation"].copy()
df["year"] = pd.to_datetime(df["observation_date"], errors="coerce").dt.year

# Targets
TARGETS = {
    "ACC_OWNERSHIP": "Account Ownership",
    "ACC_MM_ACCOUNT": "Mobile Money Accounts",
    "USG_DIGITAL_PAYMENT": "Digital Payment Usage"
}

df = df[df["indicator_code"].isin(TARGETS.keys())]

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Overview", "Trends", "Forecasts", "Inclusion Projections"]
)

# -----------------------------
# OVERVIEW
# -----------------------------
if page == "Overview":
    st.title("Financial Inclusion Overview")

    latest = df.sort_values("year").groupby("indicator_code").last()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Account Ownership (%)",
        f"{latest.loc['ACC_OWNERSHIP', 'value_numeric']:.1f}"
    )

    col2.metric(
        "Mobile Money Accounts (%)",
        f"{latest.loc['ACC_MM_ACCOUNT', 'value_numeric']:.1f}"
    )

    if "USG_DIGITAL_PAYMENT" in latest.index:
        col3.metric(
            "Digital Payment Usage (%)",
            f"{latest.loc['USG_DIGITAL_PAYMENT', 'value_numeric']:.1f}"
        )
    else:
        col3.metric("Digital Payment Usage (%)", "N/A")

    st.subheader("Latest Observations")
    st.dataframe(latest[["value_numeric"]])

# -----------------------------
# TRENDS
# -----------------------------
elif page == "Trends":
    st.title("Historical Trends")

    indicator = st.selectbox(
        "Select Indicator",
        list(TARGETS.keys()),
        format_func=lambda x: TARGETS[x]
    )

    data = df[df["indicator_code"] == indicator]

    fig = px.line(
        data,
        x="year",
        y="value_numeric",
        markers=True,
        title=TARGETS[indicator]
    )

    st.plotly_chart(fig, use_container_width=True)

    st.download_button(
        "Download Data",
        data.to_csv(index=False),
        file_name=f"{indicator}_trend.csv"
    )

# -----------------------------
# FORECASTS
# -----------------------------
elif page == "Forecasts":
    st.title("Forecasts (2025–2027)")

    indicator = st.selectbox(
        "Select Indicator",
        list(TARGETS.keys()),
        format_func=lambda x: TARGETS[x]
    )

    hist = df[df["indicator_code"] == indicator]

    if len(hist) < 2:
        st.warning("Not enough data to forecast.")
    else:
        X = hist["year"].values.reshape(-1, 1)
        y = hist["value_numeric"].values

        model = LinearRegression()
        model.fit(X, y)

        future_years = np.array([2025, 2026, 2027]).reshape(-1, 1)
        preds = model.predict(future_years)

        forecast_df = pd.DataFrame({
            "year": future_years.flatten(),
            "forecast": preds
        })

        fig = px.line(
            forecast_df,
            x="year",
            y="forecast",
            markers=True,
            title=f"Baseline Forecast: {TARGETS[indicator]}"
        )

        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(forecast_df)

# -----------------------------
# INCLUSION PROJECTIONS
# -----------------------------
elif page == "Inclusion Projections":
    st.title("Inclusion Target Projections")

    acc = df[df["indicator_code"] == "ACC_OWNERSHIP"]

    if len(acc) < 2:
        st.warning("Not enough data to project inclusion.")
    else:
        X = acc["year"].values.reshape(-1, 1)
        y = acc["value_numeric"].values

        model = LinearRegression()
        model.fit(X, y)

        future_years = np.array([2025, 2026, 2027]).reshape(-1, 1)
        preds = model.predict(future_years)

        proj = pd.DataFrame({
            "year": future_years.flatten(),
            "forecast": preds
        })

        fig = px.line(
            proj,
            x="year",
            y="forecast",
            markers=True,
            title="Account Ownership Projection"
        )

        fig.add_hline(
            y=60,
            line_dash="dash",
            annotation_text="60% National Target"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.write(
            "This projection shows progress toward Ethiopia’s 60% financial inclusion target."
        )
