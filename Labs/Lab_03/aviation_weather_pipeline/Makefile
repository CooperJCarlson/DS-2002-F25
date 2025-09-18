.PHONY: all fetch analyze clean

all: analyze

fetch:
	@echo "Fetching raw METAR data..."
	./fetch_metars.sh
	@echo "Raw METAR data saved in 'raw_metars/'"

analyze: fetch
	@echo "Analyzing METAR data..."
	./analyze_data.sh
	@echo "Analysis complete - CSV file saved as 'weather_report.csv'"
	@echo "Pipeline completed successfully! :)"

clean:
	@echo "Cleaning up raw data and CSV output..."
	rm -rf raw_metars weather_report.csv
	@echo "Cleanup complete & workplace reset"
