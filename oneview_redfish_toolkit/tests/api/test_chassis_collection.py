# -*- coding: utf-8 -*-

# Copyright (2017) Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
    Tests for chassis_collection.py
"""

import json

from oneview_redfish_toolkit.api.chassis_collection \
    import ChassisCollection
from oneview_redfish_toolkit import util

import unittest
from unittest import mock


class TestChassisCollection(unittest.TestCase):
    """Tests for ChassisCollection class"""

    @mock.patch.object(util, 'OneViewClient')
    def setUp(self, oneview_client_mock):
        """Tests preparation"""

        # Loading variable in util module
        util.load_config('redfish.conf')

        # Loading server_hardware mockup value
        with open(
            'oneview_redfish_toolkit/mockups/oneview/'
            'ServerHardwares.json'
        ) as f:
            self.server_hardware = json.load(f)

        # Loading enclosures mockup value
        with open(
            'oneview_redfish_toolkit/mockups/oneview/'
            'Enclosures.json'
        ) as f:
            self.enclosures = json.load(f)

        # Loading racks mockup value
        with open(
            'oneview_redfish_toolkit/mockups/oneview/'
            'Racks.json'
        ) as f:
            self.racks = json.load(f)

        # Loading ChassisCollection result mockup
        with open(
            'oneview_redfish_toolkit/mockups/redfish/'
            'ChassisCollection.json'
        ) as f:
            self.chassis_collection_mockup = json.load(f)

    def test_class_instantiation(self):
        # Tests if class is correctly instantiated and validated

        try:
            chassis_collection = ChassisCollection(
                self.server_hardware,
                self.enclosures,
                self.racks
            )
        except Exception as e:
            self.fail("Failed to instantiate ChassisCollection class."
                      " Error: {}".format(e))
        self.assertIsInstance(chassis_collection, ChassisCollection)

    def test_serialize(self):
        # Tests the serialize function result against known result

        try:
            chassis_collection = ChassisCollection(
                self.server_hardware,
                self.enclosures,
                self.racks
            )
        except Exception as e:
            self.fail("Failed to instantiate ChassisCollection class."
                      " Error: {}".format(e))

        try:
            result = json.loads(chassis_collection.serialize())
        except Exception as e:
            self.fail("Failed to serialize. Error: ".format(e))

        self.assertEqual(self.chassis_collection_mockup, result)
