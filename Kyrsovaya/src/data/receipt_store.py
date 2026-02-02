from __future__ import annotations
from pathlib import Path


class ReceiptStore:
    def __init__(self, file_path: str = "receipts.txt") -> None:
        self._path = Path(file_path)

    def save(self, receipt_text: str) -> None:
        with self._path.open("a", encoding="utf-8") as f:
            f.write(receipt_text)
            f.write("\n\n" + "=" * 40 + "\n\n")
