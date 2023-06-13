"""
Course:     ICT40120 Cert IV in IT (Programming)
    Name:       Emma'Jane Kane
    Id:         V244681
    Unit:       IP4RIoT (Cluster)
    Assessment: AT3 Project
    Date:       June 2023
    Purpose:    Carpark Project with MQTT, TOML config file, Unittest
                This script is to emulate a sensor that registers when a car enters or exits a car park.
                This is done by way of the tkinter GUI with buttons to click for a car to Enter and Exit.
                Each action is Published to the MQTT server

"""
import tkinter as tk
from typing import Iterable
import paho.mqtt.client as paho
import tomllib

# open the config file and retrieve the required values
with open("config.toml", "rb") as f:
    config = tomllib.load(f)
    location = (config["config"]["location"])
    total_spaces = (config["config"]["total_spaces"])
    BROKER = (config["config"]["broker_host"])
    PORT = (config["config"]["broker_port"])

# ------------------------------------------------------------------------------------#
# You don't need to understand how to implement this class, just how to use it.       #
# ------------------------------------------------------------------------------------#
# TODO: got to the main section of this script **first** and run the CarParkDisplay.  #

# Setup and connect to the MQTT Client
client = paho.Client()
client.connect(BROKER, PORT)


class WindowedDisplay:
    DISPLAY_INIT = '– – –'
    SEP = ':'  # field name separator

    def __init__(self, title: str, display_fields: Iterable[str]):
        self.window = tk.Tk()
        self.window.title(f'{title}: Parking')
        self.window.geometry('800x400')
        self.window.resizable(False, False)
        self.display_fields = display_fields

        self.gui_elements = {}
        for i, field in enumerate(self.display_fields):

            # create the elements
            self.gui_elements[f'lbl_field_{i}'] = tk.Label(
                self.window, text=field+self.SEP, font=('Arial', 50))
            self.gui_elements[f'lbl_value_{i}'] = tk.Label(
                self.window, text=self.DISPLAY_INIT, font=('Arial', 50))

            # position the elements
            self.gui_elements[f'lbl_field_{i}'].grid(
                row=i, column=0, sticky=tk.E, padx=5, pady=5)
            self.gui_elements[f'lbl_value_{i}'].grid(
                row=i, column=2, sticky=tk.W, padx=10)

    def show(self):
        """Display the GUI. Blocking call."""
        self.window.mainloop()

    def update(self, updated_values: dict):
        for field in self.gui_elements:
            if field.startswith('lbl_field'):
                field_value = field.replace('field', 'value')
                self.gui_elements[field_value].configure(
                    text=updated_values[self.gui_elements[field].cget('text').rstrip(self.SEP)])
        self.window.update()

# -----------------------------------------#
# TODO: STUDENT IMPLEMENTATION STARTS HERE #
# -----------------------------------------#


class CarDetector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Car Detector ULTRA")

        self.btn_incoming_car = tk.Button(
            self.root, text='🚘 Incoming Car', font=('Arial', 50), cursor='right_side', command=self.incoming_car)
        self.btn_incoming_car.pack(padx=10, pady=5)
        self.btn_outgoing_car = tk.Button(
            self.root, text='Outgoing Car 🚘',  font=('Arial', 50), cursor='bottom_left_corner', command=self.outgoing_car)
        self.btn_outgoing_car.pack(padx=10, pady=5)

        self.root.mainloop()

    def incoming_car(self):
#         client.publish("lot/sensor", "CP-Car goes in")
#         Above was used for debugging to show that Publishing and Subscribing were working
        client.publish("lot/sensor", 1)
        print("Car goes in")   # To show the function has run

    def outgoing_car(self):
#        client.publish("lot/sensor", "CP-Car goes out")
#        Above was used for debugging to show that Publishing and Subscribing were working
        client.publish("lot/sensor", -1)
#        print("Car goes out") # To show the function has run


if __name__ == '__main__':
    CarDetector()
