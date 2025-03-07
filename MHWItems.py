import sys
import os
import pandas as pd
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QListWidget, QLabel
from PyQt6.QtGui import QFont, QIcon
from fuzzywuzzy import process

# Function to get the correct path to the ODS file
def get_ods_path():
    """Returns the correct path to the ODS file, considering if running as script or .exe."""
    if getattr(sys, 'frozen', False):  # If running as a bundled .exe
        base_path = sys._MEIPASS  # Temporary folder where PyInstaller unpacks files
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))  # Normal script directory
    return os.path.join(base_path, "ItemIDS.ods")

# Load data from ODS file
def load_data_from_ods(file_path):
    """Loads data from the given ODS file and returns a dictionary {Name: ID}."""
    try:
        df = pd.read_excel(file_path, engine="odf")
        return dict(zip(df.iloc[:, 1], df.iloc[:, 0]))  # {Name: ID}
    except Exception as e:
        print(f"Error loading ODS file: {e}")
        return {}

# Get the file path for ItemIDS.ods
FILE_PATH = get_ods_path()
data = load_data_from_ods(FILE_PATH)

# Path to application icon
ICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MHW.ico")

class AutoCompleteSearch(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Monster Hunter Wilds - Item IDs")
        self.setGeometry(200, 200, 400, 300)
        self.set_dark_theme()

        # Set window icon
        self.setWindowIcon(QIcon(ICON_PATH))

        layout = QVBoxLayout()

        self.entry = QLineEdit(self)
        self.entry.setPlaceholderText("Start typing an item name...")
        self.entry.setFont(QFont("Arial", 12))
        self.entry.textChanged.connect(self.update_suggestions)
        self.entry.returnPressed.connect(self.select_highlighted_item)
        layout.addWidget(self.entry)

        self.listbox = QListWidget(self)
        self.listbox.setFont(QFont("Arial", 11))
        self.listbox.itemClicked.connect(self.select_item)
        self.listbox.itemActivated.connect(self.select_item)
        layout.addWidget(self.listbox)

        self.result_label = QLabel("Item ID: ", self)
        self.result_label.setFont(QFont("Arial", 14))
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def update_suggestions(self):
        input_text = self.entry.text().strip()
        self.listbox.clear()

        if input_text:
            min_score = 50 if len(input_text) <= 3 else 60
            matches = process.extractBests(input_text, data.keys(), limit=7)
            for match, score in matches:
                if score >= min_score:
                    self.listbox.addItem(match)

            if self.listbox.count() > 0:
                self.listbox.setCurrentRow(0)

    def select_item(self, item):
        name = item.text()
        if name in data:
            self.result_label.setText(f"Item ID: {data[name]}")
            self.entry.setText(name)
            self.listbox.clear()

    def select_highlighted_item(self):
        selected_item = self.listbox.currentItem()
        if selected_item:
            self.select_item(selected_item)

    def set_dark_theme(self):
        self.setStyleSheet("""
            QWidget { background-color: #282828; color: #DCDCDC; }
            QLineEdit { background-color: #1E1E1E; color: #DCDCDC; border: 1px solid #555; padding: 5px; }
            QListWidget { background-color: #1E1E1E; color: #DCDCDC; border: none; }
            QListWidget::item:selected { background-color: #444; color: white; }
            QLabel { color: #DCDCDC; }
        """)

if __name__ == "__main__":
    app = QApplication([])

    # ✅ Explicitly set taskbar icon for Windows
    app.setWindowIcon(QIcon(ICON_PATH))

    # ✅ For Windows, force the taskbar to recognize the icon
    if sys.platform.startswith("win"):
        import ctypes
        myappid = "com.mhwitems.app"  # Unique identifier for Windows taskbar
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    window = AutoCompleteSearch()
    window.show()
    app.exec()