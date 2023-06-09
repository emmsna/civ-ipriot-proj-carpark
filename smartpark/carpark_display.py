"""The following code is used to provide an alternative to students who do not have a Raspberry Pi.
If you have a Raspberry Pi, or a SenseHAT emulator under Debian, you do not need to use this code.

You need to split the classes here into two files, one for the CarParkDisplay and one for the CarDetector.
Attend to the TODOs in each class to complete the implementation."""
import random
import threading
import time
import tkinter as tk
from typing import Iterable
import paho.mqtt.client as paho
from paho.mqtt.client import MQTTMessage
import tomllib

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
    """Displays values for a given set of fields as a simple GUI window. Use .show() to display the window; use .update() to update the values displayed.
    """

    DISPLAY_INIT = '– – –'
    SEP = ':'  # field name separator

    def __init__(self, title: str, display_fields: Iterable[str]):
        """Creates a Windowed (tkinter) display to replace sense_hat display. To show the display (blocking) call .show() on the returned object.

        Parameters
        ----------
        title : str
            The title of the window (usually the name of your carpark from the config)
        display_fields : Iterable
            An iterable (usually a list) of field names for the UI. Updates to values must be presented in a dictionary with these values as keys.
        """
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
        """Update the values displayed in the GUI. Expects a dictionary with keys matching the field names passed to the constructor."""
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
    """Provides a simple display of the car park status. This is a skeleton only. The class is designed to be customizable without requiring and understanding of tkinter or threading."""
    # determines what fields appear in the UI
    fields = ['Available bays', 'Temperature', 'At']

    def __init__(self):
        self.window = WindowedDisplay(
            location, CarParkDisplay.fields)
        updater = threading.Thread(target=self.check_updates)
        updater.daemon = True
        updater.start()
        self.window.show()


    def check_updates(self):
        # TODO: This is where you should manage the MQTT subscription

        while True:
            #BROKER, PORT = "localhost", 1883
            def on_message(client, userdata, msg):
                #print(f'Received {msg.payload.decode()}')
                decoded_message = str(msg.payload.decode())
                car_count.append(int(decoded_message))
                print(car_count)
                return car_count

            def on_disconnect(client, userdata, rc=0):
                #logging.debug("DisConnected result code " + str(rc))
                client.loop_stop()

            client = paho.Client()
            client.on_message = on_message
            client.on_disconnect = on_disconnect

            client.connect(BROKER, PORT)
            client.subscribe("lot/sensor")
            parking_spaces = total_spaces - sum(car_count)
            print(parking_spaces)
            # NOTE: Dictionary keys *must* be the same as the class fields
            field_values = dict(zip(CarParkDisplay.fields, [
                parking_spaces,
                f'{random.randint(0, 45):02d}℃',
                time.strftime("%H:%M:%S")]))
            # field_values = dict(zip(CarParkDisplay.fields, [
            #     f'{random.randint(0, 150):03d}',
            #     f'{random.randint(0, 45):02d}℃',
            #     time.strftime("%H:%M:%S")]))


            # Pretending to wait on updates from MQTT
            #print(f'Received {msg.payload.decode()}')
            client.loop_start()
            time.sleep(random.randint(1, 1))
            # When you get an update, refresh the display.
            self.window.update(field_values)
            client.loop_stop()
car_count = []





if __name__ == '__main__':
    # TODO: Run each of these classes in a separate terminal. You should see the CarParkDisplay update when you click the buttons in the CarDetector.
    # These classes are not designed to be used in the same module - they are both blocking. If you uncomment one, comment-out the other.

    CarParkDisplay()
    # CarDetector()
