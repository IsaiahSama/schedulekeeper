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

    def clrs(msg:str=""):
        """Method used to display a message after clearing the screen of all current text
        
        Args:
            msg (str): The message to be displayed after clearing the screen. Defaults to empty string
            
        """
        
        system("CLS")
        print(msg)
    

class Schedules:
    """Class which will handle everything releated to the schedules
    
    Attributes:
        None
        
    Methods:
        None
    """

utils = Utilities()
schedules = Schedules()
