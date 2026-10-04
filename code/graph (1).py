"""
Mist Resonance - live temperature graph with automatic fan control
------------------------------------------------------------------
- Fan turns ON  when temperature >= FAN_ON_TEMP
- Fan turns OFF when temperature <= FAN_OFF_TEMP
  (the gap between the two avoids the fan rapidly flicking on/off)

Data is stored in a pandas DataFrame and plotted live with matplotlib.

Install:  pip install pandas numpy matplotlib
Run:      python graph.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ---------------- SETTINGS (change these) ----------------
FAN_ON_TEMP = 30.0      # Fan starts at/above this temperature (°C)
FAN_OFF_TEMP = 26.0     # Fan stops at/below this temperature (°C)
WINDOW = 120           # number of latest points shown on the graph
INTERVAL_MS = 500      # update speed in milliseconds
SAVE_CSV = "mist_resonance_log.csv"   # set to None to disable logging
# ----------------------------------------------------------

df = pd.DataFrame(columns=["time", "temp", "fan_on"])
fan_on = False
_sim_temp = 28.0


def read_temperature():
    """
    Simulated sensor. Replace this with your real sensor reading, e.g.:

        import serial
        ser = serial.Serial("COM3", 9600)
        return float(ser.readline().decode().strip())
    """
    global _sim_temp
    drift = -0.35 if fan_on else 0.25          # fan cools, otherwise room heats up
    _sim_temp += drift + np.random.normal(0, 0.15)
    return round(_sim_temp, 2)


def control_fan(temp):
    """Hysteresis control: returns the new fan state."""
    global fan_on
    if not fan_on and temp >= FAN_ON_TEMP:
        fan_on = True
    elif fan_on and temp <= FAN_OFF_TEMP:
        fan_on = False
    return fan_on


fig, ax = plt.subplots(figsize=(11, 5), constrained_layout=True)


def update(_frame):
    global df

    temp = read_temperature()
    state = control_fan(temp)

    df.loc[len(df)] = [pd.Timestamp.now(), temp, state]

    if SAVE_CSV:
        df.tail(1).to_csv(SAVE_CSV, mode="a", index=False,
                          header=(len(df) == 1))

    view = df.tail(WINDOW).reset_index(drop=True)

    ax.clear()
    ax.plot(view.index, view["temp"].astype(float), color="tab:blue",
            linewidth=2, label="Temperature")

    # thresholds
    ax.axhline(FAN_ON_TEMP, color="red", linestyle="--", label=f"Fan ON ({FAN_ON_TEMP}°C)")
    ax.axhline(FAN_OFF_TEMP, color="green", linestyle="--", label=f"Fan OFF ({FAN_OFF_TEMP}°C)")

    # shade the periods where the fan was running
    ax.fill_between(view.index,
                    FAN_OFF_TEMP - 3, FAN_ON_TEMP + 3,
                    where=view["fan_on"].astype(bool),
                    color="cyan", alpha=0.25, step="mid", label="Fan running")

    status = "ON" if state else "OFF"
    ax.set_title(f"Mist Resonance  |  Temp: {temp:.2f}°C  |  Fan: {status}",
                 color="red" if state else "green", fontsize=14)
    ax.set_xlabel("Readings")
    ax.set_ylabel("Temperature (°C)")
    ax.set_ylim(FAN_OFF_TEMP - 3, FAN_ON_TEMP + 3)
    ax.grid(alpha=0.3)
    ax.legend(loc="upper left")


ani = FuncAnimation(fig, update, interval=INTERVAL_MS, cache_frame_data=False)
plt.show()
