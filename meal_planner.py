import json
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QComboBox,
    QFormLayout,
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


DATA_FILE = Path(__file__).with_name("meal_data.json")

DAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

EMPTY_DAY_LABEL = "-- empty --"

CATEGORY_PALETTE = [
    "#7c5cff",
    "#2dd4bf",
    "#f5a623",
    "#ec4899",
    "#38bdf8",
    "#4ade80",
    "#fb7185",
]

STYLE_SHEET = """
QMainWindow {
    background-color: #101019;
}

QWidget {
    color: #e7e8ee;
    font-size: 13px;
}

QWidget#Page {
    background-color: #101019;
}

QWidget#Sidebar {
    background-color: #161722;
    border-right: 1px solid #24263a;
}

QLabel#AppTitle {
    font-size: 16px;
    font-weight: 700;
    color: #ffffff;
}

QLabel#AppSubtitle {
    color: #6f7286;
    font-size: 11px;
}

QLabel#AppTagline {
    color: #8b8ea3;
    font-size: 11px;
}

QPushButton#NavButton {
    background-color: transparent;
    color: #9a9db3;
    border: none;
    border-radius: 8px;
    padding: 10px 14px;
    text-align: left;
    font-weight: 600;
}

QPushButton#NavButton:hover {
    background-color: #1e2032;
}

QPushButton#NavButton:checked {
    background-color: #241f42;
    color: #b9aaff;
}

QLabel#Heading {
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
}

QLabel#SubText {
    color: #8b8ea3;
}

QFrame#Card {
    background-color: #181926;
    border: 1px solid #262838;
    border-radius: 14px;
}

QFrame#DayCard {
    background-color: #181926;
    border: 1px solid #262838;
    border-radius: 12px;
}

QLabel#DayName {
    font-weight: 700;
    color: #d5d7e6;
}

QSplitter::handle {
    background-color: transparent;
    width: 10px;
}

QListWidget {
    background-color: #181926;
    border: 1px solid #262838;
    border-radius: 14px;
    padding: 6px;
    outline: none;
}

QListWidget::item {
    border-radius: 10px;
    margin: 2px;
}

QListWidget::item:selected {
    background-color: #241f42;
}

QListWidget::item:hover:!selected {
    background-color: #1d1f2e;
}

QLineEdit, QComboBox, QPlainTextEdit {
    background-color: #101019;
    border: 1px solid #2b2d42;
    border-radius: 8px;
    padding: 8px 10px;
    color: #e7e8ee;
    selection-background-color: #7c5cff;
}

QLineEdit:focus, QComboBox:focus, QPlainTextEdit:focus {
    border: 1px solid #7c5cff;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox QAbstractItemView {
    background-color: #181926;
    border: 1px solid #2b2d42;
    selection-background-color: #7c5cff;
    outline: none;
}

QPushButton {
    background-color: #7c5cff;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 700;
}

QPushButton:hover {
    background-color: #6a48f2;
}

QPushButton:pressed {
    background-color: #5a3adb;
}

QPushButton#SecondaryButton {
    background-color: transparent;
    color: #c9cbe0;
    border: 1px solid #2b2d42;
    font-weight: 600;
}

QPushButton#SecondaryButton:hover {
    background-color: #1e2032;
}

QPushButton#SecondaryButton:pressed {
    background-color: #191a28;
}

QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #2b2d42;
    border-radius: 5px;
    min-height: 24px;
}

QScrollBar::handle:vertical:hover {
    background: #3b3e5a;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
"""


def load_data():
    """Load saved meals and the weekly plan."""
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if "meals" not in data:
            data["meals"] = []

        if "weekly_plan" not in data:
            data["weekly_plan"] = {day: None for day in DAYS}

        for day in DAYS:
            data["weekly_plan"].setdefault(day, None)

        return data

    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "meals": [],
            "weekly_plan": {day: None for day in DAYS},
        }


def save_data(data):
    """Save meals and weekly-plan information."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        return True
    except OSError as error:
        QMessageBox.critical(
            None,
            "Save error",
            f"The meal data could not be saved:\n{error}",
        )
        return False


def category_color(category):
    if not category:
        return CATEGORY_PALETTE[0]

    index = sum(ord(character) for character in category) % len(CATEGORY_PALETTE)
    return CATEGORY_PALETTE[index]


def hex_to_rgba(hex_color, alpha):
    hex_color = hex_color.lstrip("#")
    red, green, blue = (int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({red}, {green}, {blue}, {alpha})"


def add_card_shadow(widget):
    effect = QGraphicsDropShadowEffect(widget)
    effect.setBlurRadius(28)
    effect.setOffset(0, 8)
    effect.setColor(QColor(0, 0, 0, 150))
    widget.setGraphicsEffect(effect)


def build_meal_row(meal):
    row = QWidget()
    layout = QHBoxLayout(row)
    layout.setContentsMargins(10, 8, 10, 8)
    layout.setSpacing(10)

    dot = QLabel()
    dot.setFixedSize(10, 10)
    dot.setStyleSheet(
        f"background-color: {category_color(meal['category'])}; border-radius: 5px;"
    )

    text_column = QVBoxLayout()
    text_column.setSpacing(1)

    name_label = QLabel(meal["name"])
    name_label.setStyleSheet("font-weight: 600;")
    category_label = QLabel(meal["category"])
    category_label.setObjectName("SubText")

    text_column.addWidget(name_label)
    text_column.addWidget(category_label)

    layout.addWidget(dot)
    layout.addLayout(text_column)
    layout.addStretch()

    return row


class SavedMealsTab(QWidget):
    """Browse saved meals and view their details."""

    def __init__(self, data, on_data_changed, go_to_add_meal, go_to_weekly_plan):
        super().__init__()
        self.data = data
        self.on_data_changed = on_data_changed
        self.go_to_add_meal = go_to_add_meal
        self.go_to_weekly_plan = go_to_weekly_plan
        self.setObjectName("Page")

        self.meal_list = QListWidget()
        self.meal_list.currentRowChanged.connect(self.show_meal_details)

        self.name_label = QLabel()
        self.name_label.setObjectName("Heading")
        self.category_badge = QLabel()
        self.category_badge.setFixedHeight(24)
        self.ingredients_view = QPlainTextEdit()
        self.ingredients_view.setReadOnly(True)
        self.notes_view = QPlainTextEdit()
        self.notes_view.setReadOnly(True)

        header_row = QHBoxLayout()
        header_row.addWidget(self.name_label)
        header_row.addWidget(self.category_badge)
        header_row.addStretch()

        details_layout = QVBoxLayout()
        details_layout.setContentsMargins(20, 20, 20, 20)
        details_layout.setSpacing(10)
        details_layout.addLayout(header_row)
        details_layout.addWidget(QLabel("Ingredients"))
        details_layout.addWidget(self.ingredients_view)
        details_layout.addWidget(QLabel("Notes"))
        details_layout.addWidget(self.notes_view)

        details_card = QFrame()
        details_card.setObjectName("Card")
        details_card.setLayout(details_layout)
        add_card_shadow(details_card)

        splitter = QSplitter()
        splitter.addWidget(self.meal_list)
        splitter.addWidget(details_card)
        splitter.setSizes([240, 440])

        heading = QLabel("Saved Meals")
        heading.setObjectName("Heading")
        subtitle = QLabel("Select a meal to see its full recipe.")
        subtitle.setObjectName("SubText")

        heading_column = QVBoxLayout()
        heading_column.setSpacing(2)
        heading_column.addWidget(heading)
        heading_column.addWidget(subtitle)

        weekly_plan_button = QPushButton("Edit Weekly Plan")
        weekly_plan_button.setObjectName("SecondaryButton")
        weekly_plan_button.setCursor(Qt.PointingHandCursor)
        weekly_plan_button.clicked.connect(lambda: self.go_to_weekly_plan())

        add_meal_button = QPushButton("+ Add New Meal")
        add_meal_button.setCursor(Qt.PointingHandCursor)
        add_meal_button.clicked.connect(lambda: self.go_to_add_meal())

        top_bar = QHBoxLayout()
        top_bar.addLayout(heading_column)
        top_bar.addStretch()
        top_bar.addWidget(weekly_plan_button)
        top_bar.addWidget(add_meal_button)

        layout = QVBoxLayout()
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(4)
        layout.addLayout(top_bar)
        layout.addSpacing(14)
        layout.addWidget(splitter)
        self.setLayout(layout)

        self.refresh()

    def refresh(self):
        self.meal_list.clear()

        for meal in self.data["meals"]:
            item = QListWidgetItem()
            row = build_meal_row(meal)
            item.setSizeHint(row.sizeHint())
            self.meal_list.addItem(item)
            self.meal_list.setItemWidget(item, row)

        self.clear_details()

        if self.data["meals"]:
            self.meal_list.setCurrentRow(0)

    def clear_details(self):
        self.name_label.setText("No meals saved yet")
        self.category_badge.setText("")
        self.category_badge.setStyleSheet("")
        self.ingredients_view.setPlainText("")
        self.notes_view.setPlainText("")

    def show_meal_details(self, row):
        if row < 0 or row >= len(self.data["meals"]):
            self.clear_details()
            return

        meal = self.data["meals"][row]
        color = category_color(meal["category"])

        self.name_label.setText(meal["name"])
        self.category_badge.setText(meal["category"])
        self.category_badge.setStyleSheet(
            f"background-color: {hex_to_rgba(color, 0.18)};"
            f"color: {color};"
            f"border: 1px solid {hex_to_rgba(color, 0.4)};"
            "border-radius: 12px;"
            "padding: 3px 12px;"
            "font-weight: 700;"
        )
        self.ingredients_view.setPlainText(
            "\n".join(f"- {ingredient}" for ingredient in meal["ingredients"])
        )
        self.notes_view.setPlainText(meal["notes"] or "No notes were added.")


class AddMealTab(QWidget):
    """Form for adding a new meal idea."""

    def __init__(self, data, on_data_changed):
        super().__init__()
        self.data = data
        self.on_data_changed = on_data_changed
        self.setObjectName("Page")

        self.name_input = QLineEdit()
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText(
            "Examples: Breakfast, Lunch, Dinner, Snack"
        )
        self.ingredients_input = QPlainTextEdit()
        self.ingredients_input.setPlaceholderText(
            "Enter ingredients separated by commas"
        )
        self.ingredients_input.setFixedHeight(80)
        self.notes_input = QPlainTextEdit()
        self.notes_input.setPlaceholderText("Notes are optional")
        self.notes_input.setFixedHeight(80)

        form = QFormLayout()
        form.setSpacing(12)
        form.addRow("1. Meal name", self.name_input)
        form.addRow("2. Category", self.category_input)
        form.addRow("3. Ingredients", self.ingredients_input)
        form.addRow("4. Notes", self.notes_input)

        save_button = QPushButton("Save Meal")
        save_button.setCursor(Qt.PointingHandCursor)
        save_button.clicked.connect(self.save_meal)

        clear_button = QPushButton("Clear Form")
        clear_button.setObjectName("SecondaryButton")
        clear_button.setCursor(Qt.PointingHandCursor)
        clear_button.clicked.connect(self.clear_form)

        button_row = QHBoxLayout()
        button_row.addWidget(save_button)
        button_row.addWidget(clear_button)
        button_row.addStretch()

        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(24, 24, 24, 24)
        form_layout.setSpacing(18)
        form_layout.addLayout(form)
        form_layout.addLayout(button_row)

        form_card = QFrame()
        form_card.setObjectName("Card")
        form_card.setLayout(form_layout)
        add_card_shadow(form_card)

        heading = QLabel("Add a Meal")
        heading.setObjectName("Heading")
        subtitle = QLabel(
            "Takes about 1 minute. Only the meal information you enter is stored locally."
        )
        subtitle.setObjectName("SubText")
        subtitle.setWordWrap(True)

        layout = QVBoxLayout()
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(4)
        layout.addWidget(heading)
        layout.addWidget(subtitle)
        layout.addSpacing(14)
        layout.addWidget(form_card)
        layout.addStretch()
        self.setLayout(layout)

    def save_meal(self):
        name = self.name_input.text().strip()
        category = self.category_input.text().strip()
        ingredients_text = self.ingredients_input.toPlainText().strip()
        notes = self.notes_input.toPlainText().strip()

        if not name:
            QMessageBox.warning(self, "Missing information", "Meal name is required.")
            return

        if not category:
            QMessageBox.warning(self, "Missing information", "Category is required.")
            return

        ingredients = [
            ingredient.strip()
            for ingredient in ingredients_text.split(",")
            if ingredient.strip()
        ]

        if not ingredients:
            QMessageBox.warning(
                self, "Missing information", "At least one ingredient is required."
            )
            return

        confirmation = QMessageBox.question(
            self,
            "Confirm meal",
            f"Save '{name}' to your meal list?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if confirmation != QMessageBox.Yes:
            return

        new_meal = {
            "name": name,
            "category": category,
            "ingredients": ingredients,
            "notes": notes,
        }

        self.data["meals"].append(new_meal)

        if not save_data(self.data):
            self.data["meals"].pop()
            return

        self.clear_form()

        QMessageBox.information(self, "Meal saved", f"Saved: {name}")
        self.on_data_changed()

    def clear_form(self):
        self.name_input.clear()
        self.category_input.clear()
        self.ingredients_input.clear()
        self.notes_input.clear()


class WeeklyPlanTab(QWidget):
    """View and edit the weekly meal plan."""

    def __init__(self, data, on_data_changed):
        super().__init__()
        self.data = data
        self.on_data_changed = on_data_changed
        self.day_combos = {}
        self.setObjectName("Page")

        heading = QLabel("Weekly Plan")
        heading.setObjectName("Heading")
        subtitle = QLabel("Assign a saved meal to each day, or leave it empty.")
        subtitle.setObjectName("SubText")

        grid = QGridLayout()
        grid.setSpacing(14)

        columns = 4
        for index, day in enumerate(DAYS):
            card = QFrame()
            card.setObjectName("DayCard")
            add_card_shadow(card)

            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(14, 14, 14, 14)
            card_layout.setSpacing(8)

            day_label = QLabel(day)
            day_label.setObjectName("DayName")

            combo = QComboBox()
            combo.currentIndexChanged.connect(self.make_day_handler(day))
            self.day_combos[day] = combo

            card_layout.addWidget(day_label)
            card_layout.addWidget(combo)

            row, col = divmod(index, columns)
            grid.addWidget(card, row, col)

        layout = QVBoxLayout()
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(4)
        layout.addWidget(heading)
        layout.addWidget(subtitle)
        layout.addSpacing(18)
        layout.addLayout(grid)
        layout.addStretch()
        self.setLayout(layout)

        self.refresh()

    def make_day_handler(self, day):
        def handler(index):
            self.assign_day(day, index)

        return handler

    def refresh(self):
        meal_names = [meal["name"] for meal in self.data["meals"]]

        for day, combo in self.day_combos.items():
            combo.blockSignals(True)
            combo.clear()
            combo.addItem(EMPTY_DAY_LABEL)
            combo.addItems(meal_names)

            current = self.data["weekly_plan"].get(day)
            if current in meal_names:
                combo.setCurrentIndex(meal_names.index(current) + 1)
            else:
                combo.setCurrentIndex(0)

            combo.blockSignals(False)

    def revert_day_combo(self, day):
        combo = self.day_combos[day]
        meal_names = [meal["name"] for meal in self.data["meals"]]
        current = self.data["weekly_plan"].get(day)

        combo.blockSignals(True)

        if current in meal_names:
            combo.setCurrentIndex(meal_names.index(current) + 1)
        else:
            combo.setCurrentIndex(0)

        combo.blockSignals(False)

    def assign_day(self, day, index):
        combo = self.day_combos[day]
        previous_meal = self.data["weekly_plan"].get(day)
        new_meal = None if index <= 0 else combo.itemText(index)

        if previous_meal == new_meal:
            return

        old_text = previous_meal or EMPTY_DAY_LABEL
        new_text = new_meal or EMPTY_DAY_LABEL

        confirmation = QMessageBox.question(
            self,
            "Confirm weekly plan change",
            f"Change {day} from '{old_text}' to '{new_text}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if confirmation != QMessageBox.Yes:
            self.revert_day_combo(day)
            return

        self.data["weekly_plan"][day] = new_meal

        if not save_data(self.data):
            self.data["weekly_plan"][day] = previous_meal
            self.revert_day_combo(day)


class MealPlannerWindow(QMainWindow):
    """Main application window for the Meal Planner."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meal Planner / Recipe Picker")
        self.resize(1020, 660)
        self.setMinimumSize(780, 520)

        self.data = load_data()
        self.nav_buttons = []

        self.stack = QStackedWidget()

        self.saved_meals_tab = SavedMealsTab(
            self.data,
            self.on_data_changed,
            go_to_add_meal=lambda: self.go_to(1),
            go_to_weekly_plan=lambda: self.go_to(2),
        )
        self.add_meal_tab = AddMealTab(self.data, self.on_data_changed)
        self.weekly_plan_tab = WeeklyPlanTab(self.data, self.on_data_changed)

        self.stack.addWidget(self.saved_meals_tab)
        self.stack.addWidget(self.add_meal_tab)
        self.stack.addWidget(self.weekly_plan_tab)

        sidebar = QWidget()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(230)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(18, 26, 18, 18)
        sidebar_layout.setSpacing(4)

        app_title = QLabel("🍲  Meal Planner")
        app_title.setObjectName("AppTitle")
        app_subtitle = QLabel("Recipe Picker")
        app_subtitle.setObjectName("AppSubtitle")
        app_tagline = QLabel(
            "Save meal ideas and plan your week without starting from scratch."
        )
        app_tagline.setObjectName("AppTagline")
        app_tagline.setWordWrap(True)
        sidebar_layout.addWidget(app_title)
        sidebar_layout.addWidget(app_subtitle)
        sidebar_layout.addSpacing(10)
        sidebar_layout.addWidget(app_tagline)
        sidebar_layout.addSpacing(20)

        nav_specs = [
            ("🍽", "Saved Meals"),
            ("➕", "Add Meal"),
            ("📅", "Weekly Plan"),
        ]

        nav_group = QButtonGroup(self)
        nav_group.setExclusive(True)

        for index, (icon, label) in enumerate(nav_specs):
            button = QPushButton(f"{icon}   {label}")
            button.setObjectName("NavButton")
            button.setCheckable(True)
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(lambda checked, i=index: self.go_to(i))
            nav_group.addButton(button)
            sidebar_layout.addWidget(button)
            self.nav_buttons.append(button)

        self.nav_buttons[0].setChecked(True)
        sidebar_layout.addStretch()

        central = QWidget()
        central_layout = QHBoxLayout(central)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)
        central_layout.addWidget(sidebar)
        central_layout.addWidget(self.stack, stretch=1)

        self.setCentralWidget(central)

    def go_to(self, index):
        self.stack.setCurrentIndex(index)
        self.nav_buttons[index].setChecked(True)

    def on_data_changed(self):
        self.saved_meals_tab.refresh()
        self.weekly_plan_tab.refresh()


def run_program():
    """Run the Meal Planner GUI application."""
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(STYLE_SHEET)
    window = MealPlannerWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_program()
