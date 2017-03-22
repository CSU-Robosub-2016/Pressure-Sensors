import numpy as np
import sys
import I2C
import I2C.pressuretrans

i2c = I2C.BusI2C('COM2')
i2c.bus.setSpeed(2000)  # you can set i2c speed adapted to your hardware
sonde = I2C.pressuretrans.LM75('Pressure Voltage', i2c)
print "T =  %02.03f C" % sonde.getTemperature()
