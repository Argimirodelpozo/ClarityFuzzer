from tree_sitter import Node


def text_as_str(node: Node) -> str:
    return node.text.decode("utf-8")

class Traductor:
    CLAR_TO_CPP = {
        "int": "__int128",
        "uint": "unsigned __int128",
        "bool": "bool",
        "principal": "string",
        "map": "map"
    }
    clar_parsed: list[Node] 
    includes: list[str]
    variables: list[str]
    functions: list[str]  

    def __init__(self, clar_parsed):
        self.includes = []
        self.variables = []
        self.functions = []
        self.clar_parsed = clar_parsed

    def transpile(self) -> str:
        for node in self.clar_parsed:
            match node.type:
                case "variable_definition": self.clar_var(node)
                case "function_definition": self.clar_fn(node)
                case "mapping_definition": self.clar_maps(node)
                case _ : print(node.type)
        
    def cpp_type(self, node: Node | str) -> str:
        if isinstance(node, str):
            return self.CLAR_TO_CPP[node]
        return self.CLAR_TO_CPP[text_as_str(node)]


    def clar_var(self, node: Node):
        """"
        [(, variable_definition, (identifier), (native_type), (int_lit), )]
        (variable_definition (identifier) (native_type) (int_lit))
        type name = value;
        """

        eq_type = self.cpp_type(node.children[3].children[0])
        name = text_as_str(node.children[2])
        val = text_as_str(node.children[4])

        cpp_string = f"{eq_type} {name} = {val};"

        self.variables.append(cpp_string)

    def clar_maps(self, node: Node):
        """
        
        (mapping_definition (identifier) key_type: (native_type) value_type: (native_type))

        map<string, int> people

        """
        
        if "#include <map>" not in self.includes:
            self.includes.append("#include <map>")
        
        map_type = self.cpp_type("map")
        key_type = self.cpp_type(node.children[3].children[0])
        value_type = self.cpp_type(node.children[4].children[0])
        name = text_as_str(node.children[2])
        
        cpp_string = f"{map_type}<{key_type}, {value_type}> {name};"

        self.variables.append(cpp_string)


    def clar_fn(self, clarity_node: Node) -> str:
        print("NOT IMPLEMENTED")

    
    def print_program(self) -> str:
        """
        Returns the cpp program as a string
        """
        print("\n".join(self.includes + self.variables + self.functions))


