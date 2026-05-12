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
C_ARITHMETIC = "C_ARITHMETIC"
C_PUSH = "C_PUSH"
C_POP = "C_POP"
C_LABEL = "C_LABEL"
C_GOTO = "C_GOTO"
C_IF = "C_IF"
C_FUNCTION = "C_FUNCTION"
C_CALL = "C_CALL"
C_RETURN = "C_RETURN"

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
            return C_ARITHMETIC
        elif command_name == "push":
            return C_PUSH
        elif command_name == "pop":
            return C_POP
        elif command_name == "label":
            return C_LABEL
        elif command_name == "goto":
            return C_GOTO
        elif command_name == "if-goto":
            return C_IF
        elif command_name == "function":
            return C_FUNCTION
        elif command_name == "call":
            return C_CALL
        elif command_name == "return":
            return C_RETURN

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
        if self.commandType() != C_RETURN:
            if self.commandType() == C_ARITHMETIC:
                return self.current_command.split()[0]
            else:
                return self.current_command.split()[1]
    
    def arg2(self):
        '''現在のコマンドの2番目の引数が返される。
        現在のコマンドがC_PUSH、C_POP,C_FUNCTION、C_CALLの場合にのみ
        本ルーチンを呼ぶようにする。
        '''
        if self.commandType() in {
            C_PUSH,
            C_POP,
            C_FUNCTION,
            C_CALL
            }:
            return self.current_command.split()[2]
