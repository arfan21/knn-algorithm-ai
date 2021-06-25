import pandas as pd
import numpy as np
import json


class KNN():    # Membuat class KNN yang berisi method untuk menghitung jarak, mendapatkan data terbaik, dan print data
    def __init__(self, data, testData): #Method untuk menginisialisasi isi dari class KNN
        self.data = data
        self.testData = testData

    def euclidean(self):    #Method untuk menghitung jarak Euclidean
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

    def manhattan(self):    #Method untuk menghitung jarak Manhattan
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

    def minkowski(self, h=3):    #Method untuk menghitung jarak Minkowski dengan h default adalah 3
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

    def supremum(self):    #Method untuk menghitung jarak Supremum
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
            "Euclidean": self.euclidean(),  #Mengembalikan jarak euclidean
            "Manhattan": self.manhattan(),  #Mengembalikan jarak manhattan
            "Minkowski": self.minkowski(),  #Mengembalikan jarak minkowski
            "Supremum": self.supremum(),    #Mengembalikan jarak supremum
        }

    def printDistance(self):    #Method untuk print semua jarak
        """Pretty Print all distance"""

        print(json.dumps(self.distances(), sort_keys=False, indent=4))

    def getBestData(self, k=3): #Method untuk mendapatkan data terbaik dari setiap metode perhitungan jarak dengan k default adalah 3
        """Mendapatkan data terbaik dari setiap metode perhitungan jarak"""
        
        #Melakukan sorting terhadap data jarak secara ascending
        bestEuclidean = sorted(self.euclidean(), key=lambda x: x["Result"])[:k] 
        bestManhattan = sorted(self.manhattan(), key=lambda x: x["Result"])[:k]
        bestMinkowski = sorted(self.minkowski(), key=lambda x: x["Result"])[:k]
        bestSupremum = sorted(self.supremum(), key=lambda x: x["Result"])[:k]

        #Menambahkan data terbaik kedalam satu array data terbaik
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

    def printBestData(self):    #Method untuk print data terbaik
        """Pretty Print best data each method"""

        print(json.dumps(self.getBestData(), sort_keys=False, indent=4))


def createTestData():   #Fungsi untuk membuat data tes
    ukuran = 1
    kenyamanan = 1
    irit = 1
    kecepatan = 1
    harga = 1

    data = {'Ukuran': [ukuran], 'Kenyamanan': [kenyamanan], 'Irit': [irit], 'Kecepatan': [kecepatan],
            'Harga (Ratus Juta)': [harga]}

    return pd.DataFrame(data)


def normalisasi(dataframe, maxRange=10):    #Fungsi untuk melakukan normalisasi terhadap data training
    coppiedDataframe = dataframe.copy()
    for col in coppiedDataframe.columns:
        if not coppiedDataframe[col].dtype == "int64" and not coppiedDataframe[col].dtype == "float64":
            continue
        max_value = coppiedDataframe[col].max()
        min_value = coppiedDataframe[col].min()
        coppiedDataframe[col] = ((coppiedDataframe[col] - min_value) /
                                 (max_value - min_value))*maxRange
    return coppiedDataframe


data = pd.read_excel("./mobil.xls") #Membaca file excel mobil.xls

normalizedData = normalisasi(data)  #Melakukan normalisasi data training dari mobil.xls
testData = createTestData()         #Membuat data tes
knn = KNN(normalizedData, testData) #Melakukan inisialisasi class knn
knn.getBestData()                   #Mendapatkan data terbaik
knn.printBestData()                 #Print data terbaik

recommendedData = pd.DataFrame(knn.getBestData())   #Menyimpan data terbaik pada dataframe
recommendedData.to_excel('rekomendasi.xlsx', index=False)   #Menyimpan dataframe data terbaik menjadi file rekomendasi.xlsx
