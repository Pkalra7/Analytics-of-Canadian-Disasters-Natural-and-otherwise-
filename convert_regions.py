import sys
import psycopg2
import csv
from geopy.geocoders import GoogleV3

output = open('region_to_cities.csv','w', newline='')

region_to_cities = {
    'Nova Scotia':['Halifax NS'], 
    'Prairie Provinces':['Winnipeg MB', 'Calgary AB', 'Edmonton AB', 'Saskatoon SK', 'Regina SK'], #Manitoba, Alberta, Saskatchewan 
    'Ontario':['Toronto ON', 'Ottawa ON'], 
    'British Columbia':['Vancouver BC'], 
    'Southern Alberta':['Lethbridge AB'], 
    'Alberta':['Calgary AB', 'Edmonton AB'], 
    'Saskatchewan':['Saskatoon SK', 'Regina SK'],
    'Manitoba':['Winnipeg MB'],
    'Newfoundland':["St John's NL"], 
    'Southern Ontario':['Toronto ON', 'Ottawa ON'], 
    'Maritime Provinces':['Halifax NS', 'Moncton NB', 'Charlottetown PE'], #Nova Scotia, New Brunswick, PEI 
    'Central Ontario':['Barrie ON'], 
    'New Brunswick':['Moncton NB'], 
    'Prince Edward Island':['Charlottetown PE'], 
    'Quebec':['Montreal QC', 'Quebec City QC'], 
    'Southern Manitoba':['Winnipeg MB']
}

with open('cleaned.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    writer = csv.DictWriter(output, fieldnames=reader.fieldnames)
    writer.writeheader()
    rowNum = 1
    for row in reader:
        place = row["PLACE"]
        if place in region_to_cities.keys():
            cities = region_to_cities[place]
            for city in cities:
                newRow = dict.copy(row)
                newRow["PLACE"] = city
                writer.writerow(newRow)
        rowNum += 1
    csvfile.close()
output.close()