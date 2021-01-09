from os import system, path, mkdir, remove, rmdir, listdir
from time import sleep, ctime
from json import dump, load, JSONDecodeError
from re import findall


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
        while True:
            print(prompt)
            response = input(": ")
            prompt = "Are you certain?\n1) Yes\n2) No"
            confirmation = Utility.verifyNumber(prompt, [1,2])
            sleep(1)
            if confirmation == 1: return response
            else: Utility.clrs()

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
        sleep(2)
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
    def get_entry(keys, mydict, edit=False):
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
        
        if not edit:
            Utility.clrs(f"Showing your schedule with the name {answer}")
            Utility.show_data(answer, mydict[answer])

        return answer, mydict[answer]

    

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
            time = findall(r"([0-9][0-9]:[0-9][0-9])", time)
            if not time: print("Invalid time."); sleep(2); continue
            prompt = f"What task would you do at {time}"
            task = Utility.verifyResponse(prompt)
            mydict[time[0]] = task
            prompt = "Would you like to set another task and time?\n\n1)Yes\n\n2)No"
            answer = Utility.verifyNumber(prompt, [1,2])
            if answer == 2: break
        Utility.save(self.mydict)

# Class responsible for the reading of a schedule
class Read:
    def __init__(self, schedule):
        self.schedule = schedule

    # Function responsible for viewing a weekly schedule
    def view_weekly(self):
        mydict = self.schedule["WEEKLY"]
        self.read("weekly", mydict)


    # Function responsible for viewing a daily schedule
    def view_daily(self):
        mydict = self.schedule["DAILY"]
        self.read("daily", mydict)
 

    # Function responsible for showing data
    def read(self, mode, mydict):
        while True:
            Utility.clrs()
            names = Utility.show_names(mode, mydict)
            _, entry = Utility.get_entry(names, mydict)
            if not entry: print("Returning to main menu"); return


# CLass responsible for handling all update methods
class Update:
    def __init__(self, schedule):
        self.schedule = schedule

    # Function for updating a daily schedule
    def update_daily(self):
        daily_dict = self.schedule["DAILY"]
        self.update("weekly", daily_dict)


    # Function for updating a weekly schedule
    def update_weekly(self):
        weekly_dict = self.schedule["WEEKLY"]
        self.update("weekly", weekly_dict)
            

    # Function responsible for updating
    def update(self, mode, mydict):
        while True:
            Utility.clrs()
            if not mydict: print(f"You do not have any {mode} schedules"); return
            names = Utility.show_names(f"{mode}", mydict)
            name, entry = Utility.get_entry(names, mydict, True)
            if not entry: print("Returning to main menu"); sleep(1); return
            new_entry = self.read_edit(name, entry)
            if not new_entry: print("Aborted update"); sleep(2); continue

            entry = new_entry

            Utility.save(self.schedule)

    # Function responsible for opening a file, and allowing users to change information
    def read_edit(self, name, entry):
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

class Delete:
    def __init__(self, schedule):
        self.schedule = schedule

    # Function responsible for deleting daily
    def delete_daily(self):
        mydict = self.schedule["DAILY"]
        self.delete("daily", mydict)

    # Function responsible for deleting weekly
    def delete_weekly(self):
        mydict = self.schedule["WEEKLY"]
        self.delete("weekly", mydict)    

    # Function responsible for deleting
    def delete(self, mode, mydict):
        while True:
            Utility.clrs()
            if not mydict: print("You do not have any weekly schedules"); return
            names = Utility.show_names("weekly", mydict)
            name, entry = Utility.get_entry(names, mydict, True)
            
            if not entry: print("Returning to main menu"); sleep(1); return

            prompt = f"Are you sure you want to delete {name}"

            confirm = Utility.verifyResponse(prompt)
            if not confirm: print("Cancelling"); sleep(2); continue

            print("Deleting")
            del(entry)
            print("Deleted")
            Utility.save(self.schedule)
            sleep(1)   
