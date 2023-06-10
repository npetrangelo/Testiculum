import time
import unittest
import RNS

APP_NAME = "QE"
configpath = None


class MyTestCase(unittest.TestCase):
    # We will need to define an announce handler class that
    # Reticulum can message when an announce arrives.
    class AnnounceHandler:
        # The initialisation method takes the optional
        # aspect_filter argument. If aspect_filter is set to
        # None, all announces will be passed to the instance.
        # If only some announces are wanted, it can be set to
        # an aspect string.
        def __init__(self, destination=None):
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
        cls.destination = RNS.Destination(
            identity,
            RNS.Destination.IN,
            RNS.Destination.SINGLE,
            APP_NAME,
            "announce"
        )
        cls.destination.set_proof_strategy(RNS.Destination.PROVE_ALL)
        cls.announce_handler = cls.AnnounceHandler()
        RNS.Transport.register_announce_handler(cls.announce_handler)

    def test_announce_received(self) -> None:
        self.destination.announce()
        # Assert announcement from EUT received
        time.sleep(5)
        self.assertTrue(self.announce_handler.received)


if __name__ == '__main__':
    unittest.main()
