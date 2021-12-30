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

class Element:
    def __init__(self, name: str, type_str: str, resistance=-1, voltage=-1, current=-1):
        type_str = type_str.lower()
        types = {
            "r": 0,
            "s": 1,
            "p": 2
        }
        self.type = types[type_str]
        self.name = name

        self.resistance = resistance
        self.voltage = voltage
        self.current = current

        self.child_Elements = []

    def output_values(self):
        type_descriptions = ["Widerstand", "Reihenschaltung", "Parallelschaltung"]
        print(f"{self.name}, {type_descriptions[self.type]}")
        if self.resistance != -1:
            print(f"    R: {self.resistance}Ω")
        if self.voltage != -1:
            print(f"    U: {self.voltage}V")
        if self.current != -1:
            print(f"    I: {self.current}A")
        print("")

        if self.type == 1 or self.type == 2:
            for child in self.child_Elements:
                child.output_values()

    def add_child(self, child):
        self.child_Elements.append(child)

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
                else: latest_elem_r = latest_elem

            current_height = 0
            for heights in parallel_heights:
                current_height += heights

            return max_steps, latest_elem_r, current_height


    def draw_as_root(self):
        d = schemdraw.Drawing()

        d += (latest_elem := elm.SourceV().up().label(self.name))

        steps, latest_elem, height = self.draw(d, latest_elem)

        d += (latest_elem := elm.Line().down().at(latest_elem.end))
        for i in range(steps):
            d += (latest_elem := elm.Line().left().at(latest_elem.end))

        d.draw()
        d.save('schematic.svg')

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
