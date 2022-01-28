# About

MyScheduleKeeper is a python programming developed to assist with creating, reading, updating and deleting schedules as the user sees fit.

## Setting up

Setting up is simple. First, go to the [Python website link here](https://www.python.org/ftp/python/3.8.7/python-3.8.7-amd64.exe) which will start your python download. When the installer begins, **tick the checkbox that says "Add to Path"**, and then press continue and go through the rest of the installer. 

After the installer is complete, you have now installed python and you are ready to run python programs. Return to this page and press the green button near the top that says Code, press it, and then press Download Zip. 

With the zip file downloaded, simply extract it using your method of choice, putting them in a folder of your choice (remember to keep all files in the same folder). 

Go to the folder where you have the files, and click the bar near the top of your file explorer, where your file path is shown (Something like "This PC > Desktop > MyFolder) as shown in this image ![](https://cdn.discordapp.com/attachments/783070812596731938/807350708667809813/unknown.png). When you click this bar, remove all the text, type cmd and press enter. This will open your command prompt. 

In your command prompt now, type "pip install -r requirements.txt". This will install the required packages. When that is completed, this program is now ready to use. 

From here just double click the main.py file to run it. Easy. I hope this comes in handy. If you have any queries or problems, feel free to email me at isaiahahmadsama@gmail.com with them. Enjoy.

## Side Note

If you get an error when trying to view or update files, fixing is easy. Open your text editor of choice and create a .json file. Afterwards go to the folder where you created the file and double click it. Select your text editor of choice when prompted, and make sure that "Use this to open this file always" checkbox is checked. Then you can try running view / update again.

## Another Side not

If you want to have notifications shown to you at all times, simply follow the instructions found [here](https://thegeekpage.com/enable-notifications-while-in-full-screen-mode-in-windows-10/)

## Creating

There are 2 schedule modes... Daily and Weekly. In both of these modes, the user is able to create a name for a unique schedule. 

### Daily

In this mode, user will be prompted to enter times in 24 hour format (02:30, 14:30), and then for the task for each entered time.

### Weekly

In this mode, user can enter the day of the week for which they wish to set a schedule for. After selecting a day, user will be prompted to enter time in 24 hour format (02:30, 14:30), then prompted to enter the task for that time. Afterwards, user can choose if they want to add a schedule for another day or not.


## Read

Allows you to view any schedule that you have previously created. Will open the schedule as a file in your default text editor for you to view. The file itself will then be deleted afterwards. 

## Update

Allows you to update a schedule that you have already created. This will open the schedule as a file in your default text editor for you to view, and make changes as you see fit. The file is a JSON file so JSON syntax will be needed. Very easy, just follow the format already laid out.

## Delete

Deletes a specified schedule.

## Track

A key factor in this program. Capable of tracking multiple schedules at once. When the time specified in the schedule has come, you will receive a notification stating the current task.

## End Note

I really hope that this program helps some of you out. Took a bit in order to get it done and I'm fairly happy with how it came out. I'm open to any suggestions.