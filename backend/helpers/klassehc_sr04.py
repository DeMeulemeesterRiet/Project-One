from RPi import GPIO
import time

class HC_SR04:
    def __init__(self, pin_trig, pin_echo):
        self.trig = pin_trig
        self.echo = pin_echo

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig,GPIO.OUT)
        GPIO.setup(self.echo,GPIO.IN)
        GPIO.output(self.trig, False)
        time.sleep(2) # Waiting a few seconds for the sensor to settle
        


    def afstand_uitlezen(self):
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)
        while GPIO.input(self.echo)==0:
            pulse_start = time.time()
        while GPIO.input(self.echo)==1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        print(f'Distance: {distance} cm')
        return distance

    
