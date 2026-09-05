import random
import time 

cwt = 30
hwt = 34
fan_status = "on"
m = 20
cp = 1 # unit of cp is cal/g/degree celcius

wbt = 28


while True:

    cwt_change = random.uniform(1 , -1)
    hwt_change = random.uniform(1 , -1)
    hwt = hwt + hwt_change
    cwt = cwt + cwt_change 
    delta_t = hwt - cwt
    heat_load = m * cp * delta_t
    approach_to_wbt = cwt - wbt
    if cwt >= 34:
        fan_status = "on 🟢"
    elif cwt <= 28:
        fan_status = "off 🔴"

    print(f"CWT = {cwt:.2f} , Fan is {fan_status} , Heat load is {heat_load:.2f} , Approach to WBT is {approach_to_wbt:.2f}")

    time.sleep(3)



