# CAN MQTT Gate

This module serves as a bridge between a MQTT broker and a CAN bus, publishing all CAN messages to the broker and also accepting messages to be send on the CAN bus via MQTT.

Incoming CAN messages are published as ``json`` to ``CAN/OUT/<ID>/<OBJ>``, where ``<ID>`` is the ID of the CAN node and ``<OBJ>`` is the object type of the message (i.e. RPDO1). All messages published on ``CAN/IN/#`` are send back on the CAN bus. These should be encoded as ``json``, following the format found in the [pycan-addons module](https://github.com/TimH96/pycan_addons).

The program is configurable via the ``settings.json`` file, which is created upon execution.

### Dependencies
+ ``paho-mqtt`` module
+ ``python-can`` module
+ ``pycan-addons`` module
+ ``singleton-decoator`` module