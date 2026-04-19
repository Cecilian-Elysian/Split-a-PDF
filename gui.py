import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pdf_processor import PDFProcessor
from i18n import t, set_language, get_language

class PDFSplitterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(t("app_title"))
        self.root.geometry("800x600")

        self.current_lang = get_language()
        self.selected_files = []
        self.output_dir = None
        self.split_mode = tk.StringVar(value="range")
        self.main_frame = None

        self.setup_ui()

    def setup_ui(self):
        if self.main_frame:
            self.main_frame.destroy()

        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_language_section(self.main_frame)
        self.create_file_section(self.main_frame)
        self.create_split_section(self.main_frame)
        self.create_preview_section(self.main_frame)

    def create_language_section(self, parent):
        lang_frame = ttk.Frame(parent)
        lang_frame.pack(fill=tk.X, pady=(0, 10))

        lang_label = t("language") + ":"
        ttk.Label(lang_frame, text=lang_label).pack(side=tk.LEFT)
        self.lang_combo = ttk.Combobox(lang_frame, values=["English", "中文"], 
                                        state="readonly", width=10)
        self.lang_combo.pack(side=tk.LEFT, padx=5)
        self.lang_combo.set("中文" if self.current_lang == "zh" else "English")
        self.lang_combo.bind("<<ComboboxSelected>>", self.on_language_change)

    def create_file_section(self, parent):
        file_list_text = t("file_list")
        file_frame = ttk.LabelFrame(parent, text=file_list_text, padding="5")
        file_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.file_listbox = tk.Listbox(file_frame, selectmode=tk.EXTENDED)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=scrollbar.set)

        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        add_text = t("add_files")
        remove_text = t("remove_selected")
        clear_text = t("clear_all")
        select_output_text = t("select_output")

        ttk.Button(btn_frame, text=add_text, command=self.add_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=remove_text, command=self.remove_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=clear_text, command=self.clear_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=select_output_text, command=self.select_output).pack(side=tk.RIGHT)

        no_output_text = t("no_output_selected")
        self.output_label = ttk.Label(parent, text=no_output_text)
        self.output_label.pack(fill=tk.X, pady=(0, 10))

    def create_split_section(self, parent):
        split_mode_text = t("split_mode")
        split_frame = ttk.LabelFrame(parent, text=split_mode_text, padding="5")
        split_frame.pack(fill=tk.X, pady=(0, 10))

        by_range_text = t("by_range")
        by_fixed_text = t("by_fixed")
        
        ttk.Radiobutton(split_frame, text=by_range_text, variable=self.split_mode, 
                        value="range", command=self.on_mode_change).pack(anchor=tk.W)
        
        range_frame = ttk.Frame(split_frame)
        range_frame.pack(fill=tk.X, padx=20)
        page_ranges_text = t("page_ranges")
        ttk.Label(range_frame, text=page_ranges_text).pack(side=tk.LEFT)
        self.range_entry = ttk.Entry(range_frame, width=30)
        self.range_entry.pack(side=tk.LEFT, padx=5)
        self.range_entry.insert(0, "1-10, 11-20, 21-30")
        range_example_text = t("range_example")
        ttk.Label(range_frame, text=range_example_text, foreground="gray").pack(side=tk.LEFT)

        ttk.Radiobutton(split_frame, text=by_fixed_text, variable=self.split_mode, 
                        value="fixed", command=self.on_mode_change).pack(anchor=tk.W)

        fixed_frame = ttk.Frame(split_frame)
        fixed_frame.pack(fill=tk.X, padx=20)
        pages_per_file_text = t("pages_per_file")
        ttk.Label(fixed_frame, text=pages_per_file_text).pack(side=tk.LEFT)
        self.fixed_entry = ttk.Entry(fixed_frame, width=10)
        self.fixed_entry.pack(side=tk.LEFT, padx=5)
        self.fixed_entry.insert(0, "10")

        self.on_mode_change()

    def create_preview_section(self, parent):
        output_preview_text = t("output_preview")
        preview_frame = ttk.LabelFrame(parent, text=output_preview_text, padding="5")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.preview_listbox = tk.Listbox(preview_frame)
        self.preview_listbox.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=self.preview_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.preview_listbox.config(yscrollcommand=scrollbar.set)

        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        preview_text = t("preview")
        split_text = t("split")
        ttk.Button(btn_frame, text=preview_text, command=self.generate_preview).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=split_text, command=self.start_split).pack(side=tk.RIGHT)

        self.progress = ttk.Progressbar(parent, mode="determinate")
        self.progress.pack(fill=tk.X, pady=(0, 5))

        self.status_label = ttk.Label(parent, text="")
        self.status_label.pack(fill=tk.X)

    def on_language_change(self, event=None):
        lang = "zh" if self.lang_combo.get() == "中文" else "en"
        set_language(lang)
        self.current_lang = lang
        self.refresh_ui()

    def refresh_ui(self):
        app_title = t("app_title")
        self.root.title(app_title)
        self.setup_ui()

    def add_files(self):
        select_files_text = t("select_files")
        files = filedialog.askopenfilenames(title=select_files_text, 
                                             filetypes=[("PDF files", "*.pdf")])
        for f in files:
            if f not in self.selected_files:
                self.selected_files.append(f)
                self.file_listbox.insert(tk.END, os.path.basename(f))

    def remove_selected(self):
        selection = list(self.file_listbox.curselection())
        for idx in reversed(selection):
            self.file_listbox.delete(idx)
            del self.selected_files[idx]

    def clear_files(self):
        self.file_listbox.delete(0, tk.END)
        self.selected_files.clear()
        self.preview_listbox.delete(0, tk.END)

    def select_output(self):
        select_output_text = t("select_output")
        directory = filedialog.askdirectory(title=select_output_text)
        if directory:
            self.output_dir = directory
            self.output_label.config(text=directory)

    def on_mode_change(self):
        mode = self.split_mode.get()
        if mode == "range":
            self.range_entry.config(state="normal")
            self.fixed_entry.config(state="disabled")
        else:
            self.range_entry.config(state="disabled")
            self.fixed_entry.config(state="normal")

    def generate_preview(self):
        no_file_selected = t("no_file_selected")
        if not self.selected_files:
            messagebox.showwarning("Warning", no_file_selected)
            return

        self.preview_listbox.delete(0, tk.END)

        try:
            mode = self.split_mode.get()
            total_pages_label = t("total_pages")
            page_count_label = t("page_count")

            for filename in self.selected_files:
                page_count = PDFProcessor.get_page_count(filename)
                display_name = f"{os.path.basename(filename)} - {total_pages_label.format(page_count)}"
                self.preview_listbox.insert(tk.END, display_name)

                if mode == "range":
                    ranges_str = self.range_entry.get()
                    ranges = PDFProcessor.parse_page_ranges(ranges_str)
                    for i, (start, end) in enumerate(ranges, 1):
                        pages_in_part = end - start + 1
                        suffix = "页" if self.current_lang == "zh" else "pages"
                        part_display = f"  Part {i}: {start}-{end} ({pages_in_part} {suffix})"
                        self.preview_listbox.insert(tk.END, part_display)
                else:
                    invalid_pages = t("invalid_pages")
                    try:
                        pages_per = int(self.fixed_entry.get())
                        if pages_per <= 0:
                            messagebox.showerror("Error", invalid_pages)
                            return
                        part = 1
                        start = 1
                        while start <= page_count:
                            end = min(start + pages_per - 1, page_count)
                            pages_in_part = end - start + 1
                            suffix = "页" if self.current_lang == "zh" else "pages"
                            part_display = f"  Part {part}: {start}-{end} ({pages_in_part} {suffix})"
                            self.preview_listbox.insert(tk.END, part_display)
                            start += pages_per
                            part += 1
                    except ValueError:
                        messagebox.showerror("Error", invalid_pages)

        except Exception as e:
            error_label = t("error")
            messagebox.showerror("Error", error_label.format(str(e)))

    def start_split(self):
        no_file_selected = t("no_file_selected")
        no_output_selected = t("no_output_selected")
        
        if not self.selected_files:
            messagebox.showwarning("Warning", no_file_selected)
            return

        if not self.output_dir:
            messagebox.showwarning("Warning", no_output_selected)
            return

        try:
            self.progress["maximum"] = len(self.selected_files)
            self.progress["value"] = 0
            processing_text = t("processing")
            self.status_label.config(text=processing_text)

            mode = self.split_mode.get()
            invalid_range = t("invalid_range")
            invalid_pages = t("invalid_pages")

            for i, filename in enumerate(self.selected_files):
                PDFProcessor.get_page_count(filename)

                if mode == "range":
                    ranges_str = self.range_entry.get()
                    ranges = PDFProcessor.parse_page_ranges(ranges_str)
                    if not ranges:
                        messagebox.showerror("Error", invalid_range)
                        return
                    PDFProcessor.split_by_ranges(filename, ranges, self.output_dir)
                else:
                    try:
                        pages_per = int(self.fixed_entry.get())
                        if pages_per <= 0:
                            messagebox.showerror("Error", invalid_pages)
                            return
                        PDFProcessor.split_by_fixed(filename, pages_per, self.output_dir)
                    except ValueError:
                        messagebox.showerror("Error", invalid_pages)
                        return

                self.progress["value"] = i + 1
                self.root.update_idletasks()

            success_text = t("success")
            self.status_label.config(text=success_text)
            messagebox.showinfo("Success", success_text)

        except Exception as e:
            error_label = t("error")
            messagebox.showerror("Error", error_label.format(str(e)))
            self.status_label.config(text="")


def main():
    root = tk.Tk()
    app = PDFSplitterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
