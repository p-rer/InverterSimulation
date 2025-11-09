import re
import numpy as np

from Circuit.Circuit import Circuit
from CircuitElement.Capacitor import Capacitor
from CircuitElement.CurrentSource import CurrentSource
from CircuitElement.Diode import Diode
from CircuitElement.Resistor import Resistor
from CircuitElement.VoltageSource import VoltageSource

class SpiceParser:
    component_map = {
        "R": Resistor,
        "C": Capacitor,
        "D": Diode,
        "V": VoltageSource,
        "I": CurrentSource,
    }

    expression_map = {
        "SIN": lambda params: (lambda t: float(params[0]) + float(params[1]) * np.sin(2 * np.pi * (float(params[2].rstrip('kK')) * 1e3 if 'k' in params[2].lower() else float(params[2])) * t))
    }

    def __init__(self, text):
        self.text = text.splitlines()
        self.models = {}

    @staticmethod
    def parse_value(val_str):
        try:
            if val_str.endswith("u"):
                return float(val_str[:-1]) * 1e-6
            elif val_str.endswith("k"):
                return float(val_str[:-1]) * 1e3
            else:
                return float(val_str)
        except ValueError:
            return val_str

    def parse_model(self, line):
        m = re.match(r"\.model\s+(\S+)\s+(\S+)\((.+)\)", line, re.IGNORECASE)
        if m:
            name, kind, params = m.groups()
            param_dict = {}
            # 空白で区切られた複数のパラメータを正しく解析
            for item in re.findall(r"(\S+?=\S+)", params):
                k, _, v = item.partition('=')
                try:
                    param_dict[k] = float(v)
                except ValueError:
                    param_dict[k] = v
            self.models[name.upper()] = (kind.upper(), param_dict)

    @staticmethod
    def parse_tran(line):
        m = re.match(r"\.tran\s+(\S+)\s+(\S+)", line, re.IGNORECASE)
        if m:
            dt, t_end = map(float, m.groups())
            return dt, t_end
        return None, None

    def parse_expression(self, expr_str):
        for key, func in self.expression_map.items():
            if expr_str.upper().startswith(key):
                m = re.match(rf"{key}\(([^)]+)\)", expr_str, re.IGNORECASE)
                if m:
                    params = m.group(1).split()
                    return func(params)
        return self.parse_value(expr_str)

    def parse_component(self, line):
        tokens = line.split(maxsplit=3)
        if not tokens or tokens[0].startswith("."):
            return None

        name, n1, n2 = tokens[0], tokens[1], tokens[2]
        rest = tokens[3] if len(tokens) > 3 else None

        kind = name[0].upper()
        cls = self.component_map.get(kind)
        if not cls:
            raise ValueError(f"Unknown component {kind}")

        n1, n2 = int(n1), int(n2)

        value = None
        if rest:
            # モデル名が登録されていれば、そのパラメータ辞書を展開して渡す
            model_info = self.models.get(rest.upper())
            if model_info:
                kind_m, params = model_info
                value = params
            else:
                value = self.parse_expression(rest)

        return cls(n1, n2, **value) if isinstance(value, dict) else cls(n1, n2, value)

    def to_circuit(self):
        for line in self.text:
            line = line.strip()
            if line.lower().startswith(".model"):
                self.parse_model(line)

        elements = []
        for line in self.text:
            line = line.strip()
            if not line or line.startswith("."):
                continue
            elem = self.parse_component(line)
            if elem:
                elements.append(elem)

        dt, t_end = None, None
        for line in self.text:
            line = line.strip()
            if line.lower().startswith(".tran"):
                dt, t_end = self.parse_tran(line)

        max_node = max([e.n1 for e in elements] + [e.n2 for e in elements])
        ckt = Circuit(num_nodes=max_node+1)
        for e in elements:
            ckt.add_element(e)
        return ckt, dt, t_end