import read_circuit

import tkinter as tk
from tkinter import filedialog, Canvas
import os
from PIL import Image, ImageTk

class InputFrame:
    def __init__(self, root):
        self.root = root
        self.fg_color = '#fff'
        self.bg_color = '#bbb'

        self.root.config(bg=self.bg_color)

        self.string = ""
        self.file_name = os.getcwd()

        # Eingabe
        self.open_file_dialog_button = tk.Button(self.root, text=self.file_name, command=self.file_dialog, bg=self.fg_color)
        self.open_file_dialog_button.grid(row=0, column=0, sticky="NSEW", padx=5, pady=5)

        self.text = tk.Text(self.root, height=20, width=30, undo=True, relief=tk.FLAT)
        self.text.grid(row=1, column=0, sticky="NS", padx=5)
        self.root.rowconfigure(1, weight=2)

        self.calc_button = tk.Button(self.root, text="calculate and render", command=self.calculate)
        self.calc_button.grid(row=2, column=0, sticky="EWS", padx=5, pady=5)

        # Zeigt den Schaltplan am Ende
        self.schematic = tk.Label(self.root, bg=self.bg_color)
        self.schematic.grid(row=0, column=1, rowspan=3, sticky="NSEW", padx=5, pady=5)
        self.root.columnconfigure(1, weight=2)

        # Ausgabe
        self.output_label = tk.Label(self.root, text="Ausgabe", bg=self.fg_color)
        self.output_label.grid(row=0, column=2, sticky="NEW", padx=5, pady=5)

        self.output_text = tk.Text(self.root, height=20, width=30, state="disabled", relief=tk.FLAT)
        self.output_text.grid(row=1, column=2, rowspan=2, sticky="NS", padx=5, pady=(0, 5))

        self.set_text()

    def set_text(self):
        if len(self.file_name) > 45:
            display_file_name = "..." + self.file_name[-42:]
            self.open_file_dialog_button.config(text=display_file_name)

    def file_dialog(self):
        file = tk.filedialog.askopenfile(mode="r", initialdir=os.getcwd())
        if file is None:
            return
        self.file_name = file.name
        self.set_text()
        self.string = file.read()
        self.text.insert(tk.END, self.string)

    def calculate(self):
        print(self.root.winfo_width(), self.root.winfo_height())

        save_to_str = self.file_name.split("/")[-1].split(".")[0]

        circuit = read_circuit.Circuit(string=self.string, save_to=save_to_str)

        img = Image.open(f'graphics/png/{save_to_str}.png')

        im_width, im_height = img.size
        elm_width, elm_height = self.schematic.winfo_width(), self.schematic.winfo_height()
        if im_width/elm_width > im_height/elm_height:
            ratio = im_height/im_width
            im_height = elm_width * ratio
            im_width = elm_width
        elif im_width/elm_width < im_height/elm_height:
            ratio = im_width/im_height
            im_width = elm_height * ratio
            im_height = elm_height
        img = img.resize((int(im_width), int(im_height)))

        self.tk_img = ImageTk.PhotoImage(img)

        self.schematic.config(image=self.tk_img)
        self.output_text.configure(state='normal')
        self.output_text.insert(tk.END, circuit.output)
        self.output_text.configure(state='disabled')


root = tk.Tk()
root.title("Schaltplan ©Lars Noack")
# root.state("zoomed")
root.geometry("800x400")

input_frame = tk.Frame(root)
input_frame.grid(row=0, column=0)
InputFrame(root)

root.mainloop()
