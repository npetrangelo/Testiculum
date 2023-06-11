# This is an example for what QE/Announce expects to interact with.
# Implement this small program in your own version of RNS to test it.

import argparse
import RNS

APP_NAME = "testiculum"
configpath = "../config"


# This initialisation is executed when the program is started
def program_setup():
    # We must first initialise Reticulum
    reticulum = RNS.Reticulum(configpath)
    broadcaster = Broadcaster()
    announcer = Announcer(identity=RNS.Identity())
    input("Hit enter to close program")


class Broadcaster:
    def __init__(self):
        self.inbound = RNS.Destination(
            None,
            RNS.Destination.IN,
            RNS.Destination.PLAIN,
            APP_NAME,
            "broadcast"
        )
        self.inbound.set_packet_callback(self.packet_callback)

    def packet_callback(self, data, packet):
        RNS.log(data.decode("utf-8"))
        broadcast_data = "EUT broadcast".encode("utf-8")
        broadcast = RNS.Packet(self.inbound, broadcast_data)
        broadcast.send()


class Announcer:
    def __init__(self, identity=RNS.Identity()):
        self.destination = RNS.Destination(
            identity,
            RNS.Destination.IN,
            RNS.Destination.SINGLE,
            APP_NAME,
            "EUT",
            "single"
        )

        # We configure the destinations to automatically prove all
        # packets addressed to it. By doing this, RNS will automatically
        # generate a proof for each incoming packet and transmit it
        # back to the sender of that packet. This will let anyone that
        # tries to communicate with the destination know whether their
        # communication was received correctly.
        self.destination.set_proof_strategy(RNS.Destination.PROVE_ALL)

        # We create an announce handler and configure it to announce the EUT node in response
        announce_handler = AnnounceHandler(aspect_filter="testiculum.QE.single", destination=self.destination)

        # We register the announce handler with Reticulum
        RNS.Transport.register_announce_handler(announce_handler)



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

    # This method will be called by Reticulum's Transport
    # system when an announce arrives.
    def received_announce(self, destination_hash, announced_identity, app_data):
        RNS.log(
            "Received an announce from " +
            RNS.prettyhexrep(destination_hash)
        )

        self.destination.announce()
        RNS.log(
            "Sent announce from " +
            RNS.prettyhexrep(self.destination.hash) +
            " (" + self.destination.name + ")"
        )


##########################################################
#### Program Startup #####################################
##########################################################

if __name__ == "__main__":
    program_setup()
