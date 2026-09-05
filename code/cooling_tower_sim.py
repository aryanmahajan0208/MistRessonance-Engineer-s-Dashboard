"""
    Sensor Simulation Program: MistRessonance Dashboard
    Date: 2026-09-05

    Description: 
        This program creates simulated values for temperatures and calculates dependent values 
        from the simulated values
"""

import random
import time 
import keyboard as kb

# function to simulate values and calculate dependents 
def sim_values():
    # initialize cold water temp, hot water temp, wet bulb temp, fan_status, mass flow rate, specific heat
    cwt, hwt, wbt = 30, 34, 28
    fan_status = "on"
    m = 20
    cp = 1 # unit of cp is cal/g/degree celcius

    while True:
        # exit condition
        # TODO: replace with event-based listener before deploying unattended
        if kb.is_pressed('q'):
            print("Q pressed, exiting...")
            break

        # random nudge to temps using gaussian distribution
        cwt_change = random.gauss(mu = 0, sigma = 1)
        hwt_change = random.gauss(mu = 0, sigma = 1)
            
        hwt += hwt_change
        cwt += cwt_change 

        # calculate dependent values
        delta_t = hwt - cwt
        heat_load = m * cp * delta_t
        approach_to_wbt = cwt - wbt

        if cwt >= 34:
            fan_status = "on"
        elif cwt <= 28:
            fan_status = "off"

        print(f"CWT = {cwt:.2f}, Fan is {fan_status}, Heat load is {heat_load:.2f}, Approach to WBT is {approach_to_wbt:.2f}")

        time.sleep(1)

sim_values()