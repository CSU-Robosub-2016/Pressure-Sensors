import numpy as np
import csv
import os.path
import matplotlib.pyplot as plt


class imu_tools():

    def __init__(self, fifoMemSize=10000):

        self.fifoMemSize = fifoMemSize
        self.fifoMemIteration = 0
        self.fifoMemory = np.zeros(self.fifoMemSize)

    def fifoMemoryUpdate(self, inputData):
        i = 0
        if self.fifoMemIteration < self.fifoMemSize:
            self.fifoMemory[self.fifoMemIteration] = inputData
        if self.fifoMemIteration >= self.fifoMemSize:
            while i <= (self.fifoMemSize - 2):
                self.fifoMemory[i] = self.fifoMemory[i+1]
                i+=1
            self.fifoMemory[self.fifoMemSize-1] = inputData
        self.fifoMemIteration += 1

    def get_fifoMemory(self):
        return self.fifoMemory

    def highPassFilter(self, filterSize = 150000):
        W = np.fft.fftfreq(self.fifoMemSize, 0.0000025)
        f_signal = np.fft.fft(self.fifoMemory)
        cut_f_signal = f_signal.copy()
        cut_f_signal[(np.abs(W) < filterSize)] = 0
        cut_signal = np.fft.ifft(cut_f_signal)
        return cut_signal

    def lowPassFilter(self, filterSize):
        W = np.fft.fftfreq(self.fifoMemSize, 0.0000025)
        f_signal = np.fft.fft(self.fifoMemory)
        cut_f_signal = f_signal.copy()
        cut_f_signal[(np.abs(W) > filterSize)] = 0
        cut_signal = np.fft.ifft(cut_f_signal)
        return cut_signal


    def print2CvFile(self, dof, data, fileName, testRawFiltered, iteration,
                     save_path='C:/Users/bob/Desktop/imu_framework/imu_framework/data/test'):

        #save_path = ''
        if testRawFiltered == 'test':
            save_path = '/home/pi/Desktop/imu_framework/imu_framework/data/test'
            fileName = fileName + '_test_data'
        if testRawFiltered == 'raw':
            save_path = 'C:/Users/bob/Desktop/imu_framework/imu_framework/data/raw'  # '/home/pi/Desktop/imu_framework/imu_framework/data/raw'
            fileName = fileName + '_raw_data'
        if testRawFiltered == 'filtered':
            save_path = 'C:/Users/bob/Desktop/imu_framework/imu_framework/data/filtered'  # '/home/pi/Desktop/imu_framework/imu_framework/data/filtered'
            fileName = fileName + '_filtered_data'

        nameOfFile = os.path.join(save_path, fileName + ".csv")

        if iteration == 0:
            with open(nameOfFile, "w") as csvfile:
                fieldnames = ['X Acc', 'Y Acc', 'Z Acc', 'X Gyro', 'Y Gyro', 'Z Gyro', 'X Mag', 'Y Mag', 'Z Mag']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'X Acc': data[0], 'Y Acc': data[1], 'Z Acc': data[2],
                                 'X Gyro': data[3], 'Y Gyro': data[4], 'Z Gyro': data[5],
                                 'X Mag': data[6], 'Y Mag': data[7], 'Z Mag': data[8]})

        if iteration != 0:
            with open(nameOfFile, "a") as csvfile:
                fieldnames = ['X Acc', 'Y Acc', 'Z Acc', 'X Gyro', 'Y Gyro', 'Z Gyro', 'X Mag', 'Y Mag', 'Z Mag']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'X Acc': data[0], 'Y Acc': data[1], 'Z Acc': data[2],
                                 'X Gyro': data[3], 'Y Gyro': data[4], 'Z Gyro': data[5],
                                 'X Mag': data[6], 'Y Mag': data[7], 'Z Mag': data[8]})

    def csvData2NpArray(self, fileName, column):

        datafile = open(fileName, 'r')
        datareader = csv.reader(datafile, delimiter=',')
        data = []
        for row in datareader:
            data.append(row[column])
        out = np.array(data)
        outPut = np.delete(out, 0)
        return outPut

    def npArray2Tuple(self, array):
        outPut = tuple(map(tuple, array))
        return outPut

    def fouriorTransform(self, inputData):
        data = np.array(inputData)
        outputData = np.fft.rfft(data)
        return data

    def livePlot(self, data):
        plt.clf()
        plt.plot(data)
        plt.pause(0.00000000001)


def fouriorTransform(self, inputData):
    data = np.array(inputData)
    outputData = np.fft.rfft(data)
    #outputData = np.fft.fftfreq(inputData)
    return outputData


def inversFouriorTransform(self, inputData):
    outputData = np.fft.irfft(inputData)
    return outputData
