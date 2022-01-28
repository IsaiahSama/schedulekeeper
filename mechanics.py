# This is the file that contains all of the mechanics used for the schedule keeper

# Imports
from pyttsx3 import init
from plyer import notification
from bs4 import BeautifulSoup
from requests import get

class Utilities:
    """A class which contains utility methods or often repeated code.
    
    Attributes:
        pass
    
    Methods:
        setup() - This will setup the schedules and everything for the user
    """

    def setup(self):
        """Sets up the program to be used by the user"""

        # Determine whether the user is a first timer or not
        