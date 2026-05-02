from pathlib import Path

asm_path = Path("Add.asm")
hack_path =asm_path.with_suffix(".hack")

print(hack_path)