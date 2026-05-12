import sys
from pathlib import Path

from code_writer import CodeWriter
from parser import CommandType, Parser


def output_path_for(input_path):
    if input_path.is_dir():
        return input_path / f"{input_path.name}.asm"
    return input_path.with_suffix(".asm")


def vm_files_for(input_path):
    if input_path.is_dir():
        return sorted(input_path.glob("*.vm"))
    return [input_path]


def translate_command(parser, code_writer):
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


def translate(input_file_or_directory):
    input_path = Path(input_file_or_directory)
    output_path = output_path_for(input_path)
    vm_files = vm_files_for(input_path)

    code_writer = CodeWriter(output_path, input_path)

    try:
        for vm_file in vm_files:
            parser = Parser(vm_file)
            code_writer.setFileName(vm_file)

            while parser.hasMoreLines():
                parser.advance()
                translate_command(parser, code_writer)
    finally:
        code_writer.close()

    return output_path


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 vm_translator.py input.vm|input_directory")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print("Error: input path does not exist")
        sys.exit(1)

    if input_path.is_file() and input_path.suffix != ".vm":
        print("Error: input file must have .vm extension")
        sys.exit(1)

    if input_path.is_dir() and not vm_files_for(input_path):
        print("Error: input directory must contain at least one .vm file")
        sys.exit(1)

    translate(input_path)


if __name__ == "__main__":
    main()
