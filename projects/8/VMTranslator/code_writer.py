from pathlib import Path

class CodeWriter:
    '''このモジュールは、Parserによって解析されたVMコードを
    Hackアセンブリコードへと変換する
    '''
    def __init__(self, output_file, input_path):
        '''出力ファイル/ストリームを開き、書き込む準備を行う。
        プログラムの実行を開始するブートストラップコードを実現するアセンブリ命令を書く。
        このコードは、生成された出力ファイル/ストリームの先頭に配置されなければならない。
        '''
        self.file = open(output_file, "w", encoding="UTF-8")
        self.file_name = None
        
        self.file_name = Path(input_path).stem
        
        self.label_count = 0
    
    def setFileName(self, filename: str):
        '''新しいVMファイルの変換が開始されたことを知らせる（VMTranslatorによって呼び出される）。
        '''

    def writeArithmetic(self, command: str):
        '''算術論値コマンドのcommandに対応するアセンブリコードを
        出力ファイルに書き込む
        '''
        if command == "add":
            '''x+y'''
            self.file.write("@SP\n")
            self.file.write("AM=M-1\n")
            self.file.write("D=M\n")
            self.file.write("A=A-1\n")
            self.file.write("M=D+M\n")

        elif command == "sub":
            '''x-y'''
            self.file.write("@SP\n")
            self.file.write("AM=M-1\n")
            self.file.write("D=M\n")
            self.file.write("A=A-1\n")
            self.file.write("M=M-D\n")
        
        elif command == "neg":
            '''-y'''
            self.file.write("@SP\n")
            self.file.write("A=M-1\n")
            self.file.write("M=-M\n")

        elif command in ("eq", "gt", "lt"):
            self.writeComparison(command)

        elif command == "and":
            '''x And y'''
            self.file.write("@SP\n")
            self.file.write("AM=M-1\n")
            self.file.write("D=M\n")
            self.file.write("A=A-1\n")
            self.file.write("M=D&M\n")
        
        elif command == "or":
            '''x Or y'''
            self.file.write("@SP\n")
            self.file.write("AM=M-1\n")
            self.file.write("D=M\n")
            self.file.write("A=A-1\n")
            self.file.write("M=D|M\n")
        
        elif command == "not":
            '''Not y'''
            self.file.write("@SP\n")
            self.file.write("A=M-1\n")
            self.file.write("M=!M\n")

    def writeComparison(self, command):
        jumps = {
            "eq": "JEQ",
            "gt": "JGT",
            "lt": "JLT",
        }

        jump = jumps[command]
        true_label = f"{command.upper()}_TRUE{self.label_count}"
        end_label = f"{command.upper()}_END{self.label_count}"
        self.label_count += 1

        self.file.write("@SP\n")
        self.file.write("AM=M-1\n")
        self.file.write("D=M\n")
        self.file.write("A=A-1\n")
        self.file.write("D=M-D\n")
        self.file.write(f"@{true_label}\n")
        self.file.write(f"D;{jump}\n")
        self.file.write("@SP\n")
        self.file.write("A=M-1\n")
        self.file.write("M=0\n")
        self.file.write(f"@{end_label}\n")
        self.file.write("0;JMP\n")
        self.file.write(f"({true_label})\n")
        self.file.write("@SP\n")
        self.file.write("A=M-1\n")
        self.file.write("M=-1\n")
        self.file.write(f"({end_label})\n")
    
    def writePushPop(self, command, segment: str, index: int):
        '''pushまたはpopのcommandに対応するアセンブリコードを
        出力ファイルに書き込む
        '''

        if command == "C_PUSH":
            if segment == "local":
                self.file.write("@LCL\n")
                self.file.write("D=M\n")
                self.file.write(f"@{index}\n")
                self.file.write("A=D+A\n")
                self.file.write("D=M\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")
            if segment == "argument":
                self.file.write("@ARG\n")
                self.file.write("D=M\n")
                self.file.write(f"@{index}\n")
                self.file.write("A=D+A\n")
                self.file.write("D=M\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")
            if segment == "this":
                self.file.write("@THIS\n")
                self.file.write("D=M\n")
                self.file.write(f"@{index}\n")
                self.file.write("A=D+A\n")
                self.file.write("D=M\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")
            if segment == "that":
                self.file.write("@THAT\n")
                self.file.write("D=M\n")
                self.file.write(f"@{index}\n")
                self.file.write("A=D+A\n")
                self.file.write("D=M\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")
            if segment == "pointer":
                if index == 0:
                    self.file.write("@THIS\n")
                    self.file.write("D=M\n")
                    self.file.write("@SP\n")
                    self.file.write("A=M\n")
                    self.file.write("M=D\n")
                    self.file.write("@SP\n")
                    self.file.write("M=M+1\n")
                if index == 1:
                    self.file.write("@THAT\n")
                    self.file.write("D=M\n")
                    self.file.write("@SP\n")
                    self.file.write("A=M\n")
                    self.file.write("M=D\n")
                    self.file.write("@SP\n")
                    self.file.write("M=M+1\n")
            if segment == "temp":
                address = 5 + index
                self.file.write(f"@R{address}\n")
                self.file.write("D=M\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")
            if segment == "constant":
                self.file.write(f"@{index}\n")
                self.file.write("D=A\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")
            if segment == "static":
                symbol = f"{self.file_name}.{index}"

                self.file.write(f"@{symbol}\n")
                self.file.write("D=M\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")
        
        if command == "C_POP":
            if segment == "local":
                self.file.write("@SP\n")
                self.file.write("AM=M-1\n")
                self.file.write("D=M\n")
                self.file.write("@LCL\n")
                self.file.write("A=M\n")
                for i in range(index):
                    self.file.write("A=A+1\n")
                self.file.write("M=D\n")
            if segment == "argument":
                self.file.write("@SP\n")
                self.file.write("AM=M-1\n")
                self.file.write("D=M\n")
                self.file.write("@ARG\n")
                self.file.write("A=M\n")
                for i in range(index):
                    self.file.write("A=A+1\n")
                self.file.write("M=D\n")
            if segment == "this":
                self.file.write("@SP\n")
                self.file.write("AM=M-1\n")
                self.file.write("D=M\n")
                self.file.write("@THIS\n")
                self.file.write("A=M\n")
                for i in range(index):
                    self.file.write("A=A+1\n")
                self.file.write("M=D\n")
            if segment == "that":
                self.file.write("@SP\n")
                self.file.write("AM=M-1\n")
                self.file.write("D=M\n")
                self.file.write("@THAT\n")
                self.file.write("A=M\n")
                for i in range(index):
                    self.file.write("A=A+1\n")
                self.file.write("M=D\n")
            if segment == "pointer":
                if index == 0:
                    self.file.write("@SP\n")
                    self.file.write("AM=M-1\n")
                    self.file.write("D=M\n")
                    self.file.write("@THIS\n")
                    self.file.write("M=D\n")
                if index == 1:
                    self.file.write("@SP\n")
                    self.file.write("AM=M-1\n")
                    self.file.write("D=M\n")
                    self.file.write("@THAT\n")
                    self.file.write("M=D\n")
            if segment == "temp":
                address = 5 + index
                self.file.write("@SP\n")
                self.file.write("AM=M-1\n")
                self.file.write("D=M\n")
                self.file.write(f"@R{address}\n")
                self.file.write("M=D\n")
            if segment == "static":
                symbol = f"{self.file_name}.{index}"

                self.file.write("@SP\n")
                self.file.write("AM=M-1\n")
                self.file.write("D=M\n")
                self.file.write(f"@{symbol}\n")
                self.file.write("M=D\n")
    
    def writeLabel(self, label: str):
        '''labelコマンドを実装するアセンブリコードを書き出す。'''
        self.file.write(f"({label})\n")

    def writeGoto(self, label: str):
        '''gotoコマンドを実装するアセンブリコードを書き出す。'''
        self.file.write(f"@{label}\n")
        self.file.write("0;JMP\n")  
    
    def writeIf(self, label: str):
        '''if-gotoコマンドを実装するアセンブリコードを書き出す。'''
        self.file.write("@SP\n")
        self.file.write("AM=M-1\n")
        self.file.write("D=M\n")
        self.file.write(f"@{label}\n")
        self.file.write("D;JNE\n")

    def writeFunction(self, functionName: str, nVars: int):
        '''functionコマンドを実装するアセンブリコードを書き出す。'''

    def writeCall(self, functionName: str, nArgs: int):
        '''callコマンドを実装するアセンブリコードを書き出す。'''
    
    def writeReturn(self):
        '''returnコマンドを実装するアセンブリコードを書き出す。'''
    
    def close(self):
        '''出力ファイル/ストリームを閉じる'''
        self.file.close()
