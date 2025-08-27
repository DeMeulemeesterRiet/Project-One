# C3

import RPi.GPIO as GPIO
import spidev
GPIO.setmode(GPIO.BOARD)
# Definieer de CS-pin
CS_PIN = 8  # Bijvoorbeeld GPIO pin 8

# SPI-interface initialiseren
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000  # Stel de SPI-snelheid in

# Initialiseer de GPIO

GPIO.setup(CS_PIN, GPIO.OUT)

# Zet de CS-pin laag voordat SPI-communicatie begint
GPIO.output(CS_PIN, GPIO.LOW)

for i in range(9):
    spi.writebytes([i-1, 0x0])
# Voer SPI-communicatie uit
# Bijvoorbeeld: data = spi.xfer([0x01, 0x02, 0x03])

# Zet de CS-pin hoog na voltooiing van de SPI-communicatie
GPIO.output(CS_PIN, GPIO.HIGH)

for i in range(10):
    spi.writebytes(0xc4)

GPIO.output(CS_PIN, GPIO.LOW)
# Opruimen
GPIO.cleanup()
spi.close()



#x
00000
10001
01010
00100
01010
10001
00000
00000

#0
01110
10001
10001
10001
10001
10001
01110
00000

#1
00100
01100
00100
00100
00100
00100
01110
00000

#2
01110
10001
00001
00010
00100
01000
11111
00000

#3
01110
10001
00001
00110
00001
10001
01110
00000

#4
00010
00110
01010
10010
11111
00010
00010
00000

#5
11111
10000
10000
11110
00001
00001
11110
00000

#6
01110
10001
10000
11110
10001
10001
01110
00000

#7
11111
00001
00010
00100
00100
00100
00100
00000

#8
01110
10001
10001
01110
10001
10001
01110
00000

#9
01110
10001
10001
01111
00001
00010
01100
00000

