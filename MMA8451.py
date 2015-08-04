import mraa as m
import numpy as np

# Some addresses
MMA_i2caddr              = 0x1D
MMA8451_REG_WHOAMI       = 0x0D
MMA_DEVID                = 0x1A 
MMA8451_REG_XYZ_DATA_CFG = 0x0E
MMA8451_REG_OUT_X_MSB    = 0x01
MMA8451_REG_PL_STATUS    = 0x10
MMA8451_REG_PL_CFG       = 0x11
MMA8451_REG_CTRL_REG1    = 0x2A
MMA8451_REG_CTRL_REG2    = 0x2B
MMA8451_REG_CTRL_REG2    = 0x2B
MMA8451_REG_CTRL_REG4    = 0x2D
MMA8451_REG_CTRL_REG5    = 0x2E

# Range values
MMA8451_RANGE_8_G = 0b10    # +/- 8g
MMA8451_RANGE_4_G = 0b01    # +/- 4g
MMA8451_RANGE_2_G = 0b00    # +/- 2g (default value)

# Data rate values
MMA8451_DATARATE_800_HZ   = 0b000     #  800Hz 
MMA8451_DATARATE_400_HZ   = 0b001     #  400Hz
MMA8451_DATARATE_200_HZ   = 0b010     #  200Hz
MMA8451_DATARATE_100_HZ   = 0b011     #  100Hz
MMA8451_DATARATE_50_HZ    = 0b100     #   50Hz
MMA8451_DATARATE_12_5_HZ  = 0b101     # 12.5Hz
MMA8451_DATARATE_6_25HZ   = 0b110     # 6.25Hz
MMA8451_DATARATE_1_56_HZ  = 0b111     # 1.56Hz

# Orientation labeling 
MMA8451_PL_PUF =  0
MMA8451_PL_PUB =  1
MMA8451_PL_PDF =  2
MMA8451_PL_PDB =  3
MMA8451_PL_LRF =  4  
MMA8451_PL_LRB =  5  
MMA8451_PL_LLF =  6  
MMA8451_PL_LLB =  7  

class MMA8451():

    # Define range at startup 
    def __init__(self):
        # Init I2C
        self.x = m.I2c(1)
    
    # Check for mma8451
    def check8451(self):
        mma = True
        try:
            self.x.address(MMA_i2caddr)
            mma_id = self.x.readReg(MMA8451_REG_WHOAMI)
            if not mma_id == MMA_DEVID:
                print "Wrong device found! Dev ID = " + str(mma_id) 
                mma = False
            else:
                "MMA8541 Detected!"
        except:
                print "MMA Device Not Connected!"
                mma = False
        return mma

    # Perform Setup on mma, set data range
    def setup(self, datarange = MMA8451_RANGE_2_G):
        # Activation sequence!
        self.x.writeReg(MMA8451_REG_CTRL_REG2, 0x40)  # reset
        while (self.x.readReg(MMA8451_REG_CTRL_REG2) & 0x40):
            print "Checking Reset Finished"
        self.x.writeReg(MMA8451_REG_XYZ_DATA_CFG, MMA8451_RANGE_4_G)  # Enable 4G range
        self.x.writeReg(MMA8451_REG_CTRL_REG2, 0x02)  # High res
        self.x.writeReg(MMA8451_REG_CTRL_REG4, 0x01)  # Low noise!
        self.x.writeReg(MMA8451_REG_CTRL_REG4, 0x01)  # DRDY on INT1
        self.x.writeReg(MMA8451_REG_CTRL_REG5, 0x01)
        self.x.writeReg(MMA8451_REG_PL_CFG, 0x40)     # Turn on orientation config
        self.x.writeReg(MMA8451_REG_CTRL_REG1, 0x01)  # active! max rate

        # Set the accelerometer range
        self.x.writeReg(MMA8451_REG_CTRL_REG1, 0x00)    # deactivate
        self.x.writeReg(MMA8451_REG_XYZ_DATA_CFG, datarange & 0x3)    # set range
        self.x.writeReg(MMA8451_REG_CTRL_REG1, 0x01)    # reactivate

        # Read the accel range back
        mma_range = self.x.readReg(MMA8451_REG_XYZ_DATA_CFG) & 0x03
        print "Range = " + str(2 << mma_range) + "Gs"  

        # Determine calibration based on range
        if (mma_range == MMA8451_RANGE_8_G):
            self.divider = 1024.0
        elif (mma_range == MMA8451_RANGE_4_G):
            self.divider = 2048.0
        elif (mma_range == MMA8451_RANGE_2_G):
            self.divider = 4096.0
        else:
            self.divider = 1.0
            print "Invalid Data Range Found. Printing raw, uncalibrated values."

    # Read out the calibrated accel data
    def readData(self):
        # Read out the data, request 6 bytes, translate, and scale
        data = self.x.read(6)
        ax = ((np.int16(data[0] | (data[1] << 8))) >> 2 ) / self.divider
        ay = ((np.int16(data[2] | (data[3] << 8))) >> 2 ) / self.divider
        az = ((np.int16(data[4] | (data[5] << 8))) >> 2 ) / self.divider
        return ax, ay, az

    # Read out mma orientation
    def readOrientation(self):
        o = (self.x.readReg(MMA8451_REG_PL_STATUS) & 0x07)
        orientation = "Not Found"
        if o == MMA8451_PL_PUF: 
            orientation = "Portrait Up Front"
        elif o == MMA8451_PL_PUB: 
            orientation = "Portrait Up Back"
        elif o == MMA8451_PL_PDF: 
            orientation = "Portrait Down Front"
        elif o == MMA8451_PL_PDB: 
            orientation =  "Portrait Down Back"
        elif o == MMA8451_PL_LRF: 
            orientation =  "Landscape Right Front"
        elif o == MMA8451_PL_LRB: 
            orientation =  "Landscape Right Back"
        elif o == MMA8451_PL_LLF: 
            orientation =  "Landscape Left Front"
        elif o == MMA8451_PL_LLB: 
            orientation =  "Landscape Left Back"
        else:
            orientation = "Not Found"
        return orientation

    










