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

# A命令かC命令かを判定する
def command_type(command):
    if command.startswith("@"):
        return "A"
    else:
        return "C"

# A命令を変換する
def translate_a_instruction(command):
    value = int(command[1:])
    return format(value, "016b")

# C命令を分解する
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

# C命令をバイナリに変換する
def translate_c_instruction(command):
    dest, comp, jump = parse_c_instruction(command)
    return "111" + COMP[comp] + DEST[dest] + JUMP[jump]

# 1つの .asm ファイル全体を変換する
def assemble_basic(lines):
    result = []

    for raw_line in lines:
        command = clean_line(raw_line)

        if command == "":
            continue

        if command_type(command) == "A":
            binary = translate_a_instruction(command)
        else:
            binary = translate_c_instruction(command)

        result.append(binary)

    return result


def main():
    asm_path = Path(sys.argv[1])
    hack_path = asm_path.with_suffix(".hack")

    lines = asm_path.read_text(encoding="utf-8").splitlines()
    binary_lines = assemble_basic(lines)

    hack_path.write_text("\n".join(binary_lines), encoding="utf-8")

# このファイルが直接実行されたときだけ、main() を動かす
if __name__ == "__main__":
    main()