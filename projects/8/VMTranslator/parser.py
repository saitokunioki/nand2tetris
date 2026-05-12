# 辞書
ARITHMETIC_COMMANDS = [
    "add",
    "sub",
    "neg",
    "eq",
    "gt",
    "lt",
    "and",
    "or",
    "not",
]

# 定数
class CommandType:
    ARITHMETIC = "C_ARITHMETIC"
    PUSH = "C_PUSH"
    POP = "C_POP"
    LABEL = "C_LABEL"
    GOTO = "C_GOTO"
    IF = "C_IF"
    FUNCTION = "C_FUNCTION"
    CALL = "C_CALL"
    RETURN = "C_RETURN"


C_ARITHMETIC = CommandType.ARITHMETIC
C_PUSH = CommandType.PUSH
C_POP = CommandType.POP
C_LABEL = CommandType.LABEL
C_GOTO = CommandType.GOTO
C_IF = CommandType.IF
C_FUNCTION = CommandType.FUNCTION
C_CALL = CommandType.CALL
C_RETURN = CommandType.RETURN

class Parser:
    '''このモジュールは、1つの.vmファイルの解析を行う。'''
    def __init__(self, input_file):
        '''入力ファイル/ストリームを開き、パースを行う準備をする。'''
        
        with open(input_file, "r", encoding="UTF-8") as file:
            lines = file.readlines()

        self.commands = []

        for line in lines:
            command = self.clean_line(line)

            if command != "":
                self.commands.append(command)
        
        self.current_command = None
        self.current_index = -1
    
    def clean_line(self, line):
        command = line.split("//")[0]
        command = command.strip()
        return command

    def hasMoreLines(self):
        '''入力にさらに行があるか？'''
        next_index = self.current_index + 1
        return next_index < len(self.commands)
    
    def commandType(self):
        '''現在のコマンドの種類を表す定数を返す。
        算術/論理コマンドはC_ARITHMETICが返される。
        '''
        command_name = self.current_command.split()[0]

        if command_name in ARITHMETIC_COMMANDS:
            return CommandType.ARITHMETIC
        elif command_name == "push":
            return CommandType.PUSH
        elif command_name == "pop":
            return CommandType.POP
        elif command_name == "label":
            return CommandType.LABEL
        elif command_name == "goto":
            return CommandType.GOTO
        elif command_name == "if-goto":
            return CommandType.IF
        elif command_name == "function":
            return CommandType.FUNCTION
        elif command_name == "call":
            return CommandType.CALL
        elif command_name == "return":
            return CommandType.RETURN

    def advance(self):
        '''入力から次のコマンドを読み、それを現在のコマンドとする。
        hasMoreLinesがtrueの場合にのみ、本ルーチンを呼ぶようにする。
        最初は現在のコマンドは空である。
        '''
        if self.hasMoreLines():
            self.current_index = self.current_index + 1
            self.current_command = self.commands[self.current_index]

    def arg1(self):
        '''現在のコマンドの最初の引数が返される。
        C_ARITHMETICの場合、コマンド自体が返される。
        現在のコマンドがC_RETURNの場合、本ルーチンは呼ばないようにする。
        '''
        if self.commandType() != CommandType.RETURN:
            if self.commandType() == CommandType.ARITHMETIC:
                return self.current_command.split()[0]
            else:
                return self.current_command.split()[1]
    
    def arg2(self):
        '''現在のコマンドの2番目の引数が返される。
        現在のコマンドがC_PUSH、C_POP,C_FUNCTION、C_CALLの場合にのみ
        本ルーチンを呼ぶようにする。
        '''
        if self.commandType() in {
            CommandType.PUSH,
            CommandType.POP,
            CommandType.FUNCTION,
            CommandType.CALL
            }:
            return int(self.current_command.split()[2])
