# Program will accept a time table for different periods of times and then manage them
# Will include day-to-day tasks as well as weekly tasks
# WIll have full CRUD (Create Read Update Delete) Functionality


# structure of dict:
# {
#     username :username,
#     Daily: {
#             schedulename: {
#                 times: task
#             }
#         },
#     Weekly: {
#         schedulename: {
#             day: {
#                 times: task
#                 }
#             }
#     }
# }

from mechanics import *

dict_of_days = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thur": "Thursday", "Fri": "Friday", "Sat": "Saturday", "Sun": "Sunday"}

# Function which returns the long version of the current day
def currentday(): 
    return dict_of_days[ctime().split(" ")[0]]

        
class Main:
    def __init__(self):
        self.schedule = None
        print("Beginning")

    # Function that handles the setting up of file and folder
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

        Utility.clrs("Finished Setup")
        Utility.clrs(f"Welcome {self.schedule['username']}")
        sleep(2)

    # Function that handles the main menu
    def menu(self):
        Utility.clrs(f"How May I help you today {self.schedule['username']}?\n\n")
        prompt = "1)Create A New Schedule\n\n2)View an Existing Schedule\n\n3)Update an Existing Schedule\n\n4)Delete an Existing Schedule\n\n5)Track a Schedule\n\n6)Exit this program\n\n7)Uninstall this program"
        response = Utility.verifyNumber(prompt, [1,2,3,4,5,6])

        if response == 7: self.uninstall()
        if response == 6: self.close()
        if response == 5: self.track()
        if response == 4: self.delete()
        if response == 3: self.update()
        if response == 2: self.view()
        if response == 1: self.create()

    # Function that handles creation of a new schedule
    def create(self):
        print("Creating new schedule...")
        prompt = "What would you like to name this schedule?"
        name = Utility.verifyResponse(prompt)
        print("Noted")
        while True:
            print("What would you like to do next")
            prompt = "\n1)Create day-to-day schedule\n\n2)Create weekly schedule\n\n3)Return to menu"
            answer = Utility.verifyNumber(prompt, [1,2,3])
            if answer == 3: return
            create = Create(name.capitalize(), self.schedule)
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
            read = Read(self.schedule)
            if response == 2: read.view_weekly()
            if response == 1: read.view_daily()


    # Function that handles updating an existing schedule
    def update(self):
        if not self.schedule: print("You have no existing schedules to update."); return
        
        while True:
            
            Utility.clrs("Would you like to update a daily or weekly schedule?")
            prompt = "\n1)Update Daily\n2)Update Weekly\n3)Return to menu"
            response = Utility.verifyNumber(prompt, [1,2,3])
            if response == 3: print("Returning to menu"); return 
            update = Update(self.schedule)
            if response == 2: update.update_weekly()
            if response == 1: update.update_daily()

    # Function that handles deleting an existing schedule
    def delete(self):
        if not self.schedule: print("You have no existing schedules to delete."); return
            
        while True:
            
            Utility.clrs("Would you like to delete a daily or weekly schedule?")
            prompt = "\n1)Delete Daily\n2)Delete Weekly\n3)Return to menu"
            response = Utility.verifyNumber(prompt, [1,2,3])
            if response == 3: print("Returning to menu"); return 
            delete = Delete(self.schedule)
            if response == 2: delete.delete_weekly()
            if response == 1: delete.delete_daily()

    # Function that handles deleting an existing Schedule
    def track(self):
        if not self.schedule: print("You have no existing schedules to track."); return    

    # Function that closes the program
    def close(self):
        print("See ya next time.")
        input("Press enter key...")
        raise SystemExit

    # Function that uninstalls the program
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

while True: main.menu() 
