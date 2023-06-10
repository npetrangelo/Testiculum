import unittest
import RNS
from EUT.Announce import AnnounceHandler

APP_NAME = "QE"
configpath = None


class MyTestCase(unittest.TestCase):
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
        announce_handler = AnnounceHandler()
        RNS.Transport.register_announce_handler(announce_handler)

    def test_something(self) -> None:
        self.assertEqual(True, False)  # add assertion here
        self.destination.announce()
        # Assert announcement from EUT received
        # Assert packet valid


if __name__ == '__main__':
    unittest.main()
