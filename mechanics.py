# This is the file that contains all of the mechanics used for the schedule keeper

# Imports
from json import JSONDecodeError, dump, load
from msilib.schema import File
from os import system, get_terminal_size
from os.path import exists
from re import compile
from threading import Thread
from pyttsx3 import init
from plyer import notification
from bs4 import BeautifulSoup
from requests import get
from config import config
from time import sleep, ctime
from pyinputplus import inputMenu, inputStr, inputNum, inputYesNo

class Utilities:
    """A class which contains utility methods or often repeated code.
    
    Attributes:
        days_of_the_week (list): A list of the days of the week
        schedule_types (list): A list of the valid schedule types
        time_pattern (str): The pattern used to select the current time 
        notification_list (list): A list of strings, pending being notified
    
    Methods:
        clrs(msg:str="") - Clears the screen and then displays a message
        version_check() - Checks the current version of the program, to make sure that it is up_to_date
        prompt_for_time() - Prompts for the user to enter an appropiate time
        prompt_for_schedule_type() - Prompts the user for the type of schedule.
        get_schedule_by_name(name:str, schedules:list) - Gets a schedule from the list of schedules by name
        display_dict(schedule:dict) - Pretty formats a schedule for display
        get_current_day() - Gets the current day
        get_current_time() - Gets the current time
        get_schedule_list() - Used to get the list of schedule names.
        notify() - Uses text to speech and a notification to alert the user of a schedule 
        add_notif(title:str, msg:str) - Adds a tuple to the notification list to be queued for notification
        exit() - Exits the program
    """

    days_of_the_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    schedule_types = ["ONE-TIME", "WEEKLY", "DAILY", "TIMER"]
    time_pattern = compile(r"[0-2][0-9]:[0-5][0-9]")
    notification_list = []

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

    def prompt_for_time(self) -> tuple[int, int]:
        """Prompts for the user to enter a valid time in 24 hour format
        
        Returns:
            tuple[int, int]"""

        print("Enter the time in 24 hour format (Example: 200 for 2 am and 1400 for 2pm) that the event should start.")
        start_time = inputNum(min=0, max=2400)
        end_time = inputNum(prompt="Now what time should this event finish?\n", min=0, max=2400)

        return (start_time, end_time)

    def prompt_for_schedule_type(self) -> str:
        """Prompts the user to enter a valid schedule type
        
        Returns:
            str"""

        print("What type of schedules would you like to view?")
        return inputMenu(choices=self.schedule_types)

    def get_schedule_by_name(self, name:str, schedules:list) -> dict:
        target = [schedule for schedule in schedules if schedule['SCHEDULE_NAME']  == name]
        return target[0]

    def display_dict(self, schedule:dict):
        """Method used to pretty format a schedule.
        
        Args:
            schedule (dict): The schedule to be displayed"""

        abs_width = get_terminal_size()[0]
        width = round(abs_width * 0.8)
        width_2 = width // 2
        
        """Rough Format:
            ==============================================================================
            |                               SCHEDULE_NAME                               |
            -----------------------------------------------------------------------------
            | DAY    |
            
            |                  TIME                  |                Event              |
            ------------------------------------------------------------------------------
            data in below rows
            ==============================================================================
        """
        bar = f'{"=" * width}'.center(abs_width)
        bar2 = f'{"-" * width}'.center(abs_width)
        name = f'{"|" + schedule["SCHEDULE_NAME"].center(width) + "|"}'.center(abs_width)
        headers = f"{'|' + 'TIME'.center(width_2 // 2) + '|' + 'EVENT'.center(width_2 + 10) + '|'}".center(abs_width)

        print(bar)
        print(name)
        print(bar2)
        print(headers)

        if "TIMES" in schedule:
            rows = []
            for time, event in schedule['TIMES'].items():
                rows.append(f"{'|' + time.center(round(width_2 // 2)) + '|' + event.center(width_2 + 10) + '|'}".center(abs_width))
            
            rows.sort(key=lambda x: int(x.split("|")[1]))
            [print(row) for row in rows]
        else:
            days = schedule["DAYS"].keys()
            for day in days:
                day_text = day.center(width // 3)
                rows = []
                for time, event in schedule["DAYS"][day].items():
                    rows.append(f"{'|' + time.center(round(width_2 // 2)) + '|' + event.center(width_2 + 10) + '|'}".center(abs_width))
                
                rows.sort(key=lambda x: int(x.split("|")[1]))
                print(day_text)
                [print(row) for row in rows]

        print(bar)

    def get_schedule_list(self) -> tuple[list, list]:
        """Method that prompts for input and returns the list of schedule names, and schedules
        
        Returns:
            tuple(schedule_names, schedules)"""

        target = utils.prompt_for_schedule_type()
        print("Checking...")
        schedule_list = schedules.schedule.get(target, None)
        if target == "ONE-TIME": 
            schedule_list = schedules.schedule.get("DAILY", [])
            schedule_list = [schedule for schedule in schedule_list if schedule['ONE-TIME'] == True]
        if not schedule_list:
            print("You have no schedules for this type")
            return False, False

        schedule_names = [name["SCHEDULE_NAME"] for name in schedule_list]
        if not schedule_names:
            print("You have no schedules for this type")
            return False, False

        return schedule_names, schedule_list

    def get_current_day(self) -> str:
        """Gets the current day"""

        return [day for day in self.days_of_the_week if day.lower().startswith(ctime().split(" ")[0].lower())][0]

    def get_current_time(self) -> str:
        """Gets the current time"""

        current_time = self.time_pattern.findall(ctime())[0]
        return int(''.join(current_time.split(":")))

    def notify(self):
        """Method used for notifying users of their schedules"""

        while True:
            while not self.notification_list: sleep(0.1)
            title, msg = self.notification_list.pop(0)
            notification.notify(title=title, app_name="ScheduleKeeper", message=msg, app_icon=config['variables']['app_icon'])

            engine = init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[config['variables']['voice']].id) 
            engine.say(msg)
            engine.runAndWait()
            engine.stop()

    def add_notif(self, title:str, msg:str):
        """Message used to add notifications to the notification Queue
        
        Args:
            title (str): The title of the notification
            msg (str): The message to be displayed"""
        
        self.notification_list.append((title, msg))


    def exit(self):
        """Function used to close the program"""

        utils.clrs(f"Looks like this is goodbye {config['variables']['username']}. Until next time!")
        raise SystemExit
    

class Schedules:
    """Class which will handle everything releated to the schedules
    
    Attributes:
        schedule (dict): Instance of the current schedule as retrieved from the JSON file
        tracking (list[dict]): A list of schedules that are to be tracked
        current_day (str): The Current Day
        
    Methods:
        create() - Used to create a new schedule
        create_daily() - Creates a new daily schedule.
        create_weekly() - Creates a new Weekly schedules.
        timer() - Creates a timer for a task.
        view() - Used to view a created schedule
        update() - Used to update an existing schedule
        delete() - Used to remove a schedule from memory
        save() - Saves the schedule to the JSON file
        load() - Used to load the schedule from the JSON file
        start_threads() - Begins all threads
        track() - Used to track schedules. Threaded
        track_current_day() - Used to track the current day
    """

    schedule = {}
    tracking = []
    current_day = ''

    def create(self):
        """Method used to create a new schedule, and save it."""

        # raise AttributeError

        choices = {"DAILY": self.create_daily, "WEEKLY": self.create_weekly, "ONE-TIME": self.create_daily}
        response = inputMenu(prompt="What type of schedule would you like to create?\n", choices=list(choices.keys()), numbered=True)

        name = inputStr(prompt="What should I name this schedule?\n")

        try:
            schedule = choices[response]()
        except KeyboardInterrupt:
            schedule = {}
        if not schedule:
            print("Abandoned. Returning to Main menu")
            return False
        
        schedule["SCHEDULE_NAME"] = name
        schedule["ONE-TIME"] = True if response == "ONE-TIME" else False
        if response == "WEEKLY": del schedule['ONE-TIME']
        schedule['TRACKING'] = True
        try:
            self.schedule[response]
        except KeyError:
            self.schedule[response] = []
        utils.display_dict(schedule)
        self.schedule[response].append(schedule)
        self.tracking.append(schedule)
        self.save()


    def create_daily(self) -> dict:
        """Method used to create a daily schedule for the user

        Returns:
            dict: The created schedule"""

        schedule = {}
        times = {}
        while True:
            try:
                print("Press ctrl + c when you are done")
                start_time, end_time = utils.prompt_for_time()
                event_name = inputStr(prompt="What are you planning on doing during this time?\n")
                
                times[str(start_time)] = event_name
                times[str(end_time)] = event_name + " end"
            except KeyboardInterrupt:
                print("If you would like to abort creating this schedule, press ctrl + c again. To continue, just press enter")
                input()
                break

        print("Finalizing")

        schedule["TIMES"] = times
        return schedule

    def create_weekly(self) -> dict:
        """Method used to create a weekly schedule for the user
        
        Returns:
            dict: The Created Schedule"""

        schedule = {
            "DAYS": {}
        }

        print("Press ctrl + c at any point to abort creating this schedule")
        while True:
            day = inputMenu(prompt="What day would you like to give me the schedule for?\n", choices=utils.days_of_the_week)
            
            schedule["DAYS"][day] = {}

            while True:
                start_time, end_time = utils.prompt_for_time()
                event = inputStr(prompt="What event would you like to do during this time?\n")
                schedule["DAYS"][day][str(start_time)] = event
                schedule['DAYS'][day][str(end_time)] = "end " + event
                
                resp = inputYesNo(prompt=f"Would you like to add another time for {day}\n")
                if resp == 'no': break
            resp = inputYesNo(prompt="Would you like to add a schedule for another day?\n")
            if resp == 'no':break 
        
        print("Finalizing.")

        return schedule
        

    def view(self):
        """Method used to view created schedules."""

        schedule_names, schedule_list = utils.get_schedule_list()
        if not (schedule_names and schedule_list):
            return False

        print("Would you like to view a specific schedule? Or all?")
        answer = inputMenu(choices=["specific", "all"])
        if answer == "all": [utils.display_dict(schedule) for schedule in schedule_list]
        else:
            print("Which schedule would you like to view?")
            name = inputMenu(choices=schedule_names, blank=True)
            if not name: print("No schedule name was selected"); return False
            utils.display_dict(utils.get_schedule_by_name(name, schedule_list))

    def update(self):
        """Method used to update existing schedules"""
        if not self.schedule:
            print("You have no schedules to update.")
            return False

        self.save()
        system(f"{config['constants']['filename']}")
        input("Press enter when you are done")

        data = {}

        try:
            with open(config['constants']['filename']) as file:
                data = load(file)

        except FileNotFoundError:
            print("YOU DELETED THE FILE? Let's assume that was an accident")
            self.save()
        except JSONDecodeError:
            print("You don't know JSON? Try to follow the format I have there please. Breaks otherwise")
            self.save()
        
        if data:
            print("Press enter to confirm these changes. Else, press ctrl + c")
            input()
            print("Alright... Just to make sure... type 'YES!' to confirm these changes")
            if input(":") != "YES!": print("Didn't think so. Next time maybe"); return False
            self.schedule = data 
            self.save()
    
    def delete(self):
        """Method used to delete existing schedules"""

        schedule_names, schedule_list = utils.get_schedule_list()
        if not schedule_names and schedule_list:
            return False

        todelete = inputMenu(choices=schedule_names, prompt="Which schedule would you like to delete?\n", blank=True)

        if not todelete:
            print("No deleting then. Returning to main menu")
            return False

        schedule = utils.get_schedule_by_name(todelete, schedule_list)
        utils.display_dict(schedule)
        print("Are you sure you want to delete this schedule?")
        resp = inputYesNo()
        if resp == "yes":
            print("Final chance. Press ctrl + c to abort.")
            print("To confirm, what is the type of schedule you want to delete?")
            target = utils.prompt_for_schedule_type()
            if not [sched for sched in self.schedule[target] if sched['SCHEDULE_NAME'] == todelete]:
                print("WRONG!")
                return False
            schedule_list.remove(schedule)
            self.schedule[target] = schedule_list
            self.save()
            print("Successfully deleted")            
        else:
            print("May have been for the best!")

    def timer(self):
        """Method used for setting timers."""

        print("What are you here for?")
        resp = inputMenu(choices=["Start a timer", "Set a timer", "Stop a timer"], numbered=True) 
        if resp.lower().startswith("set"):
            print("What is the duration of the timer (in minutes)? Cannot be more than 120.")
            duration = inputNum(min=0, max=120)
            event = inputStr(prompt="What is the name of the event to be ended after this duration?\n")
            timer = {"DURATION": duration, "TIMER_NAME": event, "TRACKING": False}
            self.schedule["TIMER"] = [] if not self.schedule.get("TIMER", None) else self.schedule["TIMER"]
            self.schedule["TIMER"].append(timer)
            self.save()
            print("Your timer has been set. You can start it from the Start a Timer option")

        elif resp.lower().startswith("stop"):
            print("Just close and re-launch this program!")
        else:
            if not self.schedule.get("TIMER", None):
                print("Could not find any timers to start")
                return False
            
            timer_names = [timer['TIMER_NAME'] for timer in self.schedule['TIMER']]
            print("Which timer would you like to start?")
            chosen_name = inputMenu(choices=timer_names, numbered=True, blank=True)
            if not chosen_name:
                print("Nothing was provided")
                return False
            chosen_one = [timer for timer in self.schedule['TIMER'] if timer['TIMER_NAME'] == chosen_name][0]
            chosen_one['TRACKING'] = True
            self.tracking.append(chosen_one)


    def save(self):
        """Saves the current schedule to the JSON file"""

        with open(config['constants']['filename'], "w") as file:
            dump(self.schedule, file, indent=4)

    def load(self):
        """Attempts to load the user's schedule from the JSON file"""

        data = None

        try:
            with open(config['constants']['filename']) as file:
                data = load(file)
        except JSONDecodeError as err:
            print("An error has occurred.", err)
            print("If you have made any changes to the file, please revert them.")
        except FileNotFoundError:
            print("Doesn't seem like you have any existing schedules.")
        if data:
            print("Successfully loaded your schedule into memory")
            self.schedule = data

    def start_threads(self):
        """Method used to start all threads that the script uses."""

        threads = [Thread(target=self.track, daemon=True), Thread(target=self.track_current_day, daemon=True), Thread(target=utils.notify, daemon=True)]
        [thread.start() for thread in threads]

    def track(self):
        """Threaded Function used to keep track of schedules"""

        tracked_daily = [schedule for schedule in self.schedule.get("DAILY", []) if schedule['TRACKING'] == True]
        tracked_weekly = [schedule for schedule in self.schedule.get("WEEKLY", []) if schedule["TRACKING"] == True]
        tracked_timer = [schedule for schedule in self.schedule.get("TIMER", []) if schedule["TRACKING"] == True]

        self.tracking.extend(tracked_daily + tracked_weekly + tracked_timer)

        print("Currently tracking: ", ', '.join([schedule['SCHEDULE_NAME'] for schedule in self.tracking]))

        while True:
            while not self.tracking: sleep(1)
            for schedule in self.tracking:
                for time, event in schedule.get("TIMES", {}).items() or schedule.get("DAYS", {}).get(self.current_day, {}).items():
                    if utils.get_current_time() == int(time):
                        # Do some code here to send a notification
                        utils.add_notif("Schedule", f"It's about time. Prepare to {event}")

                if schedule.get("TIMER_NAME"):
                    schedule['DURATION'] -= 0.5
                    if schedule['DURATION'] == 0:
                        # Do some code here to send a notification
                        utils.add_notif("Timer", f"The timer set for {event} is now over.")
            sleep(30)

    def track_current_day(self):
        while True:
            self.current_day = utils.get_current_day()
            sleep(60 * 60)


utils = Utilities()
schedules = Schedules()
