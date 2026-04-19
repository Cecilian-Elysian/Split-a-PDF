import config

TRANSLATIONS = {
    "en": {
        "app_title": "PDF Splitter",
        "select_files": "Select PDF Files",
        "select_output": "Select Output Directory",
        "split_mode": "Split Mode",
        "by_range": "By Page Range (e.g., 1-10, 11-20)",
        "by_fixed": "By Fixed Pages (e.g., every 10 pages)",
        "page_ranges": "Page Ranges:",
        "pages_per_file": "Pages Per File:",
        "preview": "Preview",
        "split": "Split",
        "clear": "Clear",
        "total_pages": "Total Pages: {}",
        "output_files": "Output Files:",
        "language": "Language",
        "processing": "Processing...",
        "success": "Split completed successfully!",
        "error": "Error: {}",
        "no_file_selected": "Please select PDF files first",
        "no_output_selected": "Please select output directory",
        "invalid_range": "Invalid page range format",
        "invalid_pages": "Pages per file must be greater than 0",
        "select_language": "Select Language",
        "english": "English",
        "chinese": "中文",
        "file_list": "Selected Files",
        "add_files": "Add Files",
        "remove_selected": "Remove Selected",
        "clear_all": "Clear All",
        "range_example": "Example: 1-10, 11-20, 21-30",
        "page_count": "{} pages",
        "output_preview": "Output Preview",
    },
    "zh": {
        "app_title": "PDF 切分工具",
        "select_files": "选择 PDF 文件",
        "select_output": "选择输出目录",
        "split_mode": "切分模式",
        "by_range": "按页数范围（如 1-10, 11-20）",
        "by_fixed": "按固定页数切分（如每10页一份）",
        "page_ranges": "页数范围：",
        "pages_per_file": "每文件页数：",
        "preview": "预览",
        "split": "开始切分",
        "clear": "清空",
        "total_pages": "总页数：{}",
        "output_files": "输出文件：",
        "language": "语言",
        "processing": "处理中...",
        "success": "切分完成！",
        "error": "错误：{}",
        "no_file_selected": "请先选择 PDF 文件",
        "no_output_selected": "请选择输出目录",
        "invalid_range": "页数范围格式不正确",
        "invalid_pages": "每文件页数必须大于 0",
        "select_language": "选择语言",
        "english": "English",
        "chinese": "中文",
        "file_list": "已选文件",
        "add_files": "添加文件",
        "remove_selected": "移除所选",
        "clear_all": "清空全部",
        "range_example": "示例：1-10, 11-20, 21-30",
        "page_count": "{} 页",
        "output_preview": "输出预览",
    }
}

_current_lang = "zh"

def set_language(lang):
    global _current_lang
    if lang in TRANSLATIONS:
        _current_lang = lang

def get_language():
    return _current_lang

def t(key: str) -> str:
    return str(TRANSLATIONS[_current_lang].get(key, key))
