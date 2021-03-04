import readExcel
import pycountry_convert as pc


def getCode(name):
    try:
        if name == 'Britain':
            return getCode('United Kingdom')
        if name == 'Trinidad-Tobago':
            return getCode('Trinidad and Tobago')
        if name == 'Sao Tome':
            return getCode('São Tomé and Príncipe')
        if name == 'Bosnia':
            return getCode('Bosnia and Herzegovina')
        if name == 'UAE':
            return getCode('United Arab Emirates')
        return pc.country_name_to_country_alpha3(name)
    except KeyError as e:
        print(e)


if __name__ == '__main__':
    fileName = "China_contracts_AEI.xls"
    codeFileName = "BRI_growth.xls"
    sum = {}
    sheet = readExcel.getExcelToSheet(readExcel.PATH + fileName)
    for i in range(6, readExcel.getSheetRow(sheet)):
        code = getCode(readExcel.getValue(sheet, i, 8))
        year = int(readExcel.getValue(sheet, i, 0))
        sector = readExcel.getValue(sheet, i, 6)
        if code not in sum:
            sum[code] = {}
        if year not in sum[code]:
            sum[code][year] = 0
        if sector == "Transport":
            sum[code][readExcel.getValue(sheet, i, 0)] += readExcel.getValue(sheet, i, 3)
    codeSheet = readExcel.getExcelToSheet(readExcel.PATH + codeFileName)
    orignSheet = []
    for i in range(0, readExcel.getSheetRow(codeSheet)):
        row = []
        for j in range(0, readExcel.getSheetCol(codeSheet)):
            row.append(readExcel.getValue(codeSheet, i, j))
        orignSheet.append(row)
    for i in range(1, len(orignSheet)):
        sum_1419 = 0
        if orignSheet[i][0] in sum:
            for year in range(2014, 2021):
                if year in sum[orignSheet[i][0]]:
                    sum_1419 += sum[orignSheet[i][0]][year]
        orignSheet[i][7] = sum_1419
    readExcel.saveExcel(orignSheet, "BRI_growth_done2.xls")
