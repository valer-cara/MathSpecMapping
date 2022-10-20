from copy import copy
import graphviz
from IPython.display import display
from .classes import StateModificationEdge


def find_starting_entities(actions_to_map, behavioral_action_space, behavioral_action_edges):
    entities = []
    edges = []
    queue = []

    for action in actions_to_map:
        ba = behavioral_action_space[action]
        connections = ba.called_by
        entities.extend(connections)
        edges.extend([x.label, ba.label] for x in connections)
        queue.extend(behavioral_action_edges[action])

    entities = list(set(entities))
    return entities, edges, queue


def create_graph(actions_to_map, name, behavioral_action_space, all_edges):

    entities, edges, queue = find_starting_entities(actions_to_map, behavioral_action_space,
                                                    all_edges)
    seen = entities

    graph = graphviz.Digraph(name)

    graph_messages = []

    for e in entities:
        e.create_node(graph)

    for action in actions_to_map:
        ba = behavioral_action_space[action]
        ba.create_node(graph)
        seen.append(ba)

    for e in edges:
        graph.edge(e[0], e[1])

    sm_actions = []
    while len(queue) > 0:
        cur = queue.pop(0)
        if type(cur) == StateModificationEdge:
            sm_actions.append(cur)
        else:
            if cur.target not in seen:
                cur.target.create_node(graph)
                seen.append(cur.target)
                queue.extend(all_edges[cur.target.label])
            if cur.optional:
                graph.edge(cur.origin.label, cur.target.label,
                           color=cur.message.color, style="dashed")
            else:
                graph.edge(cur.origin.label, cur.target.label,
                           color=cur.message.color)
            if cur.message not in graph_messages:
                graph_messages.append(cur.message)

    for sm in sm_actions:
        if sm.entity not in seen:
            sm.entity.create_node(graph)
            seen.append(sm.entity)
        var_label = "{}.{}".format(sm.entity.label, sm.variable)
        if var_label not in seen:
            graph.node(var_label, var_label)
            seen.append(var_label)

        graph.edge(sm.origin.label, var_label)

    print("Message Legend:")
    print()
    for g in graph_messages:
        a = copy(g.__dict__["__annotations__"])
        a.pop('color')
        print("{}: {} -> {}".format(g.color, g.__name__, a))
        print()
    display(graph)
