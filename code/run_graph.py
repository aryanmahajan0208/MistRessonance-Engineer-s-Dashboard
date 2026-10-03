"""
    Live Graph: MistRessonance Dashboard
    Date: 2026-09-30
    
    Description:
        Data is stored in a double ended queue and plotted live with matplotlib.

"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import cooling_tower_sim as cts
import filehandler as fh

def run_graph(polling_rate=1, filename=None, window=25):
    cwt, hwt, wbt = 30, 34, 28
    fan_status = "on"
    history = {
        "cwt": deque(maxlen=window), 
        "hwt": deque(maxlen=window),
        "heat_load_kw": deque(maxlen=window)
    }

    fig, ax = plt.subplots(figsize=(11, 5))

    def update(_frame):
        nonlocal cwt, hwt, fan_status
        reading = cts.generate_reading(cwt, hwt, wbt)
        cwt, hwt = reading["cwt"], reading["hwt"]
        fan_status = reading["fan_status"] or fan_status

        if filename:
            fh.log_reading(filename, reading)

        history["cwt"].append(cwt)
        history["hwt"].append(hwt)
        history["heat_load_kw"].append(reading["heat_load_kw"])

        ax.clear()
        ax.plot(history["cwt"], label="CWT")
        ax.plot(history["hwt"], label="HWT")
        ax.set_title(f"Fan: {fan_status}", color="green" if fan_status == "on" else "red")
        ax.legend()

    ani = FuncAnimation(fig, update, interval=int(polling_rate * 1000), cache_frame_data=False)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_graph()