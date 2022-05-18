# Authors: Mayur Ryali and Tyler Pastor
# Date: 5/09/22

from googleplaces import GooglePlaces, types, lang
import requests
import json
from ast import literal_eval
import mysql.connector
from mysql.connector import Error

def sat_fat_score(val):
    score = 10
    intervals = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    for index in range(11):
        if val <= intervals[index]:
            score = score - 1
        else:
            return score
    return score

def sugar_score(val):
    score = 10
    intervals = [45, 40, 36, 31, 27, 22.5, 18, 13.5, 9, 4.5, 0]
    for index in range(11):
        if val <= intervals[index]:
            score = score - 1
        else:
            return score
    return score

def sodium_score(val):
    # convert from mg to g
    # if val >= 1000:
    #     val = val / 1000
    score = 10
    intervals = [900, 810, 720, 630, 540, 450, 360, 270, 180, 90, 0]
    for index in range(11):
        if val <= intervals[index]:
            score = score - 1
        else:
            return score
    return score

def energy_score(val):
    # convert calories to Kilojoules
    val = val * 4.184
    score = 10
    intervals = [3350, 3015, 2680, 2345, 2010, 1675, 1340, 1005, 670, 335, 0]
    for index in range(11):
        if val <= intervals[index]:
            score = score - 1
        else:
            return score
    return score

def fiber_score(val):
    score = 5
    intervals = [3.5, 2.8, 2.1, 1.4, 0.7, 0]
    for index in range(6):
        if val <= intervals[index]:
            score = score - 1
        else:
            return score
    return score

def protein_score(val):
    score = 5
    intervals = [8.0, 6.4, 4.8, 3.2, 1.6, 0]
    for index in range(6):
        if val <= intervals[index]:
            score = score - 1
        else:
            return score
    return score

# Connect to mysql database
try:
    connection = mysql.connector.connect(host='localhost',
                                         database='FoodDict',
                                         user='root',
                                         password='HamamaCS*359')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)

# finalScore = 0
# x = 1233
# y = 1260
# for j in range(x, y):
#     i = str(j)
#     satFatQuery = ("SELECT val"
#                  " FROM fooddictionary"
#                 " WHERE obj = " + i +
#                 " AND `key` = 'SAT. FAT (g)';")
#     cursor.execute(satFatQuery)
#     result = cursor.fetchall()
#     if result != []:
#         satFalVal = float(result[0][0])
#     else:
#         satFalVal = 0.0
#
#     calQuery = ("SELECT val"
#                  " FROM fooddictionary"
#                 " WHERE obj = " + i +
#                 " AND `key` = 'CAL';")
#     cursor.execute(calQuery)
#     result = cursor.fetchall()
#     if result != []:
#         calVal = float(result[0][0])
#     else:
#         calVal = 0.0
#
#     sodiumQuery = ("SELECT val"
#                  " FROM fooddictionary"
#                 " WHERE obj = " + i +
#                 " AND `key` = 'SODIUM (mg)';")
#     cursor.execute(sodiumQuery)
#     result = cursor.fetchall()
#     if result != []:
#         sodiumVal = float(result[0][0])
#     else:
#         sodiumVal = 0.0
#
#     sugarQuery = ("SELECT val"
#                  " FROM fooddictionary"
#                 " WHERE obj = " + i +
#                 " AND `key` = 'SUGAR (g)';")
#     cursor.execute(sugarQuery)
#     result = cursor.fetchall()
#     if result != []:
#         sugarVal = float(result[0][0])
#     else:
#         sugarVal = 0.0
#
#     proteinQuery = ("SELECT val"
#                  " FROM fooddictionary"
#                 " WHERE obj = " + i +
#                 " AND `key` = 'PROTEIN (g)';")
#     cursor.execute(proteinQuery)
#     result = cursor.fetchall()
#     if result != []:
#         proteinVal = float(result[0][0])
#     else:
#         proteinVal = 0.0
#
#
#     fiberQuery = ("SELECT val"
#                  " FROM fooddictionary"
#                 " WHERE obj = " + i +
#                 " AND `key` = 'FIBER (g)';")
#     cursor.execute(fiberQuery)
#     result = cursor.fetchall()
#     if result != []:
#         fiberVal = float(result[0][0])
#     else:
#         fiberVal = 0.0
#
#     score_a = energy_score(calVal) + sat_fat_score(satFalVal) + sugar_score(sugarVal) + sodium_score(sodiumVal)
#     score_c = fiber_score(fiberVal) + protein_score(proteinVal)
#     score_total = score_a - score_c
#
#     finalScore = finalScore + score_total
#
# finalScore = finalScore / (y-x)
#
# file = open('FoodScore.txt', 'a')
# file.write('In-N-Out Burger!' + str(finalScore) + '\n')
# file.close()

# cursor.close()
API_KEY = "AIzaSyDbYCT-HEriitGRU9Jg_eT65DNoQ-VRc4w"

def TextSearch(address):
    newAddress = ""
    prev = 0

    for i in range(0, len(address)):
        if address[i] == " " and i != (len(address) - 1):
            newAddress += (address[prev:i] + "%20")
            prev = i + 1

    address = newAddress + address[prev:i + 1]

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + address + "&key=" + API_KEY
    return url

def NearbySearch(location, radius, type):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + location + "&radius=" + radius + \
          "&type=" + type + "&rankby=prominence&key" + API_KEY

    return url

userAddress = input("Address: ")

t_url = TextSearch(userAddress)

# extract the latitude and longitude for the inputted address
r = requests.get(t_url)
r.json()

lat_lon_results = literal_eval(r.text)
results = lat_lon_results["results"]

str = results[0]

geometry = str["geometry"]
location = geometry["location"]
lat_coor = location["lat"]
lng_coor = location["lng"]


google_places = GooglePlaces(API_KEY)

print()
print("My Location's Coordinates: ")
print ('lat', lat_coor)
print('lng', lng_coor)
print()

print('\n-------- Restaurant List ----------\n')

restaurant_list = google_places.nearby_search(
            #location = 'Los Angeles, California', #location of search
            keyword = 'restaurant', #keyword to search for indexed in Google databases
            radius = 8046.72, #measured in meters = 5 miles
            #open_now = True, #checks if places found are open at the time of query search; only in radar search
            #min_price = 1,
            #max_price = 4,
            types = [types.TYPE_RESTAURANT], #look only for places associated with restaurants
            #lat_lng = {'lat':34.250306663736005, 'lng':-118.73379071322077} #My house
            lat_lng = {'lat':lat_coor, 'lng':lng_coor} #My house
        )

avg_score = 0
num_rest = 0
area_score = 0
count = 0

for location in restaurant_list.places: #print location details
    print('Name: ', location.name) #location name
    # print('Geolocation: ', location.geo_location) #location latitude and longitude
    #
    # location.get_details() #Retrieves full details on found location
    #
    # print('Rating: ', location.rating) #locating customer rating on google maps
    # print('Website: ', location.website) #location website
    # print('Maps Link: ', location.url) #google maps link for location
    print('\n')  # newline

    num_rest = num_rest + 1
    if location.name == "The Habit Burger Grill":
        habitQuery = ("SELECT score"
                      " FROM foodscores"
                      " WHERE rest = 'The Habit Burger Grill';")
        cursor.execute(habitQuery)
        result = cursor.fetchall()
        if result != []:
            area_score = area_score + result[0][0]
            count = count + 1
    elif location.name == "Chick-fil-A":
        chickQuery = ("SELECT score"
                      " FROM foodscores"
                      " WHERE rest = 'Chick-fil-A';")
        cursor.execute(chickQuery)
        result = cursor.fetchall()
        if result != []:
            area_score = area_score + result[0][0]
            count = count + 1
    elif location.name == "Del Taco":
        delQuery = ("SELECT score"
                      " FROM foodscores"
                      " WHERE rest = 'Del Taco';")
        cursor.execute(delQuery)
        result = cursor.fetchall()
        if result != []:
            area_score = area_score + result[0][0]
            count = count + 1
    elif location.name == "Taco Bell":
        tacoQuery = ("SELECT score"
                      " FROM foodscores"
                      " WHERE rest = 'Taco Bell';")
        cursor.execute(tacoQuery)
        result = cursor.fetchall()
        if result != []:
            area_score = area_score + result[0][0]
            count = count + 1
    elif location.name == "Subway":
        subQuery = ("SELECT score"
                      " FROM foodscores"
                      " WHERE rest = 'Subway';")
        cursor.execute(subQuery)
        result = cursor.fetchall()
        if result != []:
            area_score = area_score + result[0][0]
            count = count + 1
    elif location.name == "Panda Express":
        pandaQuery = ("SELECT score"
                      " FROM foodscores"
                      " WHERE rest = 'Panda Express';")
        cursor.execute(pandaQuery)
        result = cursor.fetchall()
        if result != []:
            area_score = area_score + result[0][0]
            count = count + 1
    elif location.name == "Burger King":
        burgerQuery = ("SELECT score"
                      " FROM foodscores"
                      " WHERE rest = 'Burger King';")
        cursor.execute(burgerQuery)
        result = cursor.fetchall()
        if result != []:
            area_score = area_score + result[0][0]
            count = count + 1
    elif location.name == "In-N-Out Burger":
        inQuery = ("SELECT score"
                      " FROM foodscores"
                      " WHERE rest = 'In-N-Out Burger';")
        cursor.execute(inQuery)
        result = cursor.fetchall()
        if result != []:
            area_score = area_score + result[0][0]
            count = count + 1
    elif location.name == "Wendy's":
        wendyQuery = ("SELECT score"
                   " FROM foodscores"
                   " WHERE rest = 'Wendy's';")
        cursor.execute(wendyQuery)
        result = cursor.fetchall()
        if result != []:
            area_score = area_score + result[0][0]
            count = count + 1

avg_score = area_score / count
print("The score for the area is: ", avg_score)
print("Total restaurants found: ", num_rest)
print("Total restaurants scored: ", count)
cursor.close()
#
#     print('\n') #newline
#
#
# # print('-------- Market List ----------\n')
# #
# # market_list = google_places.nearby_search(
# #             #location = 'Los Angeles, California', #location of search
# #             keyword = 'market', #keyword to search for indexed in Google databases
# #             radius = 8046.72, #measured in meters = 5 miles
# #             #open_now = True, #checks if places found are open at the time of query search; only in radar search
# #             #min_price = 1,
# #             #max_price = 4,
# #             types = [types.TYPE_FOOD], #look only for places associated with restaurants
# #             #lat_lng = {'lat':34.250306663736005, 'lng':-118.73379071322077} #My house
# #             lat_lng = {'lat':lat_coor, 'lng':lng_coor} #My house
# #         )
#
# # for location in market_list.places: #print location details
# #     print('Name: ', location.name) #location name
# #     print('Geolocation: ', location.geo_location) #location latitude and longitude
# #
# #     location.get_details() #Retrieves full details on found location
# #
# #     print('Rating: ', location.rating) #locating customer rating on google maps
# #     print('Website: ', location.website) #location website
# #     print('Maps Link: ', location.url) #google maps link for location
# #
# #     print('\n') #newline
#

# finally:
#     if connection.is_connected():
#         cursor.close()
#         connection.close()
#         print("MySQL connection is closed")
