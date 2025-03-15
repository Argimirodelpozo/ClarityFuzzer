from tree_sitter import Node


def text_as_str(node: Node) -> str:
    return node.text.decode("utf-8")

class Traductor:
    CLAR_TO_CPP = {
        "int": "clarity_int",
        "uint": "clarity_uint",
        "bool": "bool",
        "principal": "principal",
        "map": "clarity_map",
        "const-type": "string",
        "int_lit": "clarity_int",
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
                case "constant_definition": self.clar_const_def(node)
                case "trait_definition": self.clar_trait_def(node)
                case _ : print(node.type)
        
    def cpp_type(self, node: Node | str) -> str:
        if isinstance(node, str):
            return self.CLAR_TO_CPP[node]
        return self.CLAR_TO_CPP[text_as_str(node)]

    def print_program(self) -> str:
        """
        Returns the cpp program as a string
        """

        vars = "\n".join(self.variables)
        funcs = "\n".join(self.functions)

        fm = f"""
class contract_0
{{
    {vars}
    
    {funcs}
}}
        """


        print(fm)

    def __fn_sig_for_trait(self, nodes: list[Node]) -> str:
        """
        (lock (principal uint uint) (response bool uint))

        {"lock", "principal uint uint", "response bool uint"},
        """
        
        traits = []

        for node in nodes:   
            func_name = ""
            args = []   
            response = ""

            for n in node.children:
                if n.type == "identifier":
                    func_name = text_as_str(n)
                    
                if n.type == "parameter_type":
                    args.append(f"\"{text_as_str(n)}\"")
                    
                if n.type == "native_type":
                    response = text_as_str(n)[1:-1]

            cpp_str = f"{{\"{func_name}\", {{{', '.join(args)}}}, \"{response}\"}}"
            traits.append(cpp_str)

        return "{" + ", ".join(traits) + "};" 
    
    def clar_trait_def(self, node: Node) -> str:
        """
        (define-trait locked-wallet-trait
            (
                (lock (principal uint uint) (response bool uint))
                (bestow (principal) (response bool uint))
                (claim () (response bool uint))
            )
        )

        vector<string> locked_wallet_trait[3] = {
                {"lock", "principal uint uint", "response bool uint"},
                {"bestow", "principal", "response bool uint"}, 
                {"claim", "", "response bool uint"}
            };

        """
        # Son los parentesis y demases que hay que restar
        # para obtener la cantidad de funciones definidas en el trait
        FIXED_ITEMS = 6
        name = text_as_str(node.children[2]).replace("-", "_")
        size = len(node.children) - FIXED_ITEMS

        interface = self.__fn_sig_for_trait(node.children[4:-2])
        
        cpp_string = f"std::tuple<string, vector<string>, string> {name}[{size}] = {interface} "
        
        self.variables.append(cpp_string)
        
    def clar_trait_impl(self, node: Node) -> str:
        print("NOT IMPLEMENTED")

    def clar_trait_usage(self, node: Node) -> str:
        print("NOT IMPLEMENTED")

    def clar_token_def(self, node: Node) -> str:
        print("NOT IMPLEMENTED")

    def clar_const_def(self, node: Node) -> str:
        """
        (define-constant (identifier) (value))
        """

        name = text_as_str(node.children[2]).replace("-", "_")

        v = None
        cpp_type = None

        if node.children[3].type == "global":
            v = text_as_str(node.children[3].children[0]).replace("-", "_")
            cpp_type = self.cpp_type("const-type")
        else:
            v = text_as_str(node.children[3])
            cpp_type = self.cpp_type(node.children[3].type)

        cpp_string = f"const {cpp_type} {name} = {v};"
        self.variables.append(cpp_string)
    
    def clar_var(self, node: Node):
        """"
        [(, variable_definition, (identifier), (native_type), (int_lit), )]
        (variable_definition (identifier) (native_type) (int_lit))
        type name = value;
        """

        eq_type = self.cpp_type(node.children[3].children[0])
        name = text_as_str(node.children[2]).replace("-", "_")
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
        name = text_as_str(node.children[2]).replace("-", "_")
        
        cpp_string = f"{map_type}<{key_type}, {value_type}> {name};"

        self.variables.append(cpp_string)

    def clar_fn(self, node: Node) -> str:
        match node.child(0).type:
            case "read_only_function": self.__clar_fn_read_only(node.child(0))
            case _: print("NOT IMPLEMENTED:", node.children[0].type) 

    def __clar_fn_read_only(self, node: Node) -> str:
        for c in node.children:
            print(c.type)

    def clar_fn_call(self, node: Node) -> str:
        print("NOT IMPLEMENTED")


"""
    $.trait_definition, OK
    $.trait_implementation,
    $.trait_usage,
    $.token_definition, 
    $.constant_definition, OK
    $.variable_definition, OK
    $.mapping_definition, OK
    $.function_definition,
    $._function_call,
"""
    

    