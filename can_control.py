"""
can_control.py
"""

import can
from singleton_decorator    import singleton


class CallbackListener(can.Listener):
    """A CallbackListener that calls a user-defined function with all received messages"""

    def __init__(self, callback):
        self.callback = callback

    def on_message_received(self, msg):
        self.callback(msg)

    def set_callback(self, callback):
        self.callback = callback


@singleton
class CanControl:
    """CanControl singleton that manages operations on the bus"""

    def __init__(self):
        # settings
        self.interface  : str   = None
        self.channel    : str   = None
        self.bitrate    : str   = None

        # notifer etc
        self.bus        : can.interface.Bus     = None
        self.listener   : CallbackListener      = None
        self.notifier   : can.Notifier          = None

        # NOTE: 'set_settings', 'set_notifier' and 'set_callback' need to be called once as part of the init process

    def set_settings(self, *, interface, channel, bitrate) -> None:
        """Init static settings for canbus"""
        self.interface  = interface
        self.channel    = channel
        self.bitrate    = bitrate

    def set_notifier(self) -> None:
        """Init CAN notifier"""
        self.bus = can.interface.Bus(
            interface   = self.interface,
            channel     = self.channel,
            bitrate     = self.bitrate
        )
        self.notifier = can.Notifier(self.bus, [])

    def set_callback(self, callback) -> None:
        """Inits callback lisener"""
        self.listener = CallbackListener(callback)

    def notifier_start(self) -> None:
        """Starts notifier by adding listener"""
        self.notifier.add_listener(self.listener)

    def notifier_stop(self) -> None:
        """Stops notifier by removing listener"""
        self.notifier.remove_listener(self.listener)

    def send_msg(self, msg, timeout=1):
        """Sends a message on CAN bus"""
        try:
            self.bus.send(msg, timeout)
        except can.CanError:
            pass  # TODO error handling
