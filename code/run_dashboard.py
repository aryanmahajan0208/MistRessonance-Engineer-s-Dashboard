"""
    Main File: MistRessonance Dashboard
    Date: 2026-09-14

    Description: 
        Main file to run the MistRessonance Dashboard. 
        This file contains the main loop that runs the dashboard and displays the simulated values.
"""

import cooling_tower_sim as cts
import filehandler as fh
from rich.console import Console
from rich import print as rprint
from rich.panel import Panel
from rich import box
import sys
import time
from rich.align import Align

console = Console()

"""
Function to verify user input related to polling_rate.
Values over 20 Hz are considered extreme and require an additional confirmation to run
"""
def verify_input(hz):
    if hz > 20:
        rprint("[bright_yellow]Extreme value selected, are you sure you wish to continue?[/bright_yellow] [[bright_green]Y[/bright_green]/[bright_red]N[/bright_red]]: ", end="")
        user_confirm = input().lower().replace(" ", "")

        if user_confirm == "n":
            sys.exit(0)
        elif user_confirm == "y":
            pass
        else:
           rprint("[bright_yellow]Invalid input[/bright_yellow]") 
           verify_input(hz)


"""
Function to accept user input as Y or N to start the simulation, with invalid input handling and 
recursion to restart
"""
def start_program():
    rprint("Do you wish to start the simulation? [[bright_green]Y[/bright_green]/[bright_red]N[/bright_red]]:", end = "  ")

    # accept user input, strip white spaces, and convert it to lowercase for easy edge case handling
    start_event = input().lower().replace(" ", "")

    # y -> start; n -> exit with error code 0; anything else, invalid input
    if start_event == 'y':
        hz = int(input("Enter polling rate (in Hertz):"))
        polling_rate = abs(1 / hz)
        verify_input(hz)

        rprint("Press [magenta1]Q[/magenta1] to [magenta1]exit[/magenta1]")

        # 1 second buffer so user can read above message comfortably
        time.sleep(1)

        filename = fh.createfile()

        # run the simulation loop
        cts.sim_values(polling_rate, filename)
    elif start_event == 'n':
        print("Exiting")
        sys.exit(0)
    else:
        rprint("[bright_yellow]Invalid input[/bright_yellow]")
        start_program()

if __name__ == "__main__":
    print("\n\n")

    # print the dashboard panel
    console.print(
        Panel(
            Align.center("All temperatures are measured in °C, Heat Load is measured in kilowatts (kW)"),
            title = "[bold cyan]M i s t R e s s o n a n c e   D a s h b o a r d[/bold cyan]",
            title_align = "center",
            subtitle = "v1.0",
            subtitle_align = "center",
            expand = True,
            box = box.ROUNDED,
            padding = (1, 1)
        )
    )

    print("\n\n")

    start_program()