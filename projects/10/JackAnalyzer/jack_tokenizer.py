class JackTokenizer:
    KEYWORDS = [
        "class", "constructor", "function", "method", "field", "static",
        "var", "int", "char", "boolean", "void", "true", "false", "null",
        "this", "let", "do", "if", "else", "while", "return",
    ]

    SYMBOLS = [
        "{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/",
        "&", "|", "<", ">", "=", "~",
    ]

    def __init__(self, input_path):
        '''入力ファィルを開き、パースを行う準備をする。'''
        with open(input_path, "r") as input_file:
            source = input_file.read()

        source = self._remove_comments(source)
        self.tokens = self._tokenize(source)
        self.current_token = None
        self.current_index = -1

    def hasMoreTokens(self):
        '''入力にまだトークンは存在するか？'''
        return self.current_index + 1 < len(self.tokens)
    
    def advance(self):
        '''入力から次のトークンを取得し、それを現在のトークンとして、取得する。
            このルーチンは、hasMoreTokens()がTrueの場合のみ呼び出すことができる。
            なお、初期の状態では現在のトークンは設定されていない。
        '''
        if not self.hasMoreTokens():
            return

        self.current_index = self.current_index + 1
        self.current_token = self.tokens[self.current_index]

    def tokenType(self):
        '''現在のトークンの種類を定数として返す。'''
        if self.current_token in self.KEYWORDS:
            return "KEYWORD"

        if self.current_token in self.SYMBOLS:
            return "SYMBOL"

        if self.current_token.isdigit():
            return "INT_CONST"

        if self.current_token.startswith('"') and self.current_token.endswith('"'):
            return "STRING_CONST"

        return "IDENTIFIER"

    def keyWord(self):
        '''現在のトークンのキーワードを定数として返す。
        このルーチンは、TokenType()がKEYWORDの場合にのみ呼び出すことができる。
        '''
        return self.current_token

    def symbol(self):
        '''現在のトークンの文字を返す。
        このルーチンは、TokenType()がSYMBOLの場合にのみ呼び出すことができる。
        '''
        return self.current_token

    def identifier(self):
        '''現在のトークンの識別子（identifier）を返す。
        このルーチンは、TokenType()がIDENTIFIERの場合にのみ呼び出すことができる。
        '''
        return self.current_token

    def intVal(self):
        '''現在のトークンの整数の値を返す。
        このルーチンは、TokenType()がINT_CONSTの場合にのみ呼び出すことができる。
        '''
        return int(self.current_token)
    
    def stringVal(self):
        '''現在のトークンの識別子文字列を返す。
        このルーチンは、TokenType()がSTRING_CONSTの場合にのみ呼び出すことができる。
        '''
        return self.current_token[1:-1]

    def _remove_comments(self, source):
        result = ""
        i = 0
        in_string = False

        while i < len(source):
            current = source[i]
            next_char = ""
            if i + 1 < len(source):
                next_char = source[i + 1]

            if current == '"':
                in_string = not in_string
                result = result + current
                i = i + 1
            elif not in_string and current == "/" and next_char == "/":
                i = self._skip_line_comment(source, i)
            elif not in_string and current == "/" and next_char == "*":
                i = self._skip_block_comment(source, i)
            else:
                result = result + current
                i = i + 1

        return result

    def _skip_line_comment(self, source, i):
        while i < len(source) and source[i] != "\n":
            i = i + 1
        return i

    def _skip_block_comment(self, source, i):
        i = i + 2
        while i + 1 < len(source):
            if source[i] == "*" and source[i + 1] == "/":
                return i + 2
            i = i + 1
        return i

    def _tokenize(self, source):
        tokens = []
        i = 0

        while i < len(source):
            current = source[i]

            if current.isspace():
                i = i + 1
            elif current in self.SYMBOLS:
                tokens.append(current)
                i = i + 1
            elif current == '"':
                token, i = self._read_string(source, i)
                tokens.append(token)
            else:
                token, i = self._read_word_or_number(source, i)
                tokens.append(token)

        return tokens

    def _read_string(self, source, i):
        token = '"'
        i = i + 1

        while i < len(source) and source[i] != '"':
            token = token + source[i]
            i = i + 1

        token = token + '"'
        i = i + 1
        return token, i

    def _read_word_or_number(self, source, i):
        token = ""

        while i < len(source):
            current = source[i]
            if current.isspace() or current in self.SYMBOLS:
                break
            token = token + current
            i = i + 1

        return token, i
