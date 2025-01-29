# Testing, Bugs & Code Validation
## Manual Testing
Testing for the program has taken place in both the Heroku Terminal and on my local
machine using VS Code's debugger and terminal. 

The following tests were carried out:

## DiceRoller

| Test | Method | Desired Results | Actual Results
| --- | --- | --- | --- |
| Number of Dice - Input | Tested Dice rolls using invalid inputs, including asking for a negative number of dice, asking for a number of dice that vastly exceeds the allowed amount (9999), asking for 0 dice, asking for a float value of dice (3.52), asking for a string number of dice (using a random word) and asking for a random sample of dice within the input range. | DiceRoller should inform the user that any inputs outside of the range of 1-20 are unable to be processed, that the number provided must be an integer between 1-20. | DiceRoller performs as expected, limiting the user to inputs between 1-20 that are whole numbers. The function refuses inputs that are outside of this range.| 
|Number of Sides - Input | Testing Dice using above methods for number of dice - numbers outside of range 2-100, asking for 0 sided dice, asking for a float value for sides, a string value for sides, and a random sample of sides within the correct range. | As above, DiceRoller should refuse all inputs outside of the range of 2-100 and that aren't integers. | DiceRoller performs as expected, declining all inputs outside of the range and explaining how to provide a correct input. |
|Modifier - Input | Similar to the tests above, numbers were provided outside of the range expected (-10 to 10), floats were provided, strings were provided, and then 3 numbers within the expected range. | DiceRoller should cull any inputs that are outside of the expected range, similar to the behaviour above. | DiceRoller performs as expected.|
| Advantage Rolls - Input | Sample Dice with correct values were rolled with an Advantage, Disadvantage, and Normal Roll, using print() to confirm the advantage and disadvantage rolls were rolling twice and choosing the appropriate set of dice. | Advantage Rolls should always pick the highest sum of the two sets of dice, Disadvantage rolls should always pick the lower of the sum of two sets of dice, and Normal rolls should only roll one set of dice. | Confirmed that Advantage and Disadvantage calculations were being performed as expected, and Normal rolls were only providing one set of randomly generated numbers. | 
| Results Screen | A variety of valid rolls were rolled for each type, with the goal of confirming that the summary total + modifiers were correct and matched the individual dice lists. | Individual Dice should match up to the total, and the total + modifier should reflect the modifier chosen + total rolls of the individiual dice rolls. | Working as intended. |
| End program function - DiceRoller| Test that the prompt about rolling more dice works both ways - it allows the user to roll more dice if desired, or declines the user by using the main() function loop to go back to the program select screen. | DiceRoller should restart the dicerolling function if the user chooses to roll more dice, or take the user back to the program select screen by executing the main() function if the user declines to roll more dice. | Working as intended. |

## Fluff

| Test | Method | Desired Results | Actual Results | 
| --- | --- | --- | --- |
| Person or Place Selection - Input | Selecting a Person or Place to go to the appropriate tag selection. Choosing Go Back should instead take the user to the main program selection screen. | Selecting Person should take me to the Law and Alignment Tag selection - selecting place should take me to the location type selection. | Works as intended - However, Go Back does not clear the Terminal at time of testing. This has been corrected and detailed in the Bugs section. |
Tag Selection - Input | A combination of every possible tag type was selected for both people and place generation, ensuring that the generated content was aligning with the tags selected (e.g Chaotic Neutral people should always generate as Chaotic Neutral, and Dungeons should always generate as Dungeons) | Chosen Tags should be displayed correctly on the generation summary screen. | Mostly working as intended - selecting Neutral as the first tag changed to "True" even when not selecting Neutral/Neutral due to the condition order of the tag choice selection. Further Details provided in Bugs below. | 
| Generation - Correct Lists | Making sure that generated characteristics were being pulled from the correct lists within the Google Sheet - and that the full range was being chosen. Manually adjusted the selection tool to take ranges from the first, last and random choices from each category (race, first name, last name, hair color, rumors) and did the same for each of the appropriate place lists. Print statements used to check that the full range was being targeted. | Tool generates content using the full range of each list and pulls from each list appropriately - should not be pulling from same list twice and should not be pulling inappropriate lists (such as leadership for dungeons or POIs) | Works as intended - tool pulls only from appropriate lists and utilises the full range of each list to generate random content. |
| Generation - Correct Ranges | Similar to the above test for lists, any random numbers incorporated into generation (such as age and disposition) were generating in the correct ranges. Made sure that if the race was an elf, the age was multiplied by 10 to reflect the longevity elves experience. | Tool generates appropriate age and disposition ranges. | Working as intended - tool does not generate ages or dispositions outside of the expected range. The age for elves is multiplied by 10 as expected. | 
| Displaying Generated Content | The generated instance should have all of the appropriate characteristics - for people, this should include a name, alignment, age, race, gender, hair color, two rumors, a disposition, and appropriate text to describe the disposition. For places, this should include a location type, name, discovery date/age, rumors, and if the location type is a town, leadership and disposition information. Information that has ANSI color codes included should display the information as colored appropriately | All information is displayed correctly, ANSI color codes are also displaying correctly and the right kinds of information are provided. | Works as intended. | 
| Saving Generated Content | The user is prompted to save the generated content in the Google Sheet. If the user chooses yes, they should find a generated person under the 'characters' tab of the worksheet, and generated places under the 'places' tab. The user should then be prompted on whether to make a new character or place, or return to function selection. Users who decline to save the user should be prompted in the same way for creating new content or function selection. | People and places are saved to the correct tab in the sheet with all informaton preserved in a desired way. | Working as intended - currently, the ANSI color codes are saved as escape characters within the sheet as well. While this presents a problem if looking to copy the data directly out of the sheet (which I have detailed a workaround for in the Bugs section), this is actually useful as it means we can load the data with color codes in the instance viewer later. |
| Generating New Instances Prompt | The user is prompted at the end of the saving prompt to either create new characters/places or to go back to function selection. Both options were confirmed in testing. | Generating new characters should restart the fluff "people or place?" choice selection, and choosing not to generate new characters should take the user back to the function selection screen. | Working as intended. |

## View generated people/places
| Test | Method | Desired Results | Actual Results |
| --- | --- | --- | --- |
| Viewer Selection - Input | The options available to the user are to view people, places, or go back to function selection. Each one was selected in turn. | Selections should take the user to the people or places menu, and Go Back should take the user to the main function selection page. | Working as intended - noticed a feedback issue where if large numbers of people or places exist, the menu can take a few moments to load, which presents a UX problem. Details in Feedback below. Issue has been fixed by providing a print statement to assure the user that requested data is being loaded. | 
| Instance Loading | Selecting the desired type of instances to load, testing that the full list of instances of that type (people or places) is loaded and a menu is provided for the user to select from. | Results should load the full list of generated instances. | Working as intended - this can take a while depending on how large the list is, which can present a UX issue. Further details in Feedback section. | 
| Selecting an instance to view | Select a variety of instances, taking random samples from both the lists for people and places. | Information loaded when selected should match the character or place on the sheet, with characteristics such as age, name, leadership etc. matching up correctly. Color codes should carry across when appropriate (such as alignment or location type tags). | Working as intended. | 
Leaving an instance | Leaving a variety of instances should take the user back to the appropriate people/place list. | User can exit out of an instance and go back to the same list, with correct characteristics. | Working as intended - however, UX issue presents in that the list has to be loaded every time it is called at present. A more efficient way would be to store the data in memory rather than loading it every time. Detailed further in feedback below. | 

## Instructions 
| Test | Method | Desired Results | Actual Results | 
| --- | --- | --- | --- |
| Input Selection | The full variety of selections were made within the instructions screens, testing whether they provided correct information when navigated | Selections went to the appropriate part of the instructions. | Working as intended. |
| Information provided | Reading the information provided by each instruction for spelling mistakes, correct info. | Information provided should be correct for each section, have no spelling mistakes, and inform the user how to use that part of the program. | Working as intended. No spelling mistakes, informs the user appropriately on how to use the program. |

## Peer Reviewed Testing
- The application was tested in the deployed state by three different users on a variety of devices.
- Each user carried out the tests listed in the sections above. The users provided similar reports as above. Feedback and Bugs discovered are outlined in the sections below.

## Feedback
- Users reported that the function was simple to understand, even if they had little experience with Dungeons and Dragons. For users who had familiarity with Dungeons and Dragons, they could see how using such a tool would be useful for the functions outlined.
- Users commented that the UX design, with colors to break up the terminal, helped to make the program less intimidating to use to people without a technical background. Terminal programs can be intimidating to those who are unfamiliar with them, and using color in text to highlight key features and break up the text was helpful.
- Users reported that the instance viewer seemed slow - this is due to the data being loaded each time the user goes into the list for characters and places. In future, I would find a way to load that data into memory permanently so that it could be recalled later. 

## Bugs
- **Fluff -  Person or Place Selection. Going back does not clear the terminal and inhibits readability.**
    - Cause: The clear() function was not run before returning to the main program loop.
    - Fix: Added the clear() function to clear the terminal.

- **Fluff - Selecting Neutral for a person's caused the alignment to change to 'True' even when the moral alignment wasn't also Neutral.**
    - Cause: The logical operator check for law_tag AND moral_tag was not written correctly.
    - Fix: Change the logical operator check to be for moral_tag AND law_tag, so it checks the moral_tag first.

- **Fluff - Generating a person and saving them in the google sheet causes the ANSI color codes to save as escape characters.**
    - Cause: This is how the ANSI color codes are provided in text using constants such as Fore.RED. 
    - Fix: A plaintext version of the generated text could be created and that saved into the sheet - this was initially done before implementation of the instance viewer. However, as the color codes are desirable in the instance viewer, this was changed to later be a feature, with the main way of viewing instances to be done through the program itself rather than the Google Sheet.

## Code Validation
The code for the project was run through the CI Python Linter found [here.](https://pep8ci.herokuapp.com/)

No errors were found, as outlined in the screenshot below.
![PEP8 Linter Validation](/documentation/testing-images/pep8-validation.png)