![DNDUtils Logo](/documentation/feature-images/dndutils-logo.png)

# DNDUtils - Utility tools for Dungeons and Dragons

![Mockup of Program deployed to Heroku](/documentation/feature-images/program-mockup.png)

## About
DNDUtils is a simple python program with a few features designed to assist Dungeons and Dragons players with a few gameplay features. At time of release, the program currently has two features:

- DiceRoll: A random dice generator that allows for rolling a number of dice using the standard (x)d(y) format. (E.g. 1d6, 3d20) plus modifiers (4d5 + 2)
- Fluff: A generative tool that allows for the creation of NPCs (Non-player characters) and places using prepopulated lists.
    - A sub-feature for viewing characters and places is also included within the CLI program. The saved characters and places are stored in a Google Sheet which is later accessed by the program.

The deployed version of the program can be accessed on Heroku [here.](https://dnd-utils-a6a188c54492.herokuapp.com/)

## How To Use
Standard navigation within the program is done with the up and down arrow keys and pressing enter to confirm a selection. You may be prompted to type in a number for rolling dice, or hitting Y or N and hitting enter to confirm a choice. 

Detailed instructions for each function's use can be found within the program's 'instructions' menu option.

## UI/UX Design

The wireframes for the program's design can be found [here.](/documentation/wireframes/dndutils-wireframes.pdf)

The user interface design for DNDUtils was designed to be inherently simple - CLI terminals
can be intimidating for the average user and python error handling requires an innate ability to predict what the user is thinking. As a result, I settled for using the [CUTIE](https://pypi.org/project/cutie/) library to allow user input in a way that was highly controlled. CUTIE allows the programmer to specify select ranges of inputs, prompt the user with yes/no options, and allow for multiple choice inputs, all with inbuilt data validation using optional parameters.

I also decided to add color to the terminal using [Colorama](https://pypi.org/project/colorama/) - this allowed me to break up the large amounts of white text, highlight key words in the generation process, and improve the general presentation of the program using ANSI color codes and pre-defined constants. The pre-defined constants also helped improve code readability where used, especially in option selections that used both Colorama and CUTIE.

I decided to keep the majority of the instructions and guidance for using the program in an "instructions" section, providing only minimal instructions on the main screen of the program, encouraging users to read the instructions before use. This will hopefully mean that users are well equipped to use the program before delving into any of the specifics.

The design of the program was created so that users:

- Could intuitively determine the layout of the program, and where they needed to go to use certain features.
- Could navigate in a way that was consistent, well labelled, and prevented poor inputs leading to exceptions.
- Was responsive in terms of how the program acted when the user provided inputs.
- Was clear and readable, with judicious employment of a screen clear function to ensure that the terminal did not get cluttered.

## Target Audience

The target audience for this program is:

- Dungeons and Dragons Players, looking for a simple utility to allow them to roll dice used in the game quickly and efficiently.
- Dungeons and Dragons Players, especially Dungeon Masters, who are looking for a way to quickly generate character and places for use within gameplay sessions.

## User Stories

*DND Players:*
- As a DnD Player, I want the program's functions to be immediately obvious and well described. This allows me to quickly understand the program's purpose.
- As a DnD Player, I want navigation throguh the program's functions to be simple and easy to control, so I can use it while in the middle of a game without worrying about trying to learn how to use the program.
- As a DnD player, I want the information to be provided in a clear and readable format, so I am not trying to scour command lines for specific information in the middle of a game.
- As a DnD player, I want to be able to see how the program reached its conclusions as a result of some of the functions (for example, I want to be able to see how the dice rolling function works to ensure that calculations are correct)
-As a DnD player, I want to be able to understand which inputs are required of me (for example, when rolling Dice or creating characters), and I want the program to tell me what I need to provide for an intended output. This avoids confusion when trying to use the program.

*DnD Dungeon Masters:*
- As a DnD Dungeon Master, I want to be able to create a variety of characters and places in a short timeframe, and store them for later use within my games.
- As a DnD Dungeon Master, I would like to be able to recall a list of stored instances after generation, and be able to view the individual attributes of characters and places within that list.

## Features

### Main Screen with Function Selection

### Selection Feature navigatable with arrow keys and Enter Key

### Colorful interfaces using the Colorama library

### Instruction Screen for ease-of-use

### DiceRoller - a dice rolling function with configurable sub-features

### Fluff - a content generation tool to allow for quick generation of people and places
#### Generation of People
#### Generation of Places
#### Storage of generated data

### Viewing data generated using Fluff

## Data Models
The program uses two main classes within the Fluff functions - these classes are called Person and Place. As their names describe, they are the class of objects that data for characters and places get converted into when recalled by the viewer function. 

These classes have slightly different attributes, with the Person class containing information about the character's name, alignment (moral and lawfulness), age, race, gender, hair color, and rumors about the character that may give hints to their motivations.

The Place class contains information such as the location type, name, age, leadership, and rumors. 

These classes are then called by the viewer function to provide an easy to format and reformat data viewing option for each instance of the classes. The class format also lends itself to the ability to add methods later on - for example, you could add methods to update attributes for both the Person and Place classes - updating the name of the location or person, or changing the rumors that are associated with them.

## Testing & Bugs

## Deployment
### Deployment to Heroku
This project was deployed to Heroku. The steps to deploy this are as follows:
- Fork or clone this repository directly on github, or using your IDE terminal with the following code: 
    - `git clone https://github.com/Morgana-S/dnd-utils.git`
- Create a new application on Heroku.
- Set the buildbacks to `Python` and `NodeJS`, in that order.
- Ensure the correct config vars are in place, regarding credentials for gspread and google oauth.
- Ensure the Heroku application is linked to the GitHub repository
- Click Deploy

### Local Deployment
The project can also be deployed locally, especially if your IDE has an inbuilt Python Debugging tool or terminal.
- To deploy the project locally, please enter the following into your IDE terminal:
    - `git clone https://github.com/Morgana-S/dnd-utils.git`

## Credits
### Tools, Libraries and APIs
- [Python](https://developer.mozilla.org/en-US/docs/Glossary/Python) - Program Structure and Content
- [os](https://docs.python.org/3/library/os.html) - Functionality for Terminal clearing for readability
- [random](https://docs.python.org/3/library/random.html) - Random number generation used to pull from lists of pregenerated content
- [Colorama](https://pypi.org/project/colorama/) - ANSI Color code integration into the terminal, as well as constants that allow for colored text
- [CUTIE](https://pypi.org/project/cutie/) - User input structure as well as inbuilt validation of user inputs
- [Gspread](https://pypi.org/project/gspread/) Google Spreadsheet API Integration for use in Python
- [Google Auth](https://pypi.org/project/google-auth/) - Server-to-Server authentication mechanisms for Google APIs
- [Google Sheets API](https://developers.google.com/sheets/api/guides/concepts) - API to modify and read spreadsheet data
- [Google Drive API](https://developers.google.com/drive/api/guides/about-sdk) - API to store and access google spreadsheets in my personal Google Drive Folders