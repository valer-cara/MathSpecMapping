import graphviz
from typing import List, Union
from dataclasses import dataclass


class SystemState:
    pass


class Message:
    color: str


@dataclass
class Entity:
    label: str
    state: SystemState

    def create_node(self, graph):
        graph.node(self.label, self.label, shape="cylinder", color="black")

    def __hash__(self):
        return hash(self.label)


@dataclass
class BehavioralAction:
    label: str
    description: str
    called_by: List[Entity]
    constraints: List[str]

    action_type: str = "Behavioral"
    node_color: str = "orange"
    node_shape: str = "diamond"

    def create_node(self, graph):
        graph.node(self.label, self.label, shape=self.node_shape,
                   style='filled', color=self.node_color)


class SystemAction:
    pass


@dataclass
class PolicyAction(SystemAction):
    label: str
    description: str
    constraints: List[str]

    action_type: str = "Policy"
    node_color: str = "red"
    node_shape: str = "rectangle"

    def create_node(self, graph):
        graph.node(self.label, self.label, shape=self.node_shape,
                   style='filled', color=self.node_color)


@dataclass
class MechanismAction(SystemAction):
    label: str
    description: str
    constraints: List[str]

    action_type: str = "Mechanism"
    node_color: str = "blue"
    node_shape: str = "oval"

    def create_node(self, graph):
        graph.node(self.label, self.label, shape=self.node_shape,
                   style='filled', color=self.node_color)


@dataclass
class Edge:
    origin: Union[BehavioralAction, SystemAction]
    target: SystemAction
    message: Message
    optional: bool = False


@dataclass
class StateModificationEdge:
    origin: SystemAction
    entity: Entity
    variable: str
    optional: bool = False
