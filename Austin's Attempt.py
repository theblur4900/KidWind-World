# This code is made for solar panels on Pins 0 and 1 and Servos on Pins 2 and 3
# The Constants may be modified to change what pins the solar panels and the servos are on
# Coded by Austin Dixon github.com/theblur4900



# Constants
SolarPanel_0 = AnalogPin.P3
SolarPanel_1 = AnalogPin.P4
Servo_0 = AnalogPin.P8
Servo_1 = AnalogPin.P12
Servo_2 = AnalogPin.P0


# Variables
light_list_solar = []
max_val_solar = 0
best_angle_solar = 0
light_list_base = []
max_val_base = 0
best_angle_base = 0

# Set Pin Frequency
pins.analog_set_period(Servo_0, 20000)
pins.analog_set_period(Servo_1, 20000)
pins.analog_set_period(Servo_2, 20000)

# Actual Logic
def on_button_pressed_a():
    global light_list_solar, max_val_solar, best_angle_solar, light_list_base, max_val_base, best_angle_base
    light_list_solar = []
    max_val_solar = 0
    best_angle_solar = 0
    light_list_base = []
    max_val_base = 0
    best_angle_base = 0

    for i in range(181):
    
        pins.servo_write_pin(Servo_0, i)
        pins.servo_write_pin(Servo_2, i)
        
        pause(40)
        current_voltage_base = (pins.analog_read_pin(SolarPanel_0) + pins.analog_read_pin(SolarPanel_1))
        print("Current Voltage (Base): ~" + int((current_voltage_base/2046)*3.3)+ "V (" + current_voltage_base + "/2046)")
        light_list_base.append(current_voltage_base)

    for i in range(len(light_list_base)):
        if light_list_base[i] > max_val_base:
            max_val_base = light_list_base[i]
            best_angle_base = i

    pins.servo_write_pin(Servo_0, best_angle_base)
    pins.servo_write_pin(Servo_2, best_angle_base)
    print("Best Angle Found! " + best_angle_base + " Degrees (Base)")
    print("Maximum Voltage (Base): "+ int((max_val_base/2046)*3.3)+ "V (" + max_val_base + "/2046)")

    for i in range(181):
    
        pins.servo_write_pin(Servo_1, i)

        pause(40)
        current_voltage_solar = (pins.analog_read_pin(SolarPanel_0) + pins.analog_read_pin(SolarPanel_1))
        print("Current Voltage (Solar): ~" + int((current_voltage_solar/2046)*3.3)+ "V (" + current_voltage_solar + "/2046)")
        light_list_solar.append(current_voltage_solar)

    for i in range(len(light_list_solar)):
        if light_list_solar[i] > max_val_solar:
            max_val_solar = light_list_solar[i]
            best_angle_solar = i

    pins.servo_write_pin(Servo_1, best_angle_solar)
    print("Best Angle Found! " + best_angle_solar + " Degrees (Solar)")
    print("Maximum Voltage (Solar): "+ int((max_val_solar/2046)*3.3)+ "V (" + max_val_solar + "/2046)")

input.on_button_pressed(Button.A, on_button_pressed_a)

# Zeroing
def on_button_pressed_b():
    pins.servo_write_pin(Servo_0, 0)
    pins.servo_write_pin(Servo_1, 0)
    pins.servo_write_pin(Servo_2, 0)
    print("Successully Zero'd!")
input.on_button_pressed(Button.B, on_button_pressed_b)
