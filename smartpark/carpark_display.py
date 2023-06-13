"""
Course:     ICT40120 Cert IV in IT (Programming)
    Name:       Emma'Jane Kane
    Id:         V244681
    Unit:       IP4RIoT (Cluster)
    Assessment: AT3 Project
    Date:       June 2023
    Purpose:    Carpark Project with MQTT, TOML config file, Unittest
                This script is to emulate a display, and keep count of cars and car parking spaces in a Parking lot.
                It subscribes to the MQTT server to receive the information.

"""
import random
import threading
import time
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
        """Update the values displayed in the GUI. Expects a dictionary with keys matching the field names passed to
        the constructor."""
        for field in self.gui_elements:
            if field.startswith('lbl_field'):
                field_value = field.replace('field', 'value')
                self.gui_elements[field_value].configure(
                    text=updated_values[self.gui_elements[field].cget('text').rstrip(self.SEP)])
        self.window.update()

# -----------------------------------------#
# TODO: STUDENT IMPLEMENTATION STARTS HERE #
# -----------------------------------------#


class CarParkDisplay:
    fields = ['Available bays', 'Temperature', 'At']

    def __init__(self):
        self.window = WindowedDisplay(
            location, CarParkDisplay.fields)
        updater = threading.Thread(target=self.check_updates)
        updater.daemon = True
        updater.start()
        self.window.show()

    def check_updates(self):
        while True:
            def on_message(client, userdata, msg):
                decoded_message = str(msg.payload.decode())
                car_count.append(int(decoded_message))
#               print(car_count)
                return car_count

            def on_disconnect(client, userdata, rc=0):
                client.loop_stop()

            client = paho.Client()
            client.on_message = on_message
            client.on_disconnect = on_disconnect

            client.connect(BROKER, PORT)
            client.subscribe("lot/sensor")
#             clear the car_count list if it is less than zero to stop the list growing too long
            if sum(car_count) <= 0:
                print("Its zero")
                car_count.clear()
            parking_spaces = total_spaces - sum(car_count)
#             Do not display available spaces as less than 0 or more than the actual spaces in the lot
            if parking_spaces < 0:
                parking_spaces = 0
            elif parking_spaces > total_spaces:
                parking_spaces = total_spaces
            print(parking_spaces)
#             NOTE: Dictionary keys *must* be the same as the class fields
            field_values = dict(zip(CarParkDisplay.fields, [
                parking_spaces,
                f'{random.randint(0, 45):02d}℃',
                time.strftime("%H:%M:%S")]))

#            Pretending to wait on updates from MQTT
#            print(f'Received {msg.payload.decode()}') # Used for Testing
            client.loop_start()
            time.sleep(random.randint(1, 1))
#             When you get an update, refresh the display.
            self.window.update(field_values)
            client.loop_stop()


car_count = []


if __name__ == '__main__':
    CarParkDisplay()
