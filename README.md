# AI-Driven Data Center Reliability And Energy Optimization

This project is a beginner-friendly software prototype for predicting energy usage, estimating server temperature, and optimizing workload scheduling in a data center environment.

## Project Goal

The aim is to design an AI-based framework for hyperscale data centers that:

- predicts power usage from workload data
- predicts server temperature from workload and energy conditions
- schedules high-priority tasks on better server candidates
- shows results through a real-time Streamlit dashboard

## Current Features

- Synthetic data center dataset with 5,000 records
- Energy prediction using Random Forest Regression
- Thermal prediction using Random Forest Regression
- Rule-based optimization scheduler
- Streamlit dashboard with overview, prediction, scheduler, alerts, and dataset pages

## Folder Structure

```text
Major-project/
  dashboard/
    app.py
  data/
    raw/
      google_cluster/
      google_power/
      alibaba_cluster/
      weather/
    processed/
      samples/
        data_center_sample.csv
      final/
        optimized_schedule.csv
  models/
    energy_model.joblib
    thermal_model.joblib
  reports/
    architecture.md
    project_summary.md
  src/
    energy_model.py
    scheduler.py
    thermal_model.py
  requirements.txt
  README.md
```

## Dataset Strategy

The original Google ClusterData2019 trace is very large, around 2.4 TiB compressed, so it is not practical to store locally on a laptop. This prototype uses a realistic synthetic sample dataset for local development.

The system is designed so that later it can be extended to use:

- Google ClusterData2019
- Google PowerData2019
- Alibaba Cluster Trace
- Open-Meteo or NASA POWER weather data

## Dataset Columns

The sample dataset contains:

```text
timestamp
server_id
cpu_usage
memory_usage
disk_io
network_io
task_duration
priority
outside_temperature
cooling_efficiency
power_usage
temperature
thermal_status
```

## Setup

Open Anaconda Prompt or an activated Conda terminal.

```powershell
cd C:\Users\dhruv\OneDrive\Documents\Major-project
conda activate datacenter-ai
pip install -r requirements.txt
```

## Run The Models

Train the energy model:

```powershell
python src\energy_model.py
```

Train the thermal model:

```powershell
python src\thermal_model.py
```

Run the scheduler:

```powershell
python src\scheduler.py
```

## Run The Dashboard

```powershell
streamlit run dashboard\app.py
```

Then open the local Streamlit URL, usually:

```text
http://localhost:8501
```

## Dashboard Screenshots

Dashboard screenshots are stored in:

```text
reports/screenshots/
```

These screenshots can be used in the final project report and presentation.

### Overview Page

The overview page summarizes the simulated data center state, including server count, average CPU usage, average power usage, and average temperature. It also shows high-level charts for power trends and CPU-power relationship.

![Dashboard overview](reports/screenshots/Screenshot%202026-05-26%20143855.png)

### Prediction Page

The prediction page allows users to adjust workload and cooling inputs, then view predicted power consumption, predicted temperature, and thermal status.

![Prediction page](reports/screenshots/Screenshot%202026-05-26%20143904.png)

### Scheduler Page

The scheduler page displays optimized task allocation results, estimated power usage, estimated temperature, and the assigned server for each scheduled task.

![Scheduler page](reports/screenshots/Screenshot%202026-05-26%20143914.png)

### Alerts Page

The alerts page highlights warning and critical thermal records so that reliability risks can be identified quickly.

![Alerts page](reports/screenshots/Screenshot%202026-05-26%20143923.png)

### Dataset Page

The dataset page shows the working sample dataset used for model training, prediction, scheduling, and dashboard visualization.

![Dataset page](reports/screenshots/Screenshot%202026-05-26%20143930.png)

## Current Results

Energy prediction:

```text
MAE: 7.30
RMSE: 9.20
R2 Score: 0.9809
```

Thermal prediction:

```text
MAE: 0.56
RMSE: 0.70
R2 Score: 0.9759
```

Scheduler optimization:

```text
Average baseline temperature: 49.69 C
Average optimized temperature: 44.72 C
Estimated temperature reduction: 4.98 C

Average baseline power: 575.57 W
Average optimized power: 484.92 W
Estimated power reduction: 90.65 W
```

## Future Improvements

- Add XGBoost model comparison
- Add deep learning model such as LSTM for time-series prediction
- Use BigQuery to sample Google ClusterData2019
- Add real weather data from Open-Meteo
- Improve scheduler using genetic algorithm or reinforcement learning
- Add Docker deployment
