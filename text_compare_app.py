import tkinter as tk
from tkinter import messagebox, scrolledtext
from difflib import unified_diff

class LineNumberText(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.text = tk.Text(self, *args, **kwargs)
        self.linenumbers = tk.Text(self, width=4, padx=3, highlightthickness=0, bd=0, background='lightgrey', foreground='black', state='disabled')
        self.linenumbers.pack(side=tk.LEFT, fill=tk.Y)
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.text.bind("<KeyRelease>", self.update_line_numbers)
        self.update_line_numbers()

    def update_line_numbers(self, event=None):
        self.linenumbers.config(state=tk.NORMAL)
        self.linenumbers.delete("1.0", tk.END)
        current_line = 1
        while True:
            line_info = self.text.dlineinfo(f"{current_line}.0")
            if line_info is None:
                break
            self.linenumbers.insert(tk.END, f"{current_line}\n")
            current_line += 1
        self.linenumbers.config(state=tk.DISABLED)

def compare_text(text1_str, text2_str):
    diff = unified_diff(text1_str.splitlines(), text2_str.splitlines(), lineterm='')
    diff_lines = list(diff)
    if not diff_lines:
        return "Text objects match perfectly. ✅"

    return "\n".join(diff_lines)

def highlight_differences(text1_str, text2_str):
    diff = unified_diff(text1_str.splitlines(), text2_str.splitlines(), lineterm='')
    diff_lines = list(diff)
    if not diff_lines:
        return
    for line in diff_lines:
        if line.startswith('- '):
            highlight_line(text1.text, line[2:])
        elif line.startswith('+ '):
            highlight_line(text2.text, line[2:])

def highlight_line(text_widget, line):
    start = "1.0"
    while True:
        pos = text_widget.search(line, start, stopindex=tk.END)
        if not pos:
            break
        end = f"{pos}+{len(line)}c"
        text_widget.tag_add("highlight", pos, end)
        start = end

def on_compare():
    text1_str = text1.text.get("1.0", tk.END).strip()
    text2_str = text2.text.get("1.0", tk.END).strip()
    result = compare_text(text1_str, text2_str)
    highlight_differences(text1_str, text2_str)
    if result == "Text objects match perfectly. ✅":
        messagebox.showinfo("Result", result)
    else:
        result_window = tk.Toplevel(root)
        result_window.title("Differences")
        diff_text = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, width=100, height=30)
        diff_text.pack(padx=10, pady=10)
        diff_text.insert(tk.END, result)
        diff_text.config(state=tk.DISABLED)

        # Save results to a file
        with open("comparison_results.txt", "w") as file:
            file.write(result)

# GUI Setup
root = tk.Tk()
root.title("Text Compare Tool")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label1 = tk.Label(frame, text="Text 1")
label1.grid(row=0, column=0)
label2 = tk.Label(frame, text="Text 2")
label2.grid(row=0, column=1)

text1 = LineNumberText(frame, wrap=tk.WORD, width=50, height=20)
text1.grid(row=1, column=0, padx=5)
text2 = LineNumberText(frame, wrap=tk.WORD, width=50, height=20)
text2.grid(row=1, column=1, padx=5)

text1.text.tag_configure("highlight", background="yellow")
text2.text.tag_configure("highlight", background="yellow")

compare_btn = tk.Button(root, text="Compare Text", command=on_compare)
compare_btn.pack(pady=10)

root.mainloop()
