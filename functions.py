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
