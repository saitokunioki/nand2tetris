class CompilationEngine:
    OP_SYMBOLS = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
    UNARY_OP_SYMBOLS = ["-", "~"]
    KEYWORD_CONSTANTS = ["true", "false", "null", "this"]

    def __init__(self, tokenizer, output_path):
        '''与えられた入力と出力に対して新しいコンパイルエンジンを生成する。
        （JackAnalyzerモジュールが）次に呼ぶルーチンはcompileClass()でなければならない。
        '''
        self.tokenizer = tokenizer
        self.output_file = open(output_path, "w")
        self.indent = 0

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

    def compileClass(self):
        '''クラスをコンパイルする。'''
        self._write_start_tag("class")
        self._write_current_token()
        self._write_current_token()
        self._write_current_token()

        while self._current_token() in ["static", "field"]:
            self.compileClassVarDec()

        while self._current_token() in ["constructor", "function", "method"]:
            self.compileSubroutine()

        self._write_current_token()
        self._write_end_tag("class")
        self.output_file.close()

    def compileClassVarDec(self):
        '''スタティック変数の宣言またはフィールド変数の宣言をコンパイルする。'''
        self._write_start_tag("classVarDec")

        while self._current_token() != ";":
            self._write_current_token()

        self._write_current_token()
        self._write_end_tag("classVarDec")

    def compileSubroutine(self):
        '''メソッド、ファンション、コンストラクタをコンパイルする。'''
        self._write_start_tag("subroutineDec")
        self._write_current_token()
        self._write_current_token()
        self._write_current_token()
        self._write_current_token()
        self.compileParameterList()
        self._write_current_token()
        self.compileSubroutineBody()
        self._write_end_tag("subroutineDec")

    def compileParameterList(self):
        '''パラメータのリスト（空の可能性もある）をコンパイルする。括弧（）を処理しない。'''
        self._write_start_tag("parameterList")

        while self._current_token() != ")":
            self._write_current_token()

        self._write_end_tag("parameterList")

    def compileSubroutineBody(self):
        '''サブルーチン本体をコンパイルする。'''
        self._write_start_tag("subroutineBody")
        self._write_current_token()

        while self._current_token() == "var":
            self.compileVarDec()

        self.compileStatements()
        self._write_current_token()
        self._write_end_tag("subroutineBody")

    def compileVarDec(self):
        '''var宣言をコンパイルする。'''
        self._write_start_tag("varDec")

        while self._current_token() != ";":
            self._write_current_token()

        self._write_current_token()
        self._write_end_tag("varDec")

    def compileStatements(self):
        '''一連の文をコンパイルする。波括弧{}は処理しない。'''
        self._write_start_tag("statements")

        while self._current_token() in ["let", "if", "while", "do", "return"]:
            if self._current_token() == "let":
                self.compileLet()
            elif self._current_token() == "if":
                self.compileIf()
            elif self._current_token() == "while":
                self.compileWhile()
            elif self._current_token() == "do":
                self.compileDo()
            elif self._current_token() == "return":
                self.compileReturn()

        self._write_end_tag("statements")

    def compileLet(self):
        '''let文をコンパイルする。'''
        self._write_start_tag("letStatement")
        self._write_current_token()
        self._write_current_token()

        if self._current_token() == "[":
            self._write_current_token()
            self.compileExpression()
            self._write_current_token()

        self._write_current_token()
        self.compileExpression()
        self._write_current_token()
        self._write_end_tag("letStatement")

    def compileIf(self):
        '''if文をコンパイルする。else文を伴う可能性がある。'''
        self._write_start_tag("ifStatement")
        self._write_current_token()
        self._write_current_token()
        self.compileExpression()
        self._write_current_token()
        self._write_current_token()
        self.compileStatements()
        self._write_current_token()

        if self._current_token() == "else":
            self._write_current_token()
            self._write_current_token()
            self.compileStatements()
            self._write_current_token()

        self._write_end_tag("ifStatement")
    
    def compileWhile(self):
        '''while文をコンパイルする。'''
        self._write_start_tag("whileStatement")
        self._write_current_token()
        self._write_current_token()
        self.compileExpression()
        self._write_current_token()
        self._write_current_token()
        self.compileStatements()
        self._write_current_token()
        self._write_end_tag("whileStatement")

    def compileDo(self):
        '''do文をコンパイルする。'''
        self._write_start_tag("doStatement")
        self._write_current_token()
        self._compileSubroutineCall()
        self._write_current_token()
        self._write_end_tag("doStatement")
    
    def compileReturn(self):
        '''return文をコンパイルする。'''
        self._write_start_tag("returnStatement")
        self._write_current_token()

        if self._current_token() != ";":
            self.compileExpression()

        self._write_current_token()
        self._write_end_tag("returnStatement")

    def compileExpression(self):
        '''式をコンパイルする。'''
        self._write_start_tag("expression")
        self.compileTerm()

        while self._current_token() in self.OP_SYMBOLS:
            self._write_current_token()
            self.compileTerm()

        self._write_end_tag("expression")

    def compileEcpression(self):
        '''式をコンパイルする。'''
        self.compileExpression()

    def compileTerm(self):
        '''現在のトークンが識別子の場合、このルーチンはそれを変数、配列要素、サブルーチン呼び出しのいずれかに解決しなければならない。
        そのためには、一つ先のトークンを読み込み、そのトークンが[か(か.のどれかに該当するかを調べる。それ以外のトークンはこの項の一部ではないので、
        先に進んではならない。
        '''
        self._write_start_tag("term")

        if self._current_token() == "(":
            self._write_current_token()
            self.compileExpression()
            self._write_current_token()
        elif self._current_token() in self.UNARY_OP_SYMBOLS:
            self._write_current_token()
            self.compileTerm()
        elif self._next_token() == "[":
            self._write_current_token()
            self._write_current_token()
            self.compileExpression()
            self._write_current_token()
        elif self._next_token() == "(" or self._next_token() == ".":
            self._compileSubroutineCall()
        else:
            self._write_current_token()

        self._write_end_tag("term")

    def compileExpressionList(self):
        '''カンマ区切りの式のリスト（空の場合もある）をコンパイルする。リスト内の指揮の数を返す。'''
        count = 0
        self._write_start_tag("expressionList")

        if self._current_token() != ")":
            self.compileExpression()
            count = count + 1

            while self._current_token() == ",":
                self._write_current_token()
                self.compileExpression()
                count = count + 1

        self._write_end_tag("expressionList")
        return count

    def _compileSubroutineCall(self):
        self._write_current_token()

        if self._current_token() == ".":
            self._write_current_token()
            self._write_current_token()

        self._write_current_token()
        self.compileExpressionList()
        self._write_current_token()

    def _current_token(self):
        return self.tokenizer.current_token

    def _next_token(self):
        next_index = self.tokenizer.current_index + 1

        if next_index < len(self.tokenizer.tokens):
            return self.tokenizer.tokens[next_index]

        return None

    def _write_start_tag(self, tag_name):
        self._write_indent()
        self.output_file.write("<" + tag_name + ">\n")
        self.indent = self.indent + 1

    def _write_end_tag(self, tag_name):
        self.indent = self.indent - 1
        self._write_indent()
        self.output_file.write("</" + tag_name + ">\n")

    def _write_current_token(self):
        token_type = self.tokenizer.tokenType()
        tag_name = self._xml_tag_name(token_type)
        token_value = self._token_value(token_type)
        token_value = self._escape_xml(token_value)

        self._write_indent()
        self.output_file.write("<" + tag_name + "> ")
        self.output_file.write(token_value)
        self.output_file.write(" </" + tag_name + ">\n")

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

    def _write_indent(self):
        self.output_file.write("  " * self.indent)

    def _xml_tag_name(self, token_type):
        if token_type == "KEYWORD":
            return "keyword"
        if token_type == "SYMBOL":
            return "symbol"
        if token_type == "IDENTIFIER":
            return "identifier"
        if token_type == "INT_CONST":
            return "integerConstant"
        if token_type == "STRING_CONST":
            return "stringConstant"
        return ""

    def _token_value(self, token_type):
        if token_type == "KEYWORD":
            return self.tokenizer.keyWord()
        if token_type == "SYMBOL":
            return self.tokenizer.symbol()
        if token_type == "IDENTIFIER":
            return self.tokenizer.identifier()
        if token_type == "INT_CONST":
            return str(self.tokenizer.intVal())
        if token_type == "STRING_CONST":
            return self.tokenizer.stringVal()
        return ""

    def _escape_xml(self, value):
        value = value.replace("&", "&amp;")
        value = value.replace("<", "&lt;")
        value = value.replace(">", "&gt;")
        return value
