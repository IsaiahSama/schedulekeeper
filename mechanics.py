# This is the file that contains all of the mechanics used for the schedule keeper

# Imports
from os import system
from os.path import exists
from pyttsx3 import init
from plyer import notification
from bs4 import BeautifulSoup
from requests import get
from config import config

class Utilities:
    """A class which contains utility methods or often repeated code.
    
    Attributes:
        pass
    
    Methods:
        clrs(msg:str="") - Clears the screen and then displays a message
    """

    def clrs(self, msg:str=""):
        """Method used to display a message after clearing the screen of all current text
        
        Args:
            msg (str): The message to be displayed after clearing the screen. Defaults to empty string
            
        """
        
        system("CLS")
        print(msg)

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
