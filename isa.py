import json
from enum import Enum

start = 0


class Opcode(Enum):
    LOAD = "load"
    STORE = "store"

    ADD = "add"
    SUB = "sub"
    MUL = "mul"
    DIV = "div"
    REM = "rem"
    INC = "inc"
    DEC = "dec"
    CMP = "cmp"
    MOVH = "movh"

    JMP = "jmp"
    JE = "je"
    JNE = "jne"
    JGE = "jge"

    CALL = "call"
    FUNC = "func"

    IN = "in"
    OUT = "out"
    SIGN = "sign"
    HALT = "halt"


opcode_values = [e.value for e in Opcode]


def write_code(filename, code):
    with open(filename, "w", encoding="utf-8") as file:
        buf = [json.dumps({"_start": start})]
        for instr in code:
            buf.append(json.dumps(instr))
        file.write("[" + ",\n ".join(buf) + "]")


def read_code(filename):
    with open(filename, encoding="utf-8") as file:
        code = json.loads(file.read())
    for instr in code:
        instr["opcode"] = Opcode(instr["opcode"])
    return code
