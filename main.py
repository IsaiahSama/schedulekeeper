# This is the main file which will contain the basics of the script.
# Imports
from mechanics import schedules, utils, config, sleep
from pyinputplus import inputMenu

# Todo: Basic Menu

class Main:
    """This is the main class for the program.
    
    Attributes:
        menu_options (dict): A dictionary containing items that represent the main menu.
    
    Methods:
        main() - The main method of the entire program
        menu() - Provides the main menu for the user
    """

    menu_options = {
        "Create a schedule": schedules.create,
        "Update a schedule": schedules.update,
        "View a schedule": schedules.view,
        "Delete a schedule": schedules.delete,
        "Exit the program": utils.exit
    }

    def main(self):
        """The main method of the entire program."""

        # Ensure that the current version of the program is up to date
        utils.version_check()

        # Infinite loop to run the main menu

        while True:
            utils.clrs(f"Welcome {config['constants']['username']}")
            self.menu()

    def menu(self):
        """Provides the menu for the user."""

        print("How may I be of service to you?")
        response = inputMenu(choices=list(self.menu_options.keys()), prompt="Simply select from the following options\n", numbered=True)
        try:
            self.menu_options[response]()
        except KeyError:
            print("An invalid response was provided")
        except AttributeError:
            print("The task that you have attempted to use, does not yet exist or is a work in progress")
        
        input("Press enter to continue")

main = Main()
main.main()
