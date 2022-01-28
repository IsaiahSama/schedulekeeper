# This is the main file which will contain the basics of the script.
# Imports
from mechanics import Utilities

# Todo: Basic Menu

class Main:
    """This is the main class for the program.
    
    Attributes:
        utils (Utilities): An instance of the Utilities class
    
    Methods:
        setup() - This will setup the schedules and everything for the user
    """

    utils = Utilities()

    def __init__(self):
        self.utils.setup()

