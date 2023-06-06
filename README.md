# Testiculum
A test suite for the [Reticulum Network Stack](https://github.com/markqvist/reticulum).

## Purpose
Diversity in an ecosystem creates strength, but interoperability remains paramount for network protocols. 
Testiculum fulfills the need to diversify while maintaining compatibility. It also aids in port development itself.
It may also be used by future versions of the reference implementation to test against past versions.

This test suite only tests the core of RNS, and does not plan to test network interfaces.

Currently testing:
* Announce

## Ideas
- **local testing**: launch many destinations through the running `rnsd` instance, regardless of its source language
- **end-to-end connection testing**: announce to network to coordinate tests to echo servers
- **benchmarking**: measure performance of the tweaks you give your stack and routing protocols
- Make port authors write minimal programs for test suite to interact with

To use this test suite for your RNS implementation, you will need to write small programs
for the test suite to interact with. Examples can be found in the `tested` directory.
