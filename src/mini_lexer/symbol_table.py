"""
Identifier symbol table.
Owner: 67050219
"""
class SymbolTable:

    def __init__(self):
        self.symbols = set()

    def add(self, identifier):
        # ตรวจสอบว่า identifier มีอยู่แล้วหรือไม่
        if identifier in self.symbols:
            print(f'identifier "{identifier}" already in symbol table')
            return False

        # ถ้ายังไม่มี ให้เพิ่มเข้า Symbol Table
        self.symbols.add(identifier)
        print(f"new identifier: {identifier}")
        return True

    def contains(self, identifier):
        return identifier in self.symbols

    def get_all(self):
        return sorted(self.symbols)

