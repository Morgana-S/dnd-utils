import gspread
from google.oauth2.service_account import Credentials
import json
from colorama import Fore, Back, Style, init
init(autoreset = True)
import cutie
import random
from tabulate import tabulate
import pyperclip

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

class NPC:
    """
    Creates an instance of NPC.
    """
    def __init__(self, name, age, gender, race, law_tag, moral_tag, hair_color, disposition, disposition_text):
        self.name = name
        self.age = age
        self.gender = gender
        self.race = race
        self.law = law_tag
        self.morality = moral_tag
        self.hair_color = hair_color
        self.disposition = disposition
        self.disposition_text = disposition_text

class Place:
    """
    Creates an instance of Place.
    """
    def __init__(self, name, rumors):
        self.name = name
        self.rumors = rumors

class Town(Place):
    """
    Creates an instance of the subclass Town, to be used only with "Town" places.
    """
    def __init__(self, name, rumors, leadership, disposition, disposition_text):
        super().__init__(name, rumors)
        self.leadership = leadership
        self.disposition = disposition
        self.disposition_text = disposition_text

def introduction():
    """
    Prints an introductory message and asks the user to select which function they would like to utilize.
    """
    # Prints an introductory message using methods from colorama for color
    print(f"Welcome to" + Fore.RED + " DNDUtils" + Fore.WHITE + "!")
    print(f"Please choose a program to use:\n")
    print(Fore.YELLOW + "DiceRoller" + Fore.RESET + " - Roll Dice for your DND Game")
    print(Fore.CYAN + "Fluff" + Fore.RESET + " - Create NPCs or Places for your DND Game\n")
    print(Back.WHITE + "Please use the ↑ and ↓ arrow keys to navigate and select your option by hitting ENTER.\n")
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
    # Number of Dice to Roll
    print(Back.WHITE + "Please type in the number of dice you want to roll and hit ENTER.\n")
    num_of_dice = cutie.get_number("How many dice do you want to roll?", min_value = 1, allow_float = False)
    # Number of Sides on Each Dice
    print(Back.WHITE + "Please type in the number of sides on each dice and hit ENTER.\n")
    num_of_sides = cutie.get_number("How many sides should each dice have?", min_value = 2, allow_float = False)
    dice_rolls = [random.randint(1, num_of_sides) for value in range(num_of_dice)]
    # Skill Modifier - DND Skills allow for an additional number to be added to the end of the roll
    print(Back.WHITE + "Please enter the number for the skill modifier and press ENTER.\n")
    modifier_num = cutie.get_number("What is the modifier for the roll?", allow_float = False)
    # Asks the user to select whether the roll has Advantage, Disadvantage, or Neither
    print(Back.WHITE + "Please use the ↑ and ↓ arrow keys to navigate and select your option by hitting ENTER.\n")
    print(Fore.YELLOW + "Is this an Advantage, Disadvantage, or Normal Roll?\n")
    advantage = [
        Fore.GREEN + "Advantage",
        Fore.RED + "Disadvantage",
        Fore.BLUE + "Normal Roll"
    ]
    advantage_roll = advantage[cutie.select(advantage)]
    # Disadvantage Rolls roll two sets of dice, and pick the worse of the two outcomes
    if "Disadvantage" in advantage_roll:
        roll_one = [random.randint(1, num_of_sides) for value in range(num_of_dice)]
        roll_two = [random.randint(1, num_of_sides) for value in range(num_of_dice)]
        if roll_one > roll_two:
            dice_rolls = roll_two
        else:
            dice_rolls = roll_one
    # Advantage Rolls roll two sets of dice, and pick the better of the two outcomes
    elif "Advantage" in advantage_roll:
        roll_one = [random.randint(1, num_of_sides) for value in range(num_of_dice)]
        roll_two = [random.randint(1, num_of_sides) for value in range(num_of_dice)]
        if roll_one > roll_two:
            dice_rolls = roll_one
        else:
            dice_rolls = roll_two
    # Prints the result
    print(Fore.GREEN + "\nDice Summary")
    print(f"\n\u001b[36mThe individual dice rolls were: \u001b[33m{dice_rolls}")
    print(f"\u001b[31mThe total of all dice is: \u001b[37m{sum(dice_rolls)}")
    print(f"\u001b[35mThe sum of all dice rolls plus the modifier was: \u001b[32m{sum(dice_rolls) + modifier_num}")
    print(Back.WHITE + "Please use the ↑ and ↓ arrow keys to navigate and select your option by hitting ENTER.\n")
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
    print(Back.WHITE + "Please use the ↑ and ↓ arrow keys to navigate and select your option by hitting ENTER.\n" + Back.RESET)
    print(f"Do you want to generate a \u001b[32mPerson \u001b[37mor a \u001b[31mPlace?\n")
    options = [
        Fore.GREEN + "Person (NPC)",
        Fore.RED + "Place",
        Back.RED + "Go Back"
    ]
    chosen_option = options[cutie.select(options)]
    # Person-specific generation content
    if "Person" in chosen_option:
        print(Back.WHITE + "Please use the ↑ and ↓ arrow keys to navigate and select your option by hitting ENTER.\n" + Back.RESET)
        print(f"Please select applicable tags for the character to be generated.")
        # Asks the user to pick the generated person's lawfulness
        law_tags = [
            "Law Alignment:",
            Fore.CYAN + "Lawful",
            Fore.GREEN + "Neutral",
            Fore.RED + "Chaotic",
        ]
        law_tag = law_tags[cutie.select(law_tags, caption_indices = [0])]
        # Creates a plaintext version of the chosen lawfulness tag
        if "Lawful" in law_tag:
            law_tag_plaintext = "Lawful"
        elif "Neutral" in law_tag:
            law_tag_plaintext = "Neutral"
        else:
            law_tag_plaintext = "Chaotic"
        # Asks the user to pick the generated person's morality
        print(Back.WHITE + "Please use the ↑ and ↓ arrow keys to navigate and select your option by hitting ENTER.\n")
        moral_tags = [
            "Moral Alignment:",
            Fore.YELLOW + "Good",
            Fore.BLUE + "Neutral",
            Back.RED + "Evil",
        ]
        moral_tag = moral_tags[cutie.select(moral_tags, caption_indices = [0])]
        # Creates a plaintext version of the chosen morality tag
        if "Good" in moral_tag:
            moral_tag_plaintext = "Good"
        elif "Neutral" in moral_tag:
            moral_tag_plaintext = "Neutral"
        else:
            moral_tag_plaintext = "Evil"
        # If "Neutral" is picked for lawfulness and morality, changes the "lawfulness" tag to "True" to avoid duplication
        if "Neutral" in law_tag and "Neutral" in moral_tag:
            law_tag = Fore.GREEN + "True"
            law_tag_plaintext = "True"
        print(f"Generating Person (NPC)...")
        # Generates the name for the NPC
        f_name_import_list = CHARACTERS_LISTS_SHEET.col_values(2)
        f_name_list = [name for name in f_name_import_list[1:51]]
        l_name_import_list = CHARACTERS_LISTS_SHEET.col_values(3)
        l_name_list = [name for name in l_name_import_list[1:62]]
        f_name = f_name_list[random.randint(0,50)]
        l_name = l_name_list[random.randint(0,61)]
        name = f_name + " " + l_name
        # Generates a random age for the NPC
        age = random.randint(19, 70)
        # Generates a random race for the NPC
        race_import_list = CHARACTERS_LISTS_SHEET.col_values(1)
        race_list = [race for race in race_import_list[1:48]]
        race = race_list[random.randint(0,46)]
        # Elves typically live much longer than other races - multiplies the age by 10 if race is an Elf
        if "Elf" in race:
            age = age * 10
        # Generates a random gender for the NPC
        gender_list = [
           "\u001b[34mMale",
           "\u001b[31mFemale",
           "\u001b[33mNon-binary",
        ]
        gender = gender_list[random.randint(0,2)]
        # Generates the plaintext version of the gender as well as their gender pronouns
        if "Female" in gender:
            gender_plaintext = "Female"
            gender_pronouns = [
                "She is",
                "Her",
                "Hers",
                "She has"
            ]
        elif "Male" in gender:
            gender_plaintext = "Male"
            gender_pronouns = [
                "He is",
                "Him",
                "His",
                "He has"
            ]
        else:
            gender_plaintext = "Non-binary"
            gender_pronouns = [
                "They are",
                "Them",
                "Theirs",
                "They have"
            ]
        # Generates the NPC's hair color
        hair_color_import_list = CHARACTERS_LISTS_SHEET.col_values(4)
        hair_color_list = [color for color in hair_color_import_list[1:31]]
        hair_color = hair_color_list[random.randint(0,29)]
        # Generates two rumors the NPC is associated with
        rumors_import_list = CHARACTERS_LISTS_SHEET.col_values(5)
        rumors_list = [rumor for rumor in rumors_import_list[1:41]]
        rumors = []
        while len(rumors) < 2:
            rumor = rumors_list[random.randint(0,39)]
            if rumor not in rumors:
                rumors.append(rumor)
        # Generates the NPC's disposition and disposition text
        disposition = random.randint(-100, 100)
        if disposition < -50:
            disposition_text = "(They hate the players.)"
        elif disposition < 0:
            disposition_text = "(They dislike the players.)"
        elif 0 <= disposition <= 10:
            disposition_text = "(They feel neutral about the players.)"
        elif disposition < 50:
            disposition_text = "(They like the players.)"
        else:
            disposition_text = "(They love the players, platonically speaking.)"
        print("Character Generated!\n")
        # Outlines the description of the generated NPC
        description = f"Your NPC is named '{name}'.\n{gender_pronouns[0]} {age} years old. {gender_pronouns[0]} a {gender}\u001b[0m {race}.\n{gender_pronouns[0]} {law_tag} {moral_tag}\u001b[0m.\n{gender_pronouns[3]} {hair_color} hair.\n{gender_pronouns[0]} associated with the following rumors:\n{rumors[0]}, {rumors[1]}\nTheir disposition towards the players is {disposition} {disposition_text}\n"
        # Creates a plaintext version of the description to be copied by pyperclip - this avoids escape characters showing in the description
        description_plaintext = f"Your NPC is named '{name}'.\n{gender_pronouns[0]} {age} years old. {gender_pronouns[0]} a {gender_plaintext} {race}.\n{gender_pronouns[0]} {law_tag_plaintext} {moral_tag_plaintext}.\n{gender_pronouns[3]} {hair_color} hair.\n{gender_pronouns[0]} associated with the following rumors:\n{rumors[0]}, {rumors[1]}\nTheir disposition towards the players is {disposition} {disposition_text}\n"
        print(description)
        # Asks if the user wants to copy the NPC's plaintext description
        print(Back.WHITE + "Please use the ↑ and ↓ arrow keys to navigate and select your option by hitting ENTER.\n")
        if cutie.prompt_yes_or_no("Would you like to copy this description to your clipboard?"):
            pyperclip.copy(description_plaintext)
        # Asks if the user wants to create another NPC or place
        print(Back.WHITE + "Please use the ↑ and ↓ arrow keys to navigate and select your option by hitting ENTER.\n")
        if cutie.prompt_yes_or_no("Would you like to create a new NPC or place?"):
            # Starts the NPC / Place Generation program again
            fluff()
        else:
            # Returns the user to the main function loop of the program
            main()
    # Place specific generation content
    elif "Place" in chosen_option:
        print(Back.WHITE + "Please use the ↑ and ↓ arrow keys to navigate and select your option by hitting ENTER.\n" + Back.RESET)
        print(f"Please select applicable tags for the place to be generated.")
        # Asks the user to select a location type - towns have different attributes compared to dungeons or POIs
        location_type_tags = [
            "\u001b[34mTown",
            "\u001b[31mDungeon",
            "\u001b[32mPOI (Point of Interest)"
        ]
        location_type = location_type_tags[cutie.select(location_type_tags)]
        # Generates a random age for the place between 3 and 250 years
        age = random.randint(3, 250)
        print(f"Generating {location_type}\u001b[0m...")
        # Town Specific Generation
        if "Town" in location_type:
            # Generates the location type in plaintext to be copied later
            location_type_plaintext = "Town"
            # Calls the correct list of names for the location type to be imported from the Google Sheet
            name_import_list = PLACES_LISTS_SHEET.col_values(1)
            # Generates a leadership type for the town
            leadership_import_list = PLACES_LISTS_SHEET.col_values(4)
            leadership_list = [leadership for leadership in leadership_import_list[1:16]]
            leadership = leadership_list[random.randint(0,14)]
            # Calls the correct list of rumors for the location type from the Google Sheet
            rumors_import_list = PLACES_LISTS_SHEET.col_values(5)
            # Generates a disposition and disposition text for the town towards the players
            disposition = random.randint(-100, 100)
            if disposition < -50:
                disposition_text = "(They hate the players.)"
            elif disposition < 0:
                disposition_text = "(They dislike the players.)"
            elif 0 <= disposition <= 10:
                disposition_text = "(They feel neutral about the players.)"
            elif disposition < 50:
                disposition_text = "(They like the players.)"
            else:
                disposition_text = "(They love the players, platonically speaking.)"
        # Dungeon Specific Generation
        elif "Dungeon" in location_type:
            # Generates the location type in plaintext to be copied later
            location_type_plaintext = "Dungeon"
            # Calls the correct lists of names and rumors for the location type from the Google Sheet
            name_import_list = PLACES_LISTS_SHEET.col_values(2)
            rumors_import_list = PLACES_LISTS_SHEET.col_values(6)
        # POI Specific Generation
        else:
            #Generates the location type in plaintext to be copied later
            location_type_plaintext = "Point of Interest (POI)"
            # Calls the correct lists of names and rumors for the location type from the Google Sheet
            name_import_list = PLACES_LISTS_SHEET.col_values(3)
            rumors_import_list = PLACES_LISTS_SHEET.col_values(7)
        # Generates a name from the previously imported name list for the location type
        name_list = [name for name in name_import_list[1:51]]
        name = name_list[random.randint(0, 50)]
        # Generates two rumors from the previously imported rumor list for the location type
        rumors_list = [rumor for rumor in rumors_import_list[1:17]]
        rumors = []
        while len(rumors) < 2:
            rumor = rumors_list[random.randint(0, 15)]
            if rumor not in rumors:
                rumors.append(rumor)
        # Town Specific Description (includes leadership and disposition)
        if "Town" in location_type:
            description = f"Your {location_type}\u001b[0m is called {name}.\nIt was founded {age} years ago.\nIt is currently led by {leadership}.\nNotable rumors include:\n{rumors[0]}, {rumors[1]}\nTheir disposition towards the players is {disposition} {disposition_text}"
            # Plaintext version of the description - removes color codes for smoother copy-pasting
            description_plaintext = f"Your {location_type_plaintext} is called {name}.\nIt was founded {age} years ago.\nIt is currently led by {leadership}.\nNotable rumors include:\n{rumors[0]}, {rumors[1]}\nTheir disposition towards the players is {disposition} {disposition_text}"
        # Dungeon and POI Description
        else:
            description = f"Your {location_type}\u001b[0m is called {name}.\nIt was discovered {age} years ago.\nNotable rumors include:\n{rumors[0]}, {rumors[1]}\n"
            # Plaintext version of the description - removes color codes for smoother copy-pasting
            description_plaintext = f"Your {location_type_plaintext} is called {name}.\nIt was discovered {age} years ago.\nNotable rumors include:\n{rumors[0]}, {rumors[1]}\n"
        print(f"{location_type}\u001b[0m Generated!\n")
        print(description)
        # Asks if the user wants to copy the plaintext version of the place's description
        print(Back.WHITE + "Please use the ↑ and ↓ arrow keys to navigate and select your option by hitting ENTER.\n")
        if cutie.prompt_yes_or_no("Copy this description to your clipboard?"):
            pyperclip.copy(description_plaintext)
        # Asks if the user wants to create a new place or NPC
        print(Back.WHITE + "Please use the ↑ and ↓ arrow keys to navigate and select your option by hitting ENTER.\n")
        if cutie.prompt_yes_or_no("Create a new place or NPC?"):
            # Runs the NPC/Place Generation part of the program
            fluff()
        else:
            # Returns to the main program loop
            main()
    # Lets the user back out of the NPC/Place Generation part of the program
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
    # Finds the user's desired function by running the introduction function, which asks the user to declare their chosen function.
    chosen_function = introduction()
    # Takes the user to their chosen function
    function_selection(chosen_function)

main()