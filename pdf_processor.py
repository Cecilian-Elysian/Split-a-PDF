from pypdf import PdfReader, PdfWriter
import os

class PDFProcessor:
    @staticmethod
    def get_page_count(file_path):
        try:
            reader = PdfReader(file_path)
            return len(reader.pages)
        except Exception as e:
            raise ValueError(f"Cannot read PDF file: {file_path}, error: {e}")

    @staticmethod
    def split_by_ranges(input_path, ranges, output_dir):
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)
        output_files = []

        base_name = os.path.splitext(os.path.basename(input_path))[0]

        for i, (start, end) in enumerate(ranges, 1):
            writer = PdfWriter()
            for page_num in range(start - 1, end):
                if 0 <= page_num < total_pages:
                    writer.add_page(reader.pages[page_num])

            output_name = f"{base_name}_part{i}.pdf"
            output_path = os.path.join(output_dir, output_name)

            with open(output_path, 'wb') as f:
                writer.write(f)

            output_files.append({
                'path': output_path,
                'range': (start, end),
                'page_count': end - start + 1
            })

        return output_files

    @staticmethod
    def split_by_fixed(input_path, pages_per_file, output_dir):
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)
        output_files = []

        base_name = os.path.splitext(os.path.basename(input_path))[0]

        start = 1
        part_num = 1
        while start <= total_pages:
            end = min(start + pages_per_file - 1, total_pages)
            writer = PdfWriter()
            for page_num in range(start - 1, end):
                writer.add_page(reader.pages[page_num])

            output_name = f"{base_name}_part{part_num}.pdf"
            output_path = os.path.join(output_dir, output_name)

            with open(output_path, 'wb') as f:
                writer.write(f)

            output_files.append({
                'path': output_path,
                'range': (start, end),
                'page_count': end - start + 1
            })

            start += pages_per_file
            part_num += 1

        return output_files

    @staticmethod
    def parse_page_ranges(range_str):
        ranges = []
        parts = range_str.replace('，', ',').split(',')

        for part in parts:
            part = part.strip()
            if not part:
                continue

            if '-' in part:
                bounds = part.split('-')
                if len(bounds) == 2:
                    try:
                        start = int(bounds[0].strip())
                        end = int(bounds[1].strip())
                        if start > 0 and end >= start:
                            ranges.append((start, end))
                    except ValueError:
                        continue
            elif part.isdigit():
                page = int(part)
                if page > 0:
                    ranges.append((page, page))

        return ranges
