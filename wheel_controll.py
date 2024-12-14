import wiringpi

PWM_MAX=100
PWM_STOP=0

class WheelController:
    def __init__(self):
        self.pin_list = [2,3,14,15,27,17,23,24]
        self.front_left_f = self.pin_list[0]
        self.front_left_b = self.pin_list[1]
        self.front_right_f = self.pin_list[2]
        self.front_right_b = self.pin_list[3]
        self.rear_left_f = self.pin_list[4]
        self.rear_left_b = self.pin_list[5]
        self.rear_right_f = self.pin_list[6]
        self.rear_right_b = self.pin_list[7]
        for pin in self.pin_list:
            init_value = 0
            pwm_range = 100
            wiringpi.pinMode(pin, wiringpi.OUTPUT)
            wiringpi.softPwmCreate(pin, init_value, pwm_range)

    def front_left_motor(self, pwm):
        pwm = int(pwm)
        positive = True if pwm > 0 else False
        pwm = int(pwm/abs(pwm)*PWM_MAX) if pwm > PWM_MAX or pwm < -PWM_MAX else pwm
        if positive:
            wiringpi.softPwmWrite(self.front_left_f, pwm)
            wiringpi.softPwmWrite(self.front_left_b, PWM_STOP)
        else:
            wiringpi.softPwmWrite(self.front_left_f, PWM_STOP)
            wiringpi.softPwmWrite(self.front_left_b, -pwm)
    def front_right_motor(self, pwm):
        pwm = int(pwm)
        positive = True if pwm > 0 else False
        pwm = int(pwm/abs(pwm)*PWM_MAX) if pwm > PWM_MAX or pwm < -PWM_MAX else pwm
        if positive:
            wiringpi.softPwmWrite(self.front_right_f, pwm)
            wiringpi.softPwmWrite(self.front_right_b, PWM_STOP)
        else:
            wiringpi.softPwmWrite(self.front_right_f, PWM_STOP)
            wiringpi.softPwmWrite(self.front_right_b, -pwm)
    def rear_left_motor(self, pwm):
        pwm = int(pwm)
        positive = True if pwm > 0 else False
        pwm = int(pwm/abs(pwm)*PWM_MAX) if pwm > PWM_MAX or pwm < -PWM_MAX else pwm
        if positive:
            wiringpi.softPwmWrite(self.rear_left_f, pwm)
            wiringpi.softPwmWrite(self.rear_left_b, PWM_STOP)
        else:
            wiringpi.softPwmWrite(self.rear_left_f, PWM_STOP)
            wiringpi.softPwmWrite(self.rear_left_b, -pwm)
    def rear_right_motor(self, pwm):
        pwm = int(pwm)
        positive = True if pwm > 0 else False
        pwm = int(pwm/abs(pwm)*PWM_MAX) if pwm > PWM_MAX or pwm < -PWM_MAX else pwm
        if positive:
            wiringpi.softPwmWrite(self.rear_right_f, pwm)
            wiringpi.softPwmWrite(self.rear_right_b, PWM_STOP)
        else:
            wiringpi.softPwmWrite(self.rear_right_f, PWM_STOP)
            wiringpi.softPwmWrite(self.rear_right_b, -pwm)
    def move(self, dir_index, pwm):
        if dir_index == 0:
            self.front_left_motor(pwm)
            self.front_right_motor(pwm)
            self.rear_left_motor(pwm)
            self.rear_right_motor(pwm)
        elif dir_index == 1:
            self.front_left_motor(pwm)
            self.front_right_motor(PWM_STOP)
            self.rear_left_motor(PWM_STOP)
            self.rear_right_motor(pwm)
        elif dir_index == 2:
            self.front_left_motor(pwm)
            self.front_right_motor(-pwm)
            self.rear_left_motor(-pwm)
            self.rear_right_motor(pwm)
        elif dir_index == 3:
            self.front_left_motor(PWM_STOP)
            self.front_right_motor(-pwm)
            self.rear_left_motor(-pwm)
            self.rear_right_motor(PWM_STOP)
        elif dir_index == 4:
            self.front_left_motor(-pwm)
            self.front_right_motor(-pwm)
            self.rear_left_motor(-pwm)
            self.rear_right_motor(-pwm)
        elif dir_index == 5:
            self.front_left_motor(-pwm)
            self.front_right_motor(PWM_STOP)
            self.rear_left_motor(PWM_STOP)
            self.rear_right_motor(-pwm)
        elif dir_index == 6:
            self.front_left_motor(-pwm)
            self.front_right_motor(pwm)
            self.rear_left_motor(pwm)
            self.rear_right_motor(-pwm)
        elif dir_index == 7:
            self.front_left_motor(PWM_STOP)
            self.front_right_motor(pwm)
            self.rear_left_motor(pwm)
            self.rear_right_motor(PWM_STOP)
    def rotate(self, pwm):
        self.front_left_motor(pwm)
        self.front_right_motor(-pwm)
        self.rear_left_motor(pwm)
        self.rear_right_motor(-pwm)
    def stop(self):
        for pin in self.pin_list:
            wiringpi.softPwmWrite(pin, PWM_STOP)
        