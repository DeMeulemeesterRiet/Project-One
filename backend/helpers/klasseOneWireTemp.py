
class TempOneWire:
    def __init__(self, bestandsnaam='/sys/bus/w1/devices/28-01813c00007d/w1_slave'):
        self.bestandsnaam = bestandsnaam

    def lees_temperatuur(self) -> None:
        sensor_file = open(self.bestandsnaam, 'r')  #File-object
        temperatuur = 0
        for line in sensor_file:
            pos = line.find('t=')
            if pos != -1:
                string_temp = line[pos:]
                temperatuur = int(string_temp[2:]) /1000
                print("De temperatuur is {0} {1}Celcius".format(temperatuur, "\N{DEGREE SIGN}"))
        sensor_file.close()
        return temperatuur