from os import system, remove
from time import sleep, ctime
from json import dump, load, JSONDecodeError
from re import findall
from threading import Thread
from win10toast import ToastNotifier
import pyttsx3
import requests
from bs4 import BeautifulSoup

toaster = ToastNotifier()

# Dict of days
dict_of_days = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday", "Sat": "Saturday", "Sun": "Sunday"}

# Classes

class Utility:

    @staticmethod
    def version_update():
        version = "healplus"

        session = requests.request("GET", "https://isaiahsama.github.io/schedulekeeper/")
        soup = BeautifulSoup(session.text, "html.parser")
        next_version = soup.p.text

        if version != next_version:
            print("A new version is available, go to [https://github.com/IsaiahSama/schedulekeeper] to update. Press enter to proceed if you wish to continue with this version")
            input()

        else:
            print(f"No worries... your version of \"{version}\" is up to date.")

        sleep(2)


    # Functions
    # Function which clears the screen and sends a message
    @staticmethod
    def clrs(text="\n"):
        system("CLS")
        print(text)

    # Function which verifies that input is a number within a given range
    @staticmethod
    def verifyNumber(prompt, numrange):
        while True:
            print(prompt)
            response = input(": ")
            while not response.isnumeric():
                print(f"Unfortunately, {response} is not a valid number")
                Utility.clrs()
                print(prompt)
                response = input(": ")

            if int(response) not in numrange:
                print(f"Your response is not in the range provided. Your response must be in the range {numrange}")
                continue
            break

        return int(response)

    # Function which confirms a given input
    @staticmethod
    def verifyResponse(prompt):
        print(prompt)
        response = input(": ")
        prompt = "Are you certain?\n1) Yes\n2) No"
        confirmation = Utility.verifyNumber(prompt, [1,2])
        sleep(1)
        if confirmation == 1: return response
        else: return False

    # Function responsible for saving the scheduledict
    @staticmethod
    def save(mydict):
        with open("C:\\ScheduleKeeper\\schedule.json", "w") as f:
            dump(mydict, f, indent=4)

    # Function responsible for showing keys of a received dictionary
    @staticmethod
    def show_names(search, mydict):
        Utility.clrs(f"Showing all of the names of your {search} schedules")
        keys = [key for key in mydict.keys()]
        for position, schedulename in enumerate(mydict.keys()):
            print(f"{position}) {schedulename}\n")
        return keys

    # Function then sends data to notepad
    @staticmethod
    def show_data(name, mydict):
        with open(f"{name}.json", "w") as f:
            dump(mydict, f, indent=4)

        print("Opening data in your notepad. Return to me and press enter to proceed")
        system(f"notepad.exe {name}.json")
        input(": ")
        try:
            remove(f"{name}.json")
        except FileNotFoundError:
            print("It would seem as though you had already removed the file")
        sleep(2)
        Utility.clrs()


    # Function that gets requested dictionary entry
    @staticmethod
    def get_entry(keys, mydict, show=True):
        system("CLS")
        while True:
            system("CLS")
            Utility.show_names("aforementioned", mydict)
            print("\nEnter the name of the schedule you would like to view, or enter 0 to return to menu")
            answer = input(": ").capitalize()

            if answer == "0": print("Returning to main menu"); return None, None
            if answer not in keys: print("You don't seem to have a schedule with that name")
            else: 
                try:
                    _ = mydict[answer]
                    break
                except KeyError:
                    Utility.clrs(f"Something went wrong getting the schedule {answer}")
                    continue
        
        if show:
            Utility.clrs(f"Showing your schedule with the name {answer}")
            Utility.show_data(answer, mydict[answer])

        return answer, mydict[answer]


    # Function which returns the long version of the current day
    @staticmethod
    def currentday(): 
        return dict_of_days[ctime().split(" ")[0]]

    @staticmethod
    def currenttime():
        return findall(r"([0-2][0-9]:[0-5][0-9])", ctime())[0]

    @staticmethod
    def get_minutes(time=None):
        if not time:
            value = Utility.currenttime()
        else:
            value = time
        hours, minutes = int(value.split(":")[0]), int(value.split(":")[1])
        return (hours * 60) + minutes

    
    @staticmethod
    def send_notif(name, msg):
        engine = pyttsx3.init()

        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id) 
        count = 0
        while count < 5:
            try:
                toaster.show_toast(title=name, msg=msg, threaded=True, duration=5)
                engine.say(msg)
                engine.runAndWait()
                engine.stop()
                break
            except RuntimeError:
                sleep(5)
                Utility.send_notif(name, msg)
                count += 1

    
# Class handling creation of schedules
class Create:
    def __init__(self, name, mydict):
        self.name = name
        self.mydict = mydict
        sleep(1)

    # Function responsible for creating a new weekly schedule
    def create_weekly(self):
        dotw = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        Utility.clrs("Creating Weekly Schedule")
        self.mydict["WEEKLY"][self.name] = {}

        try:
            while True:
                Utility.clrs("Press ctrl + c when you are finished")
                print("\nWhat is the day for which you would like to create a schedule for?")
                day = input(": ").capitalize()
                if day not in dotw: print("That is not a valid day..."); sleep(2); system("CLS"); continue
                self.mydict["WEEKLY"][self.name][day] = {}
                self.set_times(self.mydict["WEEKLY"][self.name][day], day)

        except KeyboardInterrupt:
            for day in dotw:
                x = self.mydict["WEEKLY"][self.name].get(day, None)
                if not x: self.mydict["WEEKLY"][self.name][day] = {}
            print("Completed... Returning to main menu")


    # Function responsible for creating a daily schedule
    def create_daily(self):
        Utility.clrs("Creating Daily Schedule")
        print("Now, tell me the times and tasks you generally do in your day to day schedule")
        self.mydict["DAILY"][self.name] = {}
        new_dict = self.mydict["DAILY"][self.name]
        self.set_times(new_dict)

    def create_one_time(self):
        Utility.clrs("Creating one time schedule")
        self.mydict["ONE-TIME"][self.name] = {}
        print("Now, tell me the times and tasks you wish to do for this time only")
        self.set_times(self.mydict["ONE-TIME"][self.name])
        track_dict = {"MODE": "ONE-TIME", "NAME":self.name, "DICT":self.mydict["ONE-TIME"][self.name]}
        thread = Thread(target=Tracking.tracker, args=(track_dict, self.mydict, None, self.name), daemon=True)
        thread.start()
        tracking.append(track_dict)
        with open("C:\\ScheduleKeeper\\tracking.json", "w") as f:
            dump(tracking, f, indent=4)
        
    # Function resonsible for setting the times and tasks for a given input
    def set_times(self, mydict, day=Utility.currentday()):
        while True:
            Utility.clrs(f"{day}: Give me the time for the task in 24 hour format (02:00, 14:00) or a time range in the format 02:00 - 14:00")
            time = input(": ")
            time = findall(r"([0-2][0-9]:[0-5][0-9])", time)
            if not time: print("Invalid time was given."); sleep(2); continue
            for time_ in time:
                prompt = f"What task would you do at {time_}"
                task = Utility.verifyResponse(prompt)
                if not task: continue
                mydict[time_] = task
            prompt = "Would you like to set another task and time?\n\n1)Yes\n\n2)No"
            answer = Utility.verifyNumber(prompt, [1,2])
            if answer == 2: break

# Class responsible for Reading, Updating and Deleting

tracking = []

class RUD:
    "READ UPDATE AND DELETE!!!!! Staticly"

    # Function responsible for showing data
    @staticmethod
    def read(mode, myschedule):
        mydict = myschedule[mode.upper()]
        while True:
            Utility.clrs()
            names = Utility.show_names(mode, mydict)
            _, entry = Utility.get_entry(names, mydict)
            if not entry: print("Returning to main menu"); return

    # Function responsible for updating
    @staticmethod
    def update(mode, myschedule):
        mydict = myschedule[mode.upper()]
        while True:
            Utility.clrs()
            names = Utility.show_names(mode, mydict)
            name, entry = Utility.get_entry(names, mydict, False)
            if not entry: print("Returning to main menu"); sleep(1); return
            new_entry = RUD.read_edit(name, entry)
            if not new_entry: print("Aborted update"); sleep(2); continue
            myschedule[mode.upper()][name] = new_entry

    # Function responsible for opening a file, and allowing users to change information
    @staticmethod
    def read_edit(name, entry):
        print("Opening file now. Change the data as you see fit, save and then return to me and press enter.")
        with open(f"{name}.json", "w") as f:
            dump(entry, f, indent=4)

        sleep(1)
        system(f"{name}.json")
        input(": ")
        input("Again: ")
        
        try:
            with open(f"{name}.json") as f:
                try:
                    new_entry = load(f)
                except JSONDecodeError:
                    print("The file I received is invalid so the changes have not been saved")
                    sleep(2)
                    remove(f"{name}.json")
                    return None
        
        except FileNotFoundError:
            print("It would appear as though the file has gone missing... Please don't delete it next time")
            sleep(2)
            return None

        remove(f"{name}.json")
        print("Schedule updated successfully")
        return new_entry

    # Function responsible for deleting
    @staticmethod
    def delete(mode, myschedule, name=None):
        global tracking
        mydict = myschedule[mode.upper()]
        if mode == "ONE-TIME" and name:
            del(myschedule[mode][name])
        while True:
            Utility.clrs()
            names = Utility.show_names(mode, mydict)
            name, entry = Utility.get_entry(names, mydict)
            
            if not entry: del(entry); print("Returning to main menu"); sleep(1); return

            prompt = f"Are you sure you want to delete {name}\n1)Yes\n2)No"

            confirm = Utility.verifyNumber(prompt, [1,2])
            if confirm == 2: print("Cancelling"); sleep(2); continue

            print("Deleting")
            tracked = [mydict for mydict in tracking if mydict["NAME"] == name and mydict["MODE"] == mode]
            if tracked: 
                tracking.remove(tracked[0])
                with open("C:\\ScheduleKeeper\\tracking.json", "w") as f:
                    dump(tracking, f, indent=4)

            del(myschedule[mode.upper()][name])
            print("Deleted")
            sleep(1)   
        

# tracking_dict:
# [
#     {
#         mode: "WEEKLY"/"DAILY",
#         my_dict: {},
#         name: "NAME"
#     }
# ]


class Tracking:
    "Handling all the Tracking"

    def trackset(myschedule):
        global tracking
        with open("C:\\ScheduleKeeper\\tracking.json") as f:
            try:
                data = load(f)
                if not data: return
                for sched in data:
                    tracking.append(sched)
                print("Tracking has continued from last time")
            except JSONDecodeError:
                return

        names = [item["NAME"] for item in tracking]

        Utility.send_notif("Schedule Notification", f"Tracking {names}")

        sleep(0.5)

        for to_track in tracking:
            if to_track["MODE"] == "WEEKLY":
                to_track["DICT"] = myschedule["WEEKLY"][to_track["NAME"]][Utility.currentday()]
            thread = Thread(daemon=True, target=Tracking.tracker, args=(to_track, myschedule, True))
            thread.start()
            

    # Function responsible for tracking a task
    @staticmethod
    def track(mode, myschedule):
        global tracking
        mydict = myschedule[mode.upper()]
        Utility.clrs()
        names = Utility.show_names(mode, mydict)
        name, entry = Utility.get_entry(names, mydict, False)
        if not entry: print("Returning to main menu"); sleep(1); return 

        if mode == "WEEKLY":
            entry = entry[Utility.currentday()]

        print(f"I will now track your {mode} schedule {name}, If no longer using the program, feel free to minimize the window while I keep track")
        track_dict = {"MODE": mode, "NAME":name, "DICT":entry}
        thread = Thread(target=Tracking.tracker, args=(track_dict, myschedule), daemon=True)
        thread.start()
        tracking.append(track_dict)
        with open("C:\\ScheduleKeeper\\tracking.json", "w") as f:
            dump(tracking, f, indent=4)

        sleep(2)
        

    @staticmethod
    def tracker(track_dict, mydict, burst=False, name=None):
        global tracking
        sleep(2)
        
        if not burst:
            Utility.send_notif(f"Schedule of {track_dict['NAME']}",f"Tracking your {track_dict['MODE']} schedule of {track_dict['NAME']}")

        min_dict = {}
        min_list = []

        for k in track_dict["DICT"].keys():
            minutes = Utility.get_minutes(k)
            min_dict[minutes] = k
            min_list.append(minutes)

        if not min_list:
            Utility.send_notif("Schedule Notification", f"Sorry, could not start tracking the {track_dict['MODE']} {track_dict['NAME']} as you have no schedule for this day")
            return
        last = sorted(min_list)[-1]

        while track_dict in tracking:

            if Utility.get_minutes() >= last + 20:
                Utility.send_notif(f"Schedule of {track_dict['NAME']}",f"{track_dict['NAME']} is finished for today")
                if track_dict["MODE"] == "ONE-TIME":
                    sleep(10)
                    Utility.send_notif(f"Schedule of {track_dict['NAME']}","One time schedule has completed successfully... removing now")
                    Tracking.untrack(track_dict)

                if track_dict["MODE"] == "DAILY":
                    while Utility.get_minutes() != 0: sleep(40)
                    Utility.send_notif(f"Schedule of {track_dict['NAME']}", f"{track_dict['NAME']} has begun once again.")

                if track_dict["MODE"] == "WEEKLY":
                    new_dict = mydict["WEEKLY"][track_dict["NAME"]][Utility.currentday()]
                    if not new_dict: 
                        Utility.send_notif(f"Schedule of {track_dict['NAME']}","No schedule for today. Relaunch me when you have one again")
                        Tracking.untrack(track_dict)
                        break
                    
                    track_dict["DICT"] = new_dict
                    while Utility.get_minutes() != 0: sleep(40)
                    Utility.send_notif(f"Schedule of {track_dict['NAME']}", f"{track_dict['NAME']} has begun once again.")

          
            minutes = min_dict.get(Utility.get_minutes(), None)
            if not minutes: continue
            todo = track_dict["DICT"].get(minutes, None)
            if not todo: continue

            Utility.send_notif(f"Schedule of {track_dict['NAME']}", f"It's about time. {todo}")

            sleep(35)

        if track_dict["MODE"] == "ONE-TIME":
            RUD.delete("ONE-TIME", mydict, name)


    @staticmethod
    def untrack(to_remove=None):
        Utility.clrs()
        global tracking
        if not to_remove:
            if not tracking: print("No schedules are currently being tracked"); return
            prompt = "What type of schedule would you like to untrack?\n1)Daily\n2)Weekly\n3)One-Time\n4)Return to menu"

            answer = Utility.verifyNumber(prompt, [1,2,3])
            if answer == 1: mode = "DAILY"
            elif answer == 2: mode = "WEEKLY"
            elif answer == 3: mode = "ONE-TIME"
            else: print("Returning to main menu"); return

            names = [item["NAME"] for item in tracking if item["MODE"] == mode]
            print('\n'.join(names))

            print("Which schedule would you like to remove from tracking?")
            name = input(": ").capitalize()
            if name not in names: print(f"{name} is not being tracked..."); return

            to_remove = [schedule for schedule in tracking if schedule["MODE"] == mode and schedule["NAME"] == name]
            if not to_remove: print("Could not remove that schedule for some reason"); return
            to_remove = to_remove[0]

        tracking.remove(to_remove)
        
        Utility.send_notif("Schedule Notification",f"No longer tracking {to_remove['NAME']}")

        with open("C:\\ScheduleKeeper\\tracking.json", "w") as f:
            dump(tracking, f, indent=4)

    @staticmethod
    def view_tracked():
        Utility.clrs()
        global tracking
        if not tracking: print("Nothing is currently being tracked"); sleep(1); return

        print("Showing all schedules being tracked")
        print(tracking)
        print("Press enter to proceed")
        input(":")
