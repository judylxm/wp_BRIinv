import pandas as pd


def load_large_dta(fname):
    reader = pd.read_stata(fname, iterator=True)
    df = pd.DataFrame()
    try:
        chunk = reader.get_chunk(10 * 1000)
        while len(chunk) > 0:
            df = df.append(chunk, ignore_index=True)
            chunk = reader.get_chunk(10 * 1000)
    except (StopIteration, KeyboardInterrupt):
        pass
    return df


def getReporter(array):
    return array[1]['reporter']


def getPartner(array):
    return array[1]['partner']


def getYear(array):
    return array[1]['year']


def isGTT(array):
    return array[1]['sectorname'] == 'Total Goods (GTT)'


def getTij(array):
    return array[1]['tij']

def getTraiff(array):
    return array[1]['geometric_avg_tariff']


if __name__ == '__main__':
    df_2002_path = "C:\\Users\\hikki\\OneDrive\\210107\\word\\20200603-ESCAP-WB-tradecosts-dataset.dta"
    df_2002 = load_large_dta(df_2002_path)
