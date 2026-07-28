# Meal Planner / Recipe Picker

A desktop meal-planning application with a graphical interface (PySide6), created for CS 361.

## Milestone 1 Features

* View saved meal ideas
* Add new meal ideas
* Assign saved meals to days of the week
* View and update a weekly meal plan
* Validate user input
* Confirm actions before saving or removing information
* Store meal information between program sessions

## Running the Program

Install the dependency (one time):

```bash
python -m pip install -r requirements.txt
```

Run:

```bash
python meal_planner.py
```

If the `python` command is unavailable, run the program using the full path to your Python executable.

## Data Storage

Meal ideas and weekly-plan information are stored locally in `meal_data.json`.

The program does not store passwords, API keys, or other private information.
