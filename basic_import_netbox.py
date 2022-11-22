"""
INCOMPLETE!!!!

Take a list of subnets & devices with addresses and creates a Graphviz diagram of the relationships amongst them.
"""
import graphviz
import ipaddress
import yaml
import pynetbox

NETBOX_SERVER = "192.168.254.108"
NETBOX_API_KEY = "742a8ea4ab7461b0a5ef6a9f4fda786d45636347"

def main():

    debug = True

    # Connect to Netbox
    nb_conn = pynetbox.api(url=f"https://{NETBOX_SERVER}", token=NETBOX_API_KEY)
    nb_conn.http_session.verify = False
    # Get all the subnets
    nb_subnets = nb_conn.ipam.prefixes.filter(status="active")
    nb_subnets = list(nb_subnets)

    subnets = []
    for subnet in nb_subnets:
        subnets.append({"subnet": subnet.prefix})

    nb_addresses = nb_conn.ipam.ip_addresses.all()
    nb_addresses = list(nb_addresses)
    if debug:
        for address in nb_addresses:
            print(f"{address.address} on {address.assigned_object.device.name}")

    graph = graphviz.Digraph("Testing stuff", engine='circo', strict=False)
    graph.edge_attr.update(arrowhead='none')
    graph.node_attr.update(shape='box')

    for subnet in subnets:
        if 'label' in subnet.keys():
            graph.node(subnet['subnet'], label=subnet['label'], shape="oval", fillcolor="blue", style="filled", fontcolor="white")
        else:
            graph.node(subnet['subnet'], shape="oval", fillcolor="blue", style="filled", fontcolor="white")

    nodes_to_add = []

    for address in nb_addresses:
        print(f"ADDR: {address}")
        checked_node = address.assigned_object.device.name
        if checked_node not in nodes_to_add:
            nodes_to_add.append(checked_node)

    if debug:
        print(f"NODES TO ADD: {nodes_to_add}")
    for node in nodes_to_add:
        graph.node(node)

    print(nb_addresses)
    for address in nb_addresses:
        for subnet in subnets:
            checked_subnet = ipaddress.ip_network(subnet['subnet'])
            clean_address = address.address.split("/")[0]
            if debug:
                print(f"IP Address: {clean_address}")
            if ipaddress.ip_address(clean_address) in checked_subnet.hosts():
                if debug:
                    print(f"{address} is a part of {subnet['subnet']}.")
                    print(f"DEVICE: {address['assigned_object']['device']['name']}")
                    print(f"SUBNET: {subnet['subnet']}")
                graph.edge(subnet['subnet'], address['assigned_object']['device']['name'], headlabel=clean_address, labelfontsize="8")
                continue

    nb_conn.http_session.close()

    if debug:
        print(f"{graph.source}")
    graph.view()

if __name__ == "__main__":
    main()