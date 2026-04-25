# PDF Splitter

A simple tool to split large PDF files into smaller ones with a user-friendly GUI.

## Features

| Feature | Description |
|---------|-------------|
| 🌍 Language Support | English / 中文 (bilingual UI) |
| 📦 Batch Processing | Split multiple PDF files at once |
| 📄 Split Modes | By page range or fixed page count |
| 👁️ Preview | Preview split results before processing |
| 📊 Progress Bar | Visual progress indicator |
| 🎯 Smart Output | Automatic output folder selection |

## Usage

1. Run `dist/PDFSplitter.exe` (or `python main.py` from source)
2. Click "选择文件" to select PDF file(s)
3. Choose split mode:
   - **按页码范围** (By page range): e.g., `1-10, 11-20, 21-30`
   - **按固定页数** (By fixed pages): e.g., every `10` pages
4. Click "预览" to preview output results
5. Select output directory
6. Click "开始分割" to start splitting

## Output

Output files are named: `原文件名_part1.pdf`, `原文件名_part2.pdf`, ...

## Build from Source

```bash
pip install -r requirements.txt
python main.py
```

## Build Executable

```bash
pip install pyinstaller
py -m PyInstaller PDFSplitter.spec
```

## Requirements

- Python 3.8+
- pypdf >= 3.0.0

## Version

- v0.0.1

## License

MIT
