import sqlite3
import requests
import csv

def get_api_data(api_url,headers):
    response = requests.get(api_url,headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code)
        return None

def json_to_csv(json_data, csv_file):
    if json_data:
        fieldnames = json_data[0].keys()
        print(fieldnames)

        # Write JSON data to CSV
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(json_data)
        print(f"Data written to {csv_file}")
    else:
        print("No data to write")

def insert_into_DB(json_data):
    if json_data:
        # Connect to the SQLite database
        conn = sqlite3.connect('python_exercises.db')

        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY,
            wikiDataId TEXT,
            type TEXT,
            city TEXT,
            name TEXT,
            country TEXT,
            countryCode TEXT,
            region TEXT,
            regionCode TEXT,
            regionWdId TEXT,
            latitude REAL,
            longitude REAL,
            population INTEGER
        );
        '''

        cursor.execute(create_table_query)

        insert_query = 'INSERT INTO cities (id,wikiDataId,type,city,name,country,countryCode,region,regionCode,regionWdId,latitude,longitude,population) VALUES (:id,:wikiDataId,:type,:city,:name,:country,:countryCode,:region,:regionCode,:regionWdId,:latitude,:longitude,:population)'

        print(json_data)

        cursor.executemany(insert_query, json_data)

        conn.commit()

        conn.close()

api_url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
csv_file = 'api_data.csv'

headers = {
	"X-RapidAPI-Key": "2636fc2a6cmshe12aded30b561dcp132388jsn7f2610a57bd0",
	"X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
}

json_data = get_api_data(api_url,headers)
# print(json_data)
if json_data:
    json_to_csv(json_data['data'], csv_file)
    insert_into_DB(json_data['data'])