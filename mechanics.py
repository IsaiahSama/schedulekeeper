# This is the file that contains all of the mechanics used for the schedule keeper

# Imports
from os import system
from os.path import exists
from pyttsx3 import init
from plyer import notification
from bs4 import BeautifulSoup
from requests import get
from config import config
from time import sleep

class Utilities:
    """A class which contains utility methods or often repeated code.
    
    Attributes:
        pass
    
    Methods:
        clrs(msg:str="") - Clears the screen and then displays a message
        version_check() - Checks the current version of the program, to make sure that it is up_to_date
        exit() - Exits the program
    """

    def clrs(self, msg:str=""):
        """Method used to display a message after clearing the screen of all current text
        
        Args:
            msg (str): The message to be displayed after clearing the screen. Defaults to empty string
            
        """
        
        system("CLS")
        print(msg)

    def version_check(self):
        """Method that checks to see if the current version of the running program is the latest version"""

        url = "https://isaiahsama.github.io/schedulekeeper/"

        response = get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        if soup.p.text != config['constants']['version']:
            print("The current version of the program that you are using is not the latest one.\nVisit https://github.com/IsaiahSama/schedulekeeper to download the latest version")
            resp = input("Type 'UPDATE!' in all caps, to make the update now. Type anything else to continue using this version\n")
            if resp == "UPDATE!":
                # Automatically do the update here
                pass
        else:
            print("You are running the latest version of this program")
        
        sleep(2)

    def exit(self):
        """Function used to close the program"""

        utils.clrs(f"Looks like this is goodbye {config['constants']['username']}. Until next time!")
        raise SystemExit
    

class Schedules:
    """Class which will handle everything releated to the schedules
    
    Attributes:
        None
        
    Methods:
        create() - Used to create a new schedule
        view() - Used to view a created schedule
        update() - Used to update an existing schedule
        delete() - Used to remove a schedule from memory
    """

    def create(self):
        """Method used to create a new schedule, and save it."""

        raise AttributeError
    
    def view(self):
        """Method used to view created schedules."""

        raise AttributeError

    def update(self):
        """Method used to update existing schedules"""

        raise AttributeError
    
    def delete(self):
        """Method used to delete existing schedules"""

        raise AttributeError

utils = Utilities()
schedules = Schedules()
