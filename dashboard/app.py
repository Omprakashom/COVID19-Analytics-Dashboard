import streamlit as st
import pandas as pd
import plotly.express as px  

# ---------------------------------------
# Page Configuration
# ---------------------------------------
st.set_page_config(
    page_title="COVID-19 Analytics Dashboard",
    page_icon="🦠",
    layout="wide"
)

# ---------------------------------------
# Load Dataset
# ---------------------------------------
import gdown
import os

@st.cache_data
def load_data():
    file_id = "1J-XvXkqhrUakkubRmI8tmSEP1gcoP_MS"
    url = f"https://drive.google.com/uc?id={file_id}"

    output = "owid-covid-data.csv"

    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)

    df = pd.read_csv(output)
    df["date"] = pd.to_datetime(df["date"])

    return df



df = load_data()

# ---------------------------------------
# Dashboard Title
# ---------------------------------------
st.title("🦠 COVID-19 Analytics Dashboard")
st.markdown("### Interactive COVID-19 Dashboard using Streamlit")

# ---------------------------------------
# Sidebar
# ---------------------------------------
st.sidebar.header("Filters")

country = st.sidebar.selectbox(
    "Select Country",
    sorted(df["location"].dropna().unique())
)

country_df = df[df["location"] == country]

# ----------------------------
# Date Filter
# ----------------------------
min_date = country_df["date"].min()
max_date = country_df["date"].max()

date_range = st.sidebar.slider(
    "Select Date Range",
    min_value=min_date.to_pydatetime(),
    max_value=max_date.to_pydatetime(),
    value=(min_date.to_pydatetime(), max_date.to_pydatetime())
)

country_df = country_df[
    (country_df["date"] >= pd.Timestamp(date_range[0])) &
    (country_df["date"] <= pd.Timestamp(date_range[1]))
]

# ---------------------------------------
# Latest Data
# ---------------------------------------
country_df = country_df.sort_values("date")

latest = country_df.dropna(subset=["total_cases"]).iloc[-1]

# ---------------------------------------
# KPI Cards
# ---------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    total_cases = 0 if pd.isna(latest["total_cases"]) else int(latest["total_cases"])
    st.metric("Total Cases", f"{total_cases:,}")

with col2:
    total_deaths = 0 if pd.isna(latest["total_deaths"]) else int(latest["total_deaths"])
    st.metric("Total Deaths", f"{total_deaths:,}")

with col3:
    population = 0 if pd.isna(latest["population"]) else int(latest["population"])
    st.metric("Population", f"{population:,}")

# ---------------------------------------
# Daily Cases Chart
# ---------------------------------------
st.subheader(f"Daily New Cases - {country}")

chart = country_df[["date", "new_cases"]].dropna()

fig = px.line(
    chart,
    x="date",
    y="new_cases",
    title=f"Daily New Cases in {country}"
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="New Cases"
)

st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------
# Daily Deaths Chart
# ---------------------------------------
st.subheader(f"Daily New Deaths - {country}")

death_chart = country_df[["date", "new_deaths"]].dropna()

fig = px.line(
    death_chart,
    x="date",
    y="new_deaths",
    title=f"Daily New Deaths in {country}"
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="New Deaths"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------
# Vaccination Chart
# ---------------------------------------
st.subheader(f"People Vaccinated - {country}")

vacc_chart = country_df[["date", "people_vaccinated"]].dropna()

if len(vacc_chart) > 0:
    fig = px.line(
        vacc_chart,
        x="date",
        y="people_vaccinated",
        title=f"People Vaccinated in {country}"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="People Vaccinated"
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Vaccination data not available.")

# ---------------------------------------
