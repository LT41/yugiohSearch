# yugiohSearch

This project allows users to search for Yugioh cards using various criteria. The application retrieves card data from the YGOPRODeck API and stores it locally in a JSON file for faster search operations. The GUI is built using PyQt5.

## Features

- Search cards by name, card type, archetype, rarity, race, and set name
- Sort search results by price (low-to-high or high-to-low)
- View images of individual cards
- Check for updated data from the API and download it automatically if needed

The GUI allows you to input the search criteria, like name, card type, archetype, rarity, race, and set name. Once you have entered your desired filters, click the "Search" button or press Enter on your keyboard to start the search.

The search results will be displayed in the scrollable results area, with relevant card information and a link to view the image of each card.

Use the Sort by Price drop-down menu to sort search results based on the total price from the selected price sources: 'cardmarket_price', 'tcgplayer_price', 'ebay_price', 'amazon_price', or 'coolstuffinc_price'. Select the desired price sources by checking the corresponding checkboxes.
