# This program was written for EnergyOptix in the KidWInd Challenge.
# This program is not to be used by anyone other then those authorized.
# Written by Austin Dixon and Justin Pongpairoj
# Solar Panels on Pins 0 and 2, Rotation Servo on Pin 3, and Tilt Servo on Pin 4

# Variable Declarations
light_list_tilt = []
max_val_tilt = 0
best_angle_tilt = 0
light_list_rotate = []
max_val_rotate = 0
best_angle_rotate = 0


# Constants
Solar_0 = AnalogPin.P0
Solar_1 = AnalogPin.P2
Rotate = AnalogPin.P3
Tilt = AnalogPin.P4

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
        pins.servo_write_pin(Tilt, 135)
        pins.servo_write_pin(Rotate, i)
        pause(60)
        
        current_voltage_rotate = (pins.analog_read_pin(Solar_0) + pins.analog_read_pin(Solar_1))
        
        if current_voltage_rotate > max_val_rotate:
            max_val_rotate = current_voltage_rotate
            best_angle_rotate = i

    for i in range(181):
        angle = 180 - i
        pins.servo_write_pin(Tilt, 45)
        pins.servo_write_pin(Rotate, angle)
        pause(60)
        
        current_voltage_rotate = (pins.analog_read_pin(Solar_0) + pins.analog_read_pin(Solar_1))
        print(current_voltage_rotate)
        if current_voltage_rotate > max_val_rotate:
            max_val_rotate = current_voltage_rotate
            best_angle_rotate = angle


    pins.servo_write_pin(Rotate, best_angle_rotate)
    print("Best Angle Found! " + best_angle_rotate + " Degrees (Rotate)")
    print("Maximum Voltage (Rotate): ~"+ int((max_val_rotate/2046)*3.3)+ "V (" + max_val_rotate + "/2046)")
    for i in range(181): # Tilt Logic
    
        pins.servo_write_pin(Tilt, i)

        pause(60)
        current_voltage_tilt = (pins.analog_read_pin(Solar_0) + pins.analog_read_pin(Solar_1))
        print("Current Voltage (Tilt): ~" + int((current_voltage_tilt/2046)*3.3)+ "V (" + current_voltage_tilt + "/2046)")
        light_list_tilt.append(current_voltage_tilt)

    for i in range(len(light_list_tilt)):
        if light_list_tilt[i] > max_val_tilt:
            max_val_tilt = light_list_tilt[i]
            best_angle_tilt = i
        
    pins.servo_write_pin(Tilt, best_angle_tilt)
    print("Best Angle Found! " + best_angle_tilt + " Degrees (Tilt)")
    print("Maximum Voltage (Tilt): ~"+ int((max_val_tilt/2046)*3.3)+ "V (" + max_val_tilt + "/2046)")
    music.play(music.tone_playable(262, music.beat(BeatFraction.WHOLE)), music.PlaybackMode.UNTIL_DONE)
    print("\n---Results---\n")
    print("Best Angle (Rotate): " + best_angle_rotate + " Degrees")
    print("Best Angle (Tilt): " + best_angle_tilt + " Degrees")
    print("Maximum Voltage (Rotate): ~" + int((max_val_rotate/2046)*3.3)+ "V (" + max_val_rotate + "/2046)")
    print("Maximum Voltage (Tilt): ~" + int((max_val_tilt/2046)*3.3)+ "V (" + max_val_tilt + "/2046)")
input.on_button_pressed(Button.A, on_button_pressed_a)

    

def on_button_pressed_b():
    pins.servo_write_pin(Tilt, 0)
    pins.servo_write_pin(Rotate, 0)
    print("Successfully Zero'd!")
input.on_button_pressed(Button.B, on_button_pressed_b)

