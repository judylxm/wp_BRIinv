import pymysql
import xlrd
import openpyxl
import SQLFunction as sql
import readExcel as readExcel
import datetime
import readDTA as rD
import csv

PATH = "/root/word/"

if __name__ == '__main__':
    database = pymysql.connect(host=sql.LOCALHOST, port=sql.PORT, user=sql.USER, password=sql.PASSWORD,
                               database=sql.DATABASE)
    csvFile = open(PATH + 'oecd_pcgdp.csv', 'r')
    oecd = csv.reader(csvFile)

    starttime = datetime.datetime.now()
    firstLine = True
    for item in oecd:
        if firstLine:
            firstLine=False
            continue

        sql.addValue(database, item[0], int(item[5]), float(item[6]), sql.TYPE.OECD)
    endtime = datetime.datetime.now()

    invWBSheet = readExcel.getExcelToSheet(PATH + 'tariff.xls')

    #add inv_worldbank
    starttime = datetime.datetime.now()
    for row in range(5, readExcel.getSheetRow(invWBSheet)):
        for col in range(4, readExcel.getSheetCol(invWBSheet)):
            sql.addValue(database, readExcel.getValue(invWBSheet, row, 1), col - 4 + 1960,
                         readExcel.getValue(invWBSheet, row, col), sql.TYPE.TARIFF)
    endtime = datetime.datetime.now()


    tcSheet = readExcel.getExcelToSheet(PATH + 'tc.xls')
    #add inv_worldbank
    starttime = datetime.datetime.now()
    cnt = 0
    for row in range(2, readExcel.getSheetRow(tcSheet)):
        for col in range(6, readExcel.getSheetCol(tcSheet)):
            sql.addTradecostValue(database,
                                  readExcel.getValue(tcSheet, row, 1),
                                  readExcel.getValue(tcSheet, row, 3),
                                  col - 6 + 1995,
                                  readExcel.getValue(tcSheet, row, col),
                                  sql.TYPE.TC)
            cnt += 1


    endtime = datetime.datetime.now()


    pergdpSheet = readExcel.getExcelToSheet(PATH + 'gpd_per.xls')
    starttime = datetime.datetime.now()
    cnt = 0
    for row in range(5, readExcel.getSheetRow(pergdpSheet)):
        for col in range(4, readExcel.getSheetCol(pergdpSheet)):
            sql.addValue(database,
                         readExcel.getValue(pergdpSheet, row, 1),
                         col - 4 + 1960,
                         readExcel.getValue(pergdpSheet, row, col),
                         sql.TYPE.PER_GDP)
            cnt += 1


    endtime = datetime.datetime.now()


    invWBSheet = readExcel.getExcelToSheet(PATH + 'tariffVivid.xls')
    # add inv_worldbank
    starttime = datetime.datetime.now()
    for row in range(5, readExcel.getSheetRow(invWBSheet)):
        for col in range(4, readExcel.getSheetCol(invWBSheet)):
            sql.addValue(database, readExcel.getValue(invWBSheet, row, 1), col - 4 + 1960,
                         readExcel.getValue(invWBSheet, row, col), sql.TYPE.TARIFFVIVID)
    endtime = datetime.datetime.now()

