import sys
import tree_sitter_clarity as tsclar
import tree_sitter as ts

from typing import Generator

# The plan in a nutshell
# Parser the code -> generate an AST -> Walk the tree and generate the equivalent code in cpp

# We create the opaque object that defines how to parse the language
TSCLARITY = ts.Language(tsclar.language())

# The parser creates a TsTree based on the language that we have already defined
ClarityParser = ts.Parser(TSCLARITY)

def traverse_tree(tree: ts.Tree) -> Generator[ts.Node, None, None]:
    cursor = tree.walk()

    visited_children = False
    while True:
        if not visited_children:
            """
            CAMI: Lo dejo de momento

            <HELP> 

            Cuando el intérprete Python encuentra una función que incluye un yield (o varios), 
            entiende que al llamar esta función no obtendremos un valor devuelto con un return, 
            sino que obtendremos un generador (generator). Los generadores son iterables.
            
            """
            yield cursor.node
            if not cursor.goto_first_child():
                visited_children = True
        elif cursor.goto_next_sibling():
            visited_children = False
        elif not cursor.goto_parent():
            break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERROR::WRONG USE. This is the way: ClarityTranspiler path_to_clarity_contract")
        sys.exit(1)
    else:
        filename = sys.argv[1]
        file = open(filename, "r")
        file_content = file.read()
        file.close()

        clarity_tree = ClarityParser.parse(bytes(file_content, "utf8"))
        