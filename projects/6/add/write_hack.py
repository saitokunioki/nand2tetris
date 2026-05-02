from pathlib import Path

result = [
    "0001",
    "0010",
    "0011",
]

text = "\n".join(result) + "\n"
Path("Test.hack").write_text(text, encoding="utf-8")