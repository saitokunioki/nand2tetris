class SymbolTable:
    def __init__(self):
        self.table = {}

    # <symbol, address> をテーブルに追加する
    def addEntry(self, symbol, address):
        self.table[symbol] = address

    # 指定された symbol がテーブルに含まれているか？
    def contains(self, symbol):
        return symbol in self.table

    # symbol に関連付けられたアドレスを返す
    def getAddress(self, symbol):
        return self.table[symbol]
