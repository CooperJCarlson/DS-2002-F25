#!/usr/bin/env python

import sys
import update_portfolio
import generate_summary

def run_production_pipeline():
    """Executes the full production workflow: ETL + reporting."""

    # Starting message
    print("=== Starting Production Pipeline ===", file=sys.stderr)

    # Step 1: ETL
    print("-> Running ETL step: update_portfolio...", file=sys.stderr)
    update_portfolio.main()
    print("ETL step completed: card_portfolio.csv generated.", file=sys.stderr)

    # Step 2: Reporting
    print("-> Running Reporting step: generate_summary...", file=sys.stderr)
    generate_summary.main()
    
    # Completion message
    print("=== Production Pipeline Completed Successfully ===", file=sys.stderr)

if __name__ == "__main__":
    run_production_pipeline()
