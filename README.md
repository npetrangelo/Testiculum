# Testiculum
An interoperability test suite for the [Reticulum Network Stack](https://github.com/markqvist/reticulum).

## Purpose
Diversity in an ecosystem creates strength, but interoperability remains paramount for network protocols. 
Testiculum fulfills the need to diversify while maintaining compatibility. It also aids in port development itself.
It may also be used by future versions of the reference implementation to test against past versions.


## How to use
To use this test suite, you will need to rewrite `EUT.py` for the RNS implementation you want to test
for the test suite to interact with.

It is advised to implement Reticulum's features in the order they are tested here, as each successive feature
is dependent on the features tested before it to work.

To test with different interfaces, specify the interface in the config file following [these instructions](https://reticulum.network/manual/interfaces.html).

## How it works

For all tests, use the app name `testiculum`. This is because Reticulum uses app namespaces to determine which
destinations are participating in the same app.

#### Broadcast
The broadcast test works by issuing a broadcast from the QE to the EUT, to which EUT responds with its own broadcast.
To meet this test, the EUT must create a `Plain` destination with the `plain` aspect and respond using that.
See the `Broadcaster` class in `EUT.py` for an example.
The EUT does not have to implement cryptographic mechanisms at this stage.

#### Announce
The announce test works by issuing an announce and expecting one in return. To meet this test, the EUT must be able to
receive announces and make its own. Broadcasts are prerequisite because all announces are broadcasted.
See the `Single` class in `EUT.py` for an example. The EUT does not have to implement proofs at this stage.

#### Proof
The proof test works by sending a packet to the EUT and verifying that it received the proof back.
To meet this test, the Single destination in the EUT must set either a `PROVE_ALL` or a `PROVE_APP` strategy.

Note: `PROVE_ALL` is similar to TCP which ensures that packets are received intact, while `PROVE_NONE`
is analogous to UDP, which does not.

### Currently testing:
* Broadcast
* Announce
* Proof

### Future Ideas - Not currently implemented
- **local testing**: launch many destinations through the running `rnsd` instance, regardless of its source language
- **end-to-end connection testing**: announce to network to coordinate tests to echo servers
- **benchmarking**: measure performance of the tweaks you give your stack and routing protocols
- Make port authors write minimal programs for test suite to interact with
