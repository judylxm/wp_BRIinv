import readExcel
import csv
from datetime import datetime
import pycountry_convert as pc
import pymysql
import SQLFunction as sql

PATH = "/root/word/"

if __name__ == '__main__':
    starttime = datetime.now()
    csvFile = open(PATH + "AgreementsList.csv", "r")
    reader = csv.reader(csvFile)
    result = {}
    RTAName = ""
    TYPE = ""
    date = ""
    Signatories = ""
    codeList = []
    for item in reader:
        if reader.line_num == 1:
            RTAName = item[0]
            TYPE = item[2]
            date = item[5]
            Signatories = item[7]
            continue
        if "/" in item[5]:
            time = datetime.strptime(item[5].split("(", 1)[0], '%d-%b-%Y')
        else:
            time = datetime.strptime(item[5], '%d-%b-%y')
        countries = item[7].split(";")
        countriesCode = []
        for each in countries:
            if 'UNMIK/Kosovo' == each.lstrip():
                continue
            if 'Hong Kong, China' == each.lstrip():
                continue
            if 'Macao, China' == each.lstrip():
                continue
            if 'Bahrain, Kingdom of' == each.lstrip():
                each = "Bahrain"
            if 'Kuwait, the State of' == each.lstrip():
                each = 'Kuwait'
            if 'Saudi Arabia, Kingdom of' == each.lstrip():
                each = 'Saudi Arabia'
            if 'Chinese Taipei' == each.lstrip():
                continue
            if 'C__d\'Ivoire' == each.lstrip():
                each = 'Ivory Coast'
            if 'Faeroe Islands' == each.lstrip():
                each = 'Faroe Islands'
            if 'The Gambia' == each.lstrip():
                continue
            if 'Falkland Islands (Islas Malvinas)' == each.lstrip():
                continue
            if 'Netherlands Antilles' == each.lstrip():
                continue
            if 'Aruba, the Netherlands with respect to' == each.lstrip():
                continue
            if 'British Overseas Territory of Saint Helena, Ascension and Tristan da Cunha' == each.lstrip():
                continue
            if 'Wallis and Futuna Islands' == each.lstrip():
                continue
            code = pc.country_name_to_country_alpha3(each.lstrip())
            if code not in codeList:
                codeList.append(code)
            countriesCode.append(code)
        row = {TYPE: item[2], date: time, Signatories: countriesCode}
        result[item[0]] = row

    matrix = [["code1","code2"]]
    for year in range(2000,2023):
        matrix[0].append(str(year))
    for code1 in codeList:
        for code2 in codeList:
            if code1 == code2:
                continue
            row = [code1, code2]
            for year in range(2000, 2023):
                row.append(0)
            matrix.append(row)

    for value in result.values():
        if 'FTA' not in value['Type']:
            continue
        for code1 in value['Signatories']:
            for code2 in value['Signatories']:
                if code1 == code2:
                    continue
                year = value['Date of entry into force'].year
                month = value['Date of entry into force'].month
                if month >= 7:
                    year += 1
                for row in matrix:
                    if code1 == row[0] and code2 == row[1]:
                        if year >= 2000:
                            for mark in range(year - 2000 + 2, 2022 - 2000 + 3):
                                row[mark] = 1
    endtime = datetime.now()

    database = pymysql.connect(host=sql.LOCALHOST, port=sql.PORT, user=sql.USER, password=sql.PASSWORD,
                               database=sql.DATABASE)
    # readExcel.saveExcel(matrix,"1.xls")
    cnt = 0

    starttime = datetime.now()
    for row in range(1, len(matrix)):
        for col in range(2, len(matrix[row])):
            sql.addTradecostValue(database, matrix[row][0],matrix[row][1], col - 2 + 2000,
                         matrix[row][col], sql.TYPE.RTA)
            cnt += 1


    endtime = datetime.now()

