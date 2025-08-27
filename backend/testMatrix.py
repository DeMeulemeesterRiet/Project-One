import spidev 
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
chip_select = 18
GPIO.setup(chip_select, GPIO.OUT)
# MAX7219 Registers: 
#   NoOp: 0x00
#   Digit0: 0x01
#   Digit1: 0x02
#   Digit2: 0x03
#   Digit3: 0x04
#   Digit4: 0x05
#   Digit5: 0x06
#   Digit6: 0x07
#   Digit7: 0x08
#   DecodeMode: 0x09
#   Intensity: 0x0a   (van 0x0 tot en met 0xF)
#   ScanLimit: 0x0b   (van 0x0 tot en met 0x7)
#   Shutdown: 0x0c    (shutdown = 0 ; normal = 1)
#   DisplayTest: 0x0f (testmodus = 1 ; normal = 0)

# [dp, a, b, c, d, e, f, g]

class Max7219:
    # MAX7219 LED Matrix module 
    # LED dot matrix

    def __init__(self,bus=0,device=0, maxspeed_hz:int = 100000, decodeMode=0x0, scanLimiet=0x7, intensiteit = 0x0, shutdown = 0x1) -> None:
        self.segment_value = [0,0,0,0,0,0,0,0]
        self.spi = spidev.SpiDev() 
        self.spi.open(bus, device) # Bus SPI0, slave op CE 0 
        self.spi.max_speed_hz = maxspeed_hz # 10 ** 5= 100 kHz
        self.decodeMode = decodeMode
        self.intensiteit = intensiteit
        self.scanLimiet = scanLimiet
        self.shutdown = shutdown
        self.setup()
    
    def setup(self):
        
        self.spi.writebytes([0xB, self.scanLimiet])  # Zet het Scan Limit register (0xB) op 0x7 zodat alle 8 rijen kunnen worden gebruikt.
        self.spi.writebytes([0x9, self.decodeMode])  # Schrijf voor alle zekerheid een 0x0 naar register 0x9 (want we gebruiken maar 1 dot matrix)
        self.spi.writebytes([0xC, self.shutdown])  # Plaats een 1 in het Shutdown-register (display aanleggen) en dan kan je de display beginnen gebruiken 
        # door per rij een overeenkomstige byte naar het juiste register (0x1-0x8) te schrijven. 
        self.spi.writebytes([0xA, self.intensiteit])
    
    def test_matrix(self):
        self.spi.writebytes([0xF, 1])  # testmodus aan
        time.sleep(2)
        self.spi.writebytes([0xF, 0]) # testmodus uit 
        self.spi.writebytes([0xF, 0x00]) # testmodus uit voor de zekerheid

    def set_intensity(self, value_0_F:hex=0xf):
        self.intensiteit = value_0_F
        self.spi.writebytes([0xA, value_0_F])

    def set_limit(self, value_0_7=0x7):
        self.scanLimiet = value_0_7
        self.spi.writebytes([0xB, value_0_7])

    def display_on(self):
        self.shutdown = 0x1
        self.spi.writebytes([0xC, 0x1])

    def display_off(self):
        self.shutdown = 0x0
        self.spi.writebytes([0xC, 0x0])

    def draw_cross(self):
        self.spi.writebytes([0x1, 0x0]) 
        self.spi.writebytes([0x2, 0b01000010]) 
        self.spi.writebytes([0x3, 0b00100100]) 
        self.spi.writebytes([0x4, 0b00011000]) 
        self.spi.writebytes([0x5, 0b00011000]) 
        self.spi.writebytes([0x6, 0b00100100]) 
        self.spi.writebytes([0x7, 0b01000010])
        self.spi.writebytes([0x8, 0x0]) 

    def draw_rectangle(self):
        self.spi.writebytes([0x1, 0x0]) 
        self.spi.writebytes([0x2, 0b01111110]) 
        self.spi.writebytes([0x3, 0b01000010]) 
        self.spi.writebytes([0x4, 0b01000010]) 
        self.spi.writebytes([0x5, 0b01000010]) 
        self.spi.writebytes([0x6, 0b01000010]) 
        self.spi.writebytes([0x7, 0b01111110])
        self.spi.writebytes([0x8, 0x0]) 

    def draw_rectangle_with_cross(self):
        self.spi.writebytes([0x1, 0x0]) 
        self.spi.writebytes([0x2, 0b01111110]) 
        self.spi.writebytes([0x3, 0b01100110]) 
        self.spi.writebytes([0x4, 0b01011010]) 
        self.spi.writebytes([0x5, 0b01011010]) 
        self.spi.writebytes([0x6, 0b01100110]) 
        self.spi.writebytes([0x7, 0b01111110])
        self.spi.writebytes([0x8, 0x0]) 

    def delete_matrix(self):
        for i in range(9):
            self.spi.writebytes([i, 0x0]) 

    def draw_pixel(self, row_1_8, col_1_8):
        mask = 0b1 << (8-col_1_8)
        self.segment_value[row_1_8] = self.segment_value[row_1_8] | mask
        self.spi.writebytes([row_1_8, self.segment_value[row_1_8]]) 

    def clear_pixel(self, row_1_8, col_1_8):
        mask = (0b1 << (8-col_1_8)) ^ 0b11111111
        self.segment_value[row_1_8] = self.segment_value[row_1_8] & mask
        self.spi.writebytes([row_1_8, self.segment_value[row_1_8]]) 

    def toggle_pixel(self, row_1_8, col_1_8):
        mask = 0b1 << (8-col_1_8)
        self.segment_value[row_1_8] = self.segment_value[row_1_8] ^ mask
        self.spi.writebytes([row_1_8, self.segment_value[row_1_8]]) 

    def write_bytes (self, register, value):
        self.spi.writebytes([register, value])

    def write_bytes_test (self, value):
        self.spi.writebytes(value)

    def closespi(self):
        self.spi.close()



# spi.writebytes([register, value]) # Waarde naar register schrijven

# spi.writebytes([0xF, 1])  # testmodus aan
# time.sleep(2)
# spi.writebytes([0xF, 0]) # testmodus uit 
# spi.writebytes([0xF, 0x00]) # testmodus uit voor de zekerheid

mijn_matrix = Max7219(bus=0, device=0, decodeMode=0, scanLimiet=7, intensiteit=0, shutdown=1)

# mijn_matrix.write_bytes(0x09, 0x00)
# mijn_matrix.set_intensity(0x0)
# mijn_matrix.write_bytes(0x0B, 0x07)

# mijn_matrix.write_bytes(0x0c, 0x01)

# mijn_matrix.write_bytes(0x01, 0x01)
# mijn_matrix.write_bytes(0x02, 0x02)
# mijn_matrix.write_bytes(0x00, 0x03)
# mijn_matrix.write_bytes(0x03, 0x04)

# mijn_matrix.write_bytes(0x01, 0b10000010011000111000)
# mijn_matrix.write_bytes(0x01, 0xFE00000000000000)
# mijn_matrix.write_bytes(0x02, 0x02)
# mijn_matrix.write_bytes(0x03, 0x03)
# mijn_matrix.write_bytes(0x04, 0x04)
# mijn_matrix.write_bytes(0x05, 0x05)
# mijn_matrix.write_bytes(0x06, 0x06)
# mijn_matrix.write_bytes(0x07, 0x07)
# mijn_matrix.write_bytes(0x08, 0x00)

# mijn_matrix.write_bytes(0x0F, 0x01)
# time.sleep(2)
# mijn_matrix.write_bytes(0x0F, 0x00)

lijst_lijnen = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]

# GPIO.output(chip_select, GPIO.LOW)
for i in lijst_lijnen:
    mijn_matrix.write_bytes_test([i, 0xC3])
    
   
# GPIO.output(chip_select, GPIO.HIGH)

mijn_matrix.closespi()
print("gedaan")





