"""
Course:     ICT40120 Cert IV in IT (Programming)
    Name:       Emma'Jane Kane
    Id:         V244681
    Unit:       IP4RIoT (Cluster)
    Assessment: AT3 Project
    Date:       June 2023
    Purpose:    Carpark Project with MQTT, TOML config file, Unittest
                A test created to check the config file works and outputs the expected data

"""
import unittest

import samples_and_snippets.config_parser as pc


class TestConfigParsing(unittest.TestCase):
    def test_parse_config_has_correct_location_and_spaces(self):
        config_string = '''
        [parking_lot]
        location = "Moondalup City Square Parking"
        total_spaces = 192
        broker_host = "localhost"
        broker_port = 1883
        '''
        #config = tomli.loads(config_string)
        parking_lot = pc.parse_config()
        self.assertEqual(parking_lot["config"]["location"], "Moondalup City Square Parking")
        self.assertEqual(parking_lot["config"]["total_spaces"], 192)

