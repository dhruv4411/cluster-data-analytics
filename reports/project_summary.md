# Project Summary

## Title

AI-Driven Autonomous Reliability and Energy Optimization Framework for Hyperscale Data Centres

## Aim

The aim of this project is to build an AI-based software framework that predicts energy consumption, estimates thermal risk, and optimizes workload scheduling in a data center environment.

## Problem Statement

Hyperscale data centers consume large amounts of energy and must maintain reliable operating temperatures. Poor workload placement can increase power usage, create hotspots, and reduce system reliability. This project addresses the problem by combining machine learning prediction with scheduling optimization.

## Objectives

- Create a local data center workload dataset for development
- Train a machine learning model to predict power usage
- Train a machine learning model to predict temperature
- Design a scheduler that reduces energy and thermal risk
- Build a dashboard for monitoring and decision support

## Methodology

The project uses a synthetic but realistic dataset because full production traces such as Google ClusterData2019 are too large to store locally. The dataset contains CPU usage, memory usage, disk I/O, network I/O, task duration, priority, outside temperature, cooling efficiency, power usage, and temperature.

Random Forest Regression is used for both energy and thermal prediction. A rule-based optimization scheduler ranks servers using CPU load, memory usage, power usage, and temperature, then assigns high-priority tasks to better server candidates.

## Results

Energy model:

```text
MAE: 7.30
RMSE: 9.20
R2 Score: 0.9809
```

Thermal model:

```text
MAE: 0.56
RMSE: 0.70
R2 Score: 0.9759
```

Scheduler:

```text
Tasks scheduled: 100
Temperature reduction: 4.98 C
Power reduction: 90.65 W
```

## Conclusion

The prototype successfully demonstrates an AI-driven data center optimization workflow. It predicts power and temperature with high accuracy on the local dataset and shows measurable improvement after scheduling optimization. The system can be extended with larger real-world traces, real weather data, advanced optimization methods, and deployment support.
