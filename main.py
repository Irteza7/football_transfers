import os
import asyncio
import aiohttp
import csv
import pandas as pd
from transfers_data_scrape import fetch_for_year, request_headers, fetch
from utils import desired_fields

# async def main():
#     all_records = []
    
#     # Here, we're creating a new session for every year. This avoids any issues with reusing a session for too long.
#     for year in range(2013, 2024):
#         async with aiohttp.ClientSession(headers=request_headers) as session:
#             year_records = await fetch_for_year(year, session)
#             all_records.extend(year_records)

#     df = pd.DataFrame(all_records)
#     df.to_csv("output.csv", index=False)

# asyncio.run(main())


async def main():
    # Check if output.csv exists
    file_exists = os.path.isfile("output.csv")
    
    # Open the CSV file for writing or appending based on its existence
    with open("output.csv", "a" if file_exists else "w", newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.DictWriter(csvfile, fieldnames=desired_fields)
        
        # Only write the headers if the file didn't already exist
        if not file_exists:
            writer.writeheader()  # Writing the headers
        
        for year in range(2013, 2024):
            async with aiohttp.ClientSession(headers=request_headers) as session:
                year_records = await fetch_for_year(year, session)
                
                # Write the records of the year directly to the CSV file
                writer.writerows(year_records)

if __name__ == "__main__":
    asyncio.run(main())
