# This is an example implementation of what QE needs to test your implementation of RNS.

import argparse
import RNS

APP_NAME = "testiculum"
configpath = "../config"


# This initialisation is executed when the program is started
def program_setup():
    # We must first initialise Reticulum
    reticulum = RNS.Reticulum(configpath)
    broadcaster = Broadcaster()
    single = Single(identity=RNS.Identity())
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


class Single:
    def __init__(self, identity=RNS.Identity()):
        self.aspect_filter = "testiculum.in"
        self.destination = RNS.Destination(
            identity,
            RNS.Destination.IN,
            RNS.Destination.SINGLE,
            APP_NAME,
            "in"
        )

        self.destination.set_proof_strategy(RNS.Destination.PROVE_ALL)
        RNS.Transport.register_announce_handler(self)

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
