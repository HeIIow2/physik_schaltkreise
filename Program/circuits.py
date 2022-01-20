'''
Ohmsches Gesetzt
U = R * I
I = U / R
R = U / I

Knotenregel:
In einer Parallelschaltung ist die Spannung jedes Wiederstandes gleich der Gesamtspannung

Maschenregel:
In einer Reihenschaltung ist die Stromstärke jedes Wiederstandes gleich der Gesamtstromstärke

Bei änderung der werte und Erstellung:
Ohmsches Gesetzt
Knoten- und Maschenregel bei Kindern

Bei hinzufügen eines Kindes:
Knoten- und Maschenregel bei sich selber

Bei fertigstellen der Schaltung:
Reihe:
Rges = R1 + R2 + ...
Uges = U1 + U2 + ...

Parallel:
LEFT TO IMPLEMENT
        R1 * R2
Rges =  -------  ...
        R1 + R2
Iges = I1 + I2 ...

Imperativ verschachtelte Programmierung
'''

import schemdraw
import schemdraw.elements as elm
from pathlib import Path

import os
os.environ['path'] += r';C:\Program Files\UniConvertor-2.0rc5\dlls'
import cairosvg

schemdraw.use('svg')

class Element:
    def __init__(self, name: str, type_str: str, resistance=-1.0, voltage=-1.0, current=-1.0):
        type_str = type_str.lower()
        types = {
            "r": 0,
            "s": 1,
            "p": 2
        }
        self.type = types[type_str]
        self.name = name

        self.resistance = float(resistance)
        self.voltage = float(voltage)
        self.current = float(current)

        self.child_Elements = []

        self.on_change()


    def ohmsches_gesetzt(self):
        if self.resistance != -1 and self.current != -1 and self.voltage == -1:
            self.voltage = self.resistance * self.current
            return

        if self.voltage != -1 and self.resistance != -1 and self.current == -1:
            if self.resistance != 0:
                self.current = self.voltage / self.resistance
            else:
                print(f"Der Widerstand bei {self.name} ist 0.")
            return

        if self.voltage != -1 and self.current != -1 and self.resistance == -1:
            if self.current != 0:
                self.resistance = self.voltage / self.current
            else:
                print(f"Die Stromspannung bei {self.name} ist 0.")
            return

        # wenn alle Werte vorhanden sind, werden diese überprüft
        if self.voltage != -1 and self.current != -1 and self.resistance != -1:
            if int(self.voltage) != int(self.resistance * self.current):
                print(f"Spannung[{self.resistance}] != Widerstand[{self.resistance}] * Stärke[{self.current}]")

    def maschen_knoten_children(self):
        # wenn der Richtige wert bei diesem Objekt existiert, füge ihn bei den Kindern hinzu.

        if len(self.child_Elements) == 0:
            return

        if self.type == 1:
            # Maschenregel
            if self.current == -1:
                return

            for child in self.child_Elements:
                child.set_current(self.current)
            return

        if self.type == 2:
            # Knotenregel
            if self.voltage == -1:
                return

            for child in self.child_Elements:
                child.set_voltage(self.voltage)
            return

    def maschen_knoten_self(self):
        # wenn der Richtige wert bei den Kindern existiert, füge ihn bei sich selbst.

        if len(self.child_Elements) == 0:
            return

        if self.type == 1:
            # Maschenregel
            for child in self.child_Elements:
                if child.current != -1:
                    self.set_current(child.current)
                    return
            return

        if self.type == 2:
            # Knotenregel
            for child in self.child_Elements:
                if child.voltage != -1:
                    self.set_voltage(child.voltage)
            return

    def set_voltage(self, voltage):
        if self.voltage != -1:
            return -1
        self.voltage = voltage
        self.on_change()

    def set_current(self, current):
        if self.current != -1:
            return
        self.current = current
        self.on_change()

    def set_resistance(self, resistance):
        if self.resistance != -1:
            return -1
        self.resistance = resistance
        self.on_change()

    def on_change(self):
        self.ohmsches_gesetzt()
        self.maschen_knoten_children()

    def compute(self):
        if len(self.child_Elements) == 0:
            return
        if self.type == 0:
            return

        # get the amount of unknown values
        unknown_voltage = 0
        unknown_current = 0
        unknown_resistance = 0
        for child in self.child_Elements:
            if child.voltage == -1:
                unknown_voltage += 1
                missing_voltage_elem = child
            if child.current == -1:
                unknown_current += 1
                missing_current_elem = child
            if child.resistance == -1:
                unknown_resistance += 1
                missing_resistance_elem = child

        if self.type == 1:
            # Reihenschaltung
            if unknown_resistance == 0:
                total_resistance = 0
                for child in self.child_Elements:
                    total_resistance += child.resistance
                self.set_resistance(total_resistance)

            elif unknown_resistance == 1 and self.resistance != -1:
                total_resistance = 0
                for child in self.child_Elements:
                    if child.resistance != -1:
                        total_resistance += child.resistance
                missing_resistance_elem.set_resistance(self.resistance - total_resistance)

            if unknown_voltage == 0:
                total_voltage = 0
                for child in self.child_Elements:
                    total_voltage += child.voltage
                self.set_voltage(total_voltage)

            elif unknown_voltage == 1 and self.voltage != -1:
                total_voltage = 0
                for child in self.child_Elements:
                    if child.voltage != -1:
                        total_voltage += child.voltage
                missing_voltage_elem.set_voltage(self.voltage - total_voltage)


        elif self.type == 2:
            # Parallelschaltung
            if unknown_current == 0:
                total_current = 0
                for child in self.child_Elements:
                    total_current += child.current
                self.set_current(total_current)

            elif unknown_current == 1 and self.current != -1:
                total_current = 0
                for child in self.child_Elements:
                    if child.current != -1:
                        total_current += child.current

                missing_current_elem.set_current(self.current - total_current)

        self.maschen_knoten_self()
        self.maschen_knoten_children()

        for child in self.child_Elements:
            child.compute()

    def output_values(self, return_str=""):
        type_descriptions = ["Widerstand", "Reihenschaltung", "Parallelschaltung"]
        return_str += f"{self.name}, {type_descriptions[self.type]}\n"
        print(f"{self.name}, {type_descriptions[self.type]}")
        if self.resistance != -1:
            print(f"    R: {round(self.resistance, 3)}Ω")
            return_str += f"    R: {round(self.resistance, 3)}Ω\n"
        if self.voltage != -1:
            print(f"    U: {round(self.voltage, 3)}V")
            return_str += f"    U: {round(self.voltage, 3)}V\n"
        if self.current != -1:
            print(f"    I: {round(self.current, 3)}A")
            return_str += f"    I: {round(self.current, 3)}A\n"
        return_str += "\n"
        print("")

        if self.type == 1 or self.type == 2:
            for child in self.child_Elements:
                return_str = child.output_values(return_str=return_str)

        return return_str

    def add_child(self, child):
        self.child_Elements.append(child)
        self.maschen_knoten_self()

    def draw(self, d: schemdraw.Drawing, latest_elem):
        if self.type == 0:
            d += (latest_elem := elm.Resistor().right().label(self.name).at(latest_elem.end))

            return 1, latest_elem, 1

        if self.type == 1:
            steps = 0
            height = 1

            for child in self.child_Elements:
                r_steps, latest_elem, height = child.draw(d, latest_elem)
                steps += r_steps

            return steps, latest_elem, height

        if self.type == 2:
            steps, last, heights = self.child_Elements[0].draw(d, latest_elem)
            parallel_steps = [steps]
            parallel_heights = [heights]
            parallel_last = [last]

            for child in self.child_Elements[1:]:
                for n in range(parallel_heights[-1]):
                    d += (latest_elem := elm.Line().up().at(latest_elem.end))
                steps, last, height = child.draw(d, latest_elem)
                parallel_steps.append(steps)
                parallel_last.append(last)
                parallel_heights.append(height)

            # get max steps
            max_steps = 0
            for step in parallel_steps:
                if step > max_steps:
                    max_steps = step

            # draw rest of the circuit
            for i, latest_elem in enumerate(parallel_last):
                for n in range(max_steps - parallel_steps[i]):
                    d += (latest_elem := elm.Line().right().at(latest_elem.end))
                if i > 0:
                    for n in range(parallel_heights[i]):
                        d += (latest_elem := elm.Line().down().at(latest_elem.end))
                else:
                    latest_elem_r = latest_elem

            current_height = 0
            for heights in parallel_heights:
                current_height += heights

            return max_steps, latest_elem_r, current_height

    def draw_as_root(self, save_to="", bg=0xbbbbbb):
        d = schemdraw.Drawing()

        d += (latest_elem := elm.SourceV().up().label(self.name))

        steps, latest_elem, height = self.draw(d, latest_elem)

        d += (latest_elem := elm.Line().down().at(latest_elem.end))
        for i in range(steps):
            d += (latest_elem := elm.Line().left().at(latest_elem.end))

        if save_to == "":
            d.save('schematic.svg')
            cairosvg.svg2png(url='schematic.svg', write_to='schematic.png')
        else:
            try:
                os.makedirs("graphics/png")
            except FileExistsError:
                pass
            d.save(f"graphics/{save_to}.svg")
            cairosvg.svg2png(url=f"graphics/{save_to}.svg", write_to=f"graphics/png/{save_to}.png")



'''
resistor1 = Element("R1", "r")
resistor2 = Element("R2", "r", voltage=10)
resistor3 = Element("R3", "r", resistance=5)
resistor4 = Element("R3", "r", resistance=5)
resistor5 = Element("R3", "r", resistance=5)

series = Element("R23", "s", voltage=20)
series.add_child(resistor2)
series.add_child(resistor3)

parallel = Element("Rges", "p", voltage=20)
parallel.add_child(resistor1)
parallel.add_child(series)
parallel.add_child(resistor4)
parallel.add_child(resistor5)
parallel.draw_as_root()
'''
