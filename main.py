from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
import framebuf,sys,time

def altitude_HYP(pressure,temperature,adjust):
    # Hypsometric Equation (Max Altitude < 11 Km above sea level)
    temperature += 273.15
    pressure *= 0.01 # in hPa   
    altitude = ((((adjust/pressure)**(1/5.257)) - 1) * temperature ) / 0.0065
    return altitude

def altitude_IBF(pressure,adjust):
    pressure *= 0.01  # in hPa
    altitude = 44330*(1-((pressure/adjust)**(1/5.255)))
    return altitude
    
def convertFromMetersToFeet(altitudeInMeter):
    return 3.28084*altitudeInMeter

def displayAngle(angle,symbol,w,h):
    if angle > 0 :
        if angle < 10 :
            display.text(symbol+" +0"+"{:.0f}".format(angle),w,h)
        else :
            display.text(symbol+" +"+"{:.0f}".format(angle),w,h)
    else :
        if angle > -10 :
            display.text(symbol+" -0"+"{:.0f}".format(-angle),w,h)
        else :
            display.text(symbol+" "+"{:.0f}".format(angle),w,h)
            
#display.write_cmd(0xc0) # flip display to place 0,0 at lower-left corner
#adc_2 = machine.ADC(2) # ADC channel 2 for input
while True:
    imu.getPitchAndRoll()
    imu.printMeasures()
    display.fill(0) # clear the display
    displayAngle(imu.pitchAngle,"P",0,16)
    displayAngle(imu.rollAngle,"R",48,16)
    display.text("T "+"{:.1f}".format(barometer.temperature)+" P "+"{:.0f}".format(convertFromMetersToFeet(altitude_HYP(barometer.pressure,barometer.temperature,1017.00))),0,24)
    display.show() # show the new text and image
