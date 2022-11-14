import graphviz
from typing import List, Union, Tuple
from dataclasses import dataclass


class StateVariable:
    def __init__(self, variable_type: type,
                 name: str,
                 description: str = None,
                 symbol: str = None,
                 units: str = None):
        self.variable_type = variable_type
        self.name = name
        self.description = description
        self.symbol = symbol
        self.units = units

    def __repr__(self):
        return "{}-{}".format(self.name, self.variable_type)


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
            out += "<p>"
            out += "{}. {}".format(i+1, x.label)
            out += "</p>"
        out += "<h4>Constraints:</h4>\n"
        for i, x in enumerate(self.constraints):
            out += "<p>"
            out += "{}. {}".format(i+1, x)
            out += "</p>"
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
            out += "<p>"
            out += "{}. {}".format(i+1, x)
            out += "</p>"

        out += "<h4>Input Messages:</h4>\n"
        for i, x in enumerate(description_set["inputs"]):
            out += "<p>"
            out += "{}. {}".format(i+1, x)
            out += "</p>"

        out += "<h4>Followed By:</h4>\n"
        for i, x in enumerate(description_set["followed_by"]):
            out += "<p>"
            out += "{}. {}".format(i+1, x)
            out += "</p>"

        out += "<h4>Output Messages:</h4>\n"
        for i, x in enumerate(description_set["outputs"]):
            out += "<p>"
            out += "{}. {}".format(i+1, x)
            out += "</p>"

        out += "<h4>Constraints:</h4>\n"
        for i, x in enumerate(self.constraints):
            out += "<p>"
            out += "{}. {}\n".format(i+1, x)
            out += "</p>"
        if policy_options:
            out += "<h4>Policy Options:</h4>\n"
            for i, x in enumerate(policy_options):
                out += "<details>"
                out += "<summary><b>{}. {}</b></summary>".format(i+1, x.label)
                out += "<p>"
                out += x.description
                out += "</p>"

                out += "<p>"
                out += "Input Messages:"
                out += "</p>"

                for i, y in enumerate(x.inputs):
                    out += "<p>"
                    out += "{}. {}\n".format(i+1, y.__name__)
                    out += "</p>"

                out += "Output Messages:"
                for i, y in enumerate(x.outputs):
                    out += "<p>"
                    out += "{}. {}".format(i+1, y.__name__)
                    out += "</p>"

                out += "<p>"
                out += "Logic: {}".format(x.logic)
                out += "</p>"

                out += "</details>"
            out += "<br/>"

        return out


@dataclass
class PolicyActionOption(SystemAction):
    label: str
    description: str
    inputs: List[Message]
    outputs: List[Message]
    logic: str


@dataclass
class MechanismAction(SystemAction):
    label: str
    description: str
    constraints: List[str]
    logic: str = None

    action_type: str = "Mechanism"
    node_color: str = "blue"
    node_shape: str = "oval"

    def create_node(self, graph):
        graph.node(self.label, self.label, shape=self.node_shape,
                   style='filled', color=self.node_color)

    def write_description(self, description_set):
        out = ""
        out += "<h3>"
        out += self.label
        out += "</h3>"
        out += "<p>"
        out += self.description
        out += "</p>"

        out += "<h4>Input Messages:</h4>\n"
        for i, x in enumerate(description_set["inputs"]):
            out += "<p>"
            out += "{}. {}".format(i+1, x)
            out += "</p>"

        out += "<h4>Followed By:</h4>\n"
        for i, x in enumerate(description_set["followed_by"]):
            out += "<p>"
            out += "{}. {}".format(i+1, x)
            out += "</p>"

        out += "<h4>Output Messages:</h4>\n"
        for i, x in enumerate(description_set["outputs"]):
            out += "<p>"
            out += "{}. {}".format(i+1, x)
            out += "</p>"

        out += "<h4>Constraints:</h4>\n"
        for i, x in enumerate(self.constraints):
            out += "<p>"
            out += "{}. {}\n".format(i+1, x)
            out += "</p>"

        out += "<h4>Logic:</h4>\n"
        out += "<p>"
        out += self.logic
        out += "</p>"

        return out


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
