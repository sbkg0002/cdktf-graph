import json
import sys

import pydot


def _read_manifest() -> dict:
    with open('manifest.json', encoding='utf-8') as file:
        try:
            manifest = json.load(file)['stacks']
        except ValueError as err:
            sys.exit(f'Error manifest. The error was: {err}')

    return manifest


def cdktf_graph(manifest: dict):
    graph = pydot.Dot()
    root = ""
    node_edge = pydot.Edge()
    for i, (stack_name, stack_config) in enumerate(manifest.items()):
        if i == 0:
            root = stack_name
            graph = pydot.Dot(stack_name, graph_type="graph", bgcolor="white")
        # Add nodes
        else:
            graph.add_node(pydot.Node(name=stack_name, shape="circle"))

            dependencies = stack_config['dependencies']
            if dependencies:
                for dependency in dependencies:
                    node_edge = pydot.Edge(stack_name, dependency, color="blue")
            else:
                node_edge = pydot.Edge(root, stack_name, color="blue")
            graph.add_edge(node_edge)

    # Or, save it as a DOT-file:
    graph.write_dot("output_graphviz.dot")
    graph.write_png("output.png")


if __name__ == '__main__':
    cdktf_graph(manifest=_read_manifest())
