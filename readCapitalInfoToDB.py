import json
import math
import SQLFunction as sql
import pycountry_convert as pc
from datetime import datetime
import pymysql

PATH = "/root/capitals/"
EARTH_REDIUS = 6378.137


def rad(d):
    return d * math.pi / 180.0


def getDistance(country1, country2):
    lat1 = country1["Lat"]
    lng1 = country1["Lng"]
    lat2 = country2["Lat"]
    lng2 = country2["Lng"]
    radLat1 = rad(lat1)
    radLat2 = rad(lat2)
    a = radLat1 - radLat2
    b = rad(lng1) - rad(lng2)
    s = 2 * math.asin(
        math.sqrt(math.pow(math.sin(a / 2), 2) + math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b / 2), 2)))
    s = s * EARTH_REDIUS
    return s


def getJsonObject(string):
    with open(PATH + string, 'r') as f:
        return json.loads(f.read())


def getCaptial(country):
    return country['properties']['capital']


def getCountry(country):
    return country['properties']['country']


def getLng(country):
    return country['geometry']['coordinates'][0]


def getLAT(country):
    return country['geometry']['coordinates'][1]


def getCode(country):
    if getCountry(country) == 'Cocos Islands':
        return pc.country_name_to_country_alpha3('Cocos (Keeling) Islands')
    elif getCountry(country) == 'Palestinian Territory':
        return ''
    elif getCountry(country) == 'Kosovo':
        return ''
    elif getCountry(country) == 'Vatican':
        return pc.country_name_to_country_alpha3('Holy See (Vatican City State)')
    elif getCountry(country) == 'Reunion':
        return pc.country_name_to_country_alpha3('Réunion')
    elif getCountry(country) == 'Saint Helena':
        return pc.country_name_to_country_alpha3('Saint Helena, Ascension and Tristan da Cunha')
    elif getCountry(country) == 'Netherlands Antilles':
        return ''
    elif getCountry(country) == 'U.S. Virgin Islands':
        return pc.country_name_to_country_alpha3('Virgin Islands, U.S.')
    return pc.country_name_to_country_alpha3(getCountry(country))


if __name__ == '__main__':
    asia = getJsonObject("asia.json")
    eu = getJsonObject("europe.json")
    africa = getJsonObject("africa.json")
    north_am = getJsonObject("north-america.json")
    oceania = getJsonObject("oceania.json")
    south_am = getJsonObject("south-america.json")
    countries = asia + eu + africa + north_am + oceania + south_am
    countriesList = []
    for country in countries:
        countryDict = {"Code": getCode(country),
                       "Capital": getCaptial(country),
                       "Lng": getLng(country),
                       "Lat": getLAT(country)}
        if countryDict["Code"] != '':
            countriesList.append(countryDict)
    database = pymysql.connect(host=sql.LOCALHOST, port=sql.PORT, user=sql.USER, password=sql.PASSWORD,
                               database=sql.DATABASE)
    print("正在添加capital……")
    starttime = datetime.now()
    for country in countriesList:
        sql.addCapital(database, country['Code'], country['Capital'], country['Lng'],
                       country['Lat'], sql.TYPE.CAPITAL)

    endtime = datetime.now()

    cnt = 0
    starttime = datetime.now()
    for country1 in countriesList:
        for country2 in countriesList:
            if country1 == country2:
                continue
            sql.addCapitalDistance(database, country1['Code'], country2['Code'],
                                   getDistance(country1, country2), sql.TYPE.CAPITAL_DISTANCE)
            cnt += 1

    endtime = datetime.now()

