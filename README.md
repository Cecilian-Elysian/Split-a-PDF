# PDF Splitter

A simple tool to split large PDF files into smaller ones.

## Features

- **Language Support** - English / 中文
- **Batch Processing** - Split multiple PDF files at once
- **Split Modes**
  - By page range (e.g., 1-10, 11-20)
  - By fixed pages (e.g., every 10 pages)
- **Preview** - Preview split results before processing
- **Progress Bar** - Visual progress indicator

## Usage

1. Run `dist/PDFSplitter.exe`
2. Select PDF file(s)
3. Choose split mode and set parameters
4. Click "Preview" to see output
5. Select output directory
6. Click "Split" to start

## Output

Output files are named: `原文件名_part1.pdf`, `原文件名_part2.pdf`, ...

## Build from Source

```bash
pip install -r requirements.txt
py main.py
```

## Build Executable

```bash
py -m pip install pyinstaller
py -m PyInstaller --name=PDFSplitter --onefile main.py
```

## Requirements

- Python 3.8+
- pypdf >= 3.0.0

## License

MIT
