import spidev 
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
chip_select = 18
GPIO.setup(chip_select, GPIO.OUT)

GPIO.output(chip_select, GPIO.LOW)
spi = spidev.SpiDev() 
GPIO.output(chip_select, GPIO.HIGH)


GPIO.output(chip_select, GPIO.LOW)
spi.open(0,0)
GPIO.output(chip_select, GPIO.HIGH)

GPIO.output(chip_select, GPIO.LOW)
spi.max_speed_hz = 100000
GPIO.output(chip_select, GPIO.HIGH)

print("init")

GPIO.output(chip_select, GPIO.LOW)
spi.writebytes([0xF, 0x00])
GPIO.output(chip_select, GPIO.HIGH)
GPIO.output(chip_select, GPIO.LOW)
spi.writebytes([0xB, 0x7])
GPIO.output(chip_select, GPIO.HIGH)
GPIO.output(chip_select, GPIO.LOW)
spi.writebytes([0x9, 0x0])
GPIO.output(chip_select, GPIO.HIGH)
GPIO.output(chip_select, GPIO.LOW)
spi.writebytes([0xC, 0x01])
GPIO.output(chip_select, GPIO.HIGH)
GPIO.output(chip_select, GPIO.LOW)
spi.writebytes([0xA, 0x00])
GPIO.output(chip_select, GPIO.HIGH)

print("instellen ok")

lijst_lijnen = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]

test1 = [[0b1, 0b11, 0b111, 0b1111, 0b11111, 0b111111, 0b1111111, 0b11111111],
         [0b1, 0b11, 0b111, 0b1111, 0b11111, 0b111111, 0b1111111, 0b11101111]]
test2 = [[0b10101010, 0b10101010, 0b10101010, 0b10101010, 0b10101010, 0b10101010, 0b10101010, 0b10101010],
         [0b01010101, 0b01010101, 0b01010101, 0b01010101, 0b01010101, 0b01010101, 0b01010101, 0b01010101]]

test3 = [[0b1111111, 0b11111111, 0b11111111, 0b11111111, 0b10000000, 0b00000000, 0b00000000, 0b00000001],
         [0b11100000, 0b00000000, 0b00000000, 0b00000001, 0b10000000, 0b00000000, 0b00000000, 0b00000001],
         [0b11000000, 0b00000000, 0b00000000, 0b00000001, 0b10000000, 0b00000000, 0b00000000, 0b00000001],
         [0b10000000, 0b00000000, 0b10101010, 0b00000001, 0b10000000, 0b00000000, 0b00000000, 0b00000001],
         [0b10000000, 0b00000000, 0b10101010, 0b00000001, 0b10000000, 0b00000000, 0b00000000, 0b00000001],
         [0b10000000, 0b00000000, 0b00000000, 0b00000001, 0b10000000, 0b00000000, 0b00000000, 0b00000011],
         [0b10000000, 0b00000000, 0b00000000, 0b00000001, 0b10000000, 0b00000000, 0b00000000, 0b00000111],
         [0b10000000, 0b00000000, 0b00000000, 0b00000001, 0b11111111, 0b11111111, 0b11111111, 0b11111111]]

test4 = [[0b00010001, 0b11000000, 0b00010000, 0b11100000, 0b00000011, 0b10101000, 0b00010011, 0b10111000],
         [0b00110010, 0b00100000, 0b00110001, 0b00010000, 0b00000010, 0b00101010, 0b10110010, 0b10001000],
         [0b00010010, 0b00100000, 0b01010001, 0b00010000, 0b01111011, 0b10111001, 0b00010010, 0b10111000],
         [0b00010010, 0b00100000, 0b00010001, 0b00010000, 0b00000010, 0b10001010, 0b10010010, 0b10100000],
         [0b00010010, 0b00100000, 0b00010001, 0b00010000, 0b01111011, 0b10001000, 0b00111011, 0b10111000],
         [0b00010010, 0b00100000, 0b00010001, 0b00010000, 0b00000000, 0b00000000, 0b00000000, 0b00000000],
         [0b00111001, 0b11000000, 0b01111100, 0b11100000, 0b00000000, 0b00000000, 0b00000000, 0b00000000],
         [0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]]


test5 = [[0b00010001, 0b11000000, 0b00010000, 0b11100000, 0b00010001, 0b11000000, 0b00010000, 0b11100000],
         [0b00110010, 0b00100000, 0b00110001, 0b00010000, 0b00110010, 0b00100000, 0b00110001, 0b00010000],
         [0b00010011, 0b00100000, 0b01010001, 0b10010000, 0b00010010, 0b00100000, 0b01010001, 0b00010000],
         [0b00010010, 0b10100000, 0b00010001, 0b01010000, 0b00010010, 0b00100000, 0b00010001, 0b00010000],
         [0b00010010, 0b01100000, 0b00010001, 0b00110000, 0b00010010, 0b00100000, 0b00010001, 0b00010000],
         [0b00010010, 0b00100000, 0b00010001, 0b00010000, 0b00010010, 0b00100000, 0b00010001, 0b00010000],
         [0b00111001, 0b11000000, 0b01111100, 0b11100000, 0b00111001, 0b11000000, 0b01111100, 0b11100000],
         [0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]]

test6 = [[0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111],
         [0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111],
         [0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111],
         [0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111],
         [0b00010010, 0b01100000, 0b00010001, 0b00110000, 0b00010010, 0b00100000, 0b00010001, 0b00010000],
         [0b00010010, 0b00100000, 0b00010001, 0b00010000, 0b00010010, 0b00100000, 0b00010001, 0b00010000],
         [0b00111001, 0b11000000, 0b01111100, 0b11100000, 0b00111001, 0b11000000, 0b01111100, 0b11100000],
         [0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]]

# test7 = [[255, 255, 255, 255, 18, 18, 57, 0], 
#          [255, 255, 255, 255, 96, 32, 192, 0], 
#          [255, 255, 255, 255, 17, 17, 124, 0], 
#          [255, 255, 255, 255, 48, 16, 224, 0], 
#          [255, 255, 255, 255, 18, 18, 57, 0], 
#          [255, 255, 255, 255, 32, 32, 192, 0], 
#          [255, 255, 255, 255, 17, 17, 124, 0], 
#          [255, 255, 255, 255, 16, 16, 224, 0]]

print("beginnen")

# GPIO.output(chip_select, GPIO.LOW)

for j in range(10):
    for i in lijst_lijnen:
        GPIO.output(chip_select, GPIO.LOW)
        for k in test3[(i-1)%8]:
            # spi.writebytes([0xF, 0x00])
            # spi.writebytes([0xB, 0x7])
            # spi.writebytes([0x9, 0x0])
            # spi.writebytes([0xC, 0x01])
            # spi.writebytes([0xA, 0x02])
            
            
            
            spi.writebytes([i, k])
        GPIO.output(chip_select, GPIO.HIGH)
        
# print("gedaan")  
# # GPIO.output(chip_select, GPIO.HIGH)
# GPIO.output(chip_select, GPIO.LOW)
# spi.close()
# GPIO.output(chip_select, GPIO.HIGH)
# GPIO.cleanup()

# print("end")
# dict_tafel_deel1 = {1010:[]}



# list_of_lists = test6
# transposed = [list(sublist) for sublist in zip(*list_of_lists)] 
# print(transposed)



# deel1 = [["cof"]]
# deel2 = [["fie"]]

# samen = [deel1[0], deel2[0]]
# print(samen)

# ideaal = [[0b00010001, 0b11000000, 0b00010000, 0b11100000, 0b00010001, 0b11000000, 0b00010000, 0b11100000],
#          [0b00110010, 0b00100000, 0b00110001, 0b00010000, 0b00110010, 0b00100000, 0b00110001, 0b00010000],
#          [0b00010011, 0b00100000, 0b01010001, 0b10010000, 0b00010010, 0b00100000, 0b01010001, 0b00010000],
#          [0b00010010, 0b10100000, 0b00010001, 0b01010000, 0b00010010, 0b00100000, 0b00010001, 0b00010000],
#          [0b00010010, 0b01100000, 0b00010001, 0b00110000, 0b00010010, 0b00100000, 0b00010001, 0b00010000],
#          [0b00010010, 0b00100000, 0b00010001, 0b00010000, 0b00010010, 0b00100000, 0b00010001, 0b00010000],
#          [0b00111001, 0b11000000, 0b01111100, 0b11100000, 0b00111001, 0b11000000, 0b01111100, 0b11100000],
#          [0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]]


deel1 = [["B V1 R1 - 11", "B V2 R1 - 12","B V3 R1 - 13", "B V4 R1 - 14"],
         ["B V1 R2 - 21", "B V2 R2 - 22","B V3 R2 - 23", "B V4 R2 - 24"],
         ["B V1 R3 - 31", "B V2 R3 - 32","B V3 R3 - 33", "B V4 R3 - 34"],
         ["B V1 R4 - 41", "B V2 R4 - 42","B V3 R4 - 43", "B V4 R4 - 44"],
         ["B V1 R5 - 51", "B V2 R5 - 52","B V3 R5 - 53", "B V4 R5 - 54"],
         ["B V1 R6 - 61", "B V2 R6 - 62","B V3 R6 - 63", "B V4 R6 - 64"],
         ["B V1 R7 - 71", "B V2 R7 - 72","B V3 R7 - 73", "B V4 R7 - 74"],
         ["B V1 R8 - 81", "B V2 R8 - 82","B V3 R8 - 83", "B V4 R8 - 84"]]
deel2 = [["O V1 R1 - 15", "O V2 R1 - 16","O V3 R1 - 17", "O V4 R1 - 18"],
         ["O V1 R2 - 25", "O V2 R2 - 26","O V3 R2 - 27", "O V4 R2 - 28"],
         ["O V1 R3 - 35", "O V2 R3 - 36","O V3 R3 - 37", "O V4 R3 - 38"],
         ["O V1 R4 - 45", "O V2 R4 - 46","O V3 R4 - 47", "O V4 R4 - 48"],
         ["O V1 R5 - 55", "O V2 R5 - 56","O V3 R5 - 57", "O V4 R5 - 58"],
         ["O V1 R6 - 65", "O V2 R6 - 66","O V3 R6 - 67", "O V4 R6 - 68"],
         ["O V1 R7 - 75", "O V2 R7 - 76","O V3 R7 - 77", "O V4 R7 - 78"],
         ["O V1 R8 - 85", "O V2 R8 - 86","O V3 R8 - 87", "O V4 R8 - 88"]]

alles= []

for i in range(len(deel1)):
    samen = deel1[i]
    samen.extend(deel2[i])
    alles.append(samen)
# .extend(deel2[0])
print(samen)
print(alles)


resultaat = [['B V1 R1 - 11', 'B V2 R1 - 12', 'B V3 R1 - 13', 'B V4 R1 - 14', 'O V1 R1 - 15', 'O V2 R1 - 16', 'O V3 R1 - 17', 'O V4 R1 - 18'], 
            ['B V1 R2 - 21', 'B V2 R2 - 22', 'B V3 R2 - 23', 'B V4 R2 - 24', 'O V1 R2 - 25', 'O V2 R2 - 26', 'O V3 R2 - 27', 'O V4 R2 - 28'], 
            ['B V1 R3 - 31', 'B V2 R3 - 32', 'B V3 R3 - 33', 'B V4 R3 - 34', 'O V1 R3 - 35', 'O V2 R3 - 36', 'O V3 R3 - 37', 'O V4 R3 - 38'], 
            ['B V1 R4 - 41', 'B V2 R4 - 42', 'B V3 R4 - 43', 'B V4 R4 - 44', 'O V1 R4 - 45', 'O V2 R4 - 46', 'O V3 R4 - 47', 'O V4 R4 - 48'], 
            ['B V1 R5 - 51', 'B V2 R5 - 52', 'B V3 R5 - 53', 'B V4 R5 - 54', 'O V1 R5 - 55', 'O V2 R5 - 56', 'O V3 R5 - 57', 'O V4 R5 - 58'], 
            ['B V1 R6 - 61', 'B V2 R6 - 62', 'B V3 R6 - 63', 'B V4 R6 - 64', 'O V1 R6 - 65', 'O V2 R6 - 66', 'O V3 R6 - 67', 'O V4 R6 - 68'], 
            ['B V1 R7 - 71', 'B V2 R7 - 72', 'B V3 R7 - 73', 'B V4 R7 - 74', 'O V1 R7 - 75', 'O V2 R7 - 76', 'O V3 R7 - 77', 'O V4 R7 - 78'], 
            ['B V1 R8 - 81', 'B V2 R8 - 82', 'B V3 R8 - 83', 'B V4 R8 - 84', 'O V1 R8 - 85', 'O V2 R8 - 86', 'O V3 R8 - 87', 'O V4 R8 - 88']]


deel1 = [[0b10101010, 0b10101010,0b10101010,0b10101010],
         [0b10101010, 0b10101010,0b10101010,0b10101010],
         [0b10101010, 0b10101010,0b10101010,0b10101010],
         [0b10101010, 0b10101010,0b10101010,0b10101010],
         [0b10101010, 0b10101010,0b10101010,0b10101010],
         [0b10101010, 0b10101010,0b10101010,0b10101010],
         [0b10101010, 0b10101010,0b10101010,0b10101010],
         [0b10101010, 0b10101010,0b10101010,0b10101010]]
deel2 = [[0b01010101, 0b01010101,0b01010101,0b01010101],
         [0b01010101, 0b01010101,0b01010101,0b01010101],
         [0b01010101, 0b01010101,0b01010101,0b01010101],
         [0b01010101, 0b01010101,0b01010101,0b01010101],
         [0b01010101, 0b01010101,0b01010101,0b01010101],
         [0b01010101, 0b01010101,0b01010101,0b01010101],
         [0b01010101, 0b01010101,0b01010101,0b01010101],
         [0b01010101, 0b01010101,0b01010101,0b01010101]]

alles= []

for i in range(len(deel1)):
    samen = deel1[i]
    samen.extend(deel2[i])
    alles.append(samen)
# .extend(deel2[0])
print(samen)
print(alles)

for j in range(10):
    for i in lijst_lijnen:
        GPIO.output(chip_select, GPIO.LOW)
        for k in alles[(i-1)%8]:
            # spi.writebytes([0xF, 0x00])
            # spi.writebytes([0xB, 0x7])
            # spi.writebytes([0x9, 0x0])
            # spi.writebytes([0xC, 0x01])
            # spi.writebytes([0xA, 0x00])
            
            
            
            spi.writebytes([i, k])
        GPIO.output(chip_select, GPIO.HIGH)



dict_deel1 = {'1x1':[   [0b00000000, 0b00010000,0b00000000,0b00000000],
                        [0b00000000, 0b00110000,0b00000000,0b00000000],
                        [0b00000000, 0b00010000,0b00000000,0b00000000],
                        [0b00000000, 0b00010000,0b00000000,0b00000000],
                        [0b00000000, 0b00010000,0b00000000,0b00000000],
                        [0b00000000, 0b00111000,0b00000000,0b00000000],
                        [0b00000000, 0b00000000,0b00000000,0b00000000],
                        [0b00000000, 0b00000000,0b00000000,0b00000000]],
                '1x2':[ 
                        [0b00000000, 0b00000000,0b00000000,0b00000000],
                        [0b00000000, 0b01111110,0b00000000,0b00000000],
                        [0b00000000, 0b00000010,0b00000000,0b00000000],
                        [0b00000000, 0b00011100,0b00000000,0b00000000],
                        [0b00000000, 0b01000000,0b00000000,0b00000000],
                        [0b00000000, 0b01111111,0b00000000,0b00000000],
                        [0b00000000, 0b00000000,0b00000000,0b00000000],
                        [0b00000000, 0b00000000,0b00000000,0b00000000]]}

dict_deel2 = {'=1':[    [0b00000000, 0b00010000,0b00000000,0b00000000],
                        [0b00000000, 0b00110000,0b00000000,0b00000000],
                        [0b01111100, 0b00010000,0b00000000,0b00000000],
                        [0b00000000, 0b00010000,0b00000000,0b00000000],
                        [0b01111100, 0b00010000,0b00000000,0b00000000],
                        [0b00000000, 0b00111000,0b00000000,0b00000000],
                        [0b00000000, 0b00000000,0b00000000,0b00000000],
                        [0b00000000, 0b00000000,0b00000000,0b00000000]],
                '=2':[ 
                        [0b00000000, 0b00000000,0b00000000,0b00000000],
                        [0b01111100, 0b01111110,0b00000000,0b00000000],
                        [0b00000000, 0b00000010,0b00000000,0b00000000],
                        [0b00000000, 0b00011100,0b00000000,0b00000000],
                        [0b01111110, 0b01000000,0b00000000,0b00000000],
                        [0b00000000, 0b01111111,0b00000000,0b00000000],
                        [0b00000000, 0b00000000,0b00000000,0b00000000],
                        [0b00000000, 0b00000000,0b00000000,0b00000000]]}



alles= []

# for i in range(8):
#     samen = dict_deel1['1x1']
#     print(f"\n\n1){samen}")
#     samen.extend(dict_deel2['=1'])
#     print(f"\n\n2){samen}")
#     alles.append(samen)
#     print(f"\n\n3){alles}")
# # .extend(deel2[0])
# print(f"\n\n4){samen}")
# print(f"\n\n5){alles}")

print("--------------------------")  
alles_1 = dict_deel1['1x1']
print(f"alles deel 1 {alles_1}")
alles_2 = dict_deel2['=1'] 
print(f"alles deel 2 {alles_2}")

# vb dict_deel1['1x1'] = 
#         [["B V1 R1 - 11", "B V2 R1 - 12","B V3 R1 - 13", "B V4 R1 - 14"],
#          ["B V1 R2 - 21", "B V2 R2 - 22","B V3 R2 - 23", "B V4 R2 - 24"],
#          ["B V1 R3 - 31", "B V2 R3 - 32","B V3 R3 - 33", "B V4 R3 - 34"],
#          ["B V1 R4 - 41", "B V2 R4 - 42","B V3 R4 - 43", "B V4 R4 - 44"],
#          ["B V1 R5 - 51", "B V2 R5 - 52","B V3 R5 - 53", "B V4 R5 - 54"],
#          ["B V1 R6 - 61", "B V2 R6 - 62","B V3 R6 - 63", "B V4 R6 - 64"],
#          ["B V1 R7 - 71", "B V2 R7 - 72","B V3 R7 - 73", "B V4 R7 - 74"],
#          ["B V1 R8 - 81", "B V2 R8 - 82","B V3 R8 - 83", "B V4 R8 - 84"]]

# vb dict_deel2['=2] = 
#         [["O V1 R1 - 15", "O V2 R1 - 16","O V3 R1 - 17", "O V4 R1 - 18"],
#          ["O V1 R2 - 25", "O V2 R2 - 26","O V3 R2 - 27", "O V4 R2 - 28"],
#          ["O V1 R3 - 35", "O V2 R3 - 36","O V3 R3 - 37", "O V4 R3 - 38"],
#          ["O V1 R4 - 45", "O V2 R4 - 46","O V3 R4 - 47", "O V4 R4 - 48"],
#          ["O V1 R5 - 55", "O V2 R5 - 56","O V3 R5 - 57", "O V4 R5 - 58"],
#          ["O V1 R6 - 65", "O V2 R6 - 66","O V3 R6 - 67", "O V4 R6 - 68"],
#          ["O V1 R7 - 75", "O V2 R7 - 76","O V3 R7 - 77", "O V4 R7 - 78"],
#          ["O V1 R8 - 85", "O V2 R8 - 86","O V3 R8 - 87", "O V4 R8 - 88"]]



combo = []

for i in range(8):
    # 8 want er zitten 8 lijsten in alles_1 = len(alles_1)
    tussen = alles_1[i] # B V1-4    vb: ["B V1 R1 - 11", "B V2 R1 - 12","B V3 R1 - 13", "B V4 R1 - 14"]
    tussen.extend(alles_2[i]) # O V1-4 toevoegen aan B V1-4  => [B V1-4 , O V1-4]   => ['B V1 R1 - 11', 'B V2 R1 - 12', 'B V3 R1 - 13', 'B V4 R1 - 14', 'O V1 R1 - 15', 'O V2 R1 - 16', 'O V3 R1 - 17', 'O V4 R1 - 18']
    combo.append(tussen) # [...] => [... , [B V1-4 ,, O V1-4] ]
# .extend(deel2[0])
print(tussen)
print(combo)

# region setup
for j in range(10):
    for i in lijst_lijnen:
        GPIO.output(chip_select, GPIO.LOW)
        for k in combo[(i-1)%8]:
            spi.writebytes([0xF, 0x00])
            # spi.writebytes([0xB, 0x7])
            # spi.writebytes([0x9, 0x0])
            # spi.writebytes([0xC, 0x01])
            # spi.writebytes([0xA, 0x00])        
            
            # spi.writebytes([i, k])
        GPIO.output(chip_select, GPIO.HIGH)

for j in range(10):
    for i in lijst_lijnen:
        GPIO.output(chip_select, GPIO.LOW)
        for k in combo[(i-1)%8]:
            # spi.writebytes([0xF, 0x00])
            spi.writebytes([0xB, 0x7])
            # spi.writebytes([0x9, 0x0])
            # spi.writebytes([0xC, 0x01])
            # spi.writebytes([0xA, 0x00])        
            
            # spi.writebytes([i, k])
        GPIO.output(chip_select, GPIO.HIGH)

for j in range(10):
    for i in lijst_lijnen:
        GPIO.output(chip_select, GPIO.LOW)
        for k in combo[(i-1)%8]:
            # spi.writebytes([0xF, 0x00])
            # spi.writebytes([0xB, 0x7])
            spi.writebytes([0x9, 0x0])
            # spi.writebytes([0xC, 0x01])
            # spi.writebytes([0xA, 0x00])        
            
            # spi.writebytes([i, k])
        GPIO.output(chip_select, GPIO.HIGH)

for j in range(10):
    for i in lijst_lijnen:
        GPIO.output(chip_select, GPIO.LOW)
        for k in combo[(i-1)%8]:
            # spi.writebytes([0xF, 0x00])
            # spi.writebytes([0xB, 0x7])
            # spi.writebytes([0x9, 0x0])
            spi.writebytes([0xC, 0x01])
            # spi.writebytes([0xA, 0x00])        
            
            # spi.writebytes([i, k])
        GPIO.output(chip_select, GPIO.HIGH)


for j in range(10):
    for i in lijst_lijnen:
        GPIO.output(chip_select, GPIO.LOW)
        for k in combo[(i-1)%8]:
            # spi.writebytes([0xF, 0x00])
            # spi.writebytes([0xB, 0x7])
            # spi.writebytes([0x9, 0x0])
            # spi.writebytes([0xC, 0x01])
            spi.writebytes([0xA, 0x02])        
            
            # spi.writebytes([i, k])
        GPIO.output(chip_select, GPIO.HIGH)
# endregion setup

for j in range(10):
    for i in lijst_lijnen:
        GPIO.output(chip_select, GPIO.LOW)
        for k in combo[(i-1)%8]:
            # spi.writebytes([0xF, 0x00])
            # spi.writebytes([0xB, 0x7])
            # spi.writebytes([0x9, 0x0])
            # spi.writebytes([0xC, 0x01])
            # spi.writebytes([0xA, 0x00])        
            
            spi.writebytes([i, k])
        GPIO.output(chip_select, GPIO.HIGH)



print("gedaan")  
# GPIO.output(chip_select, GPIO.HIGH)
GPIO.output(chip_select, GPIO.LOW)
spi.close()
GPIO.output(chip_select, GPIO.HIGH)
GPIO.cleanup()

print("end")