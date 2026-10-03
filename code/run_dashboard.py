"""
    Main File: MistRessonance Dashboard
    Date: 2026-09-14

    Description: 
        Main file to run the MistRessonance Dashboard. 
        This file contains the main loop that runs the dashboard and displays the simulated values.
"""

import cooling_tower_sim as cts
import filehandler as fh
import run_graph as rg
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
Function to prompt user for their choice of viewmode 
T for standard text mode
G for graph mode
L for loading a logfile and gneerating a graph 
"""
def selectview():
    print("Which view would you like to access? \n")
    rprint("[orange3][T][/orange3]ext view")
    rprint("[plum3][G][/plum3]raph view")
    rprint("[dark_sea_green2][L][/dark_sea_green2]oad from logfile")
    rprint("\n Enter choice: ", end=" ")

    choice = input().lower().replace(" ", "")

    if choice in ("t", "g"):
        return choice
    elif choice == "l":
        rprint("[bright_yellow]Not available yet: coming soon[/bright_yellow]")
        return selectview()
    else:
        rprint("[bright_yellow]Invalid input[/bright_yellow]")
        return selectview()


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
        print("\n")
        view = selectview()

        hz = int(input("Enter polling rate (in Hertz):"))
        polling_rate = abs(1 / hz)
        verify_input(hz)

        filename = fh.createfile()

        if view == "t":     
            rprint("Press [magenta1]Q[/magenta1] to [magenta1]exit[/magenta1]")

            # 1 second buffer so user can read above message comfortably
            time.sleep(1)
            
            # run the simulation loop
            cts.sim_values(polling_rate, filename)
        elif view == "g": 
            rprint("Press [magenta1]X[/magenta1] in graph window to [magenta1]exit[/magenta1]")

            # 1 second buffer so user can read above message comfortably
            time.sleep(1)

            rg.run_graph(polling_rate, filename)
            
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