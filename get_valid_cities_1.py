import sys
import psycopg2
import csv
import json
import time
from unidecode import unidecode
from geopy.geocoders import GoogleV3

KEY = "AIzaSyDh6VDAlY4mgERLJInni8HSlzsmUwSLpC4"
KEY2 = "AIzaSyArCEdUsoersVSfoQjWWuul_S00icbAT2A"
invalid = {}
geocodeErrors = {}
valid = set()
output = open('cleaned_and_pruned.csv','w', newline='', encoding='utf8')
errors = open('errors.json', 'w', encoding='utf8')
geocodeErrorsFile = open('geocode_errors.json', 'w', encoding='utf8')

#pass in a row to start from in case of geocode error
startRow = 1
if len(sys.argv) > 1:
    startRow = int(sys.argv[1])

with open('cleaned.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    writer = csv.DictWriter(output, fieldnames = reader.fieldnames)
    writer.writeheader()
    rowNum = 1
    geolocator = GoogleV3(KEY2, timeout=30, )
    for row in reader:
        if rowNum >= startRow:
            place = row["PLACE"]
            if place in valid:
                #write to output
                writer.writerow(row)
            elif place in invalid:
                #add row number to errors
                invalid[place].append(rowNum)
            else:
                #check location validity
                print("ROW " + str(rowNum) + " " + place)
                hasCity = False
                addressMatches = True

                try:
                    location = geolocator.geocode(place)
                    if location:
                        normalizedAddress = unidecode(location.address)
                        print(normalizedAddress)
                        for placeComponent in place.split():
                            if unidecode(placeComponent) not in normalizedAddress:
                                addressMatches = False
                                break
                        for component in location.raw["address_components"]:
                            if "locality" in component["types"] or 'administrative_area_level_3' in component['types']:
                                hasCity = True
                                break
                    if not location or not hasCity or not addressMatches:
                        invalid[place] = [rowNum]
                    else:
                        valid.add(place)
                        writer.writerow(row)
                    time.sleep(0.1)
                    
                except Exception:
                    print("geocode error")
                    if place in geocodeErrors.keys():
                        geocodeErrors[place].append(rowNum)
                    else:
                        geocodeErrors[place] = [rowNum]
        rowNum += 1
    csvfile.close()
output.close()
#write errors dictionary to file
json.dump(invalid, errors)
errors.close()
#write geocode errors to dictionary
json.dump(geocodeErrors, geocodeErrorsFile)
geocodeErrorsFile.close()