from RPi import GPIO
import time
GPIO.setmode(GPIO.BCM)

from smbus import SMBus
i2c = SMBus()
i2c.open(1)

adres = 0x38

class Rotary:
    
    def __init__(self,clk=16,dt=20, knop_aan = True, sw=24, knop_both = False, callback = None) -> None:
        self.clk = clk
        self.dt = dt
        self.sw = sw
        self.knop_aan = knop_aan
        self.knop_both = knop_both
        self.callback = callback
        self.counter = 0
        self.richting = None
        self.status = '00'
        self.gedrukt = 0
        self.setup_pins()
        self.clkLastState = GPIO.input(self.clk)
        if self.knop_aan == True:
            self.status_knop =  GPIO.input(self.sw)
    
    # def callback_print(self, waarde, richting):
    #     print(f"{waarde}, Richting: {richting}")

    def callback_rotation_decode(self, pin):
        status_clk = GPIO.input(self.clk)
        status_dt = GPIO.input(self.dt)
        nieuwe_status = "{}{}".format(status_dt, status_clk)

        # status:             0      1     2     3    4
        # klokwijs      (R): 00 -> 01 -> 11 -> 10 -> 00
        # tegen de klok (L): 00 -> 10 -> 11 -> 01 -> 00

        if self.status == "00": # Positie in rust
            if nieuwe_status == "01": # Draaide 1 naar rechts (R0 -> R1) (clk veranderde eerst)
                self.richting = "R"
            elif nieuwe_status == "10": # Draaide 1 naar links (L0 -> L1) (dt veranderde eerst)
                self.richting = "L"

        elif self.status == "01": # R1 or L3 position
            if nieuwe_status == "11": # Draaide 1 naar rechts (R1 -> R2) (clk was al 1 en de dt wordt nu ook 1)
                self.richting = "R"
            elif nieuwe_status == "00": # Draaide 1 naar links (L3 -> L4)
                if self.richting == "L":
                    self.counter = self.counter - 1
                    if self.callback is not None:
                        self.callback(self.counter, self.richting)
        

        elif self.status == "10": # R3 or L1
            if nieuwe_status == "11": # Draaide 1 naar links (L1 -> L2)
                self.richting = "L"
            elif nieuwe_status == "00": # Draaide 1 naar rechts (R3 -> R4)
                if self.richting == "R":
                    self.counter = self.counter + 1
                    if self.callback is not None:
                        self.callback(self.counter, self.richting)

        else: # self.status == "11"
            if nieuwe_status == "01": # Draaide 1 naar links (L2 -> L3)
                self.richting = "L"
            elif nieuwe_status == "10": # Draaide 1 naar rechts (R2 -> R3)
                self.richting = "R"
            elif nieuwe_status == "00": # Sloeg een tussenstand 01 of 10 status over, hierdoor weten we de richting niet. Dus we gebruiken de voorgaande richting. 
                if self.richting == "L": # Indien de vorige keer naar links gedraaid werd:
                    self.counter = self.counter - 1
                    if self.callback is not None:
                        self.callback(self.counter, self.richting)
                elif self.richting == "R": # Indien de vorige keer naar rechts gedraaid werd: 
                    self.counter = self.counter + 1
                    if self.callback is not None:
                        self.callback(self.counter, self.richting)
                
        self.status = nieuwe_status

        # if ((status_clk != self.clkLastState) and (status_clk == 0)):
        #     # eerst een verschil opmerken en dan pas 1 van de 2 keer het doorlaten 
        #     # in de andere volgorde werkt ook (heb het getest)
        #     # == 0 want anders doorloop je het 2 keer 
        #     if (status_dt != status_clk):
        #         # print("klokwijs")
        #         self.counter += 1
        #         self.richting = '+'
        #     else:
        #         # print("tegen de klok")
        #         self.counter -= 1
        #         self.richting = '-'
        #     print(f"{self.counter} , Richting: {self.richting}")
        # self.clkLastState = status_clk # moet erbuiten staan anders blijft de waarde behouden

    def get_counter(self):
        return self.counter
        
    def reset_counter(self):
        self.counter = 0

    def get_button(self):
        result = self.gedrukt
        self.gedrukt = 0
        return result
        # vb van iets doen:
        # gedrukt_knop = mijn_rotor.get_button()
        # if (gedrukt_knop != knopVorig) and (gedrukt_knop == 1):
        #     print(f'er is op de knop van de rotor gedrukt {gedrukt_knop}')
        # knopVorig = gedrukt_knop

    def pushed_callback(self, pin):
        self.status_knop = GPIO.input(self.sw)
        if (self.status_knop == 0):
            # dus enkel als hij ingedrukt is, niet ook bij loslaten (terwijl dit initieel al niet zou mogen)
            self.gedrukt = 1
            print(f'Er werd op de knop gedrukt.')

    def setup_pins(self):
        GPIO.setup(self.clk,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.dt,GPIO.IN, pull_up_down=GPIO.PUD_UP) 
        GPIO.add_event_detect(self.clk, GPIO.BOTH, callback=self.callback_rotation_decode)
        GPIO.add_event_detect(self.dt, GPIO.BOTH, callback=self.callback_rotation_decode)
        if self.knop_aan == True:
            GPIO.setup(self.sw,GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.clkLastState = GPIO.input(self.clk)
            if (self.knop_both == True):
                GPIO.add_event_detect(self.sw, GPIO.BOTH, callback=self.pushed_callback, bouncetime=1)
            else:
                GPIO.add_event_detect(self.sw, GPIO.FALLING, callback=self.pushed_callback, bouncetime=300)

    def close_rotor(self):
        if self.knop_aan == True:
            GPIO.remove_event_detect(self.clk)
        GPIO.remove_event_detect(self.clk)
        GPIO.remove_event_detect(self.dt)
        # GPIO.cleanup()