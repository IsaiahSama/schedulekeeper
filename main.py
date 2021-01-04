# Program will accept a time table for different periods of times and then manage them
# Will include day-to-day tasks as well as weekly tasks
# WIll have full CRUD (Create Read Update Delete) Functionality

from os import system, path, mkdir, remove, rmdir, listdir
from time import sleep, ctime
from json import dump, load, JSONDecodeError

dict_of_days = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thur": "Thursday", "Fri": "Friday", "Sat": "Saturday", "Sun": "Sunday"}

def clrs():
    system("CLS")

def currentday():
    return dict_of_days[ctime().split(" ")[0]]

def verifyNumber(prompt, numrange=None):
    while True:
        print(prompt)
        response = input(": ")
        while not response.isnumeric():
            print(f"Unfortunately, {response} is not a valid number")
            clrs()
            print(prompt)
            response = input(": ")

        if numrange:
            if int(response) not in numrange:
                print(f"Your response is not in the range provided. Your response must be in the range {numrange}")
                continue
        break

    return int(response)

def verifyResponse(prompt):
    while True:
        print(prompt)
        response = input(": ")
        prompt = "Are you certain?\n1) Yes\n2) No"
        confirmation = verifyNumber(prompt, [1,2])
        sleep(1)
        if confirmation == 1: return response
        else: clrs()
    
class Main:
    def __init__(self):
        self.schedule = None
        print("Beginning")

    def setup(self):
        if not path.exists("C:\\ScheduleKeeper"): mkdir("C:\\ScheduleKeeper"); print("Created Main Directory")
        else: 
            print("Main directory already exists.")
            print("Searching for previous schedule...")
            if not path.exists("C:\\ScheduleKeeper\\schedule.json"): print("No previous schedule found")
            else:
                with open("C:\\ScheduleKeeper\\schedule.json") as f:
                    try:
                        self.schedule = load(f)
                    except JSONDecodeError:
                        print("There seems to have been an error with your schedule file.")
        sleep(2)
        clrs()


    def menu(self):
        print("What may I do for you today?\n\n")
        prompt = "1)Create A New Schedule\n\n2)View an Existing Schedule\n\n3)Update an Existing Schedule\n\n4)Delete an Existing Schedule\n\n5)Exit this program\n\n6)Uninstall this program"
        response = verifyNumber(prompt, [1,2,3,4,5,6])
        if response == 6:
            self.uninstall()
        if response == 5:
            self.close()
        if response == 4:
            self.delete()
        if response == 3:
            self.update()
        if response == 2:
            self.view()
        if response == 1:
            self.create()

    def create(self):
        print("Creating new schedule...")
        prompt = "What would you like to name this schedule?"
        name = verifyResponse(prompt)

    
    def view(self):
        if not self.schedule: print("You have no existing schedules to view."); return    


    def update(self):
        if not self.schedule: print("You have no existing schedules to update."); return


    def delete(self):
        if not self.schedule: print("You have no existing schedules to delete."); return    


    def close(self):
        print("See ya next time.")
        input("Press enter key...")
        raise SystemExit

    def uninstall(self):
        print("Beginning uninstall process.")
        try:

            rmdir("C:\\ScheduleKeeper")

        except OSError:
            print("Directory not empty... deleting inside files")
            files = listdir("C:\\ScheduleKeeper")

            for file in files:
                remove(f"C:\\ScheduleKeeper\\{file}")
                print(f"Deleted {file}.")

        if path.exists("main.py"):
            remove("main.py")

        else:
            remove("main.exe")
        print("Succesfully deleted everything relating to me. Tru goodbye")
        self.close()


main = Main()
main.setup()

while True:
    main.menu()
