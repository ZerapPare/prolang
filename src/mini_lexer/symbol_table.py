"""Store unique identifiers and check whether they have appeared before."""
class SymbolTable:

    def __init__(self):
        self.symbols = set()

    def add(self, identifier):
        # มี identifier แล้ว
        if identifier in self.symbols:
            return False

        # ไม่มีเพิ่มเข้า Symbol Table
        self.symbols.add(identifier)
        return True

    def contains(self, identifier):
        return identifier in self.symbols

    def get_all(self):
        return sorted(self.symbols)

