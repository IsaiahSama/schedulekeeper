# Program will accept a time table for different periods of times and then manage them
# Will include day-to-day tasks as well as weekly tasks
# WIll have full CRUD (Create Read Update Delete) Functionality


# structure of dict:
# {
#     username :username,
#     schedules: {
#         Daily: {
#                 schedulename: {
#                     times: task
#                 }
#             },
#         Weekly: {
#             schedulename: {
#                 day: {
#                     times: task
#                     }
#                 }
#         }
#     }
# }

from mechanics import *
from os import listdir, path, mkdir, rmdir


class Main:
    def __init__(self):
        self.mydict = {}
        print("Beginning")

    schedule = None

    # Function that handles the setting up of file and folder
    def setup(self):
        if not path.exists("C:\\ScheduleKeeper"): 
            mkdir("C:\\ScheduleKeeper")
            print("Created Main Directory")
            print("What is your name")
            name = input(": ")
            print("Noted")
            self.mydict["USERNAME"] = name
            self.mydict["SCHEDULES"] = {}
            self.schedule = self.mydict["SCHEDULES"]
            self.schedule["DAILY"] = {}
            self.schedule["WEEKLY"] = {}
            self.schedule["ONE-TIME"] = {}
        else: 
            print("Main directory already exists.")
            print("Searching for previous schedule...")

            if not path.exists("C:\\ScheduleKeeper\\schedule.json"): 
                print("No previous schedule found")
                self.uninstall(False)
            else:
                with open("C:\\ScheduleKeeper\\schedule.json") as f:
                    try:
                        self.mydict = load(f)
                        self.schedule = self.mydict["SCHEDULES"]
                    except JSONDecodeError:
                        print("There seems to have been an error with your schedule file.")
                        return

        check = self.schedule.get("ONE-TIME", None)
        if not check:
            self.schedule["ONE-TIME"] = {}
        Utility.clrs("Finished Setup")
        Utility.clrs(f"Welcome {self.mydict['USERNAME']}")

        if path.exists("C:\\ScheduleKeeper\\tracking.json"):
            Tracking.trackset(self.schedule)
 

    # Function that handles the main menu
    def menu(self):
        sleep(2)
        Utility.clrs(f"How May I help you today {self.mydict['USERNAME']}?\n\n")
        print("When in a menu, press ctrl + c at any time to return here.")
        prompt = "1)Create A New Schedule\n\n2)View an Existing Schedule\n\n3)Update an Existing Schedule\n\n4)Delete an Existing Schedule\n\n5)Track a Schedule\n\n6)Untrack a Schedule\n\n7)View Schedules Being Tracked\n\n8)Exit this program\n\n9)Uninstall this program"
        print(f"Today is {ctime()}\n")
        
        response = Utility.verifyNumber(prompt, [1,2,3,4,5,6,7,8,9])
        try:
            if response == 9: self.uninstall()
            elif response == 8: self.close()
            elif response == 7: Tracking.view_tracked()
            elif response == 6: Tracking.untrack()
            elif response == 5: self.track()
            elif response == 4: self.delete()
            elif response == 3: self.update()
            elif response == 2: self.view()
            else: self.create()
        except KeyboardInterrupt:
            print("Returning to main menu")
        
        Utility.save(self.mydict)


    # Function that handles creation of a new schedule
    def create(self):
        print("Creating new schedule...")
        prompt = "What would you like to name this schedule?"
        print("What should I call your schedule?")
        name = input(": ")
        name = name.replace(" ", "-")
        print("Noted")
        while True:
            system("CLS")
            print("What would you like to do next")
            prompt = "\n1)Create day-to-day schedule\n\n2)Create weekly schedule\n\n3)Create One-Time Schedule\n\n4)Return to menu"
            answer = Utility.verifyNumber(prompt, [1,2,3])
            if answer == 4: return
            create = Create(name.capitalize(), self.schedule)
            if answer == 3: create.create_one_time()
            if answer == 2: create.create_weekly()
            if answer == 1: create.create_daily()
        
    # Function that handles viewing an existing schedule
    def view(self):
        if not self.schedule: print("You have no existing schedules to view."); return

        while True:

            Utility.clrs("Would you like to view a daily or weekly schedule?")
            prompt = "\n1)View Daily\n2)View Weekly\n3)Return to menu"
            response = Utility.verifyNumber(prompt, [1,2,3])
            if response == 3: print("Returning to menu"); return
            if response == 2: RUD.read("WEEKLY", self.schedule)
            if response == 1: RUD.read("DAILY", self.schedule)

    # Function that handles updating an existing schedule
    def update(self):
        if not self.schedule: print("You have no existing schedules to update."); return

        while True:

            Utility.clrs("Would you like to update a daily or weekly schedule?")
            prompt = "\n1)Update Daily\n2)Update Weekly\n3)Return to menu"
            response = Utility.verifyNumber(prompt, [1,2,3])
            if response == 3: print("Returning to menu"); return
            if response == 2: RUD.update("WEEKLY", self.schedule)
            if response == 1: RUD.update("DAILY", self.schedule)


    # Function that handles deleting an existing schedule
    def delete(self):
        if not self.schedule: print("You have no existing schedules to delete."); return

        while True:

            Utility.clrs("Would you like to delete a daily or weekly schedule?")
            prompt = "\n1)Delete Daily\n2)Delete Weekly\n3)Return to menu"
            response = Utility.verifyNumber(prompt, [1,2,3])
            if response == 3: print("Returning to menu"); return
            if response == 2: RUD.delete("WEEKLY", self.schedule)
            if response == 1: RUD.delete("DAILY", self.schedule)

    # Function that handles deleting an existing Schedule
    def track(self):
        if not self.schedule: print("You have no existing schedules to track."); return   

        while True:

            Utility.clrs("Would you like to track a daily or weekly schedule?")
            prompt = "\n1)track Daily\n2)track Weekly\n3)Return to menu"
            response = Utility.verifyNumber(prompt, [1,2,3])
            if response == 3: print("Returning to menu"); return
            if response == 2: Tracking.track("WEEKLY", self.schedule)
            if response == 1: Tracking.track("DAILY", self.schedule)  

    # Function that closes the program
    def close(self):
        print("See ya next time.")
        input("Press enter key...")
        raise SystemExit

    # Function that uninstalls the program
    def uninstall(self, full=True):
        print("Beginning uninstall process.")
        if full:
            prompt = "Are you sure you want to uninstall?\n1)Yes\n2)No"
            answer = Utility.verifyNumber(prompt, [1,2])
            if answer == 2: print("Cancelling"); sleep(2); return

        try:

            rmdir("C:\\ScheduleKeeper")

        except OSError:
            print("Directory not empty... deleting inside files")
            files = listdir("C:\\ScheduleKeeper")

            for file in files:
                remove(f"C:\\ScheduleKeeper\\{file}")
                print(f"Deleted {file}.")

            rmdir("C:\\ScheduleKeeper")

        if full:
            remove(__file__)
            if path.exists("mechanics.py"): remove("mechanics.py")
            print("Succesfully deleted everything relating to me. Tru goodbye")
        

        self.close()



main = Main()
main.setup()

while True: main.menu() 
