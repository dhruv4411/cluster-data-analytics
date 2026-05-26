# Dataset Folder Guide

Store original downloaded files in `data/raw/`.

- `data/raw/google_cluster/` - Google cluster workload traces
- `data/raw/google_power/` - Google PowerData2019 traces
- `data/raw/alibaba_cluster/` - Alibaba cluster traces
- `data/raw/weather/` - Weather data for thermal simulation

Store cleaned or generated files in `data/processed/`.

- `data/processed/samples/` - small sample CSV files for testing
- `data/processed/final/` - final training datasets

Do not manually edit files inside `data/raw/`. Keep raw datasets unchanged.
