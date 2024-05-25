import argparse
from typing import Any

from op import INP_PORT, OUT_PORT
from utils import write_code


def get_meaningful_token(line: str) -> str:
    return line.split(";", 1)[0].strip()


def make_instr(index: int, opcode: str, arg: Any):
    return {"index": index, "opcode": opcode, "arg": arg}


def translate_stage_1(text: str):
    variables = {}
    labels = {}

    code = []
    data = [make_instr(0, "INT", 0), make_instr(1, "INT", 0)]  # input and output

    data_stage = True

    for line in text.splitlines():
        token = get_meaningful_token(line)

        if token == "" or token == ".data:":
            continue
        if token == ".code:":
            data_stage = False
            continue

        if data_stage:
            opcode, variable, arg = token.split(" ", 2)
            variables[variable] = len(data)
            if opcode == "INT":
                data += [make_instr(len(data), opcode, int(arg))]
            elif opcode == "STR":
                for c in arg.strip('"'):
                    data += [make_instr(len(data), opcode, ord(c))]
                data += [make_instr(len(data), opcode, 0)]
            elif opcode == "BUF":
                num = int(arg)
                for c in range(num):
                    data += [make_instr(len(data), opcode, 0)]
        else:
            if token.endswith(":"):  # label
                labels[token.strip(":")] = len(code)
            else:
                if " " in token:  # instruction with argument
                    sub_tokens = token.split(" ")
                    code += [make_instr(len(code), sub_tokens[0], sub_tokens[1])]
                else:  # instruction without argument
                    if token == "INP":
                        code += [make_instr(len(code), "LOAD", INP_PORT)]
                    elif token == "OUT":
                        code += [make_instr(len(code), "SAVE", OUT_PORT)]
                    else:
                        code += [make_instr(len(code), token, None)]

    return labels, variables, code, data


def translate_stage_2(labels: dict, variables: dict, code: list):
    for ind, token in enumerate(code):
        arg = token["arg"]
        if isinstance(arg, int) or arg is None:
            continue
        if isinstance(arg, str) and (arg.isnumeric() or arg[1:].isnumeric()):
            token["arg"] = int(arg)
        else:
            if arg in labels:
                token["arg"] = labels[arg]
            else:
                token["arg"] = variables[arg]
    return code


def translate(text: str):
    labels, variables, code, data = translate_stage_1(text)

    for d in data:
        d["index"] += len(code)
    for k in variables.keys():
        variables[k] += len(code)

    code = translate_stage_2(labels, variables, code)

    return code + data


def main(source: str, target: str):
    with open(source, "r") as f:
        text = f.read()
    code = translate(text)
    write_code(target, code)
    print("LoC:", len(text.split("\n")), "Instr:", len(code))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Трансляция кода")
    parser.add_argument("source_file", help="Имя файла с кодом")
    parser.add_argument("target_file", help="Имя выходного файла")

    args = parser.parse_args()

    main(args.source_file, args.target_file)
