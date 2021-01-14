# About

MyScheduleKeeper is a python programming developed to assist with creating, reading, updating and deleting schedules as the user sees fit.

## Creating

There are 2 schedule modes... Daily and Weekly. In both of these modes, the user is able to create a name for a unique schedule. 

### Daily

In this mode, user will be prompted to enter times in 24 hour format (02:30, 14:30), and then for the task for each entered time.

### Weekly

In this mode, each day of the week will be looped through, user will be prompted to enter times in 24 hour format (2:30, 14:30), then the task for the entered time for the day specified.

## Read

Allows you to view any schedule that you have previously created. Will open the schedule as a file in your default text editor for you to view. The file itself will then be deleted afterwards. 

## Update

Allows you to update a schedule that you have already created. This will open the schedule as a file in your default text editor for you to view, and make changes as you see fit. The file is a JSON file so JSON syntax will be needed. Very easy, just follow the format already laid out.

## Delete

Deletes a specified schedule.

## Track

A key factor in this program. Capable of tracking multiple schedules at once. When the time specified in the schedule has come, for now, will open your default text editor making it the primary focus which will contain the current time along with the task you have to do. Tracking runs until 20 minutes after the last task for the day at which point all created files will be removed.