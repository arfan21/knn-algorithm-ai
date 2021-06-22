import pandas as pd
import numpy as np
import json


class KNN():
    def __init__(self, data, testData):
        self.data = data
        self.testData = testData

    def euclidean(self):
        self.resultEuclidean = []
        for _, series in self.data.iterrows():
            resultRow = 0
            for col in series.items():
                namaColumnData = col[0]
                valueColumnData = col[1]
                if namaColumnData in self.testData.columns:
                    valueColumnTestData = self.testData[namaColumnData][0]
                    result = (valueColumnData - valueColumnTestData)**2
                    resultRow += result
            self.resultEuclidean.append(
                {"Nama Mobil": series["Nama Mobil"], "Result": resultRow**(1/2)})
        return self.resultEuclidean

    def manhattan(self):
        self.resultManhattan = []
        for _, series in self.data.iterrows():
            resultRow = 0
            for col in series.items():
                namaColumnData = col[0]
                valueColumnData = col[1]
                if namaColumnData in self.testData.columns:
                    valueColumnTestData = self.testData[namaColumnData][0]
                    result = abs(valueColumnData - valueColumnTestData)
                    resultRow += result
            self.resultManhattan.append(
                {"Nama Mobil": series["Nama Mobil"], "Result": resultRow})
        return self.resultManhattan

    def minkowski(self, h=3):
        self.resultMinkowski = []
        for _, series in self.data.iterrows():
            resultRow = 0
            for col in series.items():
                namaColumnData = col[0]
                valueColumnData = col[1]
                if namaColumnData in self.testData.columns:
                    valueColumnTestData = self.testData[namaColumnData][0]
                    result = abs(valueColumnData - valueColumnTestData)**h
                    resultRow += result
            self.resultMinkowski.append(
                {"Nama Mobil": series["Nama Mobil"], "Result": resultRow**(h)})
        return self.resultMinkowski

    def supremum(self):
        self.resultSupremum = []
        for _, series in self.data.iterrows():
            resultRow = []
            for col in series.items():
                namaColumnData = col[0]
                valueColumnData = col[1]
                if namaColumnData in self.testData.columns:
                    valueColumnTestData = self.testData[namaColumnData][0]
                    result = abs(valueColumnData - valueColumnTestData)
                    resultRow.append(result)
            self.resultSupremum.append(
                {"Nama Mobil": series["Nama Mobil"], "Result": max(resultRow)})
        return self.resultSupremum

    def distances(self):
        """Get all distance"""
        return {
            "Euclidean": self.euclidean(),
            "Manhattan": self.manhattan(),
            "Minkowski": self.minkowski(),
            "Supremum": self.supremum(),
        }

    def printDistance(self):
        """Pretty Print all distance"""
        print(json.dumps(self.distances(), sort_keys=False, indent=4))

    def getBestData(self, k=3):
        """Mendapatkan data 3 terbaik dari setiap metode perhitungan jarak"""
        bestEuclidean = sorted(self.euclidean(), key=lambda x: x["Result"])[:k]
        bestManhattan = sorted(self.manhattan(), key=lambda x: x["Result"])[:k]
        bestMinkowski = sorted(self.minkowski(), key=lambda x: x["Result"])[:k]
        bestSupremum = sorted(self.supremum(), key=lambda x: x["Result"])[:k]

        data = []
        for i in range(k):
            data.append(
                {"Method": "Euclidean", "Nama Mobil": bestEuclidean[i]["Nama Mobil"], "Result": bestEuclidean[i]["Result"]})
        for i in range(k):
            data.append(
                {"Method": "Manhattan", "Nama Mobil": bestManhattan[i]["Nama Mobil"], "Result": bestManhattan[i]["Result"]})
        for i in range(k):
            data.append(
                {"Method": "Minkowski", "Nama Mobil": bestMinkowski[i]["Nama Mobil"], "Result": bestMinkowski[i]["Result"]})
        for i in range(k):
            data.append(
                {"Method": "Supremum", "Nama Mobil": bestSupremum[i]["Nama Mobil"], "Result": bestSupremum[i]["Result"]})

        return data

    def printBestData(self):
        """Pretty Print best data each method"""
        print(json.dumps(self.getBestData(), sort_keys=False, indent=4))


data = pd.read_excel("./mobil.xls")


def createTestData():
    ukuran = 1
    kenyamanan = 1
    irit = 1
    kecepatan = 1
    harga = 1

    data = {'Ukuran': [ukuran], 'Kenyamanan': [kenyamanan], 'Irit': [irit], 'Kecepatan': [kecepatan],
            'Harga (Ratus Juta)': [harga]}

    return pd.DataFrame(data)


def normalisasi(dataframe, maxRange=10):
    coppiedDataframe = dataframe.copy()
    for col in coppiedDataframe.columns:
        if not coppiedDataframe[col].dtype == "int64" and not coppiedDataframe[col].dtype == "float64":
            continue
        max_value = coppiedDataframe[col].max()
        min_value = coppiedDataframe[col].min()
        coppiedDataframe[col] = ((coppiedDataframe[col] - min_value) /
                                 (max_value - min_value))*maxRange
    return coppiedDataframe


normalizedData = normalisasi(data)
testData = createTestData()
knn = KNN(normalizedData, testData)
knn.getBestData()
knn.printBestData()

recommendedData = pd.DataFrame(knn.getBestData())
recommendedData.to_excel('rekomendasi.xlsx', index=False)


# print(testData)
# print(data.iloc[1].values.tolist())
# Train Data = Data yang digunakan untuk membuat suatu model
# Test Data = Data yang digunakan untuk melakukan test terhadap suatu model/ yang akan mengeluarkan output (dalam kasus ini rekomendasi mobil)

# jadi training adalah data yang seharusnya keluar misalkan kalau anda belajar 3 jam keluar nilai 60, kalau 2 jam keluar nilai 40, kalau 5 jam keluar nilai 100
# walaupun actualnya tidak seperti itu
