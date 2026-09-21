"""
    File Handler: MistRessonance Dashboard
    Date: 2026-09-20

    Description:
        Handles logging of cooling tower readings to disk.
        On startup, creates a new .txt file named after the program's
        start date-time (e.g. 2026-09-15_14-32-00.txt) inside a specified
        output directory.

        The file's first line records the creation date-time. Every
        subsequent line logs one reading — timestamp, CWT, HWT, fan status,
        heat load, approach to WBT, and efficiency — as comma-separated
        values, appended once per polling interval.
"""

import time
import os

def createfile(directory='logs'):
    os.makedirs(directory, exist_ok = True)

    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{directory}/{timestamp}.txt"

    with open(filename, "w") as f:
        f.write(f"Run time: {timestamp}\n\n")

    return filename


def log_reading(filename, reading):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = (
        f"{timestamp},{reading['cwt']:.2f},{reading['hwt']:.2f},"
        f"{reading['fan_status']},{reading['heat_load_kw']:.2f},"
        f"{reading['approach_to_wbt']:.2f},{reading['efficiency']:.2f}\n"
    )

    with open(filename, "a") as f:
        f.write(line)
