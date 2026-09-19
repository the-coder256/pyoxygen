import tokeniser

class Node: pass
class Variable:
    def __init__(self, name:str): self.name = name
class Call:
    def __init__(self, callee, arguments:list): self.callee, self.arguments = callee, arguments
class Assign:
    def __init__(self, name:str, value): self.name, self.value = name, value
class IfCondition:         #   v  Look at this long boi  v
    def __init__(self, condition, statements:list, else_statements:list|None): self.condition, self.statements, self.else_statements = condition, statements, else_statements

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

    def advance_newlines(self)->None:
        while type(self.consume()) == tokeniser.T_Newline:
            self.advance()

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
        self.advance_newlines()
        return Call(callee, arguments)

    def parse_assign(self)->Assign:
        name:str = self.peek(-1).value
        self.advance()
        if type(self.consume()) in [tokeniser.T_Newline, tokeniser.T_End]:
            print("error: expected expression")
            exit(1)
        value = self.parse_expr()
        self.advance_newlines()
        return Assign(name, value)

    def parse_if_condition(self)->IfCondition:
        if type(self.consume()) == tokeniser.T_LeftBrace:
            print("error: expected expression")
            exit(1)
        condition = self.parse_expr()
        self.advance_newlines()
        if type(self.consume()) != tokeniser.T_LeftBrace:
            print("error: expected `{`")
            exit(1)
        self.advance()
        self.advance_newlines()
        statements = []
        while type(self.consume()) != tokeniser.T_RightBrace:
            stmt = self.parse_stmt()
            self.advance_newlines()
            if not stmt:
                print("error: invalid statement")    # either that or their stupid ass forgot the right brace
                exit(1)
            statements.append(stmt)
        self.advance()
        self.advance_newlines()
        # try parse else (it may not be there)
        if type(self.consume()) == tokeniser.T_Keyword and self.consume().value == "else":
            else_statements = []
            self.advance()
            self.advance_newlines()
            if type(self.consume()) != tokeniser.T_LeftBrace:
                print("error: expected `{`")
                exit(1)
            self.advance()   # adb 🥹
            self.advance_newlines()
            while type(self.consume()) != tokeniser.T_RightBrace:
                stmt = self.parse_stmt()
                self.advance_newlines()
                if not stmt:
                    print("error: invalid statement")
                    exit(1)
                else_statements.append(stmt)
            self.advance()
            self.advance_newlines()
        else:
            else_statements = None
        return IfCondition(condition, statements, else_statements)

    def parse_stmt(self)->Node:
        start = self.advance()
        if type(self.consume()) == tokeniser.T_LeftParen:
            return self.parse_call()
        elif type(self.consume()) == tokeniser.T_SingleEquals:
            return self.parse_assign()
        elif type(start) == tokeniser.T_Keyword and start.value == "if":
            return self.parse_if_condition()

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