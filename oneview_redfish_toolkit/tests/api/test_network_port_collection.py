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

import json
import unittest
from unittest import mock

from oneview_redfish_toolkit.api.network_port_collection \
    import NetworkPortCollection
from oneview_redfish_toolkit import util


class TestNetworkPortCollection(unittest.TestCase):
    """Tests for NetworkPortCollection class"""

    @mock.patch.object(util, 'OneViewClient')
    def setUp(self, oneview_client_mock):
        """Tests preparation"""

        # Loading variable in util module
        util.load_config('redfish.conf')

        # Loading ServerHardware mockup
        with open(
            'oneview_redfish_toolkit/mockups/oneview/'
            'ServerHardware.json'
        ) as f:
            self.server_hardware = json.load(f)

        # Loading NetworkInterfaceCollection mockup result
        with open(
            'oneview_redfish_toolkit/mockups/redfish/'
            'NetworkPortCollection.json'
        ) as f:
            self.network_interface_collection_mockup = json.load(f)

        self.device_id = 1

    def test_class_instantiation(self):
        # Tests if class is correctly instantiated and validated

        try:
            network_interface_collection = \
                NetworkPortCollection(self.server_hardware, self.device_id)
        except Exception as e:
            self.fail("Failed to instantiate NetworkInterfaceCollection class."
                      " Error: {}".format(e))
        self.assertIsInstance(
            network_interface_collection, NetworkPortCollection)

    def test_serialize(self):
        # Tests the serialize function result against known result

        try:
            network_interface_collection = \
                NetworkPortCollection(self.server_hardware, self.device_id)
        except Exception as e:
            self.fail("Failed to instantiate NetworkInterfaceCollection class."
                      " Error: {}".format(e))

        try:
            result = json.loads(network_interface_collection.serialize())
        except Exception as e:
            self.fail("Failed to serialize. Error: ".format(e))

        self.assertEqual(self.network_interface_collection_mockup, result)
