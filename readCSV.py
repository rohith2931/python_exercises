import csv
import json

def csv_to_json(csv_file, json_file):
    # Read CSV file and convert it to a list of dictionaries
    with open(csv_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)

    # Write the data as JSON to the specified file
    with open(json_file, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)


csv_to_json('trees.csv', 'data.json')
