import json
from pathlib import Path


DATA_FILE = Path("meal_data.json")

DAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def print_header(title):
    """Display a consistent heading for each screen."""
    print("\n" + "=" * 60)
    print(title.center(60))
    print("=" * 60)


def load_data():
    """Load saved meals and the weekly plan from the JSON file."""
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "meals": [],
            "weekly_plan": {day: None for day in DAYS},
        }


def save_data(data):
    """Save meal and weekly-plan information."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def pause():
    """Wait for the user before returning to another screen."""
    input("\nPress Enter to continue...")


def display_main_menu():
    """Show the main program menu."""
    print_header("MEAL PLANNER / RECIPE PICKER")

    print("Plan meals without starting from scratch every week.")
    print("Only the meal ideas entered into this program are stored.\n")

    print("1. View saved meals")
    print("2. Add a meal idea")
    print("3. Choose weekly meals")
    print("4. View weekly plan")
    print("5. Exit")


def view_saved_meals(data):
    """Temporary saved-meal display."""
    print_header("SAVED MEALS")

    print("Use this list to review meals before planning your week.\n")

    if not data["meals"]:
        print("No meals have been added yet.")
        print("Add your first meal from the main menu.")
        pause()
        return

    for index, meal in enumerate(data["meals"], start=1):
        print(f"{index}. {meal['name']}")
        print(f"   Category: {meal['category']}")

    pause()


def add_meal_idea(data):
    """Placeholder for the add-meal flow."""
    print_header("ADD MEAL IDEA")
    print("This feature will guide the user through adding a meal.")
    pause()


def choose_weekly_meals(data):
    """Placeholder for assigning meals to days."""
    print_header("CHOOSE WEEKLY MEALS")
    print("This feature will assign a saved meal to a day.")
    pause()


def view_weekly_plan(data):
    """Display the current weekly meal plan."""
    print_header("WEEKLY PLAN")

    print("Review your planned meals before grocery shopping.\n")

    for day in DAYS:
        meal = data["weekly_plan"].get(day)
        display_value = meal if meal else "- empty -"
        print(f"{day:<10}: {display_value}")

    pause()


def run_program():
    """Run the Meal Planner main loop."""
    data = load_data()

    while True:
        display_main_menu()
        choice = input("\nEnter a number from 1 to 5: ").strip()

        if choice == "1":
            view_saved_meals(data)
        elif choice == "2":
            add_meal_idea(data)
        elif choice == "3":
            choose_weekly_meals(data)
        elif choice == "4":
            view_weekly_plan(data)
        elif choice == "5":
            print_header("GOODBYE")
            print("Your meal ideas and weekly plan have been saved.")
            break
        else:
            print("\nPlease enter a number from 1 to 5.")
            print("Nothing was changed.")
            pause()


if __name__ == "__main__":
    run_program()