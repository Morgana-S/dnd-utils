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


class Person:
    """Creates an instance of Person."""
    def __init__(
            self,
            name,
            law_tag,
            moral_tag,
            age,
            race,
            gender,
            hair_color,
            rumor_1,
            rumor_2,
            disposition,
            disposition_text
            ):
        self.name = name
        self.alignment = law_tag + " " + moral_tag
        self.age = age
        self.race = race
        self.gender = gender
        self.hair_color = hair_color
        self.rumor_1 = rumor_1
        self.rumor_2 = rumor_2
        self.disposition = disposition
        self.disposition_text = disposition_text


class Place:
    """Creates an instance of Place."""
    def __init__(
            self,
            location_type,
            name,
            age,
            rumor_1,
            rumor_2,
            leadership,
            disposition,
            disposition_text
            ):
        self.location_type = location_type
        self.name = name
        self.age = age
        self.rumor_1 = rumor_1
        self.rumor_2 = rumor_2
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

    \u001b[31mView generated people/places\u001b[0m - View existing instances
    generated using Fluff

    \u001b[32mInstructions\u001b[0m - Shows the instructions for DiceRoller,
    Fluff, and Viewing generated people/places

    \u001b[93mPlease use the ↑ and ↓ arrows to select an option and hit ENTER.
    """
    print(introduction)
    # Defines the available options for function selection
    functions = [
        Fore.YELLOW + "DiceRoller",
        Fore.CYAN + "Fluff",
        Fore.RED + "View generated people/places",
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
    elif "Instructions" in chosen_function:
        instructions_selection()
    else:
        view_instances_selector()


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
        clear()
        main()
    else:
        fluff_tag_selector(generation_type)


def fluff_tag_selector(generation_type):
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
            caption_indices=[0],
            selected_index=1
            )]
        moral_tag = moral_tags[cutie.select(
            moral_tags,
            caption_indices=[0],
            selected_index=1
            )]
        # Change law tag to "True" if character alignment is double neutral
        if "Neutral" in moral_tag and law_tag:
            law_tag = Fore.BLUE + "True"
        generation_tags = (
            law_tag,
            moral_tag,
            )
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
        location_tag = location_tags[cutie.select(
            location_tags,
            caption_indices=[0],
            selected_index=1
        )]
        generation_tags = location_tag
    fluff_generation(generation_tags)


def fluff_generation(generation_tags):
    """
    Generates a person or place depending on the generation tags provided.
    """
    # Checks the length of the generation tags to see if generating a person
    # or place
    clear()
    if len(generation_tags) == 2:
        print("Generating Person...")
        # Pulls the name generation lists and chooses a name at random
        # from each one, combining them for the character's name
        f_name_import_list = CHARACTERS_LISTS_SHEET.col_values(2)
        f_name_list = [name for name in f_name_import_list[1:51]]
        l_name_import_list = CHARACTERS_LISTS_SHEET.col_values(3)
        l_name_list = [name for name in l_name_import_list[1:62]]
        f_name = f_name_list[random.randint(0, 49)]
        l_name = l_name_list[random.randint(0, 60)]
        name = f_name + " " + l_name
        age = random.randint(19, 70)
        # Pulls the race list and picks a random race for the person
        race_import_list = CHARACTERS_LISTS_SHEET.col_values(1)
        race_list = [race for race in race_import_list[1:48]]
        race = race_list[random.randint(0, 46)]
        # Multiplies age if character is an elf to reflect that elves
        # typically live much longer
        if "Elf" in race:
            age = age * 10
        # Generates the person's gender
        gender_list = [
            Fore.BLUE + "Male",
            Fore.RED + "Female",
            Fore.YELLOW + "Non-binary"
        ]
        gender = gender_list[random.randint(0, 2)]
        # Generates the person's hair color
        hair_color_import_list = CHARACTERS_LISTS_SHEET.col_values(4)
        hair_color_list = [color for color in hair_color_import_list[1:31]]
        hair_color = hair_color_list[random.randint(0, 29)]
        # Generates two rumors for the person
        rumors_import_list = CHARACTERS_LISTS_SHEET.col_values(5)
        rumors_list = [rumor for rumor in rumors_import_list[1:41]]
        rumors = []
        while len(rumors) < 2:
            rumor = rumors_list[random.randint(0, 39)]
            if rumor not in rumors:
                rumors.append(rumor)
        # Generates person's disposition towards the players
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
            disposition_text = "(They love the players.)"
        generated_instance = (
            generation_tags,
            name,
            age,
            race,
            gender,
            hair_color,
            rumors,
            disposition,
            disposition_text
            )
        fluff_display(generated_instance)
    else:
        print("Generating Place...")
        # Pulls correct lists depending on location type
        if "Town" in generation_tags:
            # Imports the correct lists for towns
            name_import_list = PLACES_LISTS_SHEET.col_values(1)
            leadership_import_list = PLACES_LISTS_SHEET.col_values(4)
            leadership_list = [
                leadership for leadership in leadership_import_list[1:16]
            ]
            leadership = leadership_list[random.randint(0, 14)]
            rumors_import_list = PLACES_LISTS_SHEET.col_values(5)
            disposition = random.randint(-100, 100)
            if disposition < -50:
                disposition_text = "(They hate the players.)"
            elif disposition < 0:
                disposition_text = "(They dislike the players.)"
            elif 0 <= disposition <= 10:
                disposition_text = (
                    "(They feel neutral about the players)"
                )
            elif disposition < 50:
                disposition_text = "(They like the players.)"
            else:
                disposition_text = "(They love the players.)"
        elif "Dungeon" in generation_tags:
            name_import_list = PLACES_LISTS_SHEET.col_values(2)
            rumors_import_list = PLACES_LISTS_SHEET.col_values(6)
        else:
            name_import_list = PLACES_LISTS_SHEET.col_values(3)
            rumors_import_list = PLACES_LISTS_SHEET.col_values(7)
        name_list = [name for name in name_import_list[1:51]]
        name = name_list[random.randint(0, 49)]
        age = random.randint(3, 250)
        rumors_list = [rumor for rumor in rumors_import_list[1:17]]
        rumors = []
        while len(rumors) < 2:
            rumor = rumors_list[random.randint(0, 15)]
            if rumor not in rumors:
                rumors.append(rumor)
        # Packs the generated location into a tuple depending on type
        if "Town" in generation_tags:
            generated_instance = (
                generation_tags,
                name,
                age,
                rumors,
                leadership,
                disposition,
                disposition_text
            )
        else:
            generated_instance = (
                generation_tags,
                name,
                age,
                rumors
            )
        fluff_display(generated_instance)


def fluff_display(generated_instance):
    """
    Takes the data from instance generation and displays it to the user.
    Also provides the user with the option to write the data
    to the Google Sheet.
    """
    if len(generated_instance) == 9:
        # Unpacks the tuple into more manageable items
        features = [feature for feature in generated_instance]
        name = features[1]
        (law_tag, moral_tag) = features[0]
        age = features[2]
        race = features[3]
        gender = features[4]
        hair_color = features[5]
        rumors = features[6]
        disposition = features[7]
        disposition_text = features[8]
        generation_text = (
            f"\u001b[93mPerson Generated!\u001b[0m\n\n"
            f"Name: {name}\n"
            f"Alignment: {law_tag} {moral_tag}\u001b[0m\n"
            f"Age: {age}\n"
            f"Race:{race}\n"
            f"Gender: {gender}\u001b[0m\n"
            f"Hair Color: {hair_color}\n"
            f"Rumors: {rumors[0]}, {rumors[1]}\n"
            f"Disposition: {disposition} {disposition_text}\n"
        )
        print(generation_text)
        if cutie.prompt_yes_or_no("Save person to Google Sheet?"):
            save_list = [
                name,
                law_tag,
                moral_tag,
                age,
                race,
                gender,
                hair_color,
                rumors[0],
                rumors[1],
                disposition,
                disposition_text
            ]
            CHARACTERS_SHEET.append_row(save_list, table_range="A1:K1")
            print(Fore.GREEN + "Person saved to sheet!\n")
        fluff_generate_new()
    else:
        features = [feature for feature in generated_instance]
        if "Town" in features[0]:
            name = features[1]
            location_tag = features[0]
            age = features[2]
            rumors = features[3]
            leadership = features[4]
            disposition = features[5]
            disposition_text = features[6]
            generation_text = (
                f"\u001b[93m{location_tag} Generated!\u001b[0m\n\n"
                f"Name: {name}\n"
                f"Age: {age}\n"
                f"Rumors: {rumors[0]}, {rumors[1]}\n"
                f"Leadership: {leadership}\n"
                f"Disposition: {disposition} {disposition_text}\n"
            )
            print(generation_text)
            if cutie.prompt_yes_or_no("Save location to Google Sheet?"):
                save_list = [
                    location_tag,
                    name,
                    age,
                    rumors[0],
                    rumors[1],
                    leadership,
                    disposition,
                    disposition_text
                ]
                PLACES_SHEET.append_row(save_list, table_range="A1:H1")
                print(Fore.GREEN + "Place saved to sheet!\n")
            fluff_generate_new()
        else:
            name = features[1]
            location_tag = features[0]
            age = features[2]
            rumors = features[3]
            generation_text = (
                f"\u001b[93m{location_tag} Generated!\u001b[0m\n\n"
                f"Name: {name}\n"
                f"Discovered: {age} years ago\n"
                f"Rumors: {rumors[0]}, {rumors[1]}\n"
            )
            print(generation_text)
            if cutie.prompt_yes_or_no("Save location to Google Sheet?"):
                save_list = [
                    location_tag,
                    name,
                    age,
                    rumors[0],
                    rumors[1]
                ]
                PLACES_SHEET.append_row(save_list, table_range="A1:E1")
                print(Fore.GREEN + "Place saved to sheet!\n")
            fluff_generate_new()


def fluff_generate_new():
    """
    Asks the user if they wish to generate a new person or place,
    or takes them back to the main selection screen otherwise.
    """
    print(Fore.YELLOW + "What would you like to do next?\n")
    options = [
        Fore.BLUE + "Generate a new person or place",
        Fore.RED + "Go back to the function selection page"
    ]
    chosen_option = options[cutie.select(
        options,
        selected_index=1
        )]
    if "Generate" in chosen_option:
        fluff_selector()
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
        Fore.RED + "Viewing people or places generated using Fluff",
        Back.RED + "Go Back"
    ]
    chosen_instructions = instructions[cutie.select(instructions)]
    if "Diceroller" in chosen_instructions:
        instructions_diceroller()
    elif "Viewing" in chosen_instructions:
        instructions_viewer()
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
    generated instance by selecting "Yes" when prompted and hitting ENTER.
    If you do not wish to save the instance to the sheet you can select "No"
    and hit ENTER.
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
    elif "saving" in chosen_option:
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


def instructions_viewer():
    instructions_general = """
    VIEWING GENERATED PEOPLE OR PLACES

    After generating a few people or places, you can use the third option
    in the main menu to view the people or places generated. You can
    select whether to view people or places, which will provide a list of the
    generated options. Select which one you wish to view and it will provide
    details about that person or place. You can then go back to the previous
    menu to select another person or place, or go back to the main program
    menu.
    """
    clear()
    print(instructions_general)
    option = [Back.RED + "Go Back"]
    chosen_option = option[cutie.select(
        option,
        selected_index=0
    )]
    if "Back" in chosen_option:
        instructions_selection()


def view_instances_selector():
    """
    Asks the user if they wish to view generated people or places
    and directs them to the correct function for doing so.
    """
    clear()
    print("Would you like to view all people or places?\n")
    options = [
        Fore.GREEN + "People",
        Fore.RED + "Places",
        Back.RED + "Go Back"
    ]
    chosen_option = options[cutie.select(
        options,
        selected_index=0
    )]
    if "People" in chosen_option:
        view_instances_people()
    elif "Places" in chosen_option:
        view_instances_places()
    else:
        clear()
        main()


def view_instances_people():
    """
    Shows a formatted list of all of the generated people
    by name, and allows the user to select them to view each attribute.
    """
    clear()
    print("Loading People...")
    all_characters = CHARACTERS_SHEET.get_all_records()
    people = {data["name"]: Person(**data) for data in all_characters}
    people_list = list(people.keys()) + [Back.RED + "Go Back"]
    print("Which person would you like to view?\n")
    chosen_person = people_list[cutie.select(
        people_list,
        selected_index=0
        )]
    if "Go Back" in chosen_person:
        clear()
        main()
    else:
        display_selection = people[chosen_person]
    clear()
    print("\n\u001b[33mDetails:\n")
    for attr, value in vars(display_selection).items():
        print(f"{attr.capitalize()}: {value}")
    print("\n")
    option = [
        Back.RED + "Go Back"
    ]
    chosen_option = option[cutie.select(
        option,
        selected_index=0
    )]
    if "Back" in chosen_option:
        clear()
        view_instances_people()


def view_instances_places():
    """
    Shows a formatted list of all of the generated places
    by name, and allows the user to select them to view each attribute.
    """
    clear()
    print("Loading Places...")
    all_places = PLACES_SHEET.get_all_records()
    places = {data["name"]: Place(**data) for data in all_places}
    places_list = list(places.keys()) + [Back.RED + "Go Back"]
    print("Which place would you like to view?\n")
    chosen_place = places_list[cutie.select(
        places_list,
        selected_index=0
        )]
    if "Go Back" in chosen_place:
        clear()
        main()
    else:
        display_selection = places[chosen_place]
    clear()
    print("\n\u001b[33mDetails:\n")
    for attr, value in vars(display_selection).items():
        if value not in ("", None):
            print(f"{attr.capitalize()}: {value}")
    # Creates a whitespace for a cleaner format
    print("\n")
    option = [
        Back.RED + "Go Back"
    ]
    chosen_option = option[cutie.select(
        option,
        selected_index=0
    )]
    if "Back" in chosen_option:
        clear()
        view_instances_places()


def main():
    """Runs the main program function sequence."""
    chosen_function = introduction()
    function_selection(chosen_function)


if __name__ == '__main__':
    main()
