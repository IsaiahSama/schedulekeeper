# Program will accept a time table for different periods of times and then manage them
# Will include day-to-day tasks as well as weekly tasks
# WIll have full CRUD (Create Read Update Delete) Functionality
# structure of dict:
# {
#     username :username,
#     daily: {
#             schedulename: {
#                 times: task
#             }
#         },
#     weekly: {
#         schedulename: {
#             day: {
#                 times: task
#                 }
#             }
#     }
# }


from os import system, path, mkdir, remove, rmdir, listdir
from time import sleep, ctime
from json import dump, load, JSONDecodeError
from re import findall

dict_of_days = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thur": "Thursday", "Fri": "Friday", "Sat": "Saturday", "Sun": "Sunday"}

def clrs(text="\n"):
    system("CLS")
    print(text)

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

class Create:
    def __init__(self, name, mydict):
        self.name = name
        self.mydict = mydict
        sleep(1)

    def create_weekly(self):
        dotw = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        clrs("Creating Weekly Schedule")
        self.mydict['Weekly'][self.name] = {}
        for day in dotw:
            self.mydict['Weekly'][self.name][day] = {}
            prompt = f"Would you like to create a schedule for {day}?\n\n1)Yes\n\n2)No\n\n3)Return to menu"
            answer = verifyNumber(prompt, [1,2,3])
            if answer == 3: return True
            if answer == 2: continue
            x = self.mydict['Weekly'][self.name][day]
            if answer == 1: self.set_times(x)

    def create_daily(self):
        clrs("Creating Daily Schedule")
        print("Now, tell me the times and tasks you generally do in your day to day schedule")
        self.mydict['Daily'][self.name] = {}
        x = self.mydict['Daily'][self.name]
        self.set_times(x)
        

    def set_times(self, mydict):
        while True:
            clrs("Give me the time for the task in 24 hour format (02:00, 14:00)")
            time = input(": ")
            time = findall(r"([0-9][0-9]:[0-9][0-9])", time)
            if not time: print("Invalid time."); sleep(2); continue
            prompt = f"What task would you do at {time}"
            task = verifyResponse(prompt)
            mydict[time[0]] = task
            prompt = "Would you like to set another task and time?\n\n1)Yes\n\n2)No"
            answer = verifyNumber(prompt, [1,2])
            if answer == 2: break

class Main:
    def __init__(self):
        self.schedule = None
        print("Beginning")

    def setup(self):
        if not path.exists("C:\\ScheduleKeeper"): mkdir("C:\\ScheduleKeeper"); print("Created Main Directory"); print("What is your name"); name = input(": "); print("Noted"); self.schedule["username"] = name
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
                        return

        clrs("Finished Setup")
        clrs(f"Welcome {self.schedule['username']}")
        sleep(2)

    def menu(self):
        clrs(f"How May I help you today {self.schedule['username']}?\n\n")
        prompt = "1)Create A New Schedule\n\n2)View an Existing Schedule\n\n3)Update an Existing Schedule\n\n4)Delete an Existing Schedule\n\n5)Exit this program\n\n6)Uninstall this program"
        response = verifyNumber(prompt, [1,2,3,4,5,6])
        if response == 6: self.uninstall()
        if response == 5: self.close()
        if response == 4: self.delete()
        if response == 3: self.update()
        if response == 2: self.view()
        if response == 1: self.create()

    def create(self):
        print("Creating new schedule...")
        prompt = "What would you like to name this schedule?"
        name = verifyResponse(prompt)
        print("Noted")
        while True:
            print("What would you like to do next")
            prompt = "\n1)Create day-to-day schedule\n\n2)Create weekly schedule\n\n3)Return to menu"
            answer = verifyNumber(prompt, [1,2,3])
            if answer == 3: return
            create = Create(name, self.schedule)
            if answer == 2: create.create_weekly()
            if answer == 1: create.create_daily()


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

        remove(__file__)

        print("Succesfully deleted everything relating to me. Tru goodbye")
        self.close()


main = Main()
main.setup()

while True:
    main.menu()
