#!/usr/bin/env python3

''' test_imu.py  - Tests the basic connection to the IMU, and filters by gathering
    all available data followed by filtering it.   The filtered data will be displayed
    the data to the terminal.
'''

from imus.imu_9250 import imu_9250

##
# @brief Main test code used to access all information from the IMU(s), filter it, and pass it on
# @param rawImuData initializes the IMU for use
# @param separation Separates the tuple obtained from the IMU(s) into their respective measurements
# @return separation Returns 9 DOF variables
if __name__ == '__main__':

    myIMU = imu_9250()
    while True:
        rawImuData = myIMU.getAllAvalableData()

        #separation
        (XAaccel, YAaccel, ZAaccel,
         XRotGyro, YRotGyro, ZRotGyro,
         XMagno, YMagno, ZMagno) = (rawImuData[0], rawImuData[1], rawImuData[2],
                                    rawImuData[3], rawImuData[4], rawImuData[5],
                                    rawImuData[6], rawImuData[7], rawImuData[8])
        # Filter data here

        # output or print data here

        print("X Acc: ", "{0:.2f}".format(XAaccel), "\tY Acc: ", "{0:.2f}".format(YAaccel), "\tZ Acc: ",
              "{0:.2f}".format(ZAaccel))
        # print("X Gyro:", "{0:.2f}".format(AvgGyroX - calData[3]), "\tY Gyro:", "{0:.2f}".format(AvgGyroY - calData[4]), "\tZ Gyro:", "{0:.2f}".format(AvgGyroZ - calData[5]))
        print("")

