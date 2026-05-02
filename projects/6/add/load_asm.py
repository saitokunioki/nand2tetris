from pathlib import Path

text = Path("Add.asm").read_text(encoding="utf-8")
print(text)