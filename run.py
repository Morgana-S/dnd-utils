import os
import random
import cutie
import gspread
from google.oauth2.service_account import Credentials
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


class Person:
    """Creates an instance of Person."""

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


def clear():
    """
    Clears the terminal for formatting purposes.
    Provides functionality for both Windows and OSX/Linux.
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def introduction():
    """
    Prints an introductory message and asks the user to
    select which function they would like to utilize.
    """
    introduction = """
    Welcome to \u001b[91mDNDUtils\u001b[0m!

    Please choose a program to use:

    \u001b[33mDiceRoller\u001b[0m - Roll Dice for your DND Game

    \u001b[36mFluff\u001b[0m - Generate people or places for your DND Game

    \u001b[32mInstructions\u001b[0m - Shows the instructions for DiceRoller
    and Fluff

    \u001b[93mPlease use the ↑ and ↓ arrows to select an option and hit ENTER.
    """
    print(introduction)
    # Defines the available options for function selection
    functions = [
        Fore.YELLOW + "DiceRoller",
        Fore.CYAN + "Fluff",
        Fore.GREEN + "Instructions"
    ]
    # Asks the user to choose a function from the choices above
    chosen_function = functions[cutie.select(functions)]
    return chosen_function


def function_selection(chosen_function):
    """Starts the user's chosen function."""
    if "DiceRoller" in chosen_function:
        diceroller()
    elif "Fluff" in chosen_function:
        fluff_selector()
    else:
        instructions_selection()


def diceroller():
    """
    Rolls a chosen number of dice with a designated number of sides
    plus a modifier and then displays the output
    """
    clear()
    num_of_dice = cutie.get_number(
        "How many dice do you want to roll? (Between 1 - 20)",
        min_value=1,
        max_value=20,
        allow_float=False
        )
    num_of_sides = cutie.get_number(
        "How many sides should each dice have? (Between 2 - 100)",
        min_value=2,
        max_value=100,
        allow_float=False
        )
    dice_rolls = [
        random.randint(1, num_of_sides) for value in range(num_of_dice)
        ]
    modifier_num = cutie.get_number(
        "What is the modifier for the roll? (Between -10 - 10)",
        min_value=-10,
        max_value=10,
        allow_float=False
        )
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
    # Rolls roll two sets of dice, and pick the worse of the two outcomes
    if "Disadvantage" in advantage_roll:
        roll_one = [random.randint(1, num_of_sides)
                    for value in range(num_of_dice)]
        roll_two = [random.randint(1, num_of_sides)
                    for value in range(num_of_dice)]
        if roll_one > roll_two:
            dice_rolls = roll_two
        else:
            dice_rolls = roll_one
    # Rolls two sets of dice, and pick the better of the two outcomes
    elif "Advantage" in advantage_roll:
        roll_one = [random.randint(1, num_of_sides)
                    for value in range(num_of_dice)]
        roll_two = [random.randint(1, num_of_sides)
                    for value in range(num_of_dice)]
        if roll_one > roll_two:
            dice_rolls = roll_one
        else:
            dice_rolls = roll_two
    result = (
        f"\u001b[32mDICE SUMMARY\n\n"
        f"\u001b[37mIndividual Dice: \u001b[33m{dice_rolls}\n"
        f"\u001b[37mTotal: \u001b[34m{sum(dice_rolls)}\n"
        f"\u001b[37mTotal + Modifier: "
        f"\u001b[35m{sum(dice_rolls) + modifier_num}\n"

    )
    clear()
    print(result)
    if cutie.prompt_yes_or_no(
            Fore.YELLOW + "Would you like to roll more dice?"):
        diceroller()
    else:
        clear()
        main()

def instructions_selection():
    """
    Allows the user to select which set of instructions they
    wish to view.
    """
    clear()
    general_instructions = """
    GENERAL INSTRUCTIONS

    Most selections within the program can be navigated by using the ↑ and ↓
    arrow keys and pressing ENTER to select an option. Sometimes, you may be
    prompted to type in a number (such as when rolling dice) and then hitting
    ENTER.\n
    """
    print(
        general_instructions
        + Fore.YELLOW
        + "Please choose which specific instructions you wish to read.\n"
    )
    instructions = [
        Fore.YELLOW + "Diceroller",
        Fore.CYAN + "Fluff",
        Back.RED + "Go Back"
    ]
    chosen_instructions = instructions[cutie.select(instructions)]
    if "Diceroller" in chosen_instructions:
        instructions_diceroller()
    elif "Fluff" in chosen_instructions:
        instructions_fluff()
    else:
        clear()
        main()


def instructions_diceroller():
    """Displays the instructions for the Diceroller Function"""
    clear()
    instructions_general = """
    DICEROLLER

    Diceroller is a tool used to quickly roll dice with various
    parameters for use in Dungeons and Dragons games.
    """
    instructions_selecting_numbers = """
    NUMBER SELECTION

    The Tool will first ask you to select a number of dice to roll
    and then the amount of sides on each dice. A typical example
    of a dice roll in Dungeons and Dragons is '3d6', which would be
    rolling 3 dice with 6 sides each.

    The tool will also ask if you are adding a 'modifier' to the roll.
    In Dungeons and Dragons, player statistics allow them to sometimes add
    or remove numbers from a dice roll, reflecting their character's natural
    abilities. If no modifier is required, the user can simply enter '0'.
    """
    instructions_advantage = """
    INFORMATION ABOUT ADVANTAGE / DISADVANTAGE / NORMAL ROLLS

    The tool will then ask you whether the roll has 'Advantage',
    'Disadvantage', or whether it is a 'Normal roll'. These are
    defined as follows:

    Advantage - Rolls two sets of dice and picks the 'best' outcomes,
    e.g. for a 2d6 roll, it rolls two six-sided dice twice and picks the
    best result from each set of rolls. If one total comes to 11 and the
    other total comes to 6, it picks the set with the total that comes to 11.

    Disadvantage - Rolls two sets of dice and picks the 'worst' outcomes.
    e.g. for a 2d6 roll, it rolls two six-sided dice twice and picks the
    worst result from each set of rolls. If one total comes to 11 and the
    other total comes to 6, it picks the set with the total that comes to 6.

    Normal Roll - Rolls one set of dice.

    The results of the dice roll are then displayed, with a breakdown
    of the roll so the user can see how the result was reached.
    """
    print(instructions_general)
    options = [
        Fore.CYAN + "Read about selecting numbers for rolling dice",
        Fore.GREEN + "Read about advantage, disadvantage, and normal rolls",
        Back.RED + "Go Back"
    ]
    chosen_option = options[cutie.select(options)]
    if "numbers" in chosen_option:
        clear()
        print(instructions_selecting_numbers)
        option = [Back.RED + "Go Back"]
        chosen_option = option[cutie.select(option)]
        if "Back" in chosen_option:
            instructions_diceroller()
    elif "advantage" in chosen_option:
        clear()
        print(instructions_advantage)
        option = [Back.RED + "Go Back"]
        chosen_option = option[cutie.select(option)]
        if "Back" in chosen_option:
            instructions_diceroller()
    else:
        instructions_selection()


def instructions_fluff():
    """Displays the instructions for the Fluff function"""
    clear()
    instructions_general = """
    FLUFF

    Fluff is a content generation tool to be used for creating
    characters and places within a Dungeons and Dragons Game.

    The tool will first ask the user whether they want to generate a
    person or a place.

    The options below will go into detail about generating a person or place.
    """
    instructions_person = """
    GENERATING A PERSON

    The user is asked to pick a 'Lawfulness' and 'Morality' tag for the
    person they wish to generate. In Dungeons and Dragons, each person
    has a law alignment and a moral alignment which provides a shorthand
    for how the character acts within the confines of society.

    The tool then generates a variety of characteristics for the person,
    including name, age, race, gender, hair color, two rumors (that allow
    the user to provide motiviations for the character), and how the
    character might feel about the player characters. This provides a
    foundation for the user to flesh out the characters attitude, motivations
    and actions.
    """
    instructions_place = """
    GENERATING A PLACE

    The user is asked to select whether they would like to generate a town,
    dungeon, or point of interest. These different selections have different
    parameters which the user might be interested in, such as dungeons having
    sinister place names, and towns having information on how the town is led.

    The chosen option is then generated, containing information such as the
    name of the place, age of the place, rumors concerning the place, and if
    the location is a town, information on the leadership and the town's
    general disposition towards the players.
    """
    instructions_information = """
    SAVING YOUR GENERATED PERSON/PLACE

    After generating a person or place, you will be prompted to save them to
    the Google Spreadsheet which stores this information. You can save a
    generated instance by typing 'y' and hitting ENTER. If you do not wish
    to save the instance to the sheet, you can type 'n' and hit ENTER.
    """
    print(instructions_general)
    options = [
        Fore.GREEN + "Show instructions for generating a person",
        Fore.CYAN + "Show instructions for generating a place",
        Fore.YELLOW + "Show information on saving generated people and places",
        Back.RED + "Go Back"
    ]
    chosen_option = options[cutie.select(options)]
    if "person" in chosen_option:
        clear()
        print(instructions_person)
        option = [Back.RED + "Go Back"]
        chosen_option = option[cutie.select(option)]
        if "Back" in chosen_option:
            instructions_fluff()
    elif "information" in chosen_option:
        clear()
        print(instructions_information)
        option = [Back.RED + "Go Back"]
        chosen_option = option[cutie.select(option)]
        if "Back" in chosen_option:
            instructions_fluff()
    elif "place" in chosen_option:
        clear()
        print(instructions_place)
        option = [Back.RED + "Go Back"]
        chosen_option = option[cutie.select(option)]
        if "Back" in chosen_option:
            instructions_fluff()
    else:
        instructions_selection()





def fluff_selector():
    """
    Asks the user to choose whether they're looking to generate
    a person or place.
    """
    clear()
    message = """
    Do you want to generate a \u001b[32mPerson\u001b[0m 
    or a \u001b[31mPlace?\n
    """
    print(message)
    options = [
        Fore.GREEN + "Person",
        Fore.RED + "Place",
        Back.RED + "Go Back"
    ]
    generation_type = options[cutie.select(options)]
    if "Go Back" in generation_type:
        main()
    else:
        tag_selector(generation_type)


def tag_selector(generation_type):
    """
    Takes the chosen option from the fluff_selector function
    and asks the user to choose the tags that are appropriate to
    the type of instance they're trying to generate (Person or Place).
    """
    clear()
    if "Person" in generation_type:
        message = """
        Please select applicable tags for the generation of your character.\n
        """
        print(message)
        law_tags = [
            "Law Alignment:",
            Fore.CYAN + "Lawful",
            Fore.GREEN + "Neutral",
            Fore.RED + "Chaotic",
        ]
        moral_tags = [
            "Moral Alignment:",
            Fore.YELLOW + "Good",
            Fore.BLUE + "Neutral",
            Fore.RED + "Evil"
        ]
        law_tag = law_tags[cutie.select(
            law_tags,
            caption_indices=0,
            selected_index=1
            )]
        moral_tag = moral_tags[cutie.select(
            moral_tags,
            caption_indices=0,
            selected_index=1
            )]
        # Creates plaintext versions of the tags
        # for storing in the Google Sheet
        if "Lawful" in law_tag:
            law_tag_plaintext = "Lawful"
        elif "Neutral" in law_tag:
            law_tag_plaintext = "Neutral"
        else:
            law_tag_plaintext = "Chaotic"
        if "Good" in moral_tag:
            moral_tag_plaintext = "Good"
        elif "Neutral" in law_tag and moral_tag:
            law_tag_plaintext = "True"
            moral_tag_plaintext = "Neutral"
        elif "Neutral" in moral_tag:
            moral_tag_plaintext = "Neutral"
        else:
            moral_tag_plaintext = "Evil"
        return law_tag, moral_tag, law_tag_plaintext, moral_tag_plaintext
    else:
        message = """
        Please select applicable tags for the place to be generated.
        """
        print(message)
        location_tags = [
            "Location Type:",
            Fore.BLUE + "Town",
            Fore.RED + "Dungeon",
            Fore.GREEN + "Point of Interest"
        ]
        location_tag = [cutie.select(
            location_tags,
            caption_indices=0,
            selected_index=1
        )]
        # Creates plaintext version of the location tag for storage in
        # Google Sheet
        if "Town" in location_tag:
            location_tag_plaintext = "Town"
        elif "Dungeon" in location_tag:
            location_tag_plaintext = "Dungeon"
        else:
            location_tag_plaintext = "Point of Interest"
        return location_tag, location_tag_plaintext


def fluff():
    """
    Asks the user if they want to generate a person (NPC) or place,
    takes user input for predefined features of the entity and
    then generates an entity by drawing from predefined lists of
    characteristics.
    """
    clear()
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
        # Dungeon and POI Description
        else:
            description = (
                f"Your {place_location_type}\u001b[0m is called "
                f"{place_name}.\nIt was discovered {place_age} years ago.\n"
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


def main():
    """Runs the main program function sequence."""
    chosen_function = introduction()
    function_selection(chosen_function)


main()
