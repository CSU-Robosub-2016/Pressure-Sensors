# IMU code using i2c on python

# Converts a specified number of bits using Two's Complement
def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val


# Converts two bytes into a binary String format
def tobinary(high, low):
    return '{0:08b}'.format(high) + '{0:08b}'.format(low)


# requires 16-bit String (1's and 0's)
def binary_twos(word):
    wordint = int(word, 2)
    if word[0] == '0':
        return wordint
    else:
        return twos_comp(wordint, 16)


# Given register and bus constraints, outputs the correct +/- int corresponding to high and low register values
def data_to_int(bus, link, highreg, lowreg):
    highdata = bus.read_byte_data(link, highreg)
    lowdata = bus.read_byte_data(link, lowreg)
    dblbyte = '{0:08b}'.format(highdata) + '{0:08b}'.format(lowdata)
    return twos_comp(int(dblbyte, 2), 16)


# Retrieves data from IMU (MPU-9250), returns list of [AccX, AccY, AccZ, GyroX, GyroY, GyroZ].
# Acc data is returned in relation to g.
def getDataMPU(bus, link):
    accX = data_to_int(bus, link, 59, 60) / 16384
    accY = data_to_int(bus, link, 61, 62) / 16384
    accZ = data_to_int(bus, link, 63, 64) / 16384
    gyroX = data_to_int(bus, link, 67, 68)
    gyroY = data_to_int(bus, link, 69, 70)
    gyroZ = data_to_int(bus, link, 71, 72)
    ret = [accX, accY, accZ, gyroX, gyroY, gyroZ]
    return ret


# Returns calibrated relation data to use in calculations.
# [calibAccX, calibAccY, calibAccZ, calibGyroX, calibGyroY, calibGyroZ]
# To be used as: AccX = data - calibAccX
def calibrateMPU(bus, link, iterations):
    print("Calibrating MPU-9250 IMU. Please do not touch the sensor and avoid vibrations.")
    print("Completing", iterations, "iterations.")
    start = time.time()
    calibLoop = 0
    calibData = [0, 0, 0, 0, 0, 0]
    while calibLoop < iterations:
        calibLoop += 1
        Add = getDataMPU(bus, link)
        calibData[0] += Add[0]
        calibData[1] += Add[1]
        calibData[2] += Add[2]
        calibData[3] += Add[3]
        calibData[4] += Add[4]
        calibData[5] += Add[5]
    calibData[0] = calibData[0] / iterations
    calibData[1] = calibData[1] / iterations
    calibData[2] = calibData[2] / iterations
    calibData[3] = calibData[3] / iterations
    calibData[4] = calibData[4] / iterations
    calibData[5] = calibData[5] / iterations
    end = time.time()
    print("Finished calibrating MPU-9250 IMU. Total time took:", end - start, "seconds.")
    return calibData


import smbus
import struct
import time

bus = smbus.SMBus(1)  # i2c port 1

fd = 0x68

calData = calibrateMPU(bus, fd, 1000)

loop = 0
loopIter = 1

AccXtotal = 0
AccYtotal = 0
AccZtotal = 0

GyroXtotal = 0
GyroYtotal = 0
GyroZtotal = 0

while True:
    getData = getDataMPU(bus, fd)
    AccXtotal += getData[0]
    AccYtotal += getData[1]
    AccZtotal += getData[2]
    GyroXtotal += getData[3]
    GyroYtotal += getData[4]
    GyroZtotal += getData[5]

    # Testing code
    # accXhighreal = bus.read_byte_data(fd, 59)
    # accXhigh = twos_comp(accXhighreal, 8)
    # accXlow = bus.read_byte_data(fd, 60)
    # doublebyte = tobinary(accXhighreal, accXlow)

    if loop >= loopIter:
        AvgAccX = AccXtotal / loopIter
        AvgAccY = AccYtotal / loopIter
        AvgAccZ = AccZtotal / loopIter
        AvgGyroX = GyroXtotal / loopIter
        AvgGyroY = GyroYtotal / loopIter
        AvgGyroZ = GyroZtotal / loopIter

        print("X Acc: ", "{0:.2f}".format(AvgAccX), "\tY Acc: ", "{0:.2f}".format(AvgAccY), "\tZ Acc: ",
              "{0:.2f}".format(AvgAccZ))
        print("X Gyro:", "{0:.2f}".format(AvgGyroX - calData[3]), "\tY Gyro:", "{0:.2f}".format(AvgGyroY - calData[4]),
              "\tZ Gyro:", "{0:.2f}".format(AvgGyroZ - calData[5]))
        print("")
        loop = 0
        AccXtotal = 0
        AccYtotal = 0
        AccZtotal = 0
        GyroXtotal = 0
        GyroYtotal = 0
        GyroZtotal = 0
        AccXtest = 0
    loop += 1
