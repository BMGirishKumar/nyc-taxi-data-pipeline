import csv
import logging
import os
import sys
import pandas as pd
import numpy as np

# --- Set up Automated Logging ---
# Any corrupted or broken rows will be quietly written to this log file instead of crashing the program.
logging.basicConfig(
    filename="pipeline_errors.log",
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class TaxiDataStreamer:
    """THE SMART CONVEYOR BELT: Dynamically finds columns and streams rows one-by-line."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Error: Cannot find file at: {file_path}")
        
        # Automatically discover column map keys right when the factory turns on
        self._discover_column_mappings()

    def _discover_column_mappings(self):
        """Scans the header row once to find where the critical data columns are."""
        with open(self.file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)  # Read the very first row containing header titles
            
            # Convert all titles to lowercase for consistent comparison
            lower_headers = [h.lower().strip() for h in headers]
            
            # Dynamically match column keys based on expected partial names
            self.col_vendor = headers[lower_headers.index('vendorid')] if 'vendorid' in lower_headers else (headers[lower_headers.index('vendor_id')] if 'vendor_id' in lower_headers else None)
            self.col_distance = headers[lower_headers.index('trip_distance')] if 'trip_distance' in lower_headers else None
            self.col_fare = headers[lower_headers.index('fare_amount')] if 'fare_amount' in lower_headers else None
            self.col_tip = headers[lower_headers.index('tip_amount')] if 'tip_amount' in lower_headers else None
            self.col_pickup_id = headers[lower_headers.index('pulocationid')] if 'pulocationid' in lower_headers else None
            self.col_dropoff_id = headers[lower_headers.index('dolocationid')] if 'dolocationid' in lower_headers else None

            print(f"📊 Smart Mapping Active! Matched Distance -> '{self.col_distance}', Fare -> '{self.col_fare}'")

    def stream_trips(self):
        """Generator function yielding standardized dictionary records."""
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Re-package the row using our smart mapped column keys
                yield {
                    "vendor_id": row.get(self.col_vendor, "Unknown") if self.col_vendor else "Unknown",
                    "distance": row.get(self.col_distance, "0.0"),
                    "fare": row.get(self.col_fare, "0.0"),
                    "tip": row.get(self.col_tip, "0.0"),
                    "pickup_id": row.get(self.col_pickup_id, "0"),
                    "dropoff_id": row.get(self.col_dropoff_id, "0")
                }


class TaxiZoneDictionary:
    """METADATA MAPPER: Loads the zone file into memory for instant lookup translations."""
    
    def __init__(self, lookup_path: str):
        self.zones = {}
        if not os.path.exists(lookup_path):
            raise FileNotFoundError(f"❌ Cannot find lookup file at {lookup_path}")
        
        with open(lookup_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Map LocationID (as integer) to its geographic naming metadata
                self.zones[int(row['LocationID'])] = {
                    "borough": row['Borough'],
                    "zone": row['Zone']
                }

    def get_zone_details(self, location_id: int) -> dict:
        """Safely fetch names. Returns 'Unknown' fallback objects if ID isn't indexed."""
        return self.zones.get(location_id, {"borough": "Unknown", "zone": "Unknown"})


class CleanTrip:
    """THE SANITIZER: Validates types, enforces domain logic, and updates name indices."""
    
    def __init__(self, raw_record: dict, zone_lookup: TaxiZoneDictionary):
        self.is_valid = True
        
        try:
            # 1. Enforce strict numerical conversions (Catches text anomalies or blank spaces)
            self.vendor_id = raw_record["vendor_id"]
            self.distance = float(raw_record["distance"])
            self.fare = float(raw_record["fare"])
            self.tip = float(raw_record["tip"])
            
            # 2. Extract location IDs and cross-reference geographic tags
            self.pickup_id = int(raw_record["pickup_id"])
            self.dropoff_id = int(raw_record["dropoff_id"])
            
            pickup_info = zone_lookup.get_zone_details(self.pickup_id)
            self.pickup_borough = pickup_info['borough']
            self.pickup_zone = pickup_info['zone']

            # 3. Business Rule Validation: Exclude impossible pricing or tracking anomalies
            if self.fare <= 0 or self.distance <= 0:
                raise ValueError(f"Anomalous trip flagged: Distance={self.distance}, Fare=${self.fare}")

        except (ValueError, TypeError, KeyError) as e:
            # Document errors silently to a background text file without halting data flow
            logging.warning(f"Discarded record details: {raw_record} | Error: {e}")
            self.is_valid = False

    def __repr__(self):
        """Magic Dunder Method defining exactly how clean trips display inside a printed log."""
        return f"<CleanTrip Dist: {self.distance}mi | Fare: ${self.fare} | Tip: ${self.tip} | From: {self.pickup_zone}>"


class TaxiAnalyticsEngine:
    """THE ANALYTICS MATRIX: Converts clean objects into Pandas/NumPy matrices for analytics."""
    
    def __init__(self, clean_trips_list: list):
        # Day 5 Skill: Transform our structured OOP objects into a high-performance DataFrame
        data_matrix = [
            {
                "distance": trip.distance,
                "fare": trip.fare,
                "tip": trip.tip,
                "pickup_zone": trip.pickup_zone
            }
            for trip in clean_trips_list
        ]
        self.df = pd.DataFrame(data_matrix)

    def calculate_city_metrics(self):
        """Uses NumPy vectorized arithmetic to compute aggregate travel metrics."""
        print("\n📊 Calculating High-Level Operational Metrics...")
        
        # Day 4 Skill: Vectorized math using NumPy arrays instead of slow loops
        fares = self.df['fare'].to_numpy()
        tips = self.df['tip'].to_numpy()
        
        # Calculate overall tip performance across the city segment
        total_collected = np.sum(fares) + np.sum(tips)
        avg_tip_percentage = np.mean((tips / np.where(fares == 0, 1, fares)) * 100)
        
        print(f"   💰 Total Revenue Generated: ${total_collected:,.2f}")
        print(f"   📈 Average Tip Percentage: {avg_tip_percentage:.2f}%")

        # Day 5 Skill: Pandas GroupBy aggregation to map the tipping hotspots
        print("\n📍 Top 3 Highest Tipping Pickup Neighborhoods (Average $):")
        hotspots = self.df.groupby('pickup_zone')['tip'].mean().sort_values(ascending=False).head(3)
        
        for zone, avg_tip in hotspots.items():
            print(f"   🔹 {zone}: ${avg_tip:.2f} average tip")


# --- Unified Execution Blueprint ---
if __name__ == "__main__":
    # 📌 PATH ASSIGNMENTS: Paths match your directory perfectly
    LOOKUP_FILE = r"C:\Users\girishkumar.bm\Downloads\pp\taxi_zone_lookup.csv"
    DATA_FILE   = r"C:\Users\girishkumar.bm\Downloads\pp\nyc_taxi_data.csv" 
    
    print("🎬 Initialising Streamer and Sanitizer systems...")
    
    try:
        # 1. Load the geographic names into short-term index memory
        zone_db = TaxiZoneDictionary(LOOKUP_FILE)
        print("✅ Taxi zone lookup table indexed in memory successfully.")
        
        # 2. Fire up the smart conveyor belt on the heavy ride data file
        streamer = TaxiDataStreamer(DATA_FILE)
        conveyor_belt = streamer.stream_trips()
        
        clean_storageBatch = []
        
        print("🏃 Extracting and cleaning records for analysis...")
        # Stream the first 500 records into memory to build a batch report sample
        for _ in range(500):
            try:
                raw_record = next(conveyor_belt)
                cleaned_trip = CleanTrip(raw_record, zone_db)
                if cleaned_trip.is_valid:
                    clean_storageBatch.append(cleaned_trip)
            except StopIteration:
                break
                
        print(f"✅ Successfully cleaned and stored {len(clean_storageBatch)} trips in memory.")
        print("-" * 75)
        
        # 3. Launch the high-performance analytics machine!
        if clean_storageBatch:
            engine = TaxiAnalyticsEngine(clean_storageBatch)
            engine.calculate_city_metrics()
        else:
            print("⚠️ No valid records found to analyse.")
            
        print("-" * 75)
        print("📊 Pipeline complete! The conveyor belt is clean and metrics are extracted.")

    except FileNotFoundError as e:
        print(e)
