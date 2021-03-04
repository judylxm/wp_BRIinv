import readExcel
from decimal import Decimal

ORDER = 'intra-region'
BRI = 'BRI_growth_invest.xls'


def printSwitch(str):
    return str == ORDER


if __name__ == '__main__':
    coefficient = 'coefficient.xls'
    BRISheet = readExcel.getExcelToSheet(readExcel.PATH + BRI, 1)
    coefficientSheet = readExcel.getExcelToSheet(readExcel.PATH + coefficient)
    result = [['code1', 'country1', 'region1', 'code2', 'country2', 'region2', 'type', 'value']]
    for i in range(1, readExcel.getSheetRow(BRISheet)):
        for j in range(i, readExcel.getSheetRow(BRISheet)):
            if i == j:
                continue
            code1 = readExcel.getValue(BRISheet, i, 0)
            country1 = readExcel.getValue(BRISheet, i, 1)
            region1 = readExcel.getValue(BRISheet, i, 2)
            code2 = readExcel.getValue(BRISheet, j, 0)
            country2 = readExcel.getValue(BRISheet, j, 1)
            region2 = readExcel.getValue(BRISheet, j, 2)
            value = 0.0
            type = ''
            for k in range(1, readExcel.getSheetRow(coefficientSheet)):
                if region1 == readExcel.getValue(coefficientSheet, k, 0) and \
                        region2 == readExcel.getValue(coefficientSheet, k, 1):
                    value = readExcel.getValue(BRISheet, i, 5) \
                            * readExcel.getValue(coefficientSheet, k, 3) \
                            + readExcel.getValue(BRISheet, j, 5) \
                            * readExcel.getValue(coefficientSheet, k, 4)
                    type = readExcel.getValue(coefficientSheet, k, 2)
            result.append([code1, country1, region1, code2, country2, region2, type, value])

    f = open("res.txt", 'w')
    for each in result[1:]:
        each[7] *= 100
        if each[7] > 100:
            each[7] = 100
        if each[7] < -100:
            each[7] = -100
        if each[7] > 0 and printSwitch(each[6]):
            str1 ="Shock tms(TRAD_COMM,\"" + each[0] + "\",\"" + each[3] + "\") = rate%+" + str(Decimal(each[7]).quantize(Decimal("0.00"))) + " from file tms.shk;"
            f.write(str1)
            f.write("\n")
        if each[7] < 0 and printSwitch(each[6]):
            str1 = "Shock tms(TRAD_COMM,\"" + each[0] + "\",\"" + each[3] + "\") = rate%" + str(
                Decimal(each[7]).quantize(Decimal("0.00"))) + " from file tms.shk;"
            f.write(str1)
            f.write("\n")
        if each[7] == 0 and printSwitch(each[6]):
            f.write("Shock tms(TRAD_COMM,\"" + each[0] + "\",\"" + each[3] + "\") = rate% +0 from file tms.shk;")
            f.write("\n")
    for i in range(1, readExcel.getSheetRow(BRISheet)):
        f.write("swap qo(\"Labor\",\"" + readExcel.getValue(BRISheet, i, 0) +
                "\") =ps(\"Labor\",\"" + readExcel.getValue(BRISheet, i, 0) + "\");")
        f.write("\n")
    f.close()
