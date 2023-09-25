import os
import json
import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QGridLayout, QDialog,
                             QGraphicsView, QGraphicsScene, QScrollArea,
                             QTextBrowser, QPlainTextEdit, QComboBox, QCheckBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QEvent

base_url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
json_file = 'yugioh_cards.json'

# Same as before
def main_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
    return data

# Same as before
def save_json_data(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file)

# Same as before
def load_json_data(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
    return data

# Same as before
def check_and_request_data():
    if not os.path.exists(json_file):
        print("JSON file not found. Fetching data from API...")
        raw_data = main_request(base_url)
        save_json_data(raw_data, json_file)
    else:
        print("Loading data from JSON file...")
        raw_data = load_json_data(json_file)
    return raw_data

# Cosmetic changes. Enabled sorting by price, removed unnecessary comments, removed price_sources parameter
def find_cards(cards_data, name=None, card_type=None, archetype=None,
               description=None, card_sets=None, rarity=None,
               race=None, sort_by_price=None):

    results = []

    # Same as before
    for card in cards_data:
        if name and name.lower() not in card.get('name', '').lower():
            continue
        if card_type and card_type.lower() not in card.get('type', '').lower():
            continue
        if archetype and archetype.lower() not in card.get('archetype', '').lower():
            continue
        if card_sets and card_sets.lower() not in [card_set.get('set_name', '').lower() for card_set in card.get('card_sets', [])]:
            continue
        
        results.append(card)

    # New sorting implementation
    if sort_by_price:
        considered_prices = ['cardmarket_price', 'tcgplayer_price', 'ebay_price', 'amazon_price', 'coolstuffinc_price']

        def card_sort_key(card):
            price = sum([float(card['card_prices'][0].get(price, '0')) for price in considered_prices])
            return price if sort_by_price == "low-to-high" else -price

        results.sort(key=card_sort_key)

    return results
        
def check_and_request_data():
    if not os.path.exists(json_file):
        print("JSON file not found. Fetching data from API...")
        raw_data = main_request(base_url)
        save_json_data(raw_data, json_file)
    else:
        print("Loading data from JSON file...")
        raw_data = load_json_data(json_file)
    return raw_data

class ImageWindow(QDialog):
    def __init__(self, image_path):
        super().__init__()

        self.setWindowTitle('Card Image')

        layout = QVBoxLayout()

        img_view = QGraphicsView()
        img_scene = QGraphicsScene()
        img_view.setScene(img_scene)

        pixmap = QPixmap(image_path)

        img_scene.addPixmap(pixmap)
        
        layout.addWidget(img_view)
        self.setLayout(layout)

class YugiohSearchGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Yugioh Card Search')

        layout = QGridLayout()
        layout.setVerticalSpacing(10)

        self.search_label = QLabel('Search Card by:')
        layout.addWidget(self.search_label, 0, 0)

        self.name_label = QLabel("Name")
        layout.addWidget(self.name_label, 1, 0)
        self.name_search_box = QLineEdit()
        self.name_search_box.installEventFilter(self)
        layout.addWidget(self.name_search_box, 2, 0)
        
        self.archetype_label = QLabel("Archetype")
        layout.addWidget(self.archetype_label, 1, 1)
        self.archetype_search_box = QLineEdit()
        self.archetype_search_box.installEventFilter(self)
        layout.addWidget(self.archetype_search_box, 2, 1)

        self.type_label = QLabel("Type")
        layout.addWidget(self.type_label, 1, 2)
        self.type_search_box = QLineEdit()
        self.type_search_box.installEventFilter(self)
        layout.addWidget(self.type_search_box, 2, 2)

        self.rarity_label = QLabel("Rarity")
        layout.addWidget(self.rarity_label, 3, 0)
        self.rarity_search_box = QLineEdit()
        self.rarity_search_box.installEventFilter(self)
        layout.addWidget(self.rarity_search_box, 4, 0)

        self.race_label = QLabel("Race")
        layout.addWidget(self.race_label, 3, 1)
        self.race_search_box = QLineEdit()
        self.race_search_box.installEventFilter(self)
        layout.addWidget(self.race_search_box, 4, 1)

        self.set_name_label = QLabel("Set Name")
        layout.addWidget(self.set_name_label, 3, 2)
        self.set_name_search_box = QLineEdit()
        self.set_name_search_box.installEventFilter(self)
        layout.addWidget(self.set_name_search_box, 4, 2)
        
        self.card_price_label = QLabel("Select Price Source")
        layout.addWidget(self.card_price_label, 5, 0)

# Price Source drop-down menu
        self.price_sources = ['cardmarket_price', 'tcgplayer_price', 'ebay_price', 'amazon_price', 'coolstuffinc_price']
        self.price_checkboxes = {}

        for i, price_source in enumerate(self.price_sources):
            checkbox = QCheckBox(price_source)
            self.price_checkboxes[price_source] = checkbox
            layout.addWidget(checkbox, 6 + int(i / 3), i % 3)  # positioning checkboxes in a 2x3 grid

        self.sort_by_price_label = QLabel("Sort by Price")
        layout.addWidget(self.sort_by_price_label, 8, 0)
        self.sort_by_price_combobox = QComboBox()
        self.sort_by_price_combobox.addItem("low-to-high")
        self.sort_by_price_combobox.addItem("high-to-low")
        layout.addWidget(self.sort_by_price_combobox, 8, 1)  # Change layout widget position

        self.search_button = QPushButton('Search')
        layout.addWidget(self.search_button, 9, 0, 1, 3)

        # Results area
        self.results = QScrollArea()
        self.content = QWidget()
        self.results_widget = QVBoxLayout()
        self.content.setLayout(self.results_widget)
        self.results.setWidget(self.content)
        self.results.setWidgetResizable(True)
        layout.addWidget(self.results, 10, 0, 1, 3)

        self.search_button.clicked.connect(self.search_cards)

        self.setLayout(layout)
        
    def search_cards(self):
        name_query = self.name_search_box.text().lower()
        archetype_query = self.archetype_search_box.text().lower()
        type_query = self.type_search_box.text().lower()
        name_query = self.name_search_box.text().lower()
        archetype_query = self.archetype_search_box.text().lower()
        type_query = self.type_search_box.text().lower()
        rarity_query = self.rarity_search_box.text().lower()
        race_query = self.race_search_box.text().lower()
        set_name_query = self.set_name_search_box.text().lower()

                # Clear the results before displaying new ones
        while self.results_widget.count():
            child = self.results_widget.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        card_data = check_and_request_data()
        
        found_cards = find_cards(
            card_data['data'],
            name=name_query,
            card_type=type_query,
            archetype=archetype_query,
            rarity=rarity_query,
            race=race_query,
            card_sets=set_name_query,
            sort_by_price=self.sort_by_price_combobox.currentText()
        )

        results_found = len(found_cards) > 0

        for card in found_cards:
            image_name = f"{card['id']}.jpg"
            image_path = f"images/{image_name}"
            img_link = f"<a href='{image_path}'>View Image</a>"

            card_rarity = card['card_sets'][0].get('set_rarity', 'N/A') if card.get('card_sets') else 'N/A'
            card_description = card.get('desc', 'N/A')

            card_info = f"Name: {card['name']}<br>Type: {card['type']}<br>Description: {card_description}<br>Rarity: {card_rarity}<br>Archetype: {card.get('archetype', 'N/A')}<br>"

            if 'Monster' in card['type']:
                card_attack = card.get('atk', 'N/A')
                card_defense = card.get('def', 'N/A')
                card_info += f"Attack: {card_attack}<br>Defense: {card_defense}<br>\n\n"

            card_info += f"{img_link}<br>\n\n"

            # Add the card_info (including the View Image link) to the QTextBrowser widget
            result_text = QTextBrowser()
            result_text.setHtml(card_info)
            result_text.setReadOnly(True)
            result_text.setOpenLinks(False)
            result_text.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            result_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            result_text.setMinimumHeight(150)
            result_text.anchorClicked.connect(lambda anchor: self.open_image(anchor.path()))

            self.results_widget.addWidget(result_text)

        if not results_found:
            result_text = QTextBrowser()
            result_text.setHtml("No results found.")
            result_text.setReadOnly(True)
            self.results_widget.addWidget(result_text)

    def open_image(self, image_path):
        image_window = ImageWindow(image_path)
        image_window.exec_()

    def eventFilter(self, source, event):
        if (event.type() == QEvent.KeyPress and
            event.key() == Qt.Key_Return):
            self.search_cards()
            return True
        return super(YugiohSearchGUI, self).eventFilter(source, event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = YugiohSearchGUI()
    main_window.show()
    sys.exit(app.exec_())