from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "data" / "processed" / "samples" / "data_center_sample.csv"
MODEL_PATH = ROOT_DIR / "models" / "energy_model.joblib"

FEATURE_COLUMNS = [
    "cpu_usage",
    "memory_usage",
    "disk_io",
    "network_io",
    "task_duration",
    "priority",
    "outside_temperature",
    "cooling_efficiency",
]
TARGET_COLUMN = "power_usage"


def load_dataset() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def train_energy_model() -> None:
    df = load_dataset()

    x = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print("Energy model training complete")
    print(f"Rows used: {len(df)}")
    print(f"Model saved to: {MODEL_PATH}")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R2 Score: {r2:.4f}")


if __name__ == "__main__":
    train_energy_model()
