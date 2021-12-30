'''
Ohmsches Gesetzt
U = R * I
I = U / R
R = U / I

Maschenregel:
In einer Parallelschaltung ist die Spannung jedes Wiederstandes gleich der Gesamtspannung

Kettenregel:
In einer Reihenschaltung ist die Stromstärke jedes Wiederstandes gleich der Gesamtstromstärke
'''

import schemdraw
import schemdraw.elements as elm

turns_right = 0

class Resistor:
    def __init__(self, resistance=-1, voltage=-1, current=-1):
        self.resistance = resistance
        self.voltage = voltage
        self.current = current

        self.get_values()

    def get_values(self):
        # Ohmsches Gesetzt

        if self.resistance != -1 and self.current != -1 and self.voltage == -1:
            self.voltage = self.resistance * self.current
            return

        if self.voltage != -1 and self.resistance != -1 and self.current == -1:
            self.current = self.voltage / self.resistance
            return

        if self.voltage != -1 and self.current != -1 and self.resistance == -1:
            self.resistance = self.voltage / self.current
            return

        # wenn alle Werte vorhanden sind, werden diese überprüft
        if self.voltage != -1 and self.current != -1 and self.resistance != -1:
            if int(self.voltage) != int(self.resistance * self.current):
                print(f"Spannung[{self.resistance}] != Widerstand[{self.resistance}] * Stärke[{self.current}]")

    def set_current(self, current):
        self.current = current
        self.get_values()

    def set_voltage(self, voltage):
        self.voltage = voltage
        self.get_values()

    def set_resistance(self, resistance):
        self.resistance = resistance
        self.get_values()


    def draw(self, d: schemdraw.Drawing):
        d += elm.Resistor().label(f'{self.resistance}Ω\n{self.voltage}V\n{self.current}A')

        global turns_right
        turns_right += 1

class Series:
    def __init__(self, resistance=-1, voltage=-1, current=-1):
        self.resistors = []

        self.resistance = resistance
        self.voltage = voltage
        self.current = current

    def add_resistor(self, resistor: Resistor):
        self.resistors.append(resistor)

        if self.current == -1 and resistor.current != -1:
            self.current = resistor.current

        self.get_value()

    def set_voltage(self):
        voltage_ = 0
        for resistor in self.resistors:
            if resistor.voltage == -1:
                self.voltage = -1
                return
            voltage_ += resistor.voltage

        self.voltage = voltage_

    def set_resistance(self):
        resistance_ = 0
        for resistor in self.resistors:
            if resistor.resistance == -1:
                self.resistance = -1
            resistance_ += resistor.resistance

        self.resistance = resistance_

    def get_value(self):
        for resistor in self.resistors:
            resistor.set_current(self.current)

        self.set_voltage()
        self.set_resistance()

        # Ohmsches Gesetzt
        if self.resistance != -1 and self.current != -1 and self.voltage == -1:
            self.voltage = self.resistance * self.current
            return

        if self.voltage != -1 and self.resistance != -1 and self.current == -1:
            self.current = self.voltage / self.resistance
            return

        if self.voltage != -1 and self.current != -1 and self.resistance == -1:
            self.resistance = self.voltage / self.current
            return

        # wenn alle Werte vorhanden sind, werden diese überprüft
        if self.voltage != -1 and self.current != -1 and self.resistance != -1:
            if int(self.voltage) != int(self.resistance * self.current):
                print(f"Spannung[{self.resistance}] != Widerstand[{self.resistance}] * Stärke[{self.current}]")

    def draw(self, d: schemdraw.Drawing):
        for resistor in self.resistors:
            resistor.draw(d)

d = schemdraw.Drawing()
serie = Series()

'''
serie.add_resistor(Resistor(resistance=10, current=5, voltage=8))
serie.add_resistor(Resistor(resistance=10, current=5, voltage=8))
serie.add_resistor(Resistor(resistance=10, current=5, voltage=8))
serie.add_resistor(Resistor(resistance=10, current=5, voltage=8))
serie.add_resistor(Resistor(resistance=10, current=5, voltage=8))
'''

serie.add_resistor(Resistor(current=5, voltage=30))
serie.add_resistor(Resistor(voltage=20))

serie.draw(d)

d += elm.Line().down()

for i in range(turns_right):
    d += elm.Line().left()

d += elm.SourceV().up().label('10V')
d.draw()
d.save('schematic.svg')