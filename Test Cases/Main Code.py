# This program was written for EnergyOptix in the KidWind Challenge.
# This program is not to be used by anyone other than those authorized.
# Written by Austin Dixon and Justin Pongpairoj
# Solar Panels on Pins 2, 3, and 4, Reset Button on Pin 0, Button A on Pin 5, Button B on Pin 11, Rotation Servo on Pin 6, and Tilt Servo on Pin 8
# Angle_0 can be used to set the angle of the tilt servo for the first pass, Angle_1 to set the angle for the second.

# Variable Declarations
light_list_tilt = []
max_val_tilt = 0
best_angle_tilt = 0
light_list_rotate = []
max_val_rotate = 0
best_angle_rotate = 0

# Constants
Solar_0 = AnalogPin.P2
Solar_1 = AnalogPin.P3
Solar_2 = AnalogPin.P4
Rotate = AnalogPin.P6
Tilt = AnalogPin.P8
Angle_0 = 122
Angle_1 = 32

# Movement Smoothing (Supposedly)
pins.analog_set_period(Rotate, 20000)
pins.analog_set_period(Tilt, 20000)

# Actual Logic
def on_button_pressed_a():
    global light_list_tilt, max_val_tilt, best_angle_tilt, light_list_rotate, max_val_rotate, best_angle_rotate
    light_list_tilt = []
    max_val_tilt = 0
    best_angle_tilt = 0
    light_list_rotate = []
    max_val_rotate = 0
    best_angle_rotate = 0

    for i in range(181): # Rotation Logic
        pins.servo_write_pin(Tilt, Angle_0)
        pins.servo_write_pin(Rotate, i)
        pause(55)
        
        current_voltage_rotate = (pins.analog_read_pin(Solar_0) + pins.analog_read_pin(Solar_1))
        print("Current Voltage (Rotate): ~" + str(int((current_voltage_rotate/1023)*3.3)) + "V (" + str(current_voltage_rotate) + "/3069)")
        if current_voltage_rotate > max_val_rotate:
            max_val_rotate = current_voltage_rotate
            best_angle_rotate = i

    pins.servo_write_pin(Tilt, 45)
    pins.servo_write_pin(Rotate, 180)
    pause(1000)

    for i in range(181):
        angle = 180 - i
        pins.servo_write_pin(Tilt, Angle_1)
        pins.servo_write_pin(Rotate, angle)
        pause(55)
        
        current_voltage_rotate = (pins.analog_read_pin(Solar_0) + pins.analog_read_pin(Solar_1) + pins.analog_read_pin(Solar_2))
        print("Current Voltage (Rotate): ~" + str(int((current_voltage_rotate/1023)*3.3)) + "V (" + str(current_voltage_rotate) + "/3069)")
        if current_voltage_rotate > max_val_rotate:
            max_val_rotate = current_voltage_rotate
            best_angle_rotate = angle

    pins.servo_write_pin(Rotate, best_angle_rotate)
    print("Best Angle Found! " + str(best_angle_rotate) + " Degrees (Rotate)")
    print("Maximum Voltage (Rotate): ~"+ str(int((max_val_rotate/1023)*3.3)) + "V (" + str(max_val_rotate) + "/3069)")
    
    pins.servo_write_pin(Tilt, 0)
    pause(1000)

    for i in range(181): # Tilt Logic
        pins.servo_write_pin(Tilt, i)
        pause(55)
        current_voltage_tilt = (pins.analog_read_pin(Solar_0) + pins.analog_read_pin(Solar_1))
        print("Current Voltage (Tilt): ~" + str(int((current_voltage_tilt/1023)*3.3)) + "V (" + str(current_voltage_tilt) + "/3069)")
        light_list_tilt.append(current_voltage_tilt)

    for i in range(len(light_list_tilt)):
        if light_list_tilt[i] > max_val_tilt:
            max_val_tilt = light_list_tilt[i]
            best_angle_tilt = i
        
    pins.servo_write_pin(Tilt, best_angle_tilt)
    print("Best Angle Found! " + str(best_angle_tilt) + " Degrees (Tilt)")
    print("Maximum Voltage (Tilt): ~"+ str(int((max_val_tilt/1023)*3.3)) + "V (" + str(max_val_tilt) + "/3069)")
    music.play(music.tone_playable(262, music.beat(BeatFraction.WHOLE)), music.PlaybackMode.UNTIL_DONE)
    
    print("\n---Results---\n")
    print("Best Angle (Rotate): " + str(best_angle_rotate) + " Degrees")
    print("Best Angle (Tilt): " + str(best_angle_tilt) + " Degrees")
    print("Maximum Voltage (Rotate): ~" + str(int((max_val_rotate/1023)*3.3)) + "V (" + str(max_val_rotate) + "/3069)")
    print("Maximum Voltage (Tilt): ~" + str(int((max_val_tilt/1023)*3.3)) + "V (" + str(max_val_tilt) + "/3069)")

input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_b():
    pins.servo_write_pin(Tilt, 0)
    pins.servo_write_pin(Rotate, 0)
    print("Successfully Zero'd!")

input.on_button_pressed(Button.B, on_button_pressed_b)

def on_pin_pressed_p0():
    control.reset()
input.on_pin_pressed(TouchPin.P0, on_pin_pressed_p0)
