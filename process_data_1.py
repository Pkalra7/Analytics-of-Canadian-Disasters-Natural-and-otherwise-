import sys
import psycopg2
import csv
import time
from dateutil import parser
from datetime import datetime
from datetime import date
from geopy import exc
from geopy.geocoders import GoogleV3

KEY = "AIzaSyArCEdUsoersVSfoQjWWuul_S00icbAT2A"
KEY2 = "AIzaSyDh6VDAlY4mgERLJInni8HSlzsmUwSLpC4"
KEY3 = "AIzaSyAuM8TbMttBGBqne-v3RdFu30pJhCko4V4"

INSERT_FACT = "INSERT INTO FACTCASUALTIES (start_date_key, end_date_key, location_key, disaster_key, description_key, costs_key, fatalities, injured, evacuated) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING casualty_key;"
INSERT_DISASTER = "INSERT INTO DIMDISASTER (disaster_type, disaster_subgroup, disaster_group, disaster_category, magnitude, utility_people_affected) VALUES(%s, %s, %s, %s, %s, %s) RETURNING disaster_key;"
INSERT_DATE = "INSERT INTO DIMDATE (date_actual, day_name, month_name, year_actual, weekend, season_canada, season_international) VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING date_key;"
INSERT_SUMMARY = "INSERT INTO DIMSUMMARY (summary, keyword_one, keyword_two, keyword_three) VALUES(%s, %s, %s, %s) RETURNING description_key;"
INSERT_COSTS = "INSERT INTO DIMCOSTS (estimated_total_cost, normalized_total_cost, federal_payments, provincial_payments, provincial_department_payments, municipal_costs, ogd_costs, insurance_payments, ngo_payments) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING costs_key;"
INSERT_LOCATION = "INSERT INTO DIMLOCATION (city, province, country, canada) VALUES(%s, %s, %s, %s) RETURNING location_key;"

disaster_ids = {}
date_ids = {}
summary_ids = {}
cost_ids = {}
location_ids = {}

NORTH_TO_SOUTH_SEASONS = {
    "winter":"summer",
    "spring":"autumn",
    "summer":"winter",
    "autumn":"spring"
}

Y = 2000 # dummy leap year to allow input X-02-29 (leap day)
SEASONS = [('winter', (datetime(Y,  1,  1),  datetime(Y,  3, 20))),
           ('spring', (datetime(Y,  3, 21),  datetime(Y,  6, 20))),
           ('summer', (datetime(Y,  6, 21),  datetime(Y,  9, 22))),
           ('autumn', (datetime(Y,  9, 23),  datetime(Y, 12, 20))),
           ('winter', (datetime(Y, 12, 21),  datetime(Y, 12, 31)))]

hostname = sys.argv[1]
database = sys.argv[2]
username = sys.argv[3]

password = None
if len(sys.argv) > 4:
    password = sys.argv[4]

port = 5432
if len(sys.argv) > 5:
    port = sys.argv[5]

connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database, port=port)
cursor = connection.cursor()
location = None
geolocator = GoogleV3(KEY3, timeout=30)

csvfile = open('cleaned_final.csv')
reader = csv.DictReader(csvfile)

errors = open('dbErrors.csv','w',newline='')
errorWriter = csv.DictWriter(errors, fieldnames=reader.fieldnames)

def valOrNone(val):
    if not val:
        return None
    return val

def valOrZero(val):
    if not val:
        return 0
    return val

def createFactRecord(data):
    global location
    try:
        print(data["PLACE"])
        location = geolocator.geocode(data["PLACE"])
    except exc.GeopyError:
        try:
            print("error: trying again...")
            location = geolocator.geocode(data["PLACE"])
        except exc.GeopyError:
            print("geocode error")
            errorWriter.writerow(data)
    print(location.address)
    time.sleep(0.1)
    startDateKey = getDateRecord(parser.parse(data["EVENT START DATE"]))
    endDateKey = getDateRecord(parser.parse(data["EVENT END DATE"]))
    locationKey = getLocationRecord()
    disasterKey = getDisasterRecord(data["EVENT CATEGORY"], data["EVENT TYPE"], data["EVENT GROUP"], data["EVENT SUBGROUP"], valOrNone(data["MAGNITUDE"]), valOrNone(data["UTILITY - PEOPLE AFFECTED"]))
    descriptionKey = getSummaryRecord(data["COMMENTS"])
    costKey = getCostsRecord(   valOrNone(data["ESTIMATED TOTAL COST"]),
                                valOrNone(data["NORMALIZED TOTAL COST"]), 
                                valOrNone(data["FEDERAL DFAA PAYMENTS"]), 
                                valOrNone(data["PROVINCIAL DFAA PAYMENTS"]), 
                                valOrNone(data["PROVINCIAL DEPARTMENT PAYMENTS"]), 
                                valOrNone(data["MUNICIPAL COSTS"]), 
                                valOrNone(data["OGD COSTS"]), 
                                valOrNone(data["INSURANCE PAYMENTS"]), 
                                valOrNone(data["NGO PAYMENTS"]))
    fatalities = valOrNone(data["FATALITIES"])
    injured = valOrNone(data["INJURED / INFECTED"])
    evacuated = valOrNone(data["EVACUATED"])
    cursor.execute(INSERT_FACT, (startDateKey, endDateKey, locationKey, disasterKey, descriptionKey, costKey, fatalities, injured, evacuated))

def getDateRecord(date):
    if date in date_ids.keys():
        return date_ids[date]
    season = getSeason(date)
    print(season)
    isWeekend = date.weekday() < 5
    season_canada = None
    season_international = None
    if "Canada" in location.address:
        season_canada = season
    else:
        season_international = season
    cursor.execute(INSERT_DATE, (date.strftime('%Y-%m-%d'), date.strftime('%A'), date.strftime('%B'), date.year, isWeekend, season_canada, season_international))
    dateKey = cursor.fetchone()[0]
    date_ids[date] = dateKey
    return dateKey

def getDisasterRecord(category, disaster_type, group, subgroup, magnitude, up_affected):
    disasterHash = ','.join(map(str, [category, disaster_type, group, subgroup, magnitude, up_affected]))
    if disasterHash in disaster_ids.keys():
        return disaster_ids[disasterHash]
    cursor.execute(INSERT_DISASTER, (disaster_type, subgroup, group, category, magnitude, up_affected))
    disasterKey = cursor.fetchone()[0]
    disaster_ids[disasterHash] = disasterKey
    return disasterKey

def getSummaryRecord(summary):
    if summary in summary_ids.keys():
        return summary_ids[summary]
    #TODO keyword extraction
    cursor.execute(INSERT_SUMMARY, (summary, None, None, None))
    summaryKey = cursor.fetchone()[0]
    summary_ids[summary] = summaryKey
    return summaryKey

def getCostsRecord(estimated_total, normalized_total, federal_dfaa, provincial_dfaa, provincial_department, municipal_costs, ogd_costs, insurance_payments, ngo_payments):
    costHash = ','.join(map(str, [estimated_total, normalized_total, federal_dfaa, provincial_dfaa, provincial_department, municipal_costs, ogd_costs, insurance_payments, ngo_payments]))
    if costHash in cost_ids.keys():
        return cost_ids[costHash]
    cursor.execute(INSERT_COSTS, (estimated_total, normalized_total, federal_dfaa, provincial_dfaa, provincial_department, municipal_costs, ogd_costs, insurance_payments, ngo_payments))
    costKey = cursor.fetchone()[0]
    cost_ids[costHash] = costKey
    return costKey

def getLocationRecord():
    if location.address in location_ids.keys():
        return location_ids[location.address]
    city = None
    province = None
    country = None
    for component in location.raw["address_components"]:
        if 'locality' in component["types"]:
            city = component["long_name"]
        if 'administrative_area_level_3' in component["types"] and city == None:
            city = component["long_name"]
        if 'administrative_area_level_1' in component["types"]:
            province = component["long_name"]
        if 'country' in component["types"]:
            country = component["long_name"]
    canada = "Canada" in location.address
    cursor.execute(INSERT_LOCATION, (city, province, country, canada))
    locationKey = cursor.fetchone()[0]
    location_ids[location.address] = locationKey
    return locationKey

def getSeason(date):
    dateCheck = datetime(
        year = Y,
        month = date.month,
        day = date.day
    )
    season_north = None
    for season, (start, end) in SEASONS:
        if start <= dateCheck <= end:
            season_north = season
            break
    if location.latitude < 0:
        return NORTH_TO_SOUTH_SEASONS[season_north]
    return season_north


rowNum = 1
for row in reader:
    print("Row " + str(rowNum))
    createFactRecord(row)
    rowNum += 1
connection.commit()
cursor.close()
connection.close()
csvfile.close()
errors.close()
