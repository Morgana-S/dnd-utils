import gspread
from google.oauth2.service_account import Credentials
import json
from colorama import Fore, Back, Style, init
init(autoreset = True)
import cutie
import random
from tabulate import tabulate

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("dnd_utils")

CHARACTERS_SHEET = SHEET.worksheet("characters")
CHARACTERS_LISTS_SHEET = SHEET.worksheet("characters_lists")
PLACES_SHEET = SHEET.worksheet("places")
PLACES_LISTS_SHEET = SHEET.worksheet("places_lists")



def introduction():
    """
    Prints an introductory message and asks the user to select which function they would like to utilize.
    """
    # Prints an introductory message using methods from colorama for color
    print(f"Welcome to" + Fore.RED + " DNDUtils" + Fore.WHITE + "!")
    print(f"Please choose a program to use:\n")
    print(Fore.YELLOW + "DiceRoller" + Fore.RESET + " - Roll Dice for your DND Game")
    print(Fore.CYAN + "Fluff" + Fore.RESET + " - Create NPCs or Places for your DND Game\n")
    # Defines the available options for function selection
    functions = [
        Fore.YELLOW + "DiceRoller",
        Fore.CYAN + "Fluff",
        Back.RED + "Exit DNDUtils"
    ]
    # Asks the user to choose a function from the choices above
    chosen_function = functions[cutie.select(functions)]
    return chosen_function

def diceroller():
    """
    Rolls a chosen number of dice with a designated number of sides plus a modifier
    and then displays the output
    """
    # Defines the variables used to calculate the dice rolls with user input - validates for number-only input
    num_of_dice = cutie.get_number("How many dice do you want to roll?", min_value = 1, allow_float = False)
    num_of_sides = cutie.get_number("How many sides should each dice have?", min_value = 2, allow_float = False)
    dice_rolls = [random.randint(1, num_of_sides) for value in range(num_of_dice)]
    modifier_num = cutie.get_number("What is the modifier for the roll?", allow_float = False)
    advantage = [
        Fore.GREEN + "Advantage",
        Fore.RED + "Disadvantage",
        Fore.BLUE + "Normal Roll"
    ]
    advantage_roll = advantage[cutie.select(advantage)]
    # Prints the result
    print(Fore.GREEN + "\nDice Summary")
    print(f"\n\u001b[36mThe individual dice rolls were: \u001b[33m{dice_rolls}")
    print(f"\u001b[31mThe total of all dice is: \u001b[37m{sum(dice_rolls)}")
    print(f"\u001b[35mThe sum of all dice rolls plus the modifier was: \u001b[32m{sum(dice_rolls) + modifier_num}")
    if cutie.prompt_yes_or_no(Fore.YELLOW + "Would you like to roll more dice?"):
        # Begins the dice-rolling function again
        diceroller()
    else:
        # Loops the program back to the start
        main() 

def fluff():
    """
    Asks the user if they want to generate a person (NPC) or place, takes user input for predefined features
    of the entity and then generates an entity by drawing from predefined lists of characteristics
    """
    # Asks the user whether they want to generate a person or place and assigns the selection to chosen_option
    print(f"Do you want to generate a \u001b[32mPerson \u001b[37mor a \u001b[31mPlace?\n")
    options = [
        Fore.GREEN + "Person (NPC)",
        Fore.RED + "Place",
        Back.RED + "Go Back"
    ]
    chosen_option = options[cutie.select(options)]
    if "Person" in chosen_option:
        pass
    elif "Place" in chosen_option:
        pass
    else:
        main()
    
def function_selection(chosen_function):
    """
    Starts the user's chosen function
    """
    # Checks the string in chosen_function and starts the appropriate part of the program
    if "DiceRoller" in chosen_function:
        print(f"Starting" + Fore.YELLOW + " DiceRoller" + Fore.RESET + "...")
        diceroller()
    elif "Fluff" in chosen_function:
        print(f"Starting" + Fore.CYAN + " Fluff" + Fore.RESET + "...")
        fluff()
    else: 
        print(Back.RED + "Exiting DNDUtils" + Back.RESET + "...")

def main():
    """
    Runs the main program function sequence
    """
    chosen_function = introduction()
    function_selection(chosen_function)

main()

