import sys
from pathlib import Path

from code_writer import CodeWriter
from parser import CommandType, Parser


def output_path_for(input_path):
    return input_path.with_suffix(".asm")


def translate(input_file):
    input_path = Path(input_file)
    output_path = output_path_for(input_path)

    parser = Parser(input_path)
    code_writer = CodeWriter(output_path, input_path)

    try:
        while parser.hasMoreLines():
            parser.advance()
            command_type = parser.commandType()

            if command_type == CommandType.ARITHMETIC:
                code_writer.writeArithmetic(parser.arg1())
            elif command_type in {CommandType.PUSH, CommandType.POP}:
                code_writer.writePushPop(command_type, parser.arg1(), parser.arg2())
            elif command_type == CommandType.LABEL:
                code_writer.writeLabel(parser.arg1())
            elif command_type == CommandType.GOTO:
                code_writer.writeGoto(parser.arg1())
            elif command_type == CommandType.IF:
                code_writer.writeIf(parser.arg1())
            elif command_type == CommandType.FUNCTION:
                code_writer.writeFunction(parser.arg1(), parser.arg2())
            elif command_type == CommandType.CALL:
                code_writer.writeCall(parser.arg1(), parser.arg2())
            elif command_type == CommandType.RETURN:
                code_writer.writeReturn()
    finally:
        code_writer.close()

    return output_path


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 vm_translator.py input.vm")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if input_path.suffix != ".vm":
        print("Error: input file must have .vm extension")
        sys.exit(1)

    translate(input_path)


if __name__ == "__main__":
    main()
