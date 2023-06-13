"""
Course:     ICT40120 Cert IV in IT (Programming)
    Name:       Emma'Jane Kane
    Id:         V244681
    Unit:       IP4RIoT (Cluster)
    Assessment: AT3 Project
    Date:       June 2023
    Purpose:    Carpark Project with MQTT, TOML config file, Unittest
                This script is to run the classes to open the two windows required to run this emulation

"""
from car_detector import CarDetector
from carpark_display import CarParkDisplay
import multiprocessing
import tkinter


def car_park_ui():
    tkinter.Tk().mainloop()


if __name__ == '__main__':
    multiprocessing.Process(target=CarDetector).start()
    multiprocessing.Process(target=CarParkDisplay).start()
