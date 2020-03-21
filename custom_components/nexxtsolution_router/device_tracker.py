"""Support for NEXXT_SOLUTION routers."""
from random import seed
from random import random
from collections import namedtuple
import logging
import hashlib
import json
import requests
import voluptuous as vol

from homeassistant.components.device_tracker import (
    DOMAIN,
    PLATFORM_SCHEMA,
    DeviceScanner,
)
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
    }
)


def get_scanner(hass, config):
    """Validate the configuration and return a NEXXT_SOLUTION scanner."""
    scanner = NexxtSolutionDeviceScanner(config[DOMAIN])

    return scanner


Device = namedtuple("Device", ["name", "ip", "mac", "state"])


class NexxtSolutionDeviceScanner(DeviceScanner):
    """This class queries a router running NEXXT_SOLUTION firmware."""

    def __init__(self, config):
        """Initialize the scanner."""

        # encoding clear password
        md5_result = hashlib.md5(config[CONF_PASSWORD].encode())

        self.host = config[CONF_HOST]
        self.username = config[CONF_USERNAME]
        self.password = md5_result.hexdigest()

        self.last_results = []

    def scan_devices(self):
        """Scan for new devices and return a list with found device IDs."""
        self._update_info()
        return [client.mac for client in self.last_results]

    def get_device_name(self, device):
        """Return the name of the given device or None if we don't know."""
        if not self.last_results:
            return None
        for client in self.last_results:
            if client.mac == device:
                return client.name
        return None

    def _update_info(self):
        """Ensure the information from the router is up to date.

        Return boolean if scanning successful.
        """
        data = self._get_data()
        if not data:
            return False

        active_clients = [client for client in data if client.state]
        self.last_results = active_clients

        _LOGGER.debug(
            "LCBA Active clients: %s",
            "\n".join(f"{client.mac} {client.name}" for client in active_clients),
        )
        return True

    def _get_data(self):
        """Get the devices' data from the router.

        Returns a list with all the devices known to the router DHCP server.
        """
        _json = self._get_devices_response()
        _LOGGER.debug("LCBA Device response", _json)
        _devices = json.loads(_json)

        devices = []
        for _device in _devices:
            if "deviceId" in _device:
                devices.append(
                    Device(_device["devName"], _device["ip"], _device["deviceId"], 1,)
                )

        return devices

    def _get_devices_response(self):
        """Get the raw string with the devices from the router."""
        try:
            headers = {
                "X-Requested-With": "XMLHttpRequest",
                "Origin": f"http://{self.host}/login.html",
            }

            _LOGGER.debug("LCBA Logging in")
            login_response = requests.post(
                f"http://{self.host}/login/Auth",
                data=[("username", self.username), ("password", self.password)],
                headers=headers,
                allow_redirects=False,
            )

            if login_response.text != "1":
                headers = {
                    "X-Requested-With": "XMLHttpRequest",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                }

                seed(1)
                rand = random()
                device_response = requests.get(
                    f"http://{self.host}/goform/getOnlineList?{rand}",
                    headers=headers,
                    cookies=login_response.cookies,
                )

                if not "<html" in device_response.text:
                    return device_response.text
                else:
                    _LOGGER.debug(device_response)
            else:
                _LOGGER.debug("LCBA Incorrect username and/or password")
        except requests.exceptions.ConnectionError:
            _LOGGER.debug("LCBA Connection refused")

        return "[]"