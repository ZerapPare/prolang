# Mini Lexical Analyzer

โปรแกรมวิเคราะห์คำศัพท์ด้วย Python และ SLY อ่าน source code จากไฟล์ `.txt`
แล้วแยก operators, วงเล็บ, semicolon, integers, identifiers, keywords และ strings
ข้าม comments พร้อมเก็บ identifier ใน symbol table และหยุดเมื่อพบ lexical error

## ความสามารถ

- Operators: `+ - * / = > >= < <= == ++ --` และเครื่องหมาย `(`, `)`, `;`
- Keywords ตัวพิมพ์เล็ก: `if then else endif while do endwhile print newline read`
- Identifier ขึ้นต้นด้วยตัวอักษรอังกฤษ ตามด้วยตัวอักษรอังกฤษหรือตัวเลข ไม่รับ underscore
- Integer ไม่ติดลบ; `-10` แยกเป็น operator `-` กับ integer `10`
- String อยู่ใน double quotes ภายในบรรทัดเดียว ไม่รองรับ escape sequences
- ข้าม comments แบบ `//` และ `/* ... */` รวมถึง block comment หลายบรรทัด
- แสดง identifier ใหม่หรือซ้ำ โดยไม่เก็บ keywords และ token ประเภทอื่นใน symbol table
- เป็นการแยก token ไม่ได้คำนวณค่า รันคำสั่ง หรือตรวจไวยากรณ์ทั้งโปรแกรม

> [!NOTE]
> `newline` เป็น keyword ของภาษาจำลอง ส่วนอักขระขึ้นบรรทัดใหม่จริงจะถูกข้าม
> เช่นเดียวกับช่องว่างและ tab

## การติดตั้ง

### สิ่งที่ต้องมี

- Python 3.10 ขึ้นไป ตรวจสอบได้ด้วย `python --version`
- คำสั่งตัวอย่างด้านล่างใช้ Windows PowerShell

### ขั้นตอน

1. เปิด PowerShell ที่โฟลเดอร์โปรเจกต์
2. สร้างและเปิด virtual environment เพื่อแยกไลบรารีของโปรเจกต์
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. ติดตั้ง SLY และ pytest
   ```powershell
   python -m pip install -r requirements.txt
   ```
4. ตรวจว่าติดตั้ง SLY สำเร็จ
   ```powershell
   python -m pip show sly
   ```
   ต้องเห็นบรรทัด `Version: 0.5`

หากมี `.venv` และติดตั้งไลบรารีแล้ว ครั้งต่อไปเปิดเพียง:

```powershell
.\.venv\Scripts\Activate.ps1
```

## วิธีใช้งาน

ส่งชื่อไฟล์ `.txt` ที่มี source code ให้โปรแกรม

```powershell
python main.py path\to\input.txt
```

ตัวอย่าง:

```powershell
python main.py samples\valid_basic.txt
python main.py samples\valid_comments.txt
python main.py samples\invalid_character.txt
```

| ไฟล์ตัวอย่าง | จุดประสงค์ |
|---|---|
| [valid_basic.txt](samples/valid_basic.txt) | ตรวจ operators, identifiers, integer, keywords และ string |
| [valid_comments.txt](samples/valid_comments.txt) | ตรวจ comments ทั้งสองรูปแบบและ identifier ซ้ำ |
| [invalid_character.txt](samples/invalid_character.txt) | ตรวจการแจ้ง error และหยุดที่ `@` |

### ตัวอย่างผลลัพธ์

ตัวอย่าง source code:

```text
read A;
A++;
print "Hello World";
```

ผลลัพธ์:

```text
keyword: read
new identifier: A
semicolon: ;
identifier "A" already in symbol table
operator: ++
semicolon: ;
keyword: print
string: "Hello World"
semicolon: ;
```

### การจัดการข้อผิดพลาด

input (`samples\invalid_character.txt`):

```text
A @ B;
```

output:

```text
new identifier: A
Lexical error: unexpected character @
```

โปรแกรมหยุดทันทีเมื่อพบ `@` จึงไม่แสดง `B` และ `;`

### ข้อความ error และค่าที่โปรแกรมคืน

| สถานการณ์ | ข้อความ | ค่าที่คืน |
|---|---|---|
| ทำงานสำเร็จ | แสดง token ทีละบรรทัด | 0 |
| พบอักขระที่ไม่รู้จัก | `Lexical error: unexpected character X` | 1 |
| ไฟล์ไม่ใช่ `.txt` | `Error: input file must have a .txt extension` | 1 |
| หาไฟล์ไม่เจอ อ่านไม่ได้ หรือ encoding ไม่ถูกต้อง | `Error: cannot read <ไฟล์>: ...` | 1 |
| Block comment ไม่ปิด | `Lexical error: unterminated block comment` | 1 |

ไฟล์ต้องบันทึกเป็น UTF-8 โปรแกรมรองรับไฟล์ที่มี BOM จาก Notepad ด้วย

ตรวจ exit code ได้ทันทีหลังรันด้วย `$LASTEXITCODE` ใน PowerShell
ไฟล์ตัวอย่างที่ตั้งใจให้เกิด error จะคืนค่า `1` ตามพฤติกรรมที่ออกแบบไว้

## การรันชุดทดสอบ

```powershell
python -m pytest -v
```

รันจากโฟลเดอร์โปรเจกต์ด้วย `python -m pytest` เพื่อให้ Python หา `main.py`
และโฟลเดอร์ `src` ได้ ชุดทดสอบตรวจ tokens, comments, symbol table, การอ่านไฟล์
และการหยุดเมื่อพบ error โดยไม่ได้อ่านไฟล์ใน `samples/` อัตโนมัติ

รันเฉพาะส่วนได้ด้วย:

```powershell
python -m pytest tests/test_lexer.py -v
python -m pytest tests/test_symbol_table.py -v
python -m pytest tests/test_main.py -v
```

| ชุดทดสอบ | สิ่งที่ตรวจ |
|---|---|
| `test_lexer.py` | ประเภทและค่า token, ลำดับ operators, comments, keywords, newline และ lexical errors |
| `test_symbol_table.py` | Identifier ใหม่/ซ้ำ การค้นหา และรายชื่อเรียงลำดับ |
| `test_main.py` | Input ว่าง การอ่านไฟล์ BOM นามสกุลไฟล์ และการแสดง error |

## โครงสร้างไฟล์

```text
prolang/
|-- main.py                       จุดเริ่มโปรแกรมและการอ่านไฟล์
|-- requirements.txt              รายการไลบรารีที่ต้องติดตั้ง
|-- src/
|   `-- mini_lexer/
|       |-- lexer.py              กฎ token ของ SLY
|       |-- formatter.py          จัดข้อความ output และตรวจ identifier ซ้ำ
|       `-- symbol_table.py       เก็บและตรวจ identifier ซ้ำ
|-- samples/                      input ตัวอย่างปกติและกรณี error
|-- tests/                        automated tests
`-- README.md                     วิธีติดตั้งและใช้งาน
```

## การทำงานภายใน

1. `main.py` รับชื่อไฟล์ ตรวจนามสกุล และอ่าน source code
2. `MiniLexer` ใน `lexer.py` ใช้กฎ Regular Expression ของ SLY สร้าง token ทีละตัว
3. `format_token()` ใน `formatter.py` แปลง token เป็นข้อความสำหรับแสดงผล
4. เมื่อพบ identifier จะตรวจและเพิ่มชื่อใน `SymbolTable` ซึ่งใช้ `set` ป้องกันชื่อซ้ำ
5. เมื่อพบ `LexicalError` โปรแกรมจะแสดงข้อความและจบด้วย exit code `1`

Symbol table เริ่มใหม่ทุกครั้งที่วิเคราะห์ source code โดยแยกตัวพิมพ์เล็กและใหญ่
เช่น `A` และ `a` เป็นคนละชื่อ

### ลำดับกฎและรูปแบบ token

- เขียน operator ที่ยาวกว่าก่อน เช่น `>=` ก่อน `>` และ `++` ก่อน `+`
- วางกฎ comments ก่อน division เพื่อให้ `//` และ `/* ... */` ไม่ถูกแยกเป็น `/`
- Identifier ใช้ `[a-zA-Z][a-zA-Z0-9]*` แล้วเปลี่ยนประเภทตาม keyword mapping
- String ใช้ `"[^"\n]*"` และเก็บ double quotes ไว้ในค่า token
- Newline รองรับทั้ง LF และ CRLF โดยเพิ่มเลขบรรทัดและไม่สร้าง token

## แก้ปัญหาเบื้องต้น

| อาการ | วิธีตรวจ |
|---|---|
| `No module named sly` หรือ `pytest` | เปิด `.venv` แล้วรัน `python -m pip install -r requirements.txt` |
| `No module named src` | เข้าโฟลเดอร์ที่มี `main.py` ก่อนรันคำสั่ง |
| `cannot read ...` | ตรวจ path ของไฟล์และบันทึกไฟล์เป็น UTF-8 |
| `unexpected character ...` | ตรวจอักขระที่แจ้ง รวมถึง `_` และ string ที่ไม่มี double quote ปิด |
