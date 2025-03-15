import sys
import tree_sitter_clarity as tsclar
import tree_sitter as ts
from typing import Generator
import types_systems as traductor
from colors import TerminalColors

# The plan in a nutshell
# Parser the code -> generate an AST -> Walk the tree and generate the equivalent code in cpp

# We create the opaque object that defines how to parse the language
TSCLARITY = ts.Language(tsclar.language())

# The parser creates a TsTree based on the language that we have already defined
ClarityParser = ts.Parser(TSCLARITY)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("ERROR::WRONG USE. This is the way: ClarityTranspiler path_to_clarity_contract")
        sys.exit(1)
    else:
        filename = sys.argv[1]
        dbg = sys.argv[2]
        
        file = open(filename, "r")
        file_content = file.read()
        file.close()
     
        clarity_tree = ClarityParser.parse(bytes(file_content, "utf8"))
        root_node = clarity_tree.root_node
        
        tree_cursor = root_node.walk()
        tree_cursor.goto_first_child()
        arr = []

        while True:
            arr.append(tree_cursor.node)
            if not tree_cursor.goto_next_sibling():
                break

        
        program = traductor.Traductor(arr)

        program.transpile()
        
        if dbg == "1":
            print(f"{TerminalColors.PINK}Transpilation finished.{TerminalColors.ENDC}")
            print(f"{TerminalColors.PINK}Original program:{TerminalColors.ENDC}")
            print(file_content)
            print(f"{TerminalColors.PINK}Transpiled program:{TerminalColors.ENDC}")
            
            
            program.print_program()