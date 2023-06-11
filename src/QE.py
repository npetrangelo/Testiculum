import time
import unittest
import RNS

APP_NAME = "testiculum"
configpath = "../config"


class MyTestCase(unittest.TestCase):
    # We will need to define an announce handler class that
    # Reticulum can message when an announce arrives.
    class AnnounceHandler:
        # The initialisation method takes the optional
        # aspect_filter argument. If aspect_filter is set to
        # None, all announces will be passed to the instance.
        # If only some announces are wanted, it can be set to
        # an aspect string.
        def __init__(self, aspect_filter=None, destination=None):
            self.aspect_filter = aspect_filter
            self.destination = destination
            self.received = False

        # This method will be called by Reticulum's Transport
        # system when an announce arrives.
        def received_announce(self, destination_hash, announced_identity, app_data):
            RNS.log(
                "Received an announce from " +
                RNS.prettyhexrep(destination_hash)
            )
            self.received = True

    # This method will be called by Reticulum's Transport
    # system when a broadcast arrives.
    def packet_callback(self, data, packet):
        self.broadcast_received = data.decode("utf-8")
        RNS.log(
            "Received broadcast: " + self.broadcast_received
        )

    @classmethod
    def setUpClass(cls) -> None:
        # We must first initialise Reticulum
        cls.reticulum = RNS.Reticulum(configpath)
        # Randomly create a new identity for our example
        identity = RNS.Identity()

        # Using the identity we just created, we create one destination
        # in the "QE" application space.
        #
        # Destinations are endpoints in Reticulum, that can be addressed
        # and communicated with. Destinations can also announce their
        # existence, which will let the network know they are reachable
        # and automatically create paths to them, from anywhere else
        # in the network.
        cls.broadcast = RNS.Destination(
            None,
            RNS.Destination.IN,
            RNS.Destination.PLAIN,
            APP_NAME,
            "broadcast"
        )
        cls.broadcast.set_proof_strategy(RNS.Destination.PROVE_ALL)
        cls.broadcast.set_packet_callback(lambda data, packet: cls.packet_callback(cls, data, packet))

        cls.single = RNS.Destination(
            identity,
            RNS.Destination.IN,
            RNS.Destination.SINGLE,
            APP_NAME,
            "QE",
            "single"
        )
        cls.single.set_proof_strategy(RNS.Destination.PROVE_ALL)

        cls.announce_handler = cls.AnnounceHandler(aspect_filter="testiculum.EUT.single", destination=cls.single)
        RNS.Transport.register_announce_handler(cls.announce_handler)

    def test_broadcast_received(self) -> None:
        self.broadcast_received = None
        print("Broadcast test: Enter data to receive back")
        QE_broadcast = "QE broadcast".encode("utf-8")
        packet = RNS.Packet(self.broadcast, QE_broadcast)
        packet.send()
        time.sleep(2)
        EUT_broadcast = "EUT broadcast".encode("utf-8")
        self.assertEqual(EUT_broadcast, self.broadcast_received)

    def test_announce_received(self) -> None:
        self.single.announce()
        # Assert announcement from EUT received
        time.sleep(2)
        self.assertTrue(self.announce_handler.received)


if __name__ == '__main__':
    unittest.main()
