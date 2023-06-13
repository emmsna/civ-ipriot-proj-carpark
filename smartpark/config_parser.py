"""
Course:     ICT40120 Cert IV in IT (Programming)
    Name:       Emma'Jane Kane
    Id:         V244681
    Unit:       IP4RIoT (Cluster)
    Assessment: AT3 Project
    Date:       June 2023
    Purpose:    Carpark Project with MQTT, TOML config file, Unittest
                A class or function to parse the config file and return the values as a dictionary.
                This config parser is not required in my scripts as I used the inbuilt TOMLLIB, however
                this looks required for theUnit Test "test_config.py", so I have configured it to work for that.

"""
import tomllib

def parse_config() -> dict:
    with open("../smartpark/config.toml", "rb") as f:
        config = tomllib.load(f)
    return config

#print(parse_config())