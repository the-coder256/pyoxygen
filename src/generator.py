import parser

class Generator:
    def __init__(self):
        self.tree = []
        self.bytecode = ""
        self.label_num = 1

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
        elif type(node) == parser.IfCondition:
            self.generate_from_expr(node.condition)
            self.bytecode += f"jump_if_false _l{self.label_num}\n"
            if node.else_statements:
                for stmt in node.statements:
                    self.generate_from_node(stmt)
                self.bytecode += f"jump_label _l{self.label_num + 1}\n"
                self.bytecode += f"_l{self.label_num}:\n"
                for stmt in node.else_statements:
                    self.generate_from_node(stmt)
                self.label_num += 1
                self.bytecode += f"_l{self.label_num}:\n"
                self.label_num += 1
            else:
                for stmt in node.statements:
                    self.generate_from_node(stmt)
                self.bytecode += f"_l{self.label_num}:\n"
                self.label_num += 1

    def generate(self, tree:list[parser.Node])->str:
        self.tree = tree
        self.bytecode = ""
        self.label_num = 1
        for node in tree:
            self.generate_from_node(node)
        self.bytecode += "return_value"
        return self.bytecode