#!/usr/bin/env python

import os
import sys
import json
import pandas as pd

# -----------------------------
# Helper Function 1: Load JSON Lookup Data
# -----------------------------
def _load_lookup_data(lookup_dir):
    all_rows = []

    if not os.path.exists(lookup_dir):
        print(f"ERROR: Lookup directory '{lookup_dir}' does not exist.", file=sys.stderr)
        return pd.DataFrame()

    files = os.listdir(lookup_dir)
    print("DEBUG: Files in lookup_dir:", files)

    for file_name in files:
        if not file_name.endswith(".json"):
            continue
        file_path = os.path.join(lookup_dir, file_name)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"ERROR: Could not read JSON file '{file_name}': {e}", file=sys.stderr)
            continue

        for card in data.get("data", []):
            card_id = card.get("id", "")
            card_name = card.get("name", "")
            card_number = card.get("number", "")
            set_id = card.get("set", {}).get("id", "")
            set_name = card.get("set", {}).get("name", "")

            holo_price = card.get("tcgplayer", {}).get("prices", {}).get("holofoil", {}).get("market", None)
            normal_price = card.get("tcgplayer", {}).get("prices", {}).get("normal", {}).get("market", None)
            card_market_value = holo_price if holo_price is not None else (normal_price if normal_price is not None else 0.0)

            all_rows.append({
                "card_id": card_id,
                "card_name": card_name,
                "card_number": card_number,
                "set_id": set_id,
                "set_name": set_name,
                "card_market_value": card_market_value
            })

    lookup_df = pd.DataFrame(all_rows)

    print("DEBUG: lookup_df columns:", lookup_df.columns.tolist())
    print("DEBUG: Number of cards loaded:", len(lookup_df))

    if not lookup_df.empty:
        lookup_df = lookup_df.sort_values("card_market_value", ascending=False)\
                             .drop_duplicates(subset=["card_id"], keep="first")

    return lookup_df


# -----------------------------
# Helper Function 2: Load CSV Inventory
# -----------------------------
def _load_inventory_data(inventory_dir):
    inventory_data = []

    if not os.path.exists(inventory_dir):
        print(f"ERROR: Inventory directory '{inventory_dir}' does not exist.", file=sys.stderr)
        return pd.DataFrame()

    files = os.listdir(inventory_dir)
    for file_name in files:
        if not file_name.endswith(".csv"):
            continue
        file_path = os.path.join(inventory_dir, file_name)
        try:
            df = pd.read_csv(file_path)
            inventory_data.append(df)
        except Exception as e:
            print(f"ERROR: Could not read CSV file '{file_name}': {e}", file=sys.stderr)

    if not inventory_data:
        return pd.DataFrame()

    inventory_df = pd.concat(inventory_data, ignore_index=True)

    # Create unified card_id key (ensure both parts are strings)
    inventory_df['card_id'] = inventory_df['set_id'].astype(str) + "-" + inventory_df['card_number'].astype(str)

    return inventory_df


# -----------------------------
# Main ETL Function
# -----------------------------
def update_portfolio(inventory_dir, lookup_dir, output_file):
    print(f"Starting update_portfolio() with inventory_dir={inventory_dir}, lookup_dir={lookup_dir}")
    
    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)

    if inventory_df.empty:
        print("ERROR: Inventory is empty. Nothing to process.", file=sys.stderr)
        pd.DataFrame(columns=['card_id','card_name','card_number','set_id','set_name','card_market_value','binder_name','page_number','slot_number','index']).to_csv(output_file, index=False)
        return

    print("DEBUG: Merging inventory with lookup data...")

    merged_df = pd.merge(
        inventory_df,
        lookup_df[['card_id', 'card_name', 'card_market_value', 'set_name']],
        on='card_id',
        how='left',
        suffixes=('_inv', '_lookup')
    )

    # Fill missing data
    merged_df['card_name'] = merged_df['card_name_lookup']
    merged_df['card_market_value'] = merged_df['card_market_value'].fillna(0.0)
    merged_df['set_name'] = merged_df['set_name'].fillna('NOT_FOUND')

    # Create location index
    merged_df['index'] = merged_df['binder_name'].astype(str) + "-" + merged_df['page_number'].astype(str) + "-" + merged_df['slot_number'].astype(str)

    final_cols = ['card_id','card_name','card_number','set_id','set_name','card_market_value','binder_name','page_number','slot_number','index']

    # Check that final_cols exist
    missing_cols = [c for c in final_cols if c not in merged_df.columns]
    if missing_cols:
        print(f"ERROR: Missing columns after merge: {missing_cols}", file=sys.stderr)
        print("DEBUG: merged_df columns:", merged_df.columns.tolist(), file=sys.stderr)
        sys.exit(1)

    merged_df[final_cols].to_csv(output_file, index=False)
    print(f"Portfolio CSV written to {output_file}")


# -----------------------------
# Public Interface
# -----------------------------
def main():
    update_portfolio("./card_inventory/", "./card_set_lookup/", "card_portfolio.csv")

def test():
    print("Starting update_portfolio.py in TEST mode")
    update_portfolio("./card_inventory_test/", "./card_set_lookup_test/", "test_card_portfolio.csv")


# -----------------------------
# Run block
# -----------------------------
if __name__ == "__main__":
    test()
