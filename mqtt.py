"""
mqtt.py
"""

from can                import Message
from paho.mqtt          import client as mqtt
from pycan_addons       import class_bind
from network_interface  import NetworkInterface
from can_control        import CanControl


class MQTTBridge(mqtt.Client, NetworkInterface):
    """
    MQTT bridge broadcasting CAN messages to MQTT broker as json and distributes incoming messages back on CAN
    """

    def __init__(
        self,
        *,
        client_id="",
        clean_session=True,
        userdata=None,
        protocol=mqtt.MQTTv311,
        transport="tcp",
        broker
    ):
        super(MQTTBridge, self).__init__(client_id, clean_session, userdata, protocol, transport)
        self.broker = broker

    def do_on_mqtt_message(self, client, userdata, msg) -> None:
        """Callback method for paho.mqtt.client 'on_message' event"""
        # parse payload and send on CAN bus
        new_msg = Message()
        new_msg.json_parse(msg.payload)
        CanControl().send_msg(new_msg)

    def do_on_can_message(self, msg: Message) -> None:
        """Callback method for can_control.CanControl.listener 'on_message_received' event"""
        json_payload    = msg.json_stringify()
        address_data    = msg.get_address_data()
        topic           = "CAN/OUT/%s/%s" % (address_data["node_id"], address_data["object_type"])
        self.publish(topic, payload=json_payload, qos=0)

    def enter_network_code(self):
        """Main MQTT code called from main thread"""
        # init CanControl notifier
        CanControl().set_notifier()
        CanControl().set_callback(self.do_on_can_message)
        CanControl().notifier_start()
        # connect MQTT callback function
        self.on_message = self.do_on_mqtt_message
        # connect to broker and block thread
        self.connect(
            self.broker["host"],
            self.broker["port"],
        )
        self.subscribe("CAN/IN", qos=0)
        self.subscribe("CAN/IN/#", qos=0)
        self.loop_forever()