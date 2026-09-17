import parser

class Generator:
    def __init__(self):
        self.tree = []
        self.bytecode = ""

    def generate_from_expr(self, expr)->None:
        if type(expr) == parser.Variable:
            self.bytecode += f"load_name {expr.name}\n"
        elif type(expr) == str:
            self.bytecode += f'load_value "{expr}"\n'
        else:
            self.bytecode += f"load_value {expr}\n"

    def generate_from_node(self, node)->None:
        if type(node) == parser.Call:
            self.generate_from_expr(node.callee)
            for arg in node.arguments:
                self.generate_from_expr(arg)
            self.bytecode += f"call {len(node.arguments)}\n"
        elif type(node) == parser.Assign:
            self.generate_from_expr(node.value)
            self.bytecode += f"store_name {node.name}\n"

    def generate(self, tree:list[parser.Node])->str:
        self.tree = tree
        self.bytecode = ""
        for node in tree:
            self.generate_from_node(node)
        return self.bytecode