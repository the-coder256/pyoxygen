class T_Token:
    def __init__(self, value): self.value = value
class T_Integer:
    def __init__(self, value): self.value = int(value)
class T_Float:
    def __init__(self, value): self.value = float(value)
class T_String:
    def __init__(self, value): self.value = value[1:]
class T_Name:
    def __init__(self, value): self.value = value
class T_Keyword:
    def __init__(self, value): self.value = value
class T_Newline:
    def __init__(self, value): self.value = value
class T_End:
    def __init__(self, value): self.value = value
class T_LeftParen:
    def __init__(self, value): self.value = value
class T_RightParen:
    def __init__(self, value): self.value = value
class T_SingleEquals:
    def __init__(self, value): self.value = value
class T_Comma:
    def __init__(self, value): self.value = value
class T_LeftBrace:
    def __init__(self, value): self.value = value
class T_RightBrace:
    def __init__(self, value): self.value = value

keywords = [
    "if", "else"
]

class Tokeniser:
    def __init__(self):
        self.content = ""
        self.tokens = []
        self.curr_tok = ""
        self.index = 0

    def peek(self, amount:int = 1)->str:    # idk if i need this
        try:
            return self.content[self.index + amount]
        except IndexError:
            return ""

    def consume(self)->str:
        try:
            return self.content[self.index]
        except IndexError:
            return ""

    def advance(self)->str:
        value = self.consume()
        self.index += 1
        return value

    def create_token(self, value:str)->T_Token:
        t_type:type = T_Token
        if value == "\n":
            t_type = T_Newline
        elif value == "(":
            t_type = T_LeftParen
        elif value == ")":
            t_type = T_RightParen
        elif value == "=":
            t_type = T_SingleEquals
        elif value == ",":
            t_type = T_Comma
        elif value == "{":
            t_type = T_LeftBrace    # does anyone even read this code?
        elif value == "}":
            t_type = T_RightBrace   # probably not (it may be just me for now and forever)
        elif value[0] in ["'", '"']:
            t_type = T_String
        elif value in keywords:
            t_type = T_Keyword
        else:
            try:
                x = float(value)
                if value.count(".") == 0:
                    t_type = T_Integer
                else:
                    t_type = T_Float
            except ValueError:
                t_type = T_Name
        return t_type(value)

    def append_token(self, extra:str|None=None)->None:
        if self.curr_tok:
            self.tokens.append(self.create_token(self.curr_tok))
            self.curr_tok = ""
        if extra:
            self.tokens.append(self.create_token(extra))

    def at_end(self)->bool:
        return len(self.consume()) == 0

    def tokenise(self, content:str)->list[T_Token]:
        self.content = content
        self.tokens = []
        self.curr_tok = ""
        self.index = 0
        in_comment = 0
        in_string = 0
        string_char = ""
        while not self.at_end():
            char = self.advance()
            if char == "\n":
                self.append_token("\n")
                in_comment = 0
            elif char == "/" and self.consume() == "/":
                self.advance()
                in_comment = 1
            elif char in ["'", '"'] and not in_string:
                self.curr_tok += char
                in_string = 1
                string_char = char
            elif char == string_char and in_string:
                in_string = 0
            elif in_string:
                self.curr_tok += char
            elif char in [" ", "\t"]:
                self.append_token()
            elif char == "(":
                self.append_token("(")
            elif char == ")":
                self.append_token(")")
            elif char == "=":
                self.append_token("=")
            elif char == ",":
                self.append_token(",")
            elif char == "{":
                self.append_token("{")
            elif char == "}":
                self.append_token("}")
            else:
                self.curr_tok += char
        self.append_token()
        self.tokens.append(T_End("END"))
        return self.tokens