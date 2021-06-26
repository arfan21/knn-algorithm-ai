import pandas as pd
import json


class KNN():    # Membuat class KNN yang berisi method untuk menghitung jarak, mendapatkan data terbaik, dan print data
    def __init__(self, data, testData):  # Method untuk menginisialisasi isi dari class KNN
        self.data = data
        self.testData = testData

    def euclidean(self):  # Method untuk menghitung jarak Euclidean
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

    def manhattan(self):  # Method untuk menghitung jarak Manhattan
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

    def minkowski(self, h=3):  # Method untuk menghitung jarak Minkowski dengan h default adalah 3
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

    def supremum(self):  # Method untuk menghitung jarak Supremum
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
            "Euclidean": self.euclidean(),  # Mengembalikan jarak euclidean
            "Manhattan": self.manhattan(),  # Mengembalikan jarak manhattan
            "Minkowski": self.minkowski(),  # Mengembalikan jarak minkowski
            "Supremum": self.supremum(),  # Mengembalikan jarak supremum
        }

    def printDistance(self, k=3):  # Method untuk print data terbaik dari semua metode distance
        """Pretty Print best data from all distance"""

        allDistance = self.distances()

        # Melakukan sorting terhadap data jarak secara ascending
        bestEuclidean = sorted(
            allDistance["Euclidean"], key=lambda x: x["Result"])[:k]
        bestManhattan = sorted(
            allDistance["Manhattan"], key=lambda x: x["Result"])[:k]
        bestMinkowski = sorted(
            allDistance["Minkowski"], key=lambda x: x["Result"])[:k]
        bestSupremum = sorted(
            allDistance["Supremum"], key=lambda x: x["Result"])[:k]

        data = {
            "Euclidean": bestEuclidean,
            "Manhattan": bestManhattan,
            "Minkowski": bestMinkowski,
            "Supremum": bestSupremum,
        }

        print(json.dumps(data, sort_keys=False, indent=4))

    # Method untuk mendapatkan data terbaik dari metode perhitungan jarak supremum dengan k default adalah 3
    def getBestData(self, k=3):
        """Mendapatkan data terbaik dari metode perhitungan jarak supremum"""

        allDistance = self.distances()

        # Melakukan sorting terhadap data jarak secara ascending
        bestSupremum = sorted(
            allDistance["Supremum"], key=lambda x: x["Result"])[:k]

        bestData = []   # Array yang menyimpan nama mobil terbaik
        for i in range(len(bestSupremum)):
            bestData.append(bestSupremum[i]["Nama Mobil"])

        return bestData

    def printBestData(self):  # Method untuk print data terbaik
        """Pretty Print best data each method"""

        print(json.dumps(self.getBestData(), sort_keys=False, indent=4))


def createTestData():  # Fungsi untuk membuat data tes
    ukuran = 7
    kenyamanan = 7
    irit = 7
    kecepatan = 7
    harga = 2.3

    data = {'Ukuran': [ukuran], 'Kenyamanan': [kenyamanan], 'Irit': [irit], 'Kecepatan': [kecepatan],
            'Harga (Ratus Juta)': [harga]}

    return pd.DataFrame(data)


# Fungsi untuk melakukan normalisasi terhadap data training
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


def main():
    data = pd.read_excel("./mobil.xls")  # Membaca file excel mobil.xls

    # Melakukan normalisasi data training dari mobil.xls
    normalizedData = normalisasi(data)
    print(normalizedData, "\n")
    testData = createTestData()  # Membuat data tes
    knn = KNN(normalizedData, testData)  # Melakukan inisialisasi class knn
    bestData = knn.getBestData()  # Mendapatkan data terbaik
    knn.printDistance()
    knn.printBestData()  # Print data terbaik

    # Menyimpan data terbaik pada dataframe
    recommendedData = pd.DataFrame(bestData)
    # Menyimpan dataframe data terbaik menjadi file rekomendasi.xlsx
    recommendedData.to_excel('rekomendasi.xlsx', index=False)


if __name__ == '__main__':
    main()
