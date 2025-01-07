![DNDUtils Logo](/documentation/feature-images/dndutils-logo.png)

# DNDUtils - Utility tools for Dungeons and Dragons
DNDUtils is a simple python program with a few features designed to assist Dungeons and Dragons players with a few gameplay features. At time of release, the program currently has two features:

- DiceRoll: A random dice generator that allows for rolling a number of dice using the standard (x)d(y) format. (E.g. 1d6, 3d20) plus modifiers (4d5 + 2)
- Fluff: A generative tool that allows for the creation of NPCs (Non-player characters) and places using prepopulated lists.

## Reminders

- Your code must be placed in the `run.py` file
- Your dependencies must be placed in the `requirements.txt` file
- Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

---

Happy coding!
