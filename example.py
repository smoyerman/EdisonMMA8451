import mma8451

# Potential range values
MMA8451_RANGE_8_G = 0b10    # +/- 8g
MMA8451_RANGE_4_G = 0b01    # +/- 4g
MMA8451_RANGE_2_G = 0b00    # +/- 2g (default value)

# Make accelerometer object
accel = mma8451.MMA8451()

# Check for MMA 8451
ismma = accel.check8451()
if ismma = True:
    print "MMA 8451 Found!"
else:
    print "No MMA Found. What is this?!"

# Set up mma, default range is 2Gs
accel.setup()

# Can declare a different range with
accel.setup(MMA8451_RANGE_8_G)

# Loop, read, and print out values
for i in range(10):
    ax,ay,az = accel.readData()
    print "(" + str(round(ax,1)) + ", " + str(round(ay,1)) + ", " + str(round(az,1)) + ")" 
    orientation = accel.readOrientation()
    print orientation
