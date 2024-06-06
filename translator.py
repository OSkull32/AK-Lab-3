import argparse
import re

from isa import Opcode, write_code

start = 0
commands_with_labels = [Opcode.JMP, Opcode.JGE, Opcode.JE, Opcode.JNE, Opcode.CALL, Opcode.FUNC]


def labels_insert(labels, instructions):
    for instr in instructions:
        if "arg" in instr and instr["arg"] in labels:
            instr["arg"] = labels[instr["arg"]]


def labels_parse(labels, line, index):
    split = re.split("\\s*:\\s*", line)
    if split[0] == "_start":
        global start
        start = index
    labels[split[0]] = index
    if split[1] == '':
        return True
    return False


def translator(origin):
    instructions = []
    labels = {}
    index = 0
    for i, line in enumerate(origin):
        line = line.strip()
        line = re.sub("\\s*;.*", "", line)
        if len(line) == 0 or line[0] == ";":
            continue

        if ":" in line:
            if labels_parse(labels, line, index):
                continue

        line = line.split(':', 1)[-1].lstrip()
        split = re.split("(?<!')\\s+(?!=')", line)
        instr = {"index": index, "opcode": split[0]}

        if len(split) > 1:
            try:
                instr["arg"] = int(split[1])
            except ValueError:
                if instr["opcode"] not in commands_with_labels and split[1][0] != '*':
                    instr["arg"] = ord(split[1][1])
                else:
                    instr["arg"] = split[1]
        instructions.append(instr)
        index += 1
    labels_insert(labels, instructions)
    return instructions


def main(code, target_file):
    with open(code, "r") as f:
        code = f.readlines()
    instructions = translator(code)

    write_code(target_file, instructions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_file")
    parser.add_argument("target_file")

    args = parser.parse_args()

    main(args.source_file, args.target_file)
