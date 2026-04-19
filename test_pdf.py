from pypdf import PdfWriter, PdfReader
import os

def create_test_pdf(path, num_pages=10):
    writer = PdfWriter()
    for i in range(num_pages):
        writer.add_blank_page(width=595, height=842)
    with open(path, 'wb') as f:
        writer.write(f)
    print(f"Created test PDF: {path} ({num_pages} pages)")

if __name__ == "__main__":
    test_dir = os.path.join(os.path.dirname(__file__), "test")
    os.makedirs(test_dir, exist_ok=True)

    test_pdf = os.path.join(test_dir, "test.pdf")
    create_test_pdf(test_pdf, 15)

    from pdf_processor import PDFProcessor

    page_count = PDFProcessor.get_page_count(test_pdf)
    print(f"Page count: {page_count}")

    ranges = PDFProcessor.parse_page_ranges("1-5, 6-10, 11-15")
    print(f"Parsed ranges: {ranges}")

    output_dir = os.path.join(test_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    files = PDFProcessor.split_by_ranges(test_pdf, ranges, output_dir)
    print(f"Created {len(files)} files:")
    for f in files:
        print(f"  {f['path']} (pages {f['range'][0]}-{f['range'][1]})")

    fixed_files = PDFProcessor.split_by_fixed(test_pdf, 5, output_dir)
    print(f"\nFixed split (5 pages each): {len(fixed_files)} files")
    for f in fixed_files:
        print(f"  {f['path']} (pages {f['range'][0]}-{f['range'][1]})")

    print("\nTest completed successfully!")
