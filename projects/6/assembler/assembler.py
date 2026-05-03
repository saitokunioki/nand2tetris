import sys

import code
import parser
import symbol_table


FIRST_VARIABLE_ADDRESS = 16


def predefined_symbols():
    symbols = symbol_table.SymbolTable()

    symbols.addEntry("SP", 0)
    symbols.addEntry("LCL", 1)
    symbols.addEntry("ARG", 2)
    symbols.addEntry("THIS", 3)
    symbols.addEntry("THAT", 4)
    symbols.addEntry("SCREEN", 16384)
    symbols.addEntry("KBD", 24576)

    for i in range(16):
        symbols.addEntry("R" + str(i), i)

    return symbols


def first_pass(input_file):
    symbols = predefined_symbols()
    asm_parser = parser.Parser(input_file)
    rom_address = 0

    while asm_parser.hasMoreLines():
        asm_parser.advance()
        command_type = asm_parser.instructionType()

        if command_type == parser.L_COMMAND:
            label = asm_parser.symbol()
            symbols.addEntry(label, rom_address)
        else:
            rom_address = rom_address + 1

    return symbols


def symbol_address(symbol, symbols, next_variable_address):
    if symbol.isdigit():
        address = int(symbol)
    else:
        if not symbols.contains(symbol):
            symbols.addEntry(symbol, next_variable_address)
            next_variable_address = next_variable_address + 1

        address = symbols.getAddress(symbol)

    return address, next_variable_address


def translate_a_command(asm_parser, symbols, next_variable_address):
    symbol = asm_parser.symbol()
    address, next_variable_address = symbol_address(
        symbol,
        symbols,
        next_variable_address,
    )
    binary = format(address, "016b")
    return binary, next_variable_address


def translate_c_command(asm_parser):
    comp_bits = code.comp(asm_parser.comp())
    dest_bits = code.dest(asm_parser.dest())
    jump_bits = code.jump(asm_parser.jump())

    return "111" + comp_bits + dest_bits + jump_bits


def assemble(input_file):
    symbols = first_pass(input_file)
    asm_parser = parser.Parser(input_file)
    next_variable_address = FIRST_VARIABLE_ADDRESS
    binary_lines = []

    while asm_parser.hasMoreLines():
        asm_parser.advance()
        command_type = asm_parser.instructionType()

        if command_type == parser.A_COMMAND:
            binary, next_variable_address = translate_a_command(
                asm_parser,
                symbols,
                next_variable_address,
            )
            binary_lines.append(binary)

        elif command_type == parser.C_COMMAND:
            binary = translate_c_command(asm_parser)
            binary_lines.append(binary)

        elif command_type == parser.L_COMMAND:
            pass

    return binary_lines


def output_file_name(input_file):
    if input_file.endswith(".asm"):
        return input_file[:-4] + ".hack"
    else:
        return input_file + ".hack"


def write_file(output_file, lines):
    file = open(output_file, "w")
    file.write("\n".join(lines))
    file.close()


def main():
    if len(sys.argv) != 2:
        print("使い方: python assembler.py Xxx.asm")
        return

    input_file = sys.argv[1]
    output_file = output_file_name(input_file)

    binary_lines = assemble(input_file)
    write_file(output_file, binary_lines)


if __name__ == "__main__":
    main()
