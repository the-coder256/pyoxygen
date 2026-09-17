from sys import argv
import tokeniser, parser, generator

if len(argv) < 2:
    print("error: no input file")
    exit(1)

with open(argv[1], "r") as file:
    content = file.read()

tokens = tokeniser.Tokeniser().tokenise(content)
tree = parser.Parser().parse(tokens)
bytecode = generator.Generator().generate(tree)

with open("output", "w") as file:
    file.write(bytecode)