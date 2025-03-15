def generate_list(max_len:int, entry_type:str):

    pass

def generate_read_only(function_name, function_args, function_body):
    out:str = function_name + ""
    pass




def parse_contract(filename:str):
    # Parses the given contract
    # Returns a list of parsed lines
    l = []
    with open(filename, 'r') as f:
        for line in f:
            #Strip away comments.
            #Then, separate all ';' finished lines
            #   (if there were any) into distinct
            #   program lines.

            #TODO: agarrar el "https://..."", o sea, el // cuando esta adentro de ""
            # esta solucion es hacky y solo sirve para este contrato
            if line.count("http") == 0:
                lines = line.split("//")[0].split(';')
            else:
                lines = [line]

            for k in lines:
                op = k.split()
                if len(op) > 0:
                    l.append(op)
    return l


def unsupported_opcode(l:str):
    return "//UNSUPPORTED OPCODE "+l[0]+'\n'


def transpile_contract(parsed_contract:str):
    transpiled_out = ""
    callsub_n = 0

    for l in parsed_contract:
        if len(l) == 1:
            # zero argument opcodes
            if l[0] == "app_global_put":
                transpiled_out += "app_global_put(s);\n"
            elif l[0] == "app_global_get":
                transpiled_out += "app_global_get(s);\n"
            elif l[0] == "len":
                transpiled_out += "len(s);\n"
            elif l[0] == "==":
                transpiled_out += "bool_eq(s);\n"
            elif l[0] == "!=":
                transpiled_out += "bool_neq(s);\n"
            elif l[0] == "<":
                transpiled_out += "bool_lt(s);\n"
            elif l[0] == ">":
                transpiled_out += "bool_gt(s);\n"
            elif l[0] == "<=":
                transpiled_out += "bool_leq(s);\n"
            elif l[0] == ">=":
                transpiled_out += "bool_geq(s);\n"
            elif l[0] == "&&":
                transpiled_out += "bool_and(s);\n"
            elif l[0] == "||":
                transpiled_out += "bool_or(s);\n"
            elif l[0] == "+":
                transpiled_out += "add(s);\n"
            elif l[0] == "-":
                transpiled_out += "sub(s);\n"
            elif l[0] == "*":
                transpiled_out += "mul(s);\n"
            elif l[0] == "/":
                transpiled_out += "div(s);\n"
            elif l[0] == "%":
                transpiled_out += "mod(s);\n"
            elif l[0] == "assert":
                transpiled_out += "avm_assert(s);\n"
            elif l[0] == "log":
                transpiled_out += "avm_log(s);\n"
            elif l[0] == "btoi":
                transpiled_out += "btoi(s);\n"
            elif l[0] == "err":
                transpiled_out += "err();\n"
            elif l[0] == "dup":
                transpiled_out += "dup(s);\n"
            elif l[0][-1] == ":":
                # its a tag
                transpiled_out += l[0]+"\n"
            elif l[0][0:5] == "intc_":
                split = l[0].split('_')
                transpiled_out += "s.push(ctx.intcblock[%s]);\n" % split[1]
            elif l[0] == "retsub":
                pass
            else:
                transpiled_out += unsupported_opcode(l)
        elif len(l) == 2:
            #single argument opcodes
            if l[0] == "pushint":
                transpiled_out += "pushint(s, %s);\n" % l[1]
            elif l[0] == "pushbytes":
                transpiled_out += "pushbytes(s, %s);\n" % l[1]
            elif l[0] == "b":
                transpiled_out += "goto %s;\n" % l[1]
            elif l[0] == "bz":
                transpiled_out += "if(s.top().value == 0) goto %s;\n" % l[1]
            elif l[0] == "bnz":
                transpiled_out += "if(s.top().value != 0) goto %s;\n" % l[1]
            elif l[0] == "callsub":
                transpiled_out += "ctx.CallsubStack.push_back(%d);\n" % callsub_n
                transpiled_out += "goto %s;\n" % l[1]
                transpiled_out += "callsub_%d:\n" % callsub_n
                callsub_n += 1
            elif l[0] == "load":
                transpiled_out += "load(s, %s);\n" % l[1]
            elif l[0] == "store":
                transpiled_out += "store(s, %s);\n" % l[1]
            else:
                transpiled_out += unsupported_opcode(l)
        elif len(l) == 3:
            if l[0] == "#pragma":
                #For now, we ignore the pragma directive.
                #Maybe we should save it as a constant somehwere.
                pass
            elif l[0] == "#define":
                transpiled_out += "#define %s %s\n" % (l[1], l[2])
                #Ver si esto funca asi. 
                #En particular esa cosa en hexa no se si esta bien definida en cpp.
            elif l[0] == "txna":
                if l[1] == "ApplicationArgs":
                    transpiled_out += "txna_ApplicationArgs(s, %s);\n" % l[2]
                else:
                    transpiled_out += unsupported_opcode(l)

            else:
                transpiled_out += unsupported_opcode(l)
        else:
            transpiled_out += unsupported_opcode(l)
        
    return transpiled_out


def write_fuzzAVM(contract_paths:[str]):
    with open('FuzzAVM.generated.cpp', 'w') as f:
        with open('AVMFuzz/FuzzAVM_template.cpp', 'r') as template:
            print(template.read(), file=f)
            # for l in template:
            #     print(l, file=f)

        for i, path in enumerate(contract_paths):
            parsed_contract = parse_contract(path)
            out = transpile_contract(parsed_contract)
            print("inline void contract_%d(Stack& s){\n" % i, file=f)
            print(out, file=f)
            print("}", file=f)


# parsed_contract = parse_contract("wormhole/algorand/teal/core_approve.teal")
# parsed_contract = parse_contract("tinyman-consensus-staking/contracts/talgo/build/talgo_approval.teal")
# out = transpile_contract(parsed_contract)

# write_fuzzAVM(["tinyman-consensus-staking/contracts/talgo/build/talgo_approval.teal"])
write_fuzzAVM(["TEALexample.teal"])

# with open('talgo_approval.generated.cpp', 'w') as f:
#     print(out, file=f)  # Python 3.x