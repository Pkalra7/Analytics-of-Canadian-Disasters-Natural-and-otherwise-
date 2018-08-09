import sys
import psycopg2
import csv
from geopy.geocoders import GoogleV3

output = open('cleaned.csv','w', newline='', encoding="utf8")

provinceShortCodes = [
    " AB", 
    " BC", 
    " MB", 	
    " NB", 
    " NL", 
    " NS",
    " NT",
    " NU",
    " ON", 
    " PE",
    " QC",
    " SK",
    " YT",
]

def parseCities(cities):
    parts = cities.split(",")
    cities = []
    provinceString = ""
    lastIndex = len(parts) - 1
    for i in range(lastIndex, -1, -1):
        if i == lastIndex:
            subparts = parts[i].split(" and ")
            for j in range(len(subparts) - 1, -1, -1):
                cityString = subparts[j].strip()
                for provinceCode in provinceShortCodes:
                    if provinceCode in cityString:
                        cityString = cityString.replace(provinceCode, "")
                        provinceString = provinceCode
                        break
                cities.append(cityString + provinceString)
        else:
            cityString = parts[i].strip()
            for provinceCode in provinceShortCodes:
                if provinceCode in cityString:
                    cityString = cityString.replace(provinceCode, "")
                    provinceString = provinceCode
                    break
            cities.append(cityString + provinceString)
    print(cities)
    return cities

with open('CanadianDisasterDatabase.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    writer = csv.DictWriter(output, fieldnames=reader.fieldnames)
    writer.writeheader()
    rowNum = 1
    for row in reader:
        place = row["PLACE"]
        cities = parseCities(place)
        for city in cities:
            newRow = dict.copy(row)
            newRow["PLACE"] = city
            writer.writerow(newRow)
        rowNum += 1
    csvfile.close()
output.close()
