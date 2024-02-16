from machine import Pin, I2C
import time
from ssd1306 import SSD1306_I2C
from bmp280 import *
from imu import MPU6050

# Setup Built-in Led Pin
led = Pin("LED",Pin.OUT)
led.low()

def initBlink(blinkTimes) :
    n = 0
    while n < blinkTimes:
        led.high()
        time.sleep(0.05)
        led.low()
        time.sleep(0.05)
        n += 1
        
# Setup I2C Bus
i2cBus = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)

# Setup Display
displayWidth  = 128 # SSD1306 horizontal resolution
displayHeight = 64   # SSD1306 vertical resolution
display = SSD1306_I2C(width=displayWidth,height=displayHeight,i2c=i2cBus)  

i2cDevices = I2C.scan(i2cBus)
print(i2cDevices)

if i2cDevices==[]:
    print('No I2C Devices Found... Exiting...') 
    sys.exit() # exit routine if no dev found
else:
    print(i2cDevices)
    
# Setup Barometer (BMP280)
barometer = BMP280(i2cBus)
barometer.use_case(BMP280_CASE_INDOOR)
barometer.temp_os = BMP280_TEMP_OS_8
barometer.press_os = BMP280_PRES_OS_4
barometer.standby = BMP280_STANDBY_250
barometer.iir = BMP280_IIR_FILTER_2
barometer.power_mode = BMP280_POWER_NORMAL
barometer.oversample = BMP280_OS_HIGH

# Setup IMU
imu = MPU6050(i2cBus)
imu.filter_range = 5
imu.accel_range = 2
imu.gyro_range = 1


initBlink(10)
display.powerOn()
display.text("ACFT IMU v1.0",0,0)
display.show()
time.sleep(0.5)
display.text("Starting up...",0,8);
display.show()
imu.calibrate(100)
display.fill(0)
display.show()


