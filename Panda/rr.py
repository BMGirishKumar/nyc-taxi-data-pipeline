import csv
import random
import os

folder_path = r"C:\Users\girishkumar.bm\Downloads\pp"
file_path = os.path.join(folder_path, "nyc_taxi_data.csv")

# A sample list of columns based on standard NYC Data
headers = ["VendorID", "trip_distance", "fare_amount", "tip_amount", "PULocationID", "DOLocationID"]

print(f"📦 Generating local mock dataset at: {file_path}...")

with open(file_path, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(headers) # Write the headers first
    
    for i in range(1000):
        # 1. 95% of the time, write perfectly normal taxi rides
        if random.random() > 0.05:
            vendor = str(random.choice([1, 2]))
            distance = round(random.uniform(0.5, 15.0), 2)
            fare = round(distance * 3.5 + 2.5, 2)
            # Pick a realistic tip amount
            tip = round(fare * random.choice([0.15, 0.18, 0.20]), 2)
            # Pick location IDs that match your lookup file
            pu_id = random.choice([1, 43, 132, 142, 230]) 
            do_id = random.choice([1, 43, 132, 142, 230])
        
        # 2. 5% of the time, inject broken data (negative fares, zero distance) to test our Sanitizer
        else:
            vendor = str(random.choice([1, 2]))
            distance = 0.0 if random.choice([True, False]) else round(random.uniform(0.5, 5.0), 2)
            fare = -10.0 if distance == 0.0 else round(random.uniform(5.0, 20.0), 2)
            tip = 0.0
            pu_id = 999 # Non-existent zone
            do_id = 999

        writer.writerow([vendor, distance, fare, tip, pu_id, do_id])

print("✅ Success! 1,000 taxi trip logs generated offline. You are ready to run your pipeline.")
