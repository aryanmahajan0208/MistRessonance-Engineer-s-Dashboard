"""
    Web Dashboard Server: MistRessonance Dashboard
    Date: 2026-11-10

    Description:
        Flask-based web server that bridges the existing MistRessonance Python
        telemetry engine (cooling_tower_sim, alert_engine, filehandler) with
        the browser-based Ableton-style industrial UI.
        Preserves 100% compatibility with the terminal version.
"""

import os
import time
from flask import Flask, send_from_directory, jsonify, request
import cooling_tower_sim as cts
import alert_engine as ae
import filehandler as fh

app = Flask(__name__, static_folder=".")

# Simulation Session State
state = {
    "cwt": 30.0,
    "hwt": 34.0,
    "wbt": 28.0,
    "fan_status": "on",
    "fan_cost_total": 0.0,
    "filename": None,
    "step_count": 0
}


def reset_session(create_new_log=True):
    """Resets the simulation state and initializes a fresh logfile."""
    state["cwt"] = 30.0
    state["hwt"] = 34.0
    state["wbt"] = 28.0
    state["fan_status"] = "on"
    state["fan_cost_total"] = 0.0
    state["step_count"] = 0
    ae.smoothed_efficiency.clear()
    if create_new_log:
        state["filename"] = fh.createfile()


@app.route("/")
def index():
    """Serves the single-page Ableton-style GUI."""
    return send_from_directory(".", "index.html")


@app.route("/api/start", methods=["POST"])
def start_sim():
    """Initializes a new logging session if none is active, or resets if requested."""
    data = request.get_json(silent=True) or {}
    if data.get("reset", False) or state["filename"] is None:
        reset_session(create_new_log=True)
    return jsonify({
        "status": "started",
        "filename": state["filename"]
    })


@app.route("/api/reset", methods=["POST"])
def reset_sim():
    """Resets simulation metrics and starts a fresh log file."""
    reset_session(create_new_log=True)
    return jsonify({
        "status": "reset",
        "filename": state["filename"]
    })


@app.route("/api/tick", methods=["GET"])
def tick():
    """
    Executes a single simulation step using the exact functions from
    cooling_tower_sim.py, alert_engine.py, and filehandler.py.
    """
    if state["filename"] is None:
        state["filename"] = fh.createfile()

    reading = cts.generate_reading(state["cwt"], state["hwt"], state["wbt"])

    # Update state and fan hysteresis
    state["cwt"] = reading["cwt"]
    state["hwt"] = reading["hwt"]
    state["fan_status"] = reading["fan_status"] or state["fan_status"]
    reading["fan_status"] = state["fan_status"]

    # Operating cost calculation (matches cooling_tower_sim.py)
    if state["fan_status"] == "on":
        fan_cost_iteration = 10.0 * reading["heat_load_kw"]
        state["fan_cost_total"] += fan_cost_iteration

    # Log reading to disk
    fh.log_reading(state["filename"], reading)

    # Alert engine pipeline
    smoothed_eff = ae.smooth_stream(reading["efficiency"])
    inst_status = ae.instant_status(smoothed_eff)
    slope = ae.get_slope()
    prediction = ae.predict_status(slope)

    state["step_count"] += 1

    return jsonify({
        "timestamp": time.strftime("%H:%M:%S"),
        "cwt": round(state["cwt"], 2),
        "hwt": round(state["hwt"], 2),
        "wbt": round(state["wbt"], 2),
        "delta_t": round(reading["delta_t"], 2),
        "heat_load_kw": round(reading["heat_load_kw"], 2),
        "approach_to_wbt": round(reading["approach_to_wbt"], 2),
        "fan_status": state["fan_status"],
        "efficiency": round(reading["efficiency"], 2),
        "smoothed_efficiency": round(smoothed_eff, 2),
        "fan_cost_total": round(state["fan_cost_total"], 2),
        "status": inst_status,
        "slope": round(slope, 3),
        "prediction": prediction,
        "filename": state["filename"],
        "step_count": state["step_count"]
    })


@app.route("/api/logs", methods=["GET"])
def list_logs():
    """Lists existing log files inside the logs/ directory."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        return jsonify({"files": []})
    files = sorted(
        [f for f in os.listdir(log_dir) if f.endswith(".txt")],
        reverse=True
    )
    return jsonify({"files": files})


@app.route("/api/logs/<path:filename>", methods=["GET"])
def get_log(filename):
    """Parses a historical logfile and returns its time-series data."""
    filepath = os.path.join("logs", filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    records = []
    run_time = ""
    with open(filepath, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    for line in lines:
        if line.startswith("Run time:"):
            run_time = line.replace("Run time:", "").strip()
            continue
        parts = line.split(",")
        if len(parts) >= 7:
            try:
                records.append({
                    "timestamp": parts[0],
                    "cwt": float(parts[1]),
                    "hwt": float(parts[2]),
                    "fan_status": parts[3],
                    "heat_load_kw": float(parts[4]),
                    "approach_to_wbt": float(parts[5]),
                    "efficiency": float(parts[6])
                })
            except ValueError:
                continue

    return jsonify({
        "filename": filename,
        "run_time": run_time,
        "records": records
    })


if __name__ == "__main__":
    print("\n" + "=" * 62)
    print("  MIST RESSONANCE — WEB TELEMETRY DASHBOARD v1.0")
    print("  Open this link in your browser: http://127.0.0.1:5000")
    print("  Press Ctrl+C in this terminal at any time to stop the server.")
    print("=" * 62 + "\n")
    app.run(host="127.0.0.1", port=5000, debug=False)
