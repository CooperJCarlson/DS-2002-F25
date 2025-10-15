#!/bin/bash

# add_card_set.sh
# Fetches Pokémon card data for a given set and stores it locally as JSON.

# Prompt the user for the TCG Card Set ID
read -p "Enter the TCG Card Set ID (e.g., base1, base4): " SET_ID

# Validate input
if [ -z "$SET_ID" ]; then
    echo "Error: Set ID cannot be empty." >&2
    exit 1
fi

# Notify the user
echo "Fetching data for Pokémon card set: $SET_ID ..."

# Ensure output directory exists
mkdir -p card_set_lookup

# Use curl to fetch the data from the Pokémon TCG API
# (This uses the v2 API — you may need your API key if the endpoint requires it)
curl -s "https://api.pokemontcg.io/v2/cards?q=set.id:${SET_ID}" -o "card_set_lookup/${SET_ID}.json"

# Check if curl succeeded
if [ $? -eq 0 ]; then
    echo "Data for set '$SET_ID' saved to card_set_lookup/${SET_ID}.json"
else
    echo "Error: Failed to fetch data for set '$SET_ID'." >&2
    exit 1
fi

