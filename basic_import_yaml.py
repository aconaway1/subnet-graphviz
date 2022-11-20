"""
Take a list of subnets & devices with addresses and creates a Graphviz diagram of the relationships amongst them.
"""
import graphviz
import ipaddress
import yaml

INPUT_FILE = "subnet_device_info.yml"

def main():

    debug = True

    try:
        with open(INPUT_FILE, 'r') as file:
            imported_data = yaml.safe_load(file)
    except FileExistsError:
        print(f"Can't read the file {INPUT_FILE}.")

    graph = graphviz.Digraph("Testing stuff", engine='circo', strict=False)
    graph.edge_attr.update(arrowhead='none')
    graph.node_attr.update(shape='box')

    for subnet in imported_data['subnets']:
        if 'label' in subnet.keys():
            subnet_node = graph.node(subnet['subnet'], label=subnet['label'], shape="diamond")
        else:
            subnet_node = graph.node(subnet['subnet'], shape="oval", fillcolor="blue", style='filled', fontcolor="white")
            # subnet_node.attr['shape'] = "oval"

        if 'adj' in subnet.keys():
            for neighbor in subnet['adj']:
                graph.edge(subnet['subnet'], neighbor)

    for device in imported_data['devices']:
        if 'label' in device.keys():
            graph.node(device['device'], label=device['label'])
        else:
            graph.node(device['device'], fillcolor="green", style="filled")

        if 'addresses' in device.keys():
            for address in device['addresses']:
                for subnet in imported_data['subnets']:
                    checked_subnet = ipaddress.ip_network(subnet['subnet'])
                    if ipaddress.ip_address(address) in checked_subnet.hosts():
                        if debug:
                            print(f"{address} is a part of {subnet['subnet']}.")
                        graph.edge(subnet['subnet'], device['device'], headlabel=address, labelfontsize="8")

    print(f"{graph.source}")
    graph.view()



if __name__ == "__main__":
    main()