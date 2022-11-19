# Summary
This is a very simple script that generates a graphviz diagram for a list of subnets and devices.

The endgame for me here is to be able to generate network diagrams on demand using data from Netbox. There's lots of work to do on that front yet, but we're getting there.

The subnets are in dictionary format and include the subnet in CIDR format.

    devices: [
              { "subnet": "192.168.0.0/24" },
              { "subnet": "192.168.1.0/24" },
              ...
    ]

The devices are in dictionary format and include the name and a list of interface IP addresses.

    devices = [
        {"device": "ROUTER A", "addresses": ["192.168.0.1", "192.168.1.1", "192.168.2.1"]},
        {"device": "ROUTER B", "addresses": ["192.168.0.2", "192.168.3.2"]},
        ...
    ]

# Requirements

## Python

This probably works in very every Python version out there.

## Python Modules
### graphviz: For creating the graph and showing it.
### ipaddress: For handling IP addresses.

# FAQ
## Where's your IPv6 support?
I just started this project 15 minutes ago. I'll get to it.