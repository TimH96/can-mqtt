"""
network_interface.py
"""

from abc import ABCMeta, abstractmethod
from can import Message


class NetworkInterface(metaclass=ABCMeta):
    """Common interface of all network variations"""

    @abstractmethod
    def publish(self, msg: Message):
        """
        Publish a CAN message on the network as json
        """
        raise NotImplementedError

    @abstractmethod
    def enter_network_code(self, **kwargs):
        """
        Enter blocking network code, called from main thread with configured settings after everything is initialized.

        CAN notifier also needs to be connected to callback and started from here.
        """
        raise NotImplementedError
