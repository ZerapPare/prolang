# Mini Lexical Analyzer

โครงเริ่มต้นสำหรับรายวิชา 05506237 Programming Languages Concepts and
Paradigms โปรแกรมจะใช้ Python และ SLY เพื่ออ่าน source code จากไฟล์ `.txt`
และแยก token ตามข้อกำหนดใน `TermReport1-2569.pdf`

> ตอนนี้เป็นเพียงโครงเริ่มต้น กฎ token หลักใน `lexer.py` ยังเป็น `TODO`

## ติดตั้งและทดลอง

ต้องมี Python 3.10 หรือใหม่กว่า จากนั้นรันคำสั่ง:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest
python main.py samples\valid_basic.txt
```

ในช่วงแรก `valid_basic.txt` จะยังเกิด lexical error เพราะสมาชิกแต่ละคนยังต้อง
เพิ่มกฎ token ของตนเองให้ครบ

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

