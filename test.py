from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QListWidget, QLabel
from PyQt6.QtGui import QFont
from fuzzywuzzy import process

# Sample data (Name: ID)
data = {
    "Apple": 101, "Banana": 102, "Cherry": 103, "Date": 104, "Elderberry": 105,
    "Fig": 106, "Grape": 107, "Honeydew": 108, "Kiwi": 109, "Lemon": 110,
    "Mango": 111, "Nectarine": 112, "Orange": 113, "Papaya": 114, "Quince": 115,
    "Raspberry": 116, "Strawberry": 117, "Tangerine": 118, "Ugli Fruit": 119, "Watermelon": 120
}

class AutoCompleteSearch(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Advanced Name Lookup")
        self.setGeometry(200, 200, 400, 300)

        # Apply Dark Theme
        self.set_dark_theme()

        layout = QVBoxLayout()

        self.entry = QLineEdit(self)
        self.entry.setPlaceholderText("Start typing a name...")
        self.entry.setFont(QFont("Arial", 12))
        self.entry.textChanged.connect(self.update_suggestions)
        self.entry.returnPressed.connect(self.select_highlighted_item)  # Enter key selection
        layout.addWidget(self.entry)

        self.listbox = QListWidget(self)
        self.listbox.setFont(QFont("Arial", 11))
        self.listbox.itemClicked.connect(self.select_item)
        self.listbox.itemActivated.connect(self.select_item)  # Activate on Enter key
        layout.addWidget(self.listbox)

        self.result_label = QLabel("ID: ", self)
        self.result_label.setFont(QFont("Arial", 14))
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def update_suggestions(self):
        input_text = self.entry.text().strip()
        self.listbox.clear()

        if input_text:
            # Adjust similarity threshold dynamically based on input length
            min_score = 50 if len(input_text) <= 3 else 60

            matches = process.extractBests(input_text, data.keys(), limit=7)
            for match, score in matches:
                if score >= min_score:
                    self.listbox.addItem(match)

            # Auto-select first item for easier keyboard navigation
            if self.listbox.count() > 0:
                self.listbox.setCurrentRow(0)

    def select_item(self, item):
        name = item.text()
        if name in data:
            self.result_label.setText(f"ID: {data[name]}")
            self.entry.setText(name)
            self.listbox.clear()

    def select_highlighted_item(self):
        """Allows selection via Enter key"""
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
    window = AutoCompleteSearch()
    window.show()
    app.exec()