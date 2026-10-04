# Mini Lexical Analyzer

โครงเริ่มต้นสำหรับรายวิชา 05506237 Programming Languages Concepts and
Paradigms โปรแกรมจะใช้ Python และ SLY เพื่ออ่าน source code จากไฟล์ `.txt`
และแยก token ตามข้อกำหนดใน `TermReport1-2569.pdf`

> ตอนนี้เป็นเพียงโครงเริ่มต้น กฎ token หลักใน `lexer.py` ยังเป็น `TODO`

## การติดตั้ง

### สิ่งที่ต้องมี
- Python 3.10 ขึ้นไป ตรวจสอบได้ด้วย `python --version`

### ขั้นตอน
1. เปิด PowerShell ที่โฟลเดอร์โปรเจกต์
2. (ไม่บังคับ) สร้าง virtual environment เพื่อแยกไลบรารีออกจากเครื่อง
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

## วิธีใช้งาน

ส่งชื่อไฟล์ `.txt` ที่มี source code ให้โปรแกรม

```powershell
python main.py <ชื่อไฟล์.txt>
```

ตัวอย่าง:

```powershell
python main.py samples\valid_basic.txt
python main.py samples\valid_comments.txt
python main.py samples\invalid_character.txt
```

ในช่วงแรก `valid_basic.txt` จะยังเกิด lexical error เพราะสมาชิกแต่ละคนยังต้อง
เพิ่มกฎ token ของตนเองให้ครบ

### ตัวอย่างผลลัพธ์

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
| หาไฟล์ไม่เจอ หรืออ่านไม่ได้ | `Error: cannot read <ไฟล์>: ...` | 1 |

ไฟล์ต้องบันทึกเป็น UTF-8 โปรแกรมรองรับไฟล์ที่มี BOM จาก Notepad ด้วย

## การรันชุดทดสอบ

```powershell
python -m pytest -v
```

ต้องใช้ `python -m pytest` ไม่ใช่ `pytest` เฉย ๆ เพื่อให้ Python หาไฟล์ `main.py`
และโฟลเดอร์ `src` เจอ

## โครงสร้างไฟล์

```text
prolang/
|-- main.py                       จุดเริ่มโปรแกรมและการอ่านไฟล์
|-- requirements.txt              รายการไลบรารีที่ต้องติดตั้ง
|-- src/
|   `-- mini_lexer/
|       |-- lexer.py              กฎ token ของ SLY
|       |-- formatter.py          จัดข้อความ output ให้ตรงโจทย์
|       `-- symbol_table.py       เก็บและตรวจ identifier ซ้ำ
|-- samples/                      input ตัวอย่างอย่างน้อย 3 ไฟล์
|-- tests/                        automated tests
`-- README.md                     วิธีติดตั้ง ใช้งาน และแบ่งงาน
```

## การแบ่งงาน 6 คน

1. **คนที่ 1:** `main.py` และ `formatter.py` - อ่านไฟล์ เชื่อมส่วนต่าง ๆ และจัด output
2. **คนที่ 2:** ส่วนที่ทำเครื่องหมาย MEMBER 2 ใน `lexer.py` - operators และ punctuation
3. **คนที่ 3:** ส่วน MEMBER 3 - integer, identifier และ keywords
4. **คนที่ 4:** `symbol_table.py` และ test ของ symbol table
5. **คนที่ 5:** ส่วน MEMBER 5 - string และ comments
6. **คนที่ 6:** ส่วน MEMBER 6, error handling และชุดทดสอบรวม

สมาชิกทุกคนต้องเพิ่ม test ของส่วนตัวเองอย่างน้อย 4 กรณีใน `tests/`

## ลำดับการทำงาน

1. ตกลงชื่อ token และรูปแบบ output จากโครงนี้ร่วมกัน
2. ทุกคนสร้าง branch ของตัวเองแล้วเขียนส่วนที่รับผิดชอบพร้อมกัน
3. รัน `python -m pytest` ก่อนส่งงานของตัวเอง
4. รวมงานทีละคนและทดสอบหลังรวมทุกครั้ง
5. ทดสอบไฟล์ใน `samples/` ทั้งสามไฟล์และตรวจ output กับโจทย์

## ข้อควรระวัง

- เขียน operator ที่ยาวกว่าก่อน เช่น `>=` ก่อน `>` และ `++` ก่อน `+`
- keyword ยอมรับเฉพาะตัวพิมพ์เล็ก
- comment ต้องไม่สร้าง token ใด ๆ
- เมื่อพบ lexical error ต้องแสดงอักขระที่ผิดและหยุดทันที
- ห้ามแทนที่ lexer ด้วยชุด `if-else` สำหรับตรวจ token ทั้งหมด

