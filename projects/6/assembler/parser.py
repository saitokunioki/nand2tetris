import sys


A_COMMAND = "A_COMMAND"
C_COMMAND = "C_COMMAND"
L_COMMAND = "L_COMMAND"


class Parser:
    def __init__(self, input_file=None):
        if input_file is None:
            input_file = sys.argv[1]

        file = open(input_file, "r")
        lines = file.readlines()
        file.close()

        self.commands = []

        for line in lines:
            command = self.clean_line(line)

            if command != "":
                self.commands.append(command)

        self.current_command = None
        self.current_index = -1

    # 1行からコメントと空白を取り除く
    def clean_line(self, line):
        command = line.split("//")[0]
        command = command.strip()
        command = command.replace(" ", "")

        return command

    # 入力にまだ命令があるか？
    def hasMoreLines(self):
        next_index = self.current_index + 1
        return next_index < len(self.commands)

    # 次の命令を現在の命令にする
    def advance(self):
        if self.hasMoreLines():
            self.current_index = self.current_index + 1
            self.current_command = self.commands[self.current_index]

    # 現在の命令の種類を返す
    def instructionType(self):
        if self.current_command.startswith("@"):
            return A_COMMAND
        elif self.current_command.startswith("(") and self.current_command.endswith(")"):
            return L_COMMAND
        else:
            return C_COMMAND

    # A命令またはL命令のシンボルを返す
    def symbol(self):
        if self.instructionType() == A_COMMAND:
            return self.current_command[1:]
        elif self.instructionType() == L_COMMAND:
            return self.current_command[1:-1]
        else:
            return None

    # C命令のdest部分を返す
    def dest(self):
        if "=" in self.current_command:
            parts = self.current_command.split("=")
            return parts[0]
        else:
            return None

    # C命令のcomp部分を返す
    def comp(self):
        command = self.current_command

        if "=" in command:
            parts = command.split("=")
            command = parts[1]

        if ";" in command:
            parts = command.split(";")
            command = parts[0]

        return command

    # C命令のjump部分を返す
    def jump(self):
        if ";" in self.current_command:
            parts = self.current_command.split(";")
            return parts[1]
        else:
            return None
