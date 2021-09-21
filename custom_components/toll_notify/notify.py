"""
Custom component for Home Assistant to enable sending messages via tollfree notify API.
Example configuration.yaml entry:
notify:
  - name: tollfree_call
    platform: toll_notify
    access_token: 'tag key'    
    
With this custom component loaded, you can send messaged to tollfree notify.
"""

import requests
import logging


from aiohttp.hdrs import AUTHORIZATION

from homeassistant.const import CONF_ACCESS_TOKEN
from homeassistant.components.notify import (
    ATTR_DATA,
    PLATFORM_SCHEMA,
    BaseNotificationService,
)

_LOGGER = logging.getLogger(__name__)

BASE_URL = "https://homeassistant.systems/push/toll"


def get_service(hass, config, discovery_info=None):
    """Get the tollfree notification service."""
    access_token = config.get(CONF_ACCESS_TOKEN)
    return TollFreeNotificationService(access_token)


class TollFreeNotificationService(BaseNotificationService):
    """Implementation of a notification service for the tollfree Messaging service."""

    def __init__(self, access_token):
        """Initialize the service."""
        self.access_token = access_token

    def send_message(self, message="", **kwargs):
        """Send some message."""
        headers = {AUTHORIZATION: "Bearer " + self.access_token}

        payload = {"message": message, "tagkey": self.access_token}

        r = requests.Session().post(BASE_URL, headers=headers, data=payload)
        if r.status_code != 200:
            _LOGGER.error(r.text)
