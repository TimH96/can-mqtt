"""
__main__.py
"""

import json
from can_control    import CanControl
from mqtt           import MQTTBridge
from pathlib        import Path

DEFAULTS = {
    "can": {
        "interface": "virtual",
        "channel": "net0",
        "bitrate": "125000"
    },
    "mqtt": {
        "client_id": "CAN Gate",
        "clean_session": None,
        "userdata": None,
        "transport": "tcp",
        "broker": {
            "host": "localhost",
            "port": 1883
        }
    }
}

# read out default settings
settings : dict = {}
path = Path(__file__).parent / "settings.json"
try:
    with open(path, "r") as file:
        settings = json.loads(file.read())
except FileNotFoundError:
    settings = DEFAULTS
    with open(path, "w+") as file:
        file.write(json.dumps(settings, indent=4))

# TODO read and overwrite CL arguments here eventually, for now just take config file

# initiate CAN object
CanControl()
CanControl().set_settings(**settings["can"])

# initiate main network code
mqtt_gate = MQTTBridge(**settings["mqtt"])
try:
    mqtt_gate.enter_network_code()
except KeyboardInterrupt:
    pass
