import random


class Tafels:
    def __init__(self, tafel, beginwaarde = 0, eindwaarde=12):
        self.tafel = tafel
        self.beginwaarde = beginwaarde
        self.eindwaarde = eindwaarde
        
    def genereer_tafels(self):
        tafels = []
        lijst_getal2 = []
        antwoorden = []
        for i in range(self.beginwaarde, self.eindwaarde + 1):
            lijst_getal2.append(i)
        random.shuffle(lijst_getal2)

        for getal in lijst_getal2:
            tafels.append(f"{self.tafel}x{getal}")
            antwoorden.append(f"{self.tafel * getal}")
            
        return tafels, antwoorden, lijst_getal2


