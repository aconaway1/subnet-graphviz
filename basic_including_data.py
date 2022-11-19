"""
Take a list of subnets & devices with addresses and creates a Graphviz diagram of the relationships amongst them.
"""
import graphviz
import ipaddress

def main():

    debug = True

    subnets = [
        {"subnet": "192.168.0.0/24"},
        {"subnet": "192.168.1.0/24"},
        {"subnet": "192.168.2.0/24"},
        {"subnet": "192.168.3.0/24"},
        {"subnet": "10.0.0.0/24"},
        {"subnet": "10.0.1.0/24"},
        {"subnet": "10.0.2.0/25"},
        {"subnet": "10.0.2.128/25"},
    ]

    devices = [
        {"device": "ROUTER A", "addresses": ["192.168.0.1", "192.168.1.1", "192.168.2.1"]},
        {"device": "ROUTER B", "addresses": ["192.168.0.2", "192.168.3.2"]},
        {"device": "ROUTER C", "addresses": ["192.168.2.3", "192.168.3.3", "10.0.1.3"]},
        {"device": "ROUTER D", "addresses": ["192.168.3.4", "10.0.0.4", "10.0.2.132", "10.0.2.142"]},
        {"device": "ROUTER E", "addresses": ["192.168.2.5", "10.0.2.5"]}
    ]

    graph = graphviz.Digraph("Testing stuff", engine='neato')
    graph.edge_attr.update(arrowhead='none')
    graph.node_attr.update(shape='box')

    for subnet in subnets:
        if 'label' in subnet.keys():
            subnet_node = graph.node(subnet['subnet'], label=subnet['label'])
            subnet_node.attr['shape'] = "oval"
        else:
            subnet_node = graph.node(subnet['subnet'])
            # subnet_node.attr['shape'] = "oval"

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
                        if debug:
                            print(f"{address} is a part of {subnet['subnet']}.")
                        graph.edge(subnet['subnet'], device['device'], headlabel=address)

    print(f"{graph.source}")
    graph.view()



if __name__ == "__main__":
    main()