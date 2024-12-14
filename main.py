import os
import pygame
import wiringpi
import sympy
import math
from multiprocessing import Process
import subprocess


from wheel_controll import WheelController
os.environ["SDL_VIDEODRIVER"] = "dummy"
sqrt2 = math.sqrt(2)
LED1 = 4
LED2 = 18

# pygame初期化
pygame.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()


# ジョイスティックの出力数値を調整
def map_axis(val):
    val = round(val, 2)
    in_min = -1
    in_max = 1
    out_min = -100
    out_max = 100
    return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


# ジョイスティックの出力数値を調整(L2 R2ボタン)
def map_axis_t(val):
    val = map_axis(val)
    if val <= 0 and val >= -100:
        in_min = -100
        in_max = 0
        out_min = 0
        out_max = 50
        return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
    else:
        in_min = 0
        in_max = 100
        out_min = 50
        out_max = 100
        return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def led_blinking():
    wiringpi.pinMode(LED1, wiringpi.OUTPUT)
    wiringpi.pinMode(LED2, wiringpi.OUTPUT)
    for i in range(39):
        wiringpi.digitalWrite(LED1,wiringpi.HIGH)
        wiringpi.digitalWrite(LED2,wiringpi.HIGH)
        wiringpi.delayMicroseconds(1000_000)
        wiringpi.digitalWrite(LED2,wiringpi.LOW)
        wiringpi.digitalWrite(LED1,wiringpi.LOW)
        wiringpi.delayMicroseconds(1000_000)
def play_music():
    subprocess.call("mpg321 jingle_bell.mp3", shell=True)
    
def led_pwm():
    pin = 2
    init_value = 0
    pwm_range = 100
    wiringpi.pinMode(pin, wiringpi.OUTPUT)
    wiringpi.softPwmCreate(pin, init_value, pwm_range)
    while True:
        for value in range(100):
            wiringpi.softPwmWrite(pin, value)
            wiringpi.delay(10)
        for value in list(range(100))[::-1]:
            wiringpi.softPwmWrite(pin, value)
            wiringpi.delay(10)
def move(wheel_controller, gamepad_data):
    x = gamepad_data["joy_lx"]
    y = gamepad_data["joy_ly"]
    norm = math.sqrt(x*x+y*y)
    if norm == 0:
        wheel_controller.stop()
        return
    x = x/norm
    y = y/norm
    direction_vector = [[0,1],[1/sqrt2,1/sqrt2],[1,0],[1/sqrt2,-1/sqrt2],[0,-1],[-1/sqrt2,-1/sqrt2],[-1,-0],[-1/sqrt2,1/sqrt2]]
    cosine_values = []
    for vector in direction_vector:
        cosine_value = vector[0] * x + vector[1] * y
        cosine_values.append(cosine_value)
    direction_index = cosine_values.index(max(cosine_values))
    if direction_index in [1,3,5,7]:
        norm /= sqrt2
    print(direction_index, norm)
    wheel_controller.move(direction_index, norm)
def rotate(wheel_controller, gamepad_data):
    r = gamepad_data["joy_rx"]
    wheel_controller.rotate(r)



def main():
    wiringpi.wiringPiSetupGpio()
    wheel_controller = WheelController()

    while True:
        # イベントチェック
        if pygame.event.get():
            gamepad_data = {
                "joy_lx": map_axis(joystick.get_axis(0)),
                "joy_ly": -map_axis(joystick.get_axis(1)),
                "joy_rx": map_axis(joystick.get_axis(3)),
                "joy_ry": -map_axis(joystick.get_axis(4)),
                "joy_lt": map_axis_t(joystick.get_axis(2)),
                "joy_rt": map_axis_t(joystick.get_axis(5)),
                "hat_x": joystick.get_hat(0)[0],
                "hat_y": joystick.get_hat(0)[1],
                "btn_a": joystick.get_button(0),
                "btn_b": joystick.get_button(1),
                "btn_x": joystick.get_button(2),
                "btn_y": joystick.get_button(3),
                "btn_lb": joystick.get_button(4),
                "btn_rb": joystick.get_button(5),
                "btn_back": joystick.get_button(6),
                "btn_start": joystick.get_button(7),
                "btn_guide": joystick.get_button(8),
                "btn_joyl": joystick.get_button(9),
                "btn_joyr": joystick.get_button(10)
            }
            print(gamepad_data)
            if gamepad_data["joy_rx"] == 0:
                move(wheel_controller, gamepad_data)
            else:
                rotate(wheel_controller, gamepad_data)
            if gamepad_data["btn_a"] != 0:
                led_process = Process(target=led_blinking, args=())
                music_process = Process(target=play_music, args=())
                led_process.start()
                music_process.start()
            
            


if __name__ == '__main__':
    main()