import tokeniser

class Node: pass
class Variable:
    def __init__(self, name:str): self.name = name
class Call:
    def __init__(self, callee, arguments:list): self.callee, self.arguments = callee, arguments
class Assign:
    def __init__(self, name:str, value): self.name, self.value = name, value

class Parser:
    def __init__(self):
        self.tokens = []
        self.tree = []
        self.index = 0

    def peek(self, amount:int=1)->tokeniser.T_Token:
        try:
            return self.tokens[self.index + amount]
        except IndexError:
            return tokeniser.T_End("END")

    def consume(self)->tokeniser.T_Token:
        try:
            return self.tokens[self.index]
        except IndexError:
            return tokeniser.T_End("END")

    def advance(self)->tokeniser.T_Token:
        value = self.consume()
        self.index += 1
        return value

    def parse_expr(self):
        start = self.advance()
        if type(start) == tokeniser.T_Name:
            return Variable(start.value)
        else:
            return start.value

    def parse_call(self)->Call:
        self.index -= 1
        callee = self.parse_expr()
        if type(self.consume()) != tokeniser.T_LeftParen:
            print("error: expected `(`")
            exit(1)
        self.advance()
        arguments = []
        if type(self.consume()) != tokeniser.T_RightParen:
            arguments.append(self.parse_expr())
        while type(self.consume()) != tokeniser.T_RightParen:
            if type(self.consume()) != tokeniser.T_Comma:
                print("error: expected `,`")
                exit(1)
            self.advance()
            if type(self.consume()) == tokeniser.T_RightParen:
                print("error: expected expression")
                exit(1)
            arg = self.parse_expr()
            arguments.append(arg)
        self.advance()
        if type(self.consume()) == tokeniser.T_Newline:
            self.advance()
        return Call(callee, arguments)

    def parse_assign(self)->Assign:
        name:str = self.peek(-1).value
        self.advance()
        if type(self.consume()) in [tokeniser.T_Newline, tokeniser.T_End]:
            print("error: expected expression")
            exit(1)
        value = self.parse_expr()
        if type(self.consume()) == tokeniser.T_Newline:
            self.advance()
        return Assign(name, value)

    def parse_stmt(self)->Node:
        start = self.advance()
        if type(self.consume()) == tokeniser.T_LeftParen:
            return self.parse_call()
        elif type(self.consume()) == tokeniser.T_SingleEquals:
            return self.parse_assign()

    def at_end(self)->bool:
        return type(self.consume()) == tokeniser.T_End

    def parse(self, tokens:list[tokeniser.T_Token])->list[Node]:
        self.tokens = tokens
        self.tree = []
        self.index = 0
        while not self.at_end():
            node = self.parse_stmt()
            self.tree.append(node)
        return self.tree