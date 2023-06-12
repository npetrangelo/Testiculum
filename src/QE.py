import time
import unittest
import RNS

APP_NAME = "testiculum"
configpath = "../config"


class Broadcaster:
    def __init__(self):
        self.received = None
        self.destination = RNS.Destination(
            None,
            RNS.Destination.IN,
            RNS.Destination.PLAIN,
            APP_NAME,
            "broadcast"
        )
        self.destination.set_proof_strategy(RNS.Destination.PROVE_ALL)
        self.destination.set_packet_callback(self.packet_callback)

    def broadcast(self, data):
        packet = RNS.Packet(self.destination, data.encode("utf-8"))
        packet.send()

    # This method will be called by Reticulum's Transport
    # system when a broadcast arrives.
    def packet_callback(self, data, packet):
        self.received = data.decode("utf-8")
        RNS.log(
            "Received broadcast: " + self.received
        )

    def tearDown(self):
        RNS.Transport.deregister_destination(self.destination)


class Single:
    def __init__(self, identity=RNS.Identity()):
        self.announce_received = False
        self.aspect_filter = "testiculum.in"
        self.inbox = RNS.Destination(
            identity,
            RNS.Destination.IN,
            RNS.Destination.SINGLE,
            APP_NAME,
            "in"
        )
        self.inbox.set_proof_strategy(RNS.Destination.PROVE_ALL)
        self.outbox = None
        RNS.Transport.register_announce_handler(self)

    def announce(self):
        self.inbox.announce()

    def received_announce(self, destination_hash, announced_identity, app_data):
        self.announce_received = True
        self.outbox = RNS.Destination(
            announced_identity,
            RNS.Destination.OUT,
            RNS.Destination.SINGLE,
            APP_NAME,
            "out"
        )
        RNS.log(
            "Received an announce from " +
            RNS.prettyhexrep(destination_hash)
        )

    def echo(self):
        echo_request = RNS.Packet(self.outbox, RNS.Identity.get_random_hash())
        return echo_request.send()

    def tearDown(self):
        RNS.Transport.deregister_destination(self.inbox)
        RNS.Transport.deregister_announce_handler(self)


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # We must first initialise Reticulum
        cls.reticulum = RNS.Reticulum(configpath)
        cls.broadcaster = Broadcaster()
        cls.single = Single()
        cls.single.announce()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.broadcaster.tearDown()
        cls.single.tearDown()

    def test_broadcast_received(self) -> None:
        self.broadcaster.broadcast("QE broadcast")
        time.sleep(2)
        self.assertEqual("EUT broadcast", self.broadcaster.received)
        self.broadcaster.tearDown()

    def test_announce_received(self) -> None:
        # Assert announcement from EUT received
        time.sleep(2)
        self.assertTrue(self.single.announce_received)

    def test_echo(self) -> None:
        time.sleep(2)
        self.assertIsNotNone(self.single.outbox)
        self.assertTrue(self.single.echo())


if __name__ == '__main__':
    unittest.main()
