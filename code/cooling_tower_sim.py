"""
    Sensor Simulation: MistRessonance Dashboard
    Date: 2026-09-08

    Description: 
        This program creates simulated values for temperatures and calculates dependent values 
        from the simulated values
"""

import filehandler as fh
import alert_engine as ae
import random
import time 
import keyboard as kb
from rich.console import Console
from rich import print as rprint
from rich.panel import Panel

console = Console()

# style lookup for fan status
status_style = {
    "on": "light_green", 
    "off": "bright_red",
    "normal": "dark_olive_green2",
    "warning": "yellow3",
    "critical": "red1",
    "calibrating": "yellow3",
}

def generate_reading(cwt, hwt, wbt, flow_rate = 20, cp = 1, hwt_mu = 34, theta = 0.15):
    # random nudge to temps using gaussian distribution
    hwt_change = theta * (hwt_mu - hwt) + random.gauss(mu = 0, sigma = 2.5)
    hwt += hwt_change

    delta_t = max(0.1, random.gauss(mu = 4, sigma = 1))  # avg 4°C drop, never zero/negative
    cwt = hwt - delta_t

    # calculate dependent values
    heat_load = flow_rate * cp * delta_t
    heat_load_kw = heat_load * 4.184 / 1000 # calculates heat load in kW instead of cal/s

    # temporary clamp to stop negative values
    approach_to_wbt = cwt - wbt if (cwt-wbt) > 0 else 0

    # efficiency calculation
    efficiency = (delta_t / (delta_t + approach_to_wbt)) * 100 if (delta_t + approach_to_wbt) > 0 else 0

    # None = no threshold crossed; caller keeps previous fan_status
    if cwt >= 34:
        fan_status = "on"
    elif cwt <= 28:
        fan_status = "off"
    else:
        fan_status = None

    return {
        "cwt": cwt, "hwt": hwt, "delta_t": delta_t,
        "heat_load_kw": heat_load_kw, "approach_to_wbt": approach_to_wbt,
        "fan_status": fan_status, "efficiency": efficiency,
    }


# function to simulate values and calculate dependents 
def sim_values(polling_rate = 1, filename = "None"):
    # initialize cold water temp, hot water temp, wet bulb temp, fan_status, mass flow rate, specific heat
    cwt, hwt, wbt = 30, 34, 28
    fan_status = "on"
    fan_cost_total = 0

    while True:
        # exit condition    
        # TODO: replace with event-based listener before deploying unattended
        if kb.is_pressed('q'):
            console.print("\n[magenta1]Q pressed, exiting...[/magenta1]\n", justify = "center")
            break

        reading = generate_reading(cwt, hwt, wbt)

        if fan_status == "on":
            fan_cost_iteration = 10 * reading["heat_load_kw"]
            fan_cost_total += fan_cost_iteration
        else:
            fan_cost_iteration = 0
            fan_cost_total += fan_cost_iteration
            

        cwt, hwt = reading["cwt"], reading["hwt"]
        fan_status = reading["fan_status"] or fan_status  # keep old status if None
        efficiency = reading["efficiency"]

        if filename:
            fh.log_reading(filename, reading)

        smoothed_eff = ae.smooth_stream(reading["efficiency"])
        status = ae.instant_status(smoothed_eff)
        slope = ae.get_slope()
        prediction = ae.predict_status(slope)

        fan_color = status_style.get(fan_status, "white")
        status_color = status_style.get(status, "white")

        console.print(
            f"Cold Water: {cwt:.2f} °C,    "
            f"Hot Water: {hwt:.2f} °C,    "
            f"Fan: [{fan_color}]{fan_status}[/{fan_color}],    "
            f"Heat load: {reading['heat_load_kw']:.2f} kW,    "
            f"Approach: {reading['approach_to_wbt']:.2f} °C    "
            f"Efficiency: {efficiency:.2f}%    "
            f"Running Cost: ₹{fan_cost_total:.2f}   "
            f"Status: [{status_color}]{status}[/{status_color}]    "
            f"Prediction: {prediction}",
            justify = "center"
        )

        time.sleep(polling_rate)


if __name__ == "__main__":
    sim_values()