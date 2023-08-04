import csv
import json

# this function reads and extracts data from the LocationId column of the 'results.csv' file and places it within the json data of each row of the Inventory column. It then creates/writes a 'data.csv' file with just rows of the updated json data


def location_to_inventory():
    csv_file_path = '/Users/saganj/workplace/JSONtoCSV/src/Converter/results.csv'
    output_file = 'data.csv'

    updated_rows = []
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)

        for row in reader:

            location_id = row[0]

            inventory_data = json.loads(row[3])

            for item in inventory_data:
                item['M']['Bucket']['S'] = {'locationId': location_id}

            updated_row = json.dumps(inventory_data)
            updated_rows.append(updated_row)

        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(zip(*[iter(updated_rows)]))


location_to_inventory()


# this function reads the updated json data from the 'data.csv' file and extracts specific data that matches with specific column names of the Cims csv template ('CIMS_Data.csv'). It then reads the Cims template and merges the extracted data with the CIMS template.
def json_to_csv():
    # Read the JSON data from the CSV file
    extracted_data = []
    with open('/Users/saganj/workplace/JSONtoCSV/data.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            json_data = json.loads(row[0])
            for item in json_data:
                location_id = item['M']['Bucket']['S']['locationId']
                target_inventory = item['M']['TargetInventory']['N']
                min_inventory = item['M']['MinInventory']['N']
                asin = item['M']['ASIN']['S']
                max_inventory = item['M']['MaxInventory']['N']
                quantity = item['M']['Stock']['L'][0]['M']['Quantity']['N']
                extracted_data.append({
                    'Product ASIN': asin,
                    'Address ID': location_id,
                    'Maximum ': max_inventory,
                    'Minimum': min_inventory,
                    'Target Inventory Position': target_inventory,
                    'Audit Inventory Position': quantity
                })

    # Read the existing CIMS csv template file
    existing_data = []
    with open('/Users/saganj/workplace/JSONtoCSV/src/Converter/CIMS_Data.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            existing_data.append(row)

    # Merge the extracted data with the existing data from CIMS csv template file
    merged_data = []
    for extracted, existing in zip(extracted_data, existing_data):
        merged_row = {**existing, **extracted}
        merged_data.append(merged_row)

    # Write the merged data to a new CSV file
    fieldnames = list(merged_data[0].keys())
    with open('merged_csv_file.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(merged_data)


json_to_csv()
