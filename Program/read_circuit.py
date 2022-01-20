# https://ulrich-rapp.de/stoff/fahrzeug/daten/ET_Ub_Ohm.pdf

import re
import circuits


class Circuit:
    def __init__(self, path="", string="", save_to="", bg=0xbbbbbb):
        file_str = ""

        if path != "":
            with open(path, "r") as circuit_file:
                string = circuit_file.read()

        lines = string.split("\n")
        for line in lines:
            x = re.findall("^//", line)
            if not x:
                file_str += line + "\n"

        connection_list = file_str.split("\n\n")
        for i, connection in enumerate(connection_list):
            temp_connections = connection.split("\n")
            connections = []
            for connection_ in temp_connections:
                if connection_ != "":
                    connections.append(connection_)
            connection_list[i] = connections

        elements_dict = {}

        root_name = ""

        for connection in connection_list:
            connection[0] = connection[0].replace(" ", "")
            name, type_ = connection[0].split(",")

            if root_name == "":
                root_name = name

            values_dict = {"U": -1, "R": -1, "I": -1}
            values = []
            child_names = []
            for attribute in connection[1:]:
                if re.findall("^    ", attribute) or re.findall("^\t", attribute):
                    attribute = attribute.replace(" ", "").replace("\t", "")
                    values.append(attribute)
                else:
                    child_names.append(attribute)

            for value in values:
                key = value[0].upper()
                values_dict[key] = float(value[2:])

            elements_dict[name] = [child_names,
                                   circuits.Element(name, type_, voltage=values_dict["U"], resistance=values_dict["R"],
                                                    current=values_dict["I"])]

        for elem_key in list(elements_dict):
            for child_name in elements_dict[elem_key][0]:
                if child_name in elements_dict:
                    elements_dict[elem_key][1].add_child(elements_dict[child_name][1])
                else:
                    elements_dict[elem_key][1].add_child(circuits.Element(child_name, "r"))

        print(bg)
        elements_dict[root_name][1].draw_as_root(save_to=save_to, bg=bg)
        for i in range(10):
            elements_dict[root_name][1].compute()

        self.output = elements_dict[root_name][1].output_values()


if __name__ == '__main__':
    Circuit("circuits/circuit2.cd")
