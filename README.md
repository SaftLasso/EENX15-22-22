# EENX15-22-22
This is the GitHub repo for the batchelor project EENX15-22-22 done at Chalmers University of Technology.

The scripts are designed to measure one-way latency and should be used only when the clocks between the two computers are accurately synced.
To sync the clocks PTP can be used: https://manpages.debian.org/unstable/linuxptp/ptp4l.8.en.html

To run the scripts, modify the configuration variables in the top of each script to your liking. Then start receiver.py before running sender.py. The sender will send it's configuration to the receiver and the transmissions and measuring will start.
