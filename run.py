# Google Spreadsheet Access - Uncomment when creating Fluff
# import gspread
# from google.oauth2.service_account import Credentials
# import json

# SCOPE = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive.file",
#     "https://www.googleapis.com/auth/drive"
#     ]

# CREDS = Credentials.from_service_account_file("creds.json")
# SCOPED_CREDS = CREDS.with_scopes(SCOPE)
# GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# SHEET = GSPREAD_CLIENT.open("dnd_utils")

# CHARACTERS_SHEET = SHEET.worksheet("characters")
# PLACES_SHEET = SHEET.worksheet("places")
from colorama import Fore, Back, Style, init
init(autoreset = True)
import cutie
import random
from tabulate import tabulate

def introduction():
    """
    Prints an introductory message and asks the user to select which function they would like to utilize.
    """
    print(f"Welcome to" + Fore.RED + " DNDUtils" + Fore.WHITE + "!")
    print(f"Please choose a program to use:\n")
    print(Fore.YELLOW + "DiceRoller" + Fore.RESET + " - Roll Dice for your DND Game")
    print(Fore.CYAN + "Fluff" + Fore.RESET + " - Create NPCs or Places for your DND Game\n")
    functions = [
        Fore.YELLOW + "DiceRoller",
        Fore.CYAN + "Fluff",
        Back.RED + "Exit DNDUtils"
    ]
    chosen_function = functions[cutie.select(functions)]
    print(f"You have chosen {chosen_function}")
    return chosen_function

def diceroller():
    """
    Rolls a chosen number of dice with a designated number of sides plus a modifier
    and then displays the output
    """
    num_of_dice = cutie.get_number("How many dice do you want to roll?", min_value = 1, allow_float = False)
    num_of_sides = cutie.get_number("How many sides should each dice have?", min_value = 2, allow_float = False)
    dice_rolls =[random.randint(1, num_of_sides) for value in range(num_of_dice)]
    modifier_num = cutie.get_number("What is the modifier for the roll?", allow_float = False)
    print(Fore.GREEN + "\nDice Summary")
    print(f"\nThe individual dice rolls were: {dice_rolls}")
    print(f"The total of all dice is: {sum(dice_rolls)}")
    print(f"The sum of all dice rolls plus the modifier was: {sum(dice_rolls) + modifier_num}")

def function_selection():
    """
    Starts the user's chosen function
    """
    chosen_function = introduction() # Runs the introduction and asks the user to pick a function
    if "DiceRoller" in chosen_function:
        print(f"Starting" + Fore.YELLOW + " DiceRoller" + Fore.RESET + "...")
        diceroller()
    elif "Fluff" in chosen_function:
        print(f"Starting" + Fore.CYAN + " Fluff" + Fore.RESET + "...")
    else: 
        print(Back.RED + "Exiting DNDUtils" + Back.RESET + "...")

def main():
    function_selection()

main()