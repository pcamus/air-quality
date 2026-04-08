from nextion import nextion
from machine import Pin
import time

from machine import I2C, Pin
import adafruit_sen6x

DEBUG_MODE = False

def set_debug(enabled):
    global print
    if not enabled:
        # Replace print with a function that does nothing
        print = lambda *args, **kwargs: None
    else:
        # Restore the original print function
        import builtins
        print = builtins.print

# Run this at the start of your program
set_debug(DEBUG_MODE)


display = nextion(Pin(4), Pin(5), 9600) # Tx, Rx, Baud rate

def dispCO2(val, disp):
    # CO2 : 0..40000
    disp.cmd('tco2.txt="'+str(val)+'"')
    colbar=31 # bleu
    valbar=val/20
    if (val>400) & (val<1000):
        colbar=2016 # vert
        valbar=20+(val-400)/30
    if (val>=1000) & (val<2000):
        colbar=64512 # orange
        valbar=40+(val-1000)/50
    if (val>=2000) & (val<5000):
        colbar=63488 # rouge
        valbar=60+(val-2000)/150
    if (val>=5000):
        colbar=0
        valbar=80+(val-5000)/175
    
    disp.cmd('j0.val='+str(int(valbar)))
    disp.cmd('j0.pco='+str(colbar))
    


# Initialize I2C
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)

# Create SEN66 instance
sensor = adafruit_sen6x.SEN66(i2c)

# Read sensor info
print(f"Product: {sensor.product_name}")
print(f"Serial: {sensor.serial_number}")

# Check device status
status = sensor.device_status
print(f"Device {status}")

# Start measurements
sensor.start_measurement()

# Wait for first measurement to be ready
print("Waiting for first measurement...")
time.sleep(2)
print("-" * 40)

# Read data continuously
while True:
    if sensor.data_ready:
        # Check for errors before reading
        sensor.check_sensor_errors()

        # Read all measurements
        data = sensor.all_measurements()

        # Display values (None = sensor still initializing)
    if data["co2"]:
        print(f"CO2: {data['co2']} ppm")
        dispCO2(int(data['co2']), display)
    else:
        print("CO2: initializing...")
        display.cmd('tco2.txt="----"')
        
#    print(f"Temperature: {data['temperature']:.1f}°C")
#    print(f"Humidity: {data['humidity']:.1f}%")
    strt=f"{data['temperature']:.1f}"
 
    if data["temperature"]:
        strt=f"{data['temperature']:.1f}"
        print(strt+"°C")
        display.cmd('ttemp.txt="'+strt+'"')
    else:
        print("Temperature: initializing...")
        display.cmd('ttemp.txt="----"')

    if data["humidity"]:
        strh=str(int(data['humidity']))
        print(strh+"%")
        display.cmd('thum.txt="'+strh+'"')
    else:
        print("Humidity: initializing...")
        display.cmd('thum.txt="----"')
    
    if data["pm2_5"]:
        strpm2_5=f"{data['pm2_5']:.1f}"
        print(strpm2_5+"µg/m³")
        display.cmd('tpm2_5.txt="'+strpm2_5+'"')
    else:
        print("PM2.5: initializing...")
        display.cmd('tpm2_5.txt="----"')
    
    if data["pm10"]:
        strpm10=f"{data['pm10']:.1f}"
        print(strpm10+"µg/m³")
        display.cmd('tpm10.txt="'+strpm10+'"')
    else:
        print("PM10: initializing...")
        display.cmd('tpm10.txt="----"')
    
    if data["voc_index"]:
        strvoc=str(int(data["voc_index"]))
        print(f"VOC Index: {data['voc_index']:.1f}")
        display.cmd('tvoc.txt="'+strvoc+'"')
    else:
        print("VOC Index: initializing...")
        display.cmd('tvoc.txt="----"')
        
    if data["nox_index"]:
        strnox=str(int(data["nox_index"]))
        print(f"NOx Index: {data['nox_index']:.1f}")
        display.cmd('tnox.txt="'+strnox+'"')
    else:
        print("NOX Index: initializing...")
        display.cmd('tnox.txt="----"')
    
    print("-" * 40)
    
    time.sleep(2)

