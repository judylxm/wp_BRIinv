import pymysql
import xlrd
import openpyxl
import SQLFunction as sql
import readExcel as readExcel
import datetime
import readDTA as rD

PATH = "/root/word/"

if __name__ == '__main__':
    database = pymysql.connect(host=sql.LOCALHOST, port=sql.PORT, user=sql.USER, password=sql.PASSWORD,
                               database=sql.DATABASE)

    codeSheet = readExcel.getExcelToSheet(PATH + 'code.xls')
    gdpSheet = readExcel.getExcelToSheet(PATH + 'gdp.xls')
    invOECDSheet = readExcel.getExcelToSheet(PATH + 'invest_oecd_sum.xls')
    invWBSheet = readExcel.getExcelToSheet(PATH + 'invest_worldbank.xls')

    # add code
    starttime = datetime.datetime.now()
    for row in range(1, readExcel.getSheetRow(codeSheet)):
        sql.addCode(database, readExcel.getValue(codeSheet, row, 0),
                    readExcel.getValue(codeSheet, row, 1), readExcel.getValue(codeSheet, row, 2))
    endtime = datetime.datetime.now()

    # add GDP
    starttime = datetime.datetime.now()
    for row in range(4, readExcel.getSheetRow(gdpSheet)):
        for col in range(4, readExcel.getSheetCol(gdpSheet)):
            sql.addValue(database, readExcel.getValue(gdpSheet, row, 1), col - 4 + 1960,
                         readExcel.getValue(gdpSheet, row, col), sql.TYPE.GDP)
    endtime = datetime.datetime.now()

    # add inv_OECD
    starttime = datetime.datetime.now()
    for row in range(1, readExcel.getSheetRow(invOECDSheet)):
        sql.addValue(database, readExcel.getValue(invOECDSheet, row, 0),
                     readExcel.getValue(invOECDSheet, row, 1),
                     readExcel.getValue(invOECDSheet, row, 2),
                     sql.TYPE.INV_OECD)
    endtime = datetime.datetime.now()

    # add inv_worldbank
    starttime = datetime.datetime.now()
    for row in range(4, readExcel.getSheetRow(invWBSheet)):
        for col in range(4, readExcel.getSheetCol(invWBSheet)):
            sql.addValue(database, readExcel.getValue(invWBSheet, row, 1), col - 4 + 1960,
                         readExcel.getValue(invWBSheet, row, col), sql.TYPE.INV_WB)
    endtime = datetime.datetime.now()


    # add tij
    starttime = datetime.datetime.now()
    df = rD.load_large_dta(PATH + '20200603-ESCAP-WB-tradecosts-dataset.dta')
    endtime = datetime.datetime.now()
    starttime = datetime.datetime.now()
    cnt = 0
    for row in df.iterrows():
        if rD.isGTT(row):
            sql.addTradecostValue(database, rD.getReporter(row),
                                  rD.getPartner(row),
                                  rD.getYear(row),
                                  rD.getTij(row),
                                  sql.TYPE.TIJ)
            sql.addTradecostValue(database,  rD.getReporter(row),
                                  rD.getPartner(row),
                                  rD.getYear(row),
                                  rD.getTraiff(row),
                                  sql.TYPE.TRAIFF)
            cnt += 1

    endtime = datetime.datetime.now()
    database.close()
