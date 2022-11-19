# import networkx as nx
# import matplotlib.pyplot as plt
import graphviz
import ipaddress

def main():

    subnets = [
        {"subnet": "192.168.0.0/24"},
        {"subnet": "192.168.1.0/24"},
        {"subnet": "192.168.2.0/24"},
        {"subnet": "192.168.3.0/24"}
    ]

    devices = [
        {"device": "ROUTER A", "addresses": ["192.168.0.1", "192.168.1.1", "192.168.2.1"]},
        {"device": "ROUTER B", "addresses": ["192.168.0.2", "192.168.3.2"]},
        {"device": "ROUTER C", "addresses": ["192.168.2.3", "192.168.3.3"]},
    ]

    graph = graphviz.Digraph("Testing stuff")
    graph.edge_attr.update(arrowhead='none')

    for subnet in subnets:
        if 'label' in subnet.keys():
            graph.node(subnet['subnet'], label=subnet['label'])
        else:
            graph.node(subnet['subnet'])

        if 'adj' in subnet.keys():
            for neighbor in subnet['adj']:
                graph.edge(subnet['subnet'], neighbor)

    for device in devices:
        if 'label' in device.keys():
            graph.node(device['device'], label=device['label'])
        else:
            graph.node(device['device'])

        if 'addresses' in device.keys():
            for address in device['addresses']:
                for subnet in subnets:
                    checked_subnet = ipaddress.ip_network(subnet['subnet'])
                    if ipaddress.ip_address(address) in checked_subnet.hosts():
                        print(f"{address} is a part of {subnet['subnet']}.")
                        graph.edge(subnet['subnet'], device['device'])

    print(f"{graph.source}")
    graph.view()



if __name__ == "__main__":
    main()