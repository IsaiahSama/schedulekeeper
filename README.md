# Schedule Keeper

# About
ScheduleKeeper is a script created by Isaiah, which allows a user to track, and manage various schedules, with the help of some automation.

# Features
- Allows a user to create, Read, Update, and Delete a schedule.
- Allows users to create 3 different types of schedules, these being: Daily, Weekly and One-Time
- Automatically track the user's schedules
- Will speak and display a notification for schedules when their time arrives
- Allows user to create a timer, to time themselves for present events.

# Implementations
- Schedules will be stored in a JSON file for backwards compatibility with the previous version
- This JSON file will be stored in the current directory. Please do not manually edit this file unless you know what you are doing, or you risk losing your schedules for ever.
- Users should also be allowed to use a valid JSON file to add a schedule, or to bring an old schedule to this new version
- Users are allowed to tweak the config.yaml file to have their own settings

## Schedules
Schedules will be stored in the following format:

```json
{
    "DAILY": [
        {
            "SCHEDULE_NAME": "Daily_schedule_1",
            "TIMES": {
                "Time in 24 hour format": "Event to do at time",
                "1400": "Task number 2"
            },
            "TRACKING": "bool (True or False)",
            "ONE-TIME": "bool (True or False)"
        }
    ],
    "WEEKLY": [
        {
            "SCHEDULE_NAME": "Weekly_schedule_1",
            "DAYS": {
                "DAY_OF_THE_WEEK": {
                    "Time in 24 hour format": "Event to do at time"
                },
                "TUESDAY": {
                    "1200": "Sleep"
                }
            },
            "TRACKING": "bool (True or False)" 
        }
    ],
    "TIMER": [
        {
            "name_of_timer": "timer name"
            "Duration_of_timer_in_minutes": 20,
            "TRACKING": "True or false (bool)"
        },
        {
            "name_of_timer": "time to sleep",
            "duration": 30,
            "TRACKING": false
        }
    ]
}
```