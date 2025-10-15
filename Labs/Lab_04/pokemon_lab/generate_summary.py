#!/usr/bin/env python

import os
import sys
import pandas as pd

def generate_summary(portfolio_file):
    """Reads the final portfolio CSV and prints summary statistics."""

    # Check if the portfolio file exists
    if not os.path.exists(portfolio_file):
        print(f"Error: Portfolio file '{portfolio_file}' not found.", file=sys.stderr)
        sys.exit(1)

    # Read the portfolio CSV into a DataFrame
    df = pd.read_csv(portfolio_file)

    # Check if the file contains data
    if df.empty:
        print(f"The file '{portfolio_file}' is empty. No data to summarize.")
        return

    # Calculate the total portfolio value
    total_portfolio_value = df["card_market_value"].sum()

    # Find the most valuable card
    most_valuable_idx = df["card_market_value"].idxmax()
    most_valuable_card = df.loc[most_valuable_idx]

    # Print the summary report
    print("\n===== Pokémon Card Portfolio Summary =====")
    print(f"Total Portfolio Market Value: ${total_portfolio_value:,.2f}\n")
    print("Most Valuable Card:")
    print(f"  Name: {most_valuable_card['card_name']}")
    print(f"  ID: {most_valuable_card['card_id']}")
    print(f"  Market Value: ${most_valuable_card['card_market_value']:,.2f}")
    print("==========================================\n")

def main():
    """Runs the summary on the production portfolio."""
    generate_summary("card_portfolio.csv")

def test():
    """Runs the summary on the test portfolio."""
    generate_summary("test_card_portfolio.csv")

if __name__ == "__main__":
    # Default behavior: run in test mode
    print("Running generate_summary.py in Test Mode...", file=sys.stderr)
    test()


