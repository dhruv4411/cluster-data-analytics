from pathlib import Path

import joblib
import pandas as pd
import plotly.express as px
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "data" / "processed" / "samples" / "data_center_sample.csv"
SCHEDULE_PATH = ROOT_DIR / "data" / "processed" / "final" / "optimized_schedule.csv"
ENERGY_MODEL_PATH = ROOT_DIR / "models" / "energy_model.joblib"
THERMAL_MODEL_PATH = ROOT_DIR / "models" / "thermal_model.joblib"

ENERGY_FEATURES = [
    "cpu_usage",
    "memory_usage",
    "disk_io",
    "network_io",
    "task_duration",
    "priority",
    "outside_temperature",
    "cooling_efficiency",
]

THERMAL_FEATURES = ENERGY_FEATURES + ["power_usage"]


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


@st.cache_data
def load_schedule() -> pd.DataFrame:
    if not SCHEDULE_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(SCHEDULE_PATH)


@st.cache_resource
def load_model(path: Path):
    if not path.exists():
        return None
    return joblib.load(path)


def get_status(temperature: float) -> str:
    if temperature < 35:
        return "Normal"
    if temperature < 45:
        return "Warning"
    return "Critical"


def show_overview(df: pd.DataFrame) -> None:
    st.subheader("Data Center Overview")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Servers", df["server_id"].nunique())
    col2.metric("Avg CPU", f"{df['cpu_usage'].mean():.2f}%")
    col3.metric("Avg Power", f"{df['power_usage'].mean():.2f} W")
    col4.metric("Avg Temp", f"{df['temperature'].mean():.2f} C")

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        fig = px.line(
            df.head(300),
            x="timestamp",
            y="power_usage",
            title="Power Usage Over Time",
        )
        st.plotly_chart(fig, use_container_width=True)

    with chart_col2:
        fig = px.scatter(
            df,
            x="cpu_usage",
            y="power_usage",
            color="thermal_status",
            title="CPU Usage vs Power Usage",
        )
        st.plotly_chart(fig, use_container_width=True)


def show_predictions(df: pd.DataFrame) -> None:
    st.subheader("Energy And Thermal Prediction")

    energy_model = load_model(ENERGY_MODEL_PATH)
    thermal_model = load_model(THERMAL_MODEL_PATH)

    if energy_model is None or thermal_model is None:
        st.warning("Train both models before using predictions.")
        return

    col1, col2 = st.columns(2)
    cpu_usage = col1.slider("CPU Usage (%)", 5.0, 100.0, 65.0)
    memory_usage = col2.slider("Memory Usage (%)", 10.0, 100.0, 55.0)
    disk_io = col1.slider("Disk I/O", 1.0, 500.0, 140.0)
    network_io = col2.slider("Network I/O", 1.0, 1000.0, 260.0)
    task_duration = col1.slider("Task Duration (minutes)", 1.0, 240.0, 40.0)
    priority = col2.selectbox("Priority", [1, 2, 3], index=1)
    outside_temperature = col1.slider("Outside Temperature (C)", 10.0, 45.0, 28.0)
    cooling_efficiency = col2.slider("Cooling Efficiency", 0.55, 0.95, 0.78)

    energy_input = pd.DataFrame(
        [
            {
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage,
                "disk_io": disk_io,
                "network_io": network_io,
                "task_duration": task_duration,
                "priority": priority,
                "outside_temperature": outside_temperature,
                "cooling_efficiency": cooling_efficiency,
            }
        ]
    )

    predicted_power = energy_model.predict(energy_input[ENERGY_FEATURES])[0]
    thermal_input = energy_input.copy()
    thermal_input["power_usage"] = predicted_power
    predicted_temperature = thermal_model.predict(thermal_input[THERMAL_FEATURES])[0]
    status = get_status(predicted_temperature)

    result_col1, result_col2, result_col3 = st.columns(3)
    result_col1.metric("Predicted Power", f"{predicted_power:.2f} W")
    result_col2.metric("Predicted Temp", f"{predicted_temperature:.2f} C")
    result_col3.metric("Thermal Status", status)


def show_scheduler(schedule: pd.DataFrame) -> None:
    st.subheader("Optimized Scheduling")

    if schedule.empty:
        st.warning("Run src/scheduler.py before opening this page.")
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Scheduled Tasks", len(schedule))
    col2.metric("Avg Estimated Power", f"{schedule['estimated_power_usage'].mean():.2f} W")
    col3.metric("Avg Estimated Temp", f"{schedule['estimated_temperature'].mean():.2f} C")

    fig = px.bar(
        schedule.head(30),
        x="assigned_server",
        y="estimated_temperature",
        color="thermal_status",
        title="Estimated Temperature After Scheduling",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(schedule, use_container_width=True)


def show_alerts(df: pd.DataFrame) -> None:
    st.subheader("Reliability Alerts")

    hot_servers = df[df["thermal_status"] == "Critical"]
    warning_servers = df[df["thermal_status"] == "Warning"]

    col1, col2 = st.columns(2)
    col1.metric("Critical Records", len(hot_servers))
    col2.metric("Warning Records", len(warning_servers))

    alert_df = df[df["thermal_status"].isin(["Warning", "Critical"])][
        ["timestamp", "server_id", "cpu_usage", "power_usage", "temperature", "thermal_status"]
    ].sort_values("temperature", ascending=False)

    st.dataframe(alert_df.head(100), use_container_width=True)


def main() -> None:
    st.set_page_config(
        page_title="AI Data Center Optimization",
        layout="wide",
    )

    st.title("AI-Driven Data Center Reliability And Energy Optimization")

    df = load_data()
    schedule = load_schedule()

    page = st.sidebar.radio(
        "Navigation",
        ["Overview", "Prediction", "Scheduler", "Alerts", "Dataset"],
    )

    if page == "Overview":
        show_overview(df)
    elif page == "Prediction":
        show_predictions(df)
    elif page == "Scheduler":
        show_scheduler(schedule)
    elif page == "Alerts":
        show_alerts(df)
    else:
        st.subheader("Dataset Preview")
        st.dataframe(df, use_container_width=True)


if __name__ == "__main__":
    main()
