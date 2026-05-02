from pathlib import Path
import sys


DEST = {
    None: "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111",
}


JUMP = {
    None: "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}


COMP = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "M": "1110000",
    "!D": "0001101",
    "!A": "0110001",
    "!M": "1110001",
    "-D": "0001111",
    "-A": "0110011",
    "-M": "1110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "M-1": "1110010",
    "D+A": "0000010",
    "D+M": "1000010",
    "D-A": "0010011",
    "D-M": "1010011",
    "A-D": "0000111",
    "M-D": "1000111",
    "D&A": "0000000",
    "D&M": "1000000",
    "D|A": "0010101",
    "D|M": "1010101",
}

# 1行をきれいにする
def clean_line(line):
    return line.split("//")[0].strip().replace(" ", "")

# A命令かC命令かラベル命令か判別する
def command_type(command):
    if command.startswith("@"):
        return "A"
    elif command.startswith("(") and command.endswith(")"):
        return "L"
    else:
        return "C"

# 定義済みシンボルを用意する
def predefined_symbols():
    symbols = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "KBD": 24576,
    }

    for i in range(16):
        symbols[f"R{i}"] = i

    return symbols

# ラベル名を取り出す関数
def label_symbol(command):
    return command[1:-1]

# 第1パスを作る（ラベルだけを登録する）
def first_pass(lines):
    symbols = predefined_symbols()
    rom_address = 0

    for raw_line in lines:
        command = clean_line(raw_line)

        if command == "":
            continue

        kind = command_type(command)

        if kind == "L":
            label = label_symbol(command)
            symbols[label] = rom_address
        else:
            rom_address += 1

    return symbols

# C命令を分解する（基本版と同じ）
def parse_c_instruction(command):
    dest = None
    jump = None

    if "=" in command:
        dest, command = command.split("=")

    if ";" in command:
        comp, jump = command.split(";")
    else:
        comp = command

    return dest, comp, jump

# C命令をバイナリに変換する（基本版と同じ）
def translate_c_instruction(command):
    dest, comp, jump = parse_c_instruction(command)
    return "111" + COMP[comp] + DEST[dest] + JUMP[jump]

# A命令の変換（シンボル対応）
def translate_a_instruction(command, symbols, next_variable_address):
    symbol = command[1:]

    if symbol.isdigit():
        address = int(symbol)
    else:
        if symbol not in symbols:
            symbols[symbol] = next_variable_address
            next_variable_address += 1

        address = symbols[symbol]

    binary = format(address, "016b")

    return binary, next_variable_address

#第2パス（バイナリ作成）
def assemble_full(lines):
    symbols = first_pass(lines)
    next_variable_address = 16
    result = []

    for raw_line in lines:
        command = clean_line(raw_line)

        if command == "":
            continue

        kind = command_type(command)

        if kind == "L":
            continue

        if kind == "A":
            binary, next_variable_address = translate_a_instruction(
                command,
                symbols,
                next_variable_address,
            )
        else:
            binary = translate_c_instruction(command)

        result.append(binary)

    return result


def main():
    if len(sys.argv) != 2:
        print("使い方: python assembler.py Xxx.asm")
        sys.exit(1)

    asm_path = Path(sys.argv[1])
    hack_path = asm_path.with_suffix(".hack")

    lines = asm_path.read_text(encoding="utf-8").splitlines()
    binary_lines = assemble_full(lines)

    hack_path.write_text("\n".join(binary_lines), encoding="utf-8")


if __name__ == "__main__":
    main()