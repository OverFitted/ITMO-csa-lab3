import argparse
import logging

import microprogram
from control_unit import ControlUnit
from datapath import DataPath
from utils import read_code


def simulation(
    code: list,
    microprogram: list,
    input_buffer: list,
    debug_limit: int,
    limit: int,
):
    datapath = DataPath(code, input_buffer)
    control_unit = ControlUnit(code, microprogram, datapath)

    instructions = 0
    try:
        while control_unit.cur_tick() < limit:
            if control_unit.mpc_reg == 0:
                instructions += 1

            control_unit.decode_and_execute()
            if control_unit.cur_tick() < debug_limit:
                logging.debug(control_unit)
            elif control_unit.cur_tick() == debug_limit:
                logging.warning("Debug limit exceeded!")
    except StopIteration:
        pass

    if control_unit.cur_tick() >= limit:
        logging.warning("Limit exceeded!")
        pass

    output = "".join(
        map(lambda x: chr(x) if x < 256 else str(x), datapath.output_buffer)
    )
    logging.info(f"output_buffer: {output}")

    return output, instructions, control_unit.cur_tick()


def main(code_file: str, input_file: str, debug_limit: int, limit: int):
    machine_code = read_code(code_file)
    if input_file is None:
        input_buffer = []
    else:
        with open(input_file, "r") as f:
            input_buffer = list(f.read()) + [chr(0)]

    logging.info("Start simulation")
    output, instructions, ticks = simulation(
        machine_code, microprogram.memory, input_buffer, debug_limit, limit
    )
    logging.info("End simulation")

    print(output)
    print(f"Instructions: {instructions} Ticks: {ticks}")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)  # DEBUG | INFO

    parser = argparse.ArgumentParser(description="Симуляция процессора")
    parser.add_argument("code_file", help="Имя файла бинарным с кодом")
    parser.add_argument(
        "input_file", nargs="?", help="Имя входного файла (опционально)"
    )
    parser.add_argument(
        "--debug_limit", type=int, default=200, help="Лимит отладки (по умолчанию 200)"
    )
    parser.add_argument(
        "--limit", type=int, default=100000, help="Лимит тиков (по умолчанию 100000)"
    )
    args = parser.parse_args()

    main(
        args.code_file,
        args.input_file,
        args.debug_limit,
        args.limit,
    )
