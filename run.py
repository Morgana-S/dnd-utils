import gspread
from google.oauth2.service_account import Credentials
import cutie
import random
import pyperclip
from colorama import Fore, Back, init
init(autoreset=True)


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
ALL_PLACES = PLACES_SHEET.get_all_records()
ALL_CHARACTERS = CHARACTERS_SHEET.get_all_records()


class NPC:
    """Creates an instance of NPC."""

    def __init__(self,
                 name,
                 law_tag,
                 moral_tag,
                 age,
                 race,
                 gender,
                 gender_pronouns_1,
                 gender_pronouns_2,
                 gender_pronouns_3,
                 gender_pronouns_4,
                 hair_color,
                 rumor_1,
                 rumor_2,
                 disposition,
                 disposition_text):
        self.name = name
        self.law = law_tag
        self.morality = moral_tag
        self.age = age
        self.race = race
        self.gender = gender
        self.gender_pronouns = [
            gender_pronouns_1,
            gender_pronouns_2,
            gender_pronouns_3,
            gender_pronouns_4
        ]
        self.hair_color = hair_color
        self.rumors = [
            rumor_1,
            rumor_2
        ]
        self.disposition = disposition
        self.disposition_text = disposition_text


class Place:
    """Creates an instance of Place."""

    def __init__(self,
                 location_type,
                 name,
                 age,
                 rumor_1,
                 rumor_2,):
        self.location_type = location_type
        self.name = name
        self.age = age
        self.rumors = [
            rumor_1,
            rumor_2
        ]


class Town(Place):
    """
    Crates an instance of the subclass Town
    To be used only with location_type "Town"
    members of the class Place.
    """

    def __init__(self,
                 location_type,
                 name,
                 age,
                 rumor_1,
                 rumor_2,
                 leadership,
                 disposition,
                 disposition_text):
        super.__init__(location_type,
                       name=name,
                       age=age,
                       rumor_1=rumor_1,
                       rumor_2=rumor_2,)
        self.leadership = leadership
        self.disposition = disposition
        self.disposition_text = disposition_text


def introduction():
    """
    Prints an introductory message and asks the user to
    select which function they would like to utilize.
    """
    print("Welcome to" + Fore.RED + " DNDUtils" + Fore.WHITE + "!")
    print("Please choose a program to use:\n")
    print(Fore.YELLOW + "DiceRoller" + Fore.RESET +
          " - Roll Dice for your DND Game")
    print(Fore.CYAN + "Fluff" + Fore.RESET +
          " - Create NPCs or Places for your DND Game\n")
    print(Fore.YELLOW + "Please use the ↑ and ↓ arrow keys to navigate\n"
          "and select your option by hitting ENTER.\n")
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
    Rolls a chosen number of dice with a designated number of sides
    plus a modifier and then displays the output
    """
    # Defines the variables used to calculate the dice rolls
    # with user input - validates for number-only input
    # Number of Dice to Roll
    print(
        Fore.YELLOW +
        "Please type in the number of dice you want to roll "
        "and hit ENTER.\n"
    )
    num_of_dice = cutie.get_number(
        "How many dice do you want to roll?", min_value=1, allow_float=False
    )
    # Number of Sides on Each Dice
    print(
        Fore.YELLOW +
        "Please type in the number of sides "
        "on each dice and hit ENTER.\n"
    )
    num_of_sides = cutie.get_number(
        "How many sides should each dice have?",
        min_value=2,
        allow_float=False
    )
    dice_rolls = [random.randint(1, num_of_sides)
                  for value in range(num_of_dice)]
    # Skill Modifier - DND Skills allow for an additional number
    # to be added to the end of the roll
    print(
        Fore.YELLOW +
        "Please enter the number for the skill "
        "modifier and press ENTER.\n"
    )
    modifier_num = cutie.get_number(
        "What is the modifier for the roll?", allow_float=False)
    # Asks the user to select whether the roll has
    # Advantage, Disadvantage, or Neither
    print(Fore.YELLOW + "Please use the ↑ and ↓ arrow keys to navigate\n"
          "and select your option by hitting ENTER.\n")
    print(
        Fore.YELLOW +
        "Is this an Advantage, Disadvantage, "
        "or Normal Roll?\n"
    )
    advantage = [
        Fore.GREEN + "Advantage",
        Fore.RED + "Disadvantage",
        Fore.BLUE + "Normal Roll"
    ]
    advantage_roll = advantage[cutie.select(advantage)]
    # Disadvantage Rolls roll two sets of dice, and pick the worse
    # of the two outcomes
    if "Disadvantage" in advantage_roll:
        roll_one = [random.randint(1, num_of_sides)
                    for value in range(num_of_dice)]
        roll_two = [random.randint(1, num_of_sides)
                    for value in range(num_of_dice)]
        if roll_one > roll_two:
            dice_rolls = roll_two
        else:
            dice_rolls = roll_one
    # Advantage Rolls roll two sets of dice, and pick the better
    # of the two outcomes
    elif "Advantage" in advantage_roll:
        roll_one = [random.randint(1, num_of_sides)
                    for value in range(num_of_dice)]
        roll_two = [random.randint(1, num_of_sides)
                    for value in range(num_of_dice)]
        if roll_one > roll_two:
            dice_rolls = roll_one
        else:
            dice_rolls = roll_two
    # Prints the result
    print(Fore.GREEN + "\nDice Summary")
    print(
        f"\n\u001b[36mThe individual dice rolls were:"
        f"\u001b[33m{dice_rolls}"
    )
    print(f"\u001b[31mThe total of all dice is: \u001b[37m{sum(dice_rolls)}")
    print(
        f"\u001b[35mThe sum of all dice rolls plus the modifier was: "
        f"\u001b[32m{sum(dice_rolls) + modifier_num}"
    )
    print(
        Fore.YELLOW +
        "Please use the ↑ and ↓ arrow keys to navigate\n"
        "and select your option by hitting ENTER.\n"
    )
    if cutie.prompt_yes_or_no(Fore.YELLOW +
                              "Would you like to roll more dice?"):
        # Begins the dice-rolling function again
        diceroller()
    else:
        # Loops the program back to the start
        main()


def fluff():
    """
    Asks the user if they want to generate a person (NPC) or place,
    takes user input for predefined features of the entity and
    then generates an entity by drawing
    from predefined lists of characteristics
    """
    # Asks the user whether they want to generate a person
    # or place and assigns the selection to chosen_option
    print(Fore.YELLOW + "Please use the ↑ and ↓ arrow keys to navigate\n"
          "and select your option by hitting ENTER.\n")
    print(
        "Do you want to generate a \u001b[32mPerson "
        "\u001b[37mor a \u001b[31mPlace?\n"
    )
    options = [
        Fore.GREEN + "Person (NPC)",
        Fore.RED + "Place",
        Back.RED + "Go Back"
    ]
    chosen_option = options[cutie.select(options)]
    # Person-specific generation content
    if "Person" in chosen_option:
        print(Fore.YELLOW + "Please use the ↑ and ↓ arrow keys to navigate\n"
              "and select your option by hitting ENTER.\n")
        print("Please select applicable tags for "
              "the character to be generated.")
        # Asks the user to pick the generated person's lawfulness
        law_tags = [
            "Law Alignment:",
            Fore.CYAN + "Lawful",
            Fore.GREEN + "Neutral",
            Fore.RED + "Chaotic",
        ]
        npc_law_tag = law_tags[cutie.select(law_tags, caption_indices=[0])]
        # Creates a plaintext version of the chosen lawfulness tag
        if "Lawful" in npc_law_tag:
            law_tag_plaintext = "Lawful"
        elif "Neutral" in npc_law_tag:
            law_tag_plaintext = "Neutral"
        else:
            law_tag_plaintext = "Chaotic"
        # Asks the user to pick the generated person's morality
        print(Fore.YELLOW + "Please use the ↑ and ↓ arrow keys to navigate\n"
              "and select your option by hitting ENTER.\n")
        moral_tags = [
            "Moral Alignment:",
            Fore.YELLOW + "Good",
            Fore.BLUE + "Neutral",
            Back.RED + "Evil",
        ]
        npc_moral_tag = moral_tags[cutie.select(
            moral_tags, caption_indices=[0])]
        # Creates a plaintext version of the chosen morality tag
        if "Good" in npc_moral_tag:
            moral_tag_plaintext = "Good"
        elif "Neutral" in npc_moral_tag:
            moral_tag_plaintext = "Neutral"
        else:
            moral_tag_plaintext = "Evil"
        # If "Neutral" is picked for lawfulness and morality
        # changes the "lawfulness" tag to "True" to avoid duplication
        if "Neutral" in npc_law_tag and "Neutral" in npc_moral_tag:
            npc_law_tag = Fore.GREEN + "True"
            law_tag_plaintext = "True"
        print("Generating Person (NPC)...")
        # Generates the name for the NPC
        f_name_import_list = CHARACTERS_LISTS_SHEET.col_values(2)
        f_name_list = [name for name in f_name_import_list[1:51]]
        l_name_import_list = CHARACTERS_LISTS_SHEET.col_values(3)
        l_name_list = [name for name in l_name_import_list[1:62]]
        f_name = f_name_list[random.randint(0, 50)]
        l_name = l_name_list[random.randint(0, 61)]
        npc_name = f_name + " " + l_name
        # Generates a random age for the NPC
        npc_age = random.randint(19, 70)
        # Generates a random race for the NPC
        race_import_list = CHARACTERS_LISTS_SHEET.col_values(1)
        race_list = [race for race in race_import_list[1:48]]
        npc_race = race_list[random.randint(0, 46)]
        # Elves typically live much longer than other races
        # multiplies the age by 10 if race is an Elf
        if "Elf" in npc_race:
            npc_age = npc_age * 10
        # Generates a random gender for the NPC
        gender_list = [
            "\u001b[34mMale",
            "\u001b[31mFemale",
            "\u001b[33mNon-binary",
        ]
        npc_gender = gender_list[random.randint(0, 2)]
        # Generates the plaintext version of the gender
        # as well as their gender pronouns
        if "Female" in npc_gender:
            gender_plaintext = "Female"
            npc_gender_pronouns = [
                "She is",
                "Her",
                "Hers",
                "She has"
            ]
        elif "Male" in npc_gender:
            gender_plaintext = "Male"
            npc_gender_pronouns = [
                "He is",
                "Him",
                "His",
                "He has"
            ]
        else:
            gender_plaintext = "Non-binary"
            npc_gender_pronouns = [
                "They are",
                "Them",
                "Theirs",
                "They have"
            ]
        # Generates the NPC's hair color
        hair_color_import_list = CHARACTERS_LISTS_SHEET.col_values(4)
        hair_color_list = [color for color in hair_color_import_list[1:31]]
        npc_hair_color = hair_color_list[random.randint(0, 29)]
        # Generates two rumors the NPC is associated with
        rumors_import_list = CHARACTERS_LISTS_SHEET.col_values(5)
        rumors_list = [rumor for rumor in rumors_import_list[1:41]]
        npc_rumors = []
        while len(npc_rumors) < 2:
            rumor = rumors_list[random.randint(0, 39)]
            if rumor not in npc_rumors:
                npc_rumors.append(rumor)
        # Generates the NPC's disposition and disposition text
        npc_disposition = random.randint(-100, 100)
        if npc_disposition < -50:
            npc_disposition_text = "(They hate the players.)"
        elif npc_disposition < 0:
            npc_disposition_text = "(They dislike the players.)"
        elif 0 <= npc_disposition <= 10:
            npc_disposition_text = "(They feel neutral about the players.)"
        elif npc_disposition < 50:
            npc_disposition_text = "(They like the players.)"
        else:
            npc_disposition_text = "(They love the players, "
            "platonically speaking.)"
        print("Character Generated!\n")
        # Outlines the description of the generated NPC
        description = (
            f"Your NPC is named '{npc_name}'.\n"
            f"{npc_gender_pronouns[0]} {npc_age} years old. "
            f"{npc_gender_pronouns[0]} a "
            f"{npc_gender}\u001b[0m {npc_race}.\n"
            f"{npc_gender_pronouns[0]} {npc_law_tag} "
            f"{npc_moral_tag}\u001b[0m.\n"
            f"{npc_gender_pronouns[3]} {npc_hair_color} hair.\n"
            f"{npc_gender_pronouns[0]} associated with the following rumors:\n"
            f"{npc_rumors[0]}, {npc_rumors[1]}\nTheir disposition towards "
            f"the players is {npc_disposition} {npc_disposition_text}\n"
        )
        # Creates a plaintext version of the description to be copied
        # by pyperclip - this avoids escape characters
        # showing in the description
        description_plaintext = (
            f"Your NPC is named '{npc_name}'.\n"
            f"{npc_gender_pronouns[0]} {npc_age} years old. "
            f"{npc_gender_pronouns[0]} a {gender_plaintext} {npc_race}.\n"
            f"{npc_gender_pronouns[0]} {law_tag_plaintext} "
            f"{moral_tag_plaintext}.\n"
            f"{npc_gender_pronouns[3]} {npc_hair_color} hair.\n"
            f"{npc_gender_pronouns[0]} associated with the following rumors:\n"
            f"{npc_rumors[0]}, {npc_rumors[1]}\n"
            f"Their disposition towards the players is {npc_disposition} "
            f"{npc_disposition_text}\n"
        )
        print(description)
        print(Fore.YELLOW + "Please use the ↑ and ↓ arrow keys to navigate\n"
              "and select your option by hitting ENTER.\n")
        if cutie.prompt_yes_or_no("Convert this NPC to an object?"):
            print(Fore.YELLOW + "Converting to Object "
                  "and saving in Spreadsheet...")
            new_instance = dict(
                name=npc_name,
                law_tag=law_tag_plaintext,
                moral_tag=moral_tag_plaintext,
                age=npc_age,
                race=npc_race,
                gender=gender_plaintext,
                gender_pronouns_1=npc_gender_pronouns[0],
                gender_pronouns_2=npc_gender_pronouns[1],
                gender_pronouns_3=npc_gender_pronouns[2],
                gender_pronouns_4=npc_gender_pronouns[3],
                hair_color=npc_hair_color,
                rumor_1=npc_rumors[0],
                rumor_2=npc_rumors[1],
                disposition=npc_disposition,
                disposition_text=npc_disposition_text
            )
            new_instance_list = [value for value in new_instance.values()]
            CHARACTERS_SHEET.append_row(new_instance_list, table_range="A1:O1")
        # Asks if the user wants to create another NPC or place
        print(Fore.YELLOW + "Please use the ↑ and ↓ arrow keys to navigate\n"
              "and select your option by hitting ENTER.\n")
        if cutie.prompt_yes_or_no("Would you like to create a new NPC "
                                  "or place?"):
            # Starts the NPC / Place Generation program again
            fluff()
        else:
            # Returns the user to the main function loop of the program
            main()
    # Place specific generation content
    elif "Place" in chosen_option:
        print(Fore.YELLOW + "Please use the ↑ and ↓ arrow keys to navigate\n"
              "and select your option by hitting ENTER.\n")
        print("Please select applicable tags for the place to be generated.")
        # Asks the user to select a location type
        # towns have different attributes compared to dungeons or POIs
        location_type_tags = [
            "\u001b[34mTown",
            "\u001b[31mDungeon",
            "\u001b[32mPOI (Point of Interest)"
        ]
        place_location_type = location_type_tags[cutie.select(
            location_type_tags)]
        # Generates a random age for the place between 3 and 250 years
        place_age = random.randint(3, 250)
        print(f"Generating {place_location_type}\u001b[0m...")
        # Town Specific Generation
        if "Town" in place_location_type:
            # Generates the location type in plaintext to be copied later
            location_type_plaintext = "Town"
            # Calls the correct list of names for the location type
            # to be imported from the Google Sheet
            name_import_list = PLACES_LISTS_SHEET.col_values(1)
            # Generates a leadership type for the town
            leadership_import_list = PLACES_LISTS_SHEET.col_values(4)
            leadership_list = [
                leadership for leadership in leadership_import_list[1:16]]
            place_leadership = leadership_list[random.randint(0, 14)]
            # Calls the correct list of rumors for the location type
            # from the Google Sheet
            rumors_import_list = PLACES_LISTS_SHEET.col_values(5)
            # Generates a disposition and disposition text for the town
            # towards the players
            place_disposition = random.randint(-100, 100)
            if place_disposition < -50:
                place_disposition_text = "(They hate the players.)"
            elif place_disposition < 0:
                place_disposition_text = "(They dislike the players.)"
            elif 0 <= place_disposition <= 10:
                place_disposition_text = "(They feel neutral about the "
                "players.)"
            elif place_disposition < 50:
                place_disposition_text = "(They like the players.)"
            else:
                place_disposition_text = "(They love the players, "
                "platonically speaking.)"
        # Dungeon Specific Generation
        elif "Dungeon" in place_location_type:
            # Generates the location type in plaintext to be copied later
            location_type_plaintext = "Dungeon"
            # Calls the correct lists of names and rumors for the
            # location type from the Google Sheet
            name_import_list = PLACES_LISTS_SHEET.col_values(2)
            rumors_import_list = PLACES_LISTS_SHEET.col_values(6)
        # POI Specific Generation
        else:
            # Generates the location type in plaintext to be copied later
            location_type_plaintext = "Point of Interest (POI)"
            # Calls the correct lists of names and rumors for the
            # location type from the Google Sheet
            name_import_list = PLACES_LISTS_SHEET.col_values(3)
            rumors_import_list = PLACES_LISTS_SHEET.col_values(7)
        # Generates a name from the previously imported name list for the
        # location type
        name_list = [name for name in name_import_list[1:51]]
        place_name = name_list[random.randint(0, 50)]
        # Generates two rumors from the previously imported rumor list for the
        # location type
        rumors_list = [rumor for rumor in rumors_import_list[1:17]]
        place_rumors = []
        while len(place_rumors) < 2:
            rumor = rumors_list[random.randint(0, 15)]
            if rumor not in place_rumors:
                place_rumors.append(rumor)
        # Town Specific Description (includes leadership and disposition)
        if "Town" in place_location_type:
            description = (
                f"Your {place_location_type}\u001b[0m is called "
                f"{place_name}.\nIt was founded {place_age} years ago.\n"
                f"It is currently led by {place_leadership}.\n"
                f"Notable rumors include:\n"
                f"{place_rumors[0]}, {place_rumors[1]}\n"
                f"Their disposition towards the players "
                f"is {place_disposition} "
                f"{place_disposition_text}"
            )
            # Plaintext version of the description - removes color codes
            # for smoother copy-pasting
            description_plaintext = (
                f"Your {location_type_plaintext} is "
                f"called {place_name}.\nIt was founded "
                f"{place_age} years ago.\n"
                f"It is currently led by {place_leadership}.\n"
                f"Notable rumors include:"
                f"\n{place_rumors[0]}, {place_rumors[1]}\n"
                f"Their disposition towards the players "
                f"is {place_disposition} "
                f"{place_disposition_text}"
            )
        # Dungeon and POI Description
        else:
            description = (
                f"Your {place_location_type}\u001b[0m is called "
                f"{place_name}.\nIt was discovered {place_age} years ago.\n"
                f"Notable rumors include:\n"
                f"{place_rumors[0]}, {place_rumors[1]}\n"
            )
            # Plaintext version of the description
            # removes color codes for smoother copy-pasting
            description_plaintext = (
                f"Your {location_type_plaintext} is "
                f"called {place_name}.\n"
                f"It was discovered {place_age} years ago.\n"
                f"Notable rumors include:\n"
                f"{place_rumors[0]}, {place_rumors[1]}\n"
            )
        print(f"{place_location_type}\u001b[0m Generated!\n")
        print(description)
        print(Fore.YELLOW + "Please use the ↑ and ↓ arrow keys to navigate\n"
              "and select your option by hitting ENTER.\n")
        if cutie.prompt_yes_or_no("Convert this place to an object?"):
            print(Fore.YELLOW + "Converting to object and "
                  "saving in spreadsheet...")
            if "Town" in place_location_type:
                new_instance = dict(
                    location_type=location_type_plaintext,
                    name=place_name,
                    age=place_age,
                    rumor_1=place_rumors[0],
                    rumor_2=place_rumors[1],
                    leadership=place_leadership,
                    disposition=place_disposition,
                    disposition_text=place_disposition_text
                )
            else:
                new_instance = dict(
                    location_type=location_type_plaintext,
                    name=place_name,
                    age=place_age,
                    rumor_1=place_rumors[0],
                    rumor_2=place_rumors[1]
                )
            new_instance_list = [value for value in new_instance.values()]
            print(new_instance_list)
            PLACES_SHEET.append_row(new_instance_list, table_range="A1:H1")
        # Asks if the user wants to create a new place or NPC
        print(Fore.YELLOW + "Please use the ↑ and ↓ arrow keys to navigate\n"
              "and select your option by hitting ENTER.\n")
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
    # Checks the string in chosen_function and starts the
    # appropriate part of the program
    if "DiceRoller" in chosen_function:
        print("Starting" + Fore.YELLOW + " DiceRoller" + Fore.RESET + "...")
        diceroller()
    elif "Fluff" in chosen_function:
        print("Starting" + Fore.CYAN + " Fluff" + Fore.RESET + "...")
        fluff()
    else:
        print(Back.RED + "Exiting DNDUtils" + Back.RESET + "...")


def main():
    """
    Runs the main program function sequence
    """
    # Finds the user's desired function by running the introduction function
    # which asks the user to declare their chosen function.
    chosen_function = introduction()
    # Takes the user to their chosen function
    function_selection(chosen_function)


main()
