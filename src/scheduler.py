from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "data" / "processed" / "samples" / "data_center_sample.csv"
OUTPUT_PATH = ROOT_DIR / "data" / "processed" / "final" / "optimized_schedule.csv"


def calculate_server_summary(df: pd.DataFrame) -> pd.DataFrame:
    server_summary = (
        df.groupby("server_id")
        .agg(
            avg_cpu=("cpu_usage", "mean"),
            avg_memory=("memory_usage", "mean"),
            avg_power=("power_usage", "mean"),
            avg_temperature=("temperature", "mean"),
        )
        .reset_index()
    )

    server_summary["optimization_score"] = (
        server_summary["avg_cpu"] * 0.35
        + server_summary["avg_temperature"] * 0.40
        + server_summary["avg_power"] * 0.20
        + server_summary["avg_memory"] * 0.05
    )
    return server_summary.sort_values("optimization_score")


def get_status(temperature: float) -> str:
    if temperature < 35:
        return "Normal"
    if temperature < 45:
        return "Warning"
    return "Critical"


def optimize_schedule() -> None:
    df = pd.read_csv(DATA_PATH)
    server_summary = calculate_server_summary(df)

    best_servers = server_summary.head(10).copy()
    busiest_tasks = df.sort_values(
        ["priority", "cpu_usage", "task_duration"],
        ascending=[False, False, False],
    ).head(100).copy()

    assignments = []
    for index, task in busiest_tasks.reset_index(drop=True).iterrows():
        selected_server = best_servers.iloc[index % len(best_servers)]

        estimated_cpu = min(100, selected_server["avg_cpu"] + task["cpu_usage"] * 0.12)
        estimated_power = selected_server["avg_power"] + task["power_usage"] * 0.08
        estimated_temperature = (
            selected_server["avg_temperature"]
            + task["temperature"] * 0.05
            + task["cpu_usage"] * 0.015
        )

        assignments.append(
            {
                "task_timestamp": task["timestamp"],
                "original_server": task["server_id"],
                "assigned_server": selected_server["server_id"],
                "task_priority": task["priority"],
                "task_cpu_usage": round(task["cpu_usage"], 2),
                "estimated_server_cpu": round(estimated_cpu, 2),
                "estimated_power_usage": round(estimated_power, 2),
                "estimated_temperature": round(estimated_temperature, 2),
                "thermal_status": get_status(estimated_temperature),
                "optimization_score": round(selected_server["optimization_score"], 2),
            }
        )

    optimized_schedule = pd.DataFrame(assignments)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    optimized_schedule.to_csv(OUTPUT_PATH, index=False)

    baseline_temperature = busiest_tasks["temperature"].mean()
    optimized_temperature = optimized_schedule["estimated_temperature"].mean()
    baseline_power = busiest_tasks["power_usage"].mean()
    optimized_power = optimized_schedule["estimated_power_usage"].mean()

    temperature_reduction = baseline_temperature - optimized_temperature
    power_reduction = baseline_power - optimized_power

    print("Scheduler optimization complete")
    print(f"Tasks scheduled: {len(optimized_schedule)}")
    print(f"Schedule saved to: {OUTPUT_PATH}")
    print(f"Average baseline temperature: {baseline_temperature:.2f}")
    print(f"Average optimized temperature: {optimized_temperature:.2f}")
    print(f"Estimated temperature reduction: {temperature_reduction:.2f}")
    print(f"Average baseline power: {baseline_power:.2f}")
    print(f"Average optimized power: {optimized_power:.2f}")
    print(f"Estimated power reduction: {power_reduction:.2f}")


if __name__ == "__main__":
    optimize_schedule()
