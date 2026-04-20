light_list = []
light_list2 = []
max_val = 0
best_angle = 0
max_val2 = 0
best_angle2 = 0

pins.analog_set_period(AnalogPin.P12, 20000)
pins.analog_set_period(AnalogPin.P8, 20000)

def on_button_pressed_a():
    global light_list, max_val, best_angle, max_val2, best_angle2, light_list2
    
    light_list = []
    max_val = 0
    best_angle = 0
    max_val2 = 0
    best_angle2 = 0
    
    pins.servo_write_pin(AnalogPin.P12, 45)
    pause(500)

    for i in range(181):
        pins.servo_write_pin(AnalogPin.P8, i)
        pause(40)
        current_voltage = pins.analog_read_pin(AnalogPin.P4)
        print("Rotate Volts: " + str(current_voltage))
        light_list.append(current_voltage)

    for i in range(len(light_list)):
        if light_list[i] > max_val:
            max_val = light_list[i]
            best_angle = i

    pause(500)        
    
    pins.servo_write_pin(AnalogPin.P12, -45)
    for i in range(181):
            pins.servo_write_pin(AnalogPin.P8, i)
            pause(40)
            current_voltage = pins.analog_read_pin(AnalogPin.P4)
            print("Rotate Volts: " + str(current_voltage))
            light_list.append(current_voltage)

    for i in range(len(light_list)):
        if light_list[i] > max_val:
            max_val = light_list[i]
            best_angle = i

    pins.servo_write_pin(AnalogPin.P8, best_angle)

    for i in range(181):
        pins.servo_write_pin(AnalogPin.P12, i)
        pause(40)
        current_voltage2 = pins.analog_read_pin(AnalogPin.P4)
        print("Tilt Volts: " + str(current_voltage2))
        
        if current_voltage2 > max_val2:
            max_val2 = current_voltage2
            best_angle2 = i

    pins.servo_write_pin(AnalogPin.P12, best_angle2)
    
    print("Best Tilt: " + str(best_angle2))
    print("Best Rotate: " + str(best_angle))
    
    music.play(music.tone_playable(262, music.beat(BeatFraction.WHOLE)), music.PlaybackMode.UNTIL_DONE)

def on_button_pressed_b():
    pins.servo_write_pin(AnalogPin.P12, 0)
    pins.servo_write_pin(AnalogPin.P8, 0)

input.on_button_pressed(Button.A, on_button_pressed_a)
input.on_button_pressed(Button.B, on_button_pressed_b)
