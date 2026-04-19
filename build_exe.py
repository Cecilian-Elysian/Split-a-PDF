import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--name=PDFSplitter',
    '--onefile',
    '--icon=NONE',
    '--add-data=i18n.py;.',
    '--add-data=config.py;.',
    '--add-data=pdf_processor.py;.',
    '--hidden-import=pypdf',
    '--clean',
    '--noconfirm'
])
