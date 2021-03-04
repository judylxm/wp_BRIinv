import pymysql
from enum import Enum
import math

LOCALHOST = 'localhost'
PORT = 3306
USER = 'root'
PASSWORD = '123456'
DATABASE = 'hikki'


class TYPE(Enum):
    GDP = 1
    INV_OECD = 2
    INV_WB = 3
    TIJ = 4
    TRAIFF = 5
    OECD = 6
    TARIFF = 7
    TC = 8
    PER_GDP = 9
    TARIFFVIVID = 10,
    RTA = 11
    CAPITAL = 12
    CAPITAL_DISTANCE = 13


switch = {TYPE.GDP: "GDP_WDI",
          TYPE.INV_OECD: "inv_oecd",
          TYPE.INV_WB: "inv_worldbank",
          TYPE.TIJ: "tij",
          TYPE.TRAIFF: "geometric_avg_tariff",
          TYPE.OECD: "oecd_pcgdp",
          TYPE.TARIFF: "tariff",
          TYPE.TC: "tc",
          TYPE.PER_GDP: "per_GDP",
          TYPE.TARIFFVIVID: "tariffVivid",
          TYPE.RTA: "RTA",
          TYPE.CAPITAL: "capital",
          TYPE.CAPITAL_DISTANCE: "captial_distance"}


def addYear(database, year):
    cursor = database.cursor()
    if isYear(database, year):
        return False
    clause = "INSERT INTO `Year`(`year`)VALUES (" + str(year) + ")"
    try:
        cursor.execute(clause)
        database.commit()
    except Exception as e:
        print(e)
        database.rollback()
    return True


def addRegion(database, region):
    cursor = database.cursor()
    if isRegion(database, region):
        return False
    clause = "INSERT INTO `Region`(`region`)VALUES ('" + region + "');"
    try:
        cursor.execute(clause)
        database.commit()
    except Exception as e:
        print(e)
        database.rollback()
    return True


def isYear(database, year):
    cursor = database.cursor()
    clause = "select * from `Year` where `year`=" + str(year) + ";"
    try:
        cursor.execute(clause)
        results = cursor.fetchall()
        return False if len(results) == 0 else True
    except Exception as e:
        print(e)


def isRegion(database, region):
    cursor = database.cursor()
    clause = "select * from `Region` where `region`='" + region + "';"
    try:
        cursor.execute(clause)
        results = cursor.fetchall()
        return False if len(results) == 0 else True
    except Exception as e:
        print(e)


def isCode(database, code):
    cursor = database.cursor()
    clause = "select * from `Code` where `code`='" + code + "';"
    try:
        cursor.execute(clause)
        results = cursor.fetchall()
        return False if len(results) == 0 else True
    except Exception as e:
        print(e)


def addCode(database, code, country='null', region='null'):
    cursor = database.cursor()
    if country == 'null':
        c1 = "',"
        c2 = ","
        c3 = ");"
    else:
        c1 = "','"
        c2 = "','"
        c3 = "');"
    if isCode(database, code):
        return False
    if not isRegion(database, region):
        addRegion(database, region)
    clause = "INSERT INTO `Code`(`code`,`country`,`region`) VALUES ('" + code + c1 + country + c2 + region + c3
    try:
        cursor.execute(clause)
        database.commit()
    except Exception as e:
        print(e)
        database.rollback()
    return True


def addValue(database, code, year, value, Type):
    cursor = database.cursor()
    if value != '':
        c = ","
    else:
        c = ",null"
    if not isCode(database, code):
        addCode(database, code)
    if not isYear(database, year):
        addYear(database, year)
    clause = "INSERT INTO `" + switch[Type] + "`(`code`,`year`,`value`) VALUES ('" \
             + code + "'," + str(year) + c + str(value) + ");"
    try:
        cursor.execute(clause)
        database.commit()
    except Exception as e:
        print(e)
        database.rollback()
    return True


def isNaN(num):
    return num != num


def addTradecostValue(database, reporter, partner, year, value, Type):
    cursor = database.cursor()
    if (value is not None) and (not isNaN(value)):
        if value == '..':
            c = ",null"
        else:
            c = "," + str(value)
    else:
        c = ",null"
    if not isCode(database, reporter):
        addCode(database, reporter)
    if not isCode(database, partner):
        addCode(database, partner)
    if not isYear(database, year):
        addYear(database, year)
    clause = "INSERT INTO `" + switch[Type] + "`(`reporter`,`partner`,`year`,`value`) VALUES ('" \
             + reporter + "','" + partner + "'," + str(year) + c + ");"
    try:
        cursor.execute(clause)
        database.commit()
    except Exception as e:
        print(e)
        database.rollback()
    return True


def addCapital(database, code, capital, Lng, Lat, Type):
    cursor = database.cursor()
    if not isCode(database, code):
        addCode(database, code)
    clause = "INSERT INTO `" + switch[Type] + "`(`code`,`capital`,`Lng`,`Lat`) VALUES ('" \
             + code + "','" + capital + "'," + str(Lng) + "," + str(Lat) + ");"
    try:
        cursor.execute(clause)
        database.commit()
    except Exception as e:
        print(e)
        database.rollback()
    return True


def addCapitalDistance(database, reporter, partner, value, Type):
    cursor = database.cursor()
    if not isCode(database, reporter):
        addCode(database, reporter)
    if not isCode(database, partner):
        addCode(database, partner)
    clause = "INSERT INTO `" + switch[Type] + "`(`reporter`,`partner`,`value`) VALUES ('" \
             + reporter + "','" + partner + "'," + str(value) + ");"
    try:
        cursor.execute(clause)
        database.commit()
    except Exception as e:
        print(e)
        database.rollback()
    return True
