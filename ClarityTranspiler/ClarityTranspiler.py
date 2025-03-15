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

class NodeIterator:
    root_node: ts.Node
    cursor: ts.TreeCursor
    visited = []

    def __init__(self, node: ts.Node):
        self.root_node = node
        self.cursor = node.walk()
        self.visited = []

        while self.cursor.goto_first_child():
            pass

    def next(self) -> ts.Node | None:
        while True:
            node = self.node()

            if node not in self.visited:
                if self.cursor.goto_first_child():
                    continue
                self.visited.append(node)
                return node

            if self.cursor.goto_next_sibling():
                while self.cursor.goto_first_child():
                    pass
            else:

                if not self.cursor.goto_parent():
                    return None
                parent_node = self.cursor.node
                self.visited.append(parent_node)
                return parent_node

    def node(self) -> ts.Node | None:
        return self.cursor.node

    def __iter__(self):
        return self

    def __next__(self) -> ts.Node | None:
        node = self.next()
        if node is None:
            raise StopIteration
        return node



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
        root_node = clarity_tree.root_node
        iterator = NodeIterator(root_node)
        
        cpp_out = ""

        for node in iterator:
            print(node.type)
