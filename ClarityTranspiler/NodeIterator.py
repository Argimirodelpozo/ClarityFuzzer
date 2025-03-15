
import tree_sitter as ts

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


