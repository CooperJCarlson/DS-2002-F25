#!/bin/bash

# refresh_card_sets.sh
# Refreshes all Pokémon card set JSON files in the card_set_lookup/ directory
# by re-fetching updated data from the Pokémon TCG API.

echo "Refreshing all card sets in card_set_lookup/..."

# Loop through every .json file in the lookup directory
for FILE in card_set_lookup/*.json; do
    # Check if there are actually any files to refresh
    if [ ! -e "$FILE" ]; then
        echo "No JSON files found in card_set_lookup/. Nothing to refresh."
        exit 0
    fi

    # Extract the set ID from the filename
    SET_ID=$(basename "$FILE" .json)

    echo "Updating set: $SET_ID ..."

    # Use curl to re-fetch updated data from the API
    curl -s "https://api.pokemontcg.io/v2/cards?q=set.id:${SET_ID}" -o "$FILE"

    echo "Updated data for '$SET_ID' written to $FILE"
done

echo "✅ All card sets have been refreshed!"
