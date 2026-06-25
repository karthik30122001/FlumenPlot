
# def sort_check(nodes):
#     for i,_ in enumerate(nodes):
#         if i < len(nodes)-1:
#             if nodes[i]['percent'] >= nodes[i+1]['percent']:
#                 pass
#             else:
#                 return False
#     return True
#
# def bubble_sort(nodes):
#     if sort_check(nodes):
#         return nodes
#
#     else:
#         for i,_ in enumerate(nodes):
#             if i < len(nodes)-1:
#                 if nodes[i]['percent'] > nodes[i+1]['percent']:
#                     pass
#                 else:
#                     v1 = nodes[i]
#                     v2 = nodes[i+1]
#
#                     nodes[i] = v2
#                     nodes[i+1] = v1
#                     v1 = None
#                     v2 = None
#         return bubble_sort(nodes)
def get_roots(nodes, edges):
    targets = {edge["target"] for edge in edges}

    root_nodes = [
        node
        for node in nodes
        if node["name"] not in targets
    ]
    root_nodes.sort(key=lambda x :x["name"])
    
    return root_nodes

def get_children(node, nodes, edges):
    child_names = {
        edge["target"]
        for edge in edges
        if edge["source"] == node["name"]
    }
    
    child_nodes = [
        node
        for node in nodes
        if node["name"] in child_names
        ]
    child_nodes.sort(key=lambda x :x["value"], reverse=True)

    results = []

    for child in child_nodes:
        results.append(child)
        results.extend(
            get_children(child, nodes, edges)
        )

    return results


def order_alpabetically(dataset):
    roots = get_roots(dataset["nodes"], dataset["links"])

    ordered_nodes = []

    for root in roots:
        ordered_nodes.append(root)
        ordered_nodes.extend(get_children(root, dataset["nodes"], dataset["links"]))
        
    return ordered_nodes

