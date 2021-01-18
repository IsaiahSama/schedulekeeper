from os import system, path, mkdir, remove, rmdir, listdir
from time import sleep, ctime
from json import dump, load, JSONDecodeError
from re import findall
from threading import Thread
from win10toast import ToastNotifier


# Dict of days
dict_of_days = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday", "Sat": "Saturday", "Sun": "Sunday"}


# Classes

class Utility:

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
        system(f"{name}.json")
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
        for day in dotw:
            self.mydict["WEEKLY"][self.name][day] = {}
            prompt = f"Would you like to create a schedule for {day}?\n\n1)Yes\n\n2)No\n\n3)Return to menu"
            answer = Utility.verifyNumber(prompt, [1,2,3])
            if answer == 3: return True
            if answer == 2: continue
            x = self.mydict["WEEKLY"][self.name][day]
            if answer == 1: self.set_times(x)

    # Function responsible for creating a daily schedule
    def create_daily(self):
        Utility.clrs("Creating Daily Schedule")
        print("Now, tell me the times and tasks you generally do in your day to day schedule")
        self.mydict["DAILY"][self.name] = {}
        x = self.mydict["DAILY"][self.name]
        self.set_times(x)
        
    # Function resonsible for setting the times and tasks for a given input
    def set_times(self, mydict):
        while True:
            Utility.clrs("Give me the time for the task in 24 hour format (02:00, 14:00)")
            time = input(": ")
            time = findall(r"([0-2][0-9]:[0-5][0-9])", time)
            if not time: print("Invalid time."); sleep(2); continue
            prompt = f"What task would you do at {time}"
            task = Utility.verifyResponse(prompt)
            if not task: continue
            mydict[time[0]] = task
            prompt = "Would you like to set another task and time?\n\n1)Yes\n\n2)No"
            answer = Utility.verifyNumber(prompt, [1,2])
            if answer == 2: break

# Class responsible for Reading, Updating and Deleting

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
    def delete(mode, myschedule):
        mydict = myschedule[mode.upper()]
        while True:
            Utility.clrs()
            names = Utility.show_names(mode, mydict)
            name, entry = Utility.get_entry(names, mydict)
            
            if not entry: print("Returning to main menu"); sleep(1); return

            prompt = f"Are you sure you want to delete {name}\n1)Yes\n2)No"

            confirm = Utility.verifyNumber(prompt, [1,2])
            if confirm == 2: print("Cancelling"); sleep(2); continue

            print("Deleting")
            del(myschedule[mode.upper()][name])
            print("Deleted")
            sleep(1)   

    # Function responsible for tracking a task
    @staticmethod
    def track(mode, myschedule):
        mydict = myschedule[mode.upper()]
        Utility.clrs()
        names = Utility.show_names(mode, mydict)
        name, entry = Utility.get_entry(names, mydict, False)
        if not entry: print("Returning to main menu"); sleep(1); return 
        if mode == "weekly":
            entry = entry[Utility.currentday()]
        print(f"I will now track your {mode} schedule {name}, If no longer using the program, feel free to minimize the window while I keep track")
        thread = Thread(target=RUD.tracker, args=(name, mode, entry), daemon=True)
        thread.start()
        sleep(2)
        

    @staticmethod
    def tracker(name, mode, mydict):
        sleep(2)
        min_dict = {}
        min_list = []
        toaster = ToastNotifier()

        toaster.show_toast(title="Schedule Notification", msg=f"Tracking your {mode} schedule of {name}", threaded=True, duration=10)
        while toaster.notification_active():sleep(0.1)
        for k in mydict.keys():
            minutes = Utility.get_minutes(k)
            min_dict[minutes] = k
            min_list.append(minutes)

        terminator = sorted(min_list)[-1]

        while Utility.get_minutes() != (terminator + 20):

            try:
                todo = mydict[min_dict[Utility.get_minutes()]]
            except KeyError:
                continue

            toaster.show_toast(title="Schedule Notification", msg=f"It's about time. {todo}", threaded=True, duration=20)
            while toaster.notification_active():sleep(0.1)

            sleep(40)


        toaster.show_toast(title="Schedule Notification", msg=f"Tracking for {name} has been completed succesfully...", threaded=True, duration=10)
        while toaster.notification_active():sleep(0.1)
        sleep(2)
        
