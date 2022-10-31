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

    def write_description(self):
        out = ""
        out += "<h3>"
        out += self.label
        out += "</h3>"
        out += "<p>"
        out += self.description
        out += "</p>"
        out += "<h4>Called By:</h4>\n"
        for i, x in enumerate(self.called_by):
            out += "{}. {}\n".format(i+1, x.label)
        out += "<h4>Constraints:</h4>\n"
        for i, x in enumerate(self.constraints):
            out += "{}. {}\n".format(i+1, x)
        return out


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

    def write_description(self, description_set, policy_options=None):
        out = ""
        out += "<h3>"
        out += self.label
        out += "</h3>"
        out += "<p>"
        out += self.description
        out += "</p>"

        out += "<h4>Preceded By:</h4>\n"
        for i, x in enumerate(description_set["preceded_by"]):
            out += "{}. {}\n".format(i+1, x)

        out += "<h4>Input Messages:</h4>\n"
        for i, x in enumerate(description_set["inputs"]):
            out += "{}. {}\n".format(i+1, x)

        out += "<h4>Followed By:</h4>\n"
        for i, x in enumerate(description_set["followed_by"]):
            out += "{}. {}\n".format(i+1, x)

        out += "<h4>Output Messages:</h4>\n"
        for i, x in enumerate(description_set["outputs"]):
            out += "{}. {}\n".format(i+1, x)

        out += "<h4>Constraints:</h4>\n"
        for i, x in enumerate(self.constraints):
            out += "{}. {}\n".format(i+1, x)
        if policy_options:
            out += "<h4>Policy Options:</h4>\n"
            for i, x in enumerate(policy_options):
                out += "<details>"
                out += "<summary><b>{}. {}</b></summary>".format(i+1, x.label)
                out += x.description
                out += "</details>"

        return out


@dataclass
class PolicyActionOption(SystemAction):
    label: str
    description: str


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
