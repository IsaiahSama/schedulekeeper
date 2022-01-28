# Schedule Keeper

# About
ScheduleKeeper is a script created by Isaiah, which allows a user to track, and manage various schedules, with the help of some automation.

# Features
- Allows a user to create, Read, Update, Delete and Track a schedule.
- Allows users to create 3 different types of schedules, these being: Daily, Weekly and One-Time
- Allows user to create a timer, to time themselves for present events.

# Implementations
- Schedules will be stored in a JSON file for backwards compatibility with the previous version
- Users should also be allowed to use a valid JSON file to add a schedule, or to bring an old schedule to this new version

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
            }
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
            }
        }
    ],
    "ONE-TIME":[
        {
            "TIMES": {
                "Time in 24 hour format": "Event to do at time",
                "0000": "Other event"
            }
        }
    ],
    "TIMER": {
        "Duration_of_event_in_minutes": "name_of_event",
        "30": "game"
    }
}
```