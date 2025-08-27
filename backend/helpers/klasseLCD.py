from RPi import GPIO
from smbus import SMBus
import time

# import serial 

GPIO.setmode(GPIO.BCM)


def initialiseer(pin_RS, pin_E):
    GPIO.setup(pin_RS,GPIO.OUT)
    GPIO.setup(pin_E,GPIO.OUT)
    # for i in range(8):
    #     GPIO.setup(lijst_datapinnen[i],GPIO.OUT)

# RS = laag => sturen van instructie
# RS = hoog => sturen van karakters

# E = tijdens dalende flank => data wordt verwerkt
# E = hoog => data klaarzetten => E = laag => wachten => ...


def waardeFunctionSet(is4bit:bool):
    if is4bit == False:
        return 0x3F
    else:
        return 0b00101111

def waardeDisplayOn(displayOn:bool, cursor:bool, blinkCursor:bool):
    result = 0b00001000
    if displayOn == True:
        result = result | 0b100
    if cursor == True:
        result = result | 0b10
    if blinkCursor == True:
        result = result | 0b1
    return result

class LCD:

    def __init__(self,adres_PCF,pin_RS:int, pin_E:int, isVierBits=False, displayOn=True, cursor=True, blinkCursor=True ) -> None:
        self.isVierBits = isVierBits
        self.displayOn = displayOn
        self.cursor = cursor
        self.blinkCursor = blinkCursor
        
        self.adres_PCF = adres_PCF
        self.pin_RS = pin_RS
        self.pin_E = pin_E

        self.huidige_pagina = 1

        self.i2c = SMBus()
        self.i2c.open(1)
        initialiseer(self.pin_RS, self.pin_E)
        self.init_LCD()
        
        
        
    def plaatsLCD(self, value):
        result = 0b10000000 | value
        return result

    

    # def zet_data_bits(self, value):
    #     # byte => 8 bits
    #     for i in range(8):
    #         # i gaat van 0 tot en met 7
    #         bit_i = (value >> i) & 1
    #         # print (bit_i) # LSB komt er eerst uit en kennen we toe aan D0
    #         if (bit_i == 1):
    #             GPIO.output(self.lijst_datapinnen[i],GPIO.HIGH)
    #             # print(f"bit D{i} hoog gezet")
    #         else:
    #             GPIO.output(self.lijst_datapinnen[i],GPIO.LOW)
    #             # print(f"bit D{i} laag gezet")
            
    # zet_data_bits(0b11001010)
    # zet_data_bits(0x0F)

    def stuur_instructie(self, value):
        GPIO.output(self.pin_RS,GPIO.LOW) # RS = laag => sturen van instructie
        GPIO.output(self.pin_E,GPIO.HIGH) # E = hoog => data klaarzetten
        # hierboven laten staan (binnen functie)

        # self.zet_data_bits(value)
        self.i2c.write_byte(self.adres_PCF, value)

        # hieronder laten staan (binnen functie)
        GPIO.output(self.pin_E,GPIO.LOW) # E = laag => data laten verwerken
        time.sleep(0.01) # om de data te laten verwerken


    def send_character(self, value):
        GPIO.output(self.pin_RS,GPIO.HIGH) # RS = hoog => sturen van karakters
        GPIO.output(self.pin_E,GPIO.HIGH) # E = hoog => data klaarzetten

        # self.zet_data_bits(value)
        self.i2c.write_byte(self.adres_PCF, value)
        
        GPIO.output(self.pin_E,GPIO.LOW) # E = laag => data laten verwerken
        time.sleep(0.01) # om de data te laten verwerken

    def write_message(self, message):
        if len(message) <= 32:
            teller_enkel_LCD = 0
            for teken in message:
                teller_enkel_LCD +=1
                self.send_character(ord(teken))
                if teller_enkel_LCD == 16:
                    self.cursor_einde_naar_begin_volgende()
        else:
            for teken in message:
                self.send_character(ord(teken))
                
    
    def clearLCD(self):
        self.stuur_instructie(0x01) # 01 = Clear display & Cursor home (0x00)
        
    def cursorHome_0x00(self):
        self.stuur_instructie(0x03) # 02 = Cursor home (0x00)

    def displayShift(self, links=True, volledig=False):
        # links true betekend dat de tekst links staat en dan de cursor rechts ervan
        result = 0b00000100
        if  links == True:
            #dus naar links
            result = result | 0b10
        if volledig == True:
            result = result | 0b1
        self.stuur_instructie(result)
        # return result
    
    # def cursorOrDisplayShift(self, cursor_or_display_Right=True, displayFollow=False):
    #     # niet meer nodig wegens 'cursor_shift()' en 'display_shift()'

    #     # cursorRight = True => je cursor schuift 1 op
    #     # als je op 0x27 staat (einde 1e lijn) ga je naar de volgende lijn (begin 2e lijn)

    #     # displayFollow = True => het display scherm verplaatst zich, cursor blijft op dezefde adres van blokje staan
    #     # cursorRight = True => visueel is alles 1 naar rechts verschoven (dus links een kolom bij en rechts een kolom weg)
    #     result = 0b00010000
    #     if  cursor_or_display_Right == True:
    #         result = result | 0b100
    #     if displayFollow == True:
    #         result = result | 0b1000
    #     self.stuur_instructie(result)
    #     return result


    def cursor_shift(self,aantal=1, rechts=True):
        result = 0b00010000
        if  rechts == True:
            result = result | 0b100
        for keer in range(aantal):    
            self.stuur_instructie(result)
    
    
    def display_shift(self, aantal=1, alles_1_naar_rechts=True):
        result = 0b00011000
        if  alles_1_naar_rechts == True:
            result = result | 0b100
        for keer in range(aantal):
            self.stuur_instructie(result)
        
    
    def setCursor(self, plaats):
        self.stuur_instructie(self.plaatsLCD(plaats))

    def cursor_omhoog_omlaag(self):
        # deze functie werkt volgens mij niet
        for keer in range(40):
            self.cursor_shift()
    
    def cursor_einde_naar_begin_volgende(self):
        for keer in range(24):
            self.cursor_shift()
    
    def cursor_ga_naar(self, pagina=1, lijn=1):
        if pagina == 1:
            if lijn == 1:
                self.setCursor(0x00)
            elif lijn == 2:
                self.setCursor(0x40)
        elif pagina == 2:
            if lijn == 1:
                self.setCursor(0x10)
            elif lijn == 2:
                self.setCursor(0x50)
            

    def display_zichtbaar_maken(self, pagina:int = 1):
        if self.huidige_pagina != pagina:
            if ((self.huidige_pagina == 1) and (pagina == 2)):
                self.display_shift(16, False)
                self.huidige_pagina = pagina
            elif ((self.huidige_pagina == 2) and (pagina == 1)):
                self.display_shift(16,True)
                self.huidige_pagina = pagina
            else:
                print("Geef pagina nummer 1 of 2 op.")
        else:
            return None
        
    def pagina_legen(self, pagina:int=1, lengte_lijn=16):
        if pagina == 1:
            self.cursorHome_0x00()
            for i in range(lengte_lijn):
                self.write_message(" ")  
            self.cursor_ga_naar(1,2)
            for i in range(lengte_lijn):
                self.write_message(" ")  
        elif pagina == 2:
            self.cursor_ga_naar(2,1)
            for i in range(lengte_lijn):
                self.write_message(" ") 
            self.cursor_ga_naar(2,2)
            for i in range(lengte_lijn):
                self.write_message(" ")         


    def set_cursor_display(self, cursorOn = None, blinkCursor = None, displayOn = None):
        if cursorOn is not None:
            self.cursor = cursorOn
        if blinkCursor is not None:
            self.blinkCursor = blinkCursor
        if displayOn is not None:
            self.displayOn = displayOn
        self.stuur_instructie(waardeDisplayOn(self.displayOn, self.cursor, self.blinkCursor))

    def init_LCD(self):
        self.stuur_instructie(waardeFunctionSet(self.isVierBits)) # vb 3F = function set - 8bits - 2 lijnen
        self.stuur_instructie(waardeDisplayOn(self.displayOn, self.cursor, self.blinkCursor)) # vb 0F = Display on - cursor on - blink on
        self.stuur_instructie(0x01) # 01 = Clear display & Cursor home
        
        # self.displayShift()
        

    def closesLCD(self):
        # GPIO.cleanup()
        self.i2c.close()