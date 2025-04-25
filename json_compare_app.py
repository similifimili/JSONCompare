import json
import tkinter as tk
from tkinter import messagebox, scrolledtext
from deepdiff import DeepDiff

def compare_json(json1_str, json2_str):
    try:
        obj1 = json.loads(json1_str)
        obj2 = json.loads(json2_str)
    except json.JSONDecodeError as e:
        return f"Invalid JSON: {e}"

    diff = DeepDiff(obj1, obj2, view='tree')
    if not diff:
        return "JSON objects match perfectly. ✅"

    diff_lines = []
    for item in diff:
        for detail in diff[item]:
            diff_lines.append(f"{item}: {detail.path()}\n  - {detail.t1} → {detail.t2}")

    return "\n".join(diff_lines)

def highlight_differences(json1_str, json2_str):
    try:
        obj1 = json.loads(json1_str)
        obj2 = json.loads(json2_str)
    except json.JSONDecodeError:
        return

    diff = DeepDiff(obj1, obj2, view='tree')
    if not diff:
        return

    for item in diff:
        for detail in diff[item]:
            path = detail.path()
            highlight_path(text1, path)
            highlight_path(text2, path)

def highlight_path(text_widget, path):
    # This function highlights the differences in the text widget based on the path
    start = "1.0"
    while True:
        pos = text_widget.search(path, start, stopindex=tk.END)
        if not pos:
            break
        end = f"{pos}+{len(path)}c"
        text_widget.tag_add("highlight", pos, end)
        start = end

def on_compare():
    json1 = text1.get("1.0", tk.END).strip()
    json2 = text2.get("1.0", tk.END).strip()
    result = compare_json(json1, json2)
    highlight_differences(json1, json2)
    if result == "JSON objects match perfectly. ✅":
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

def add_line_numbers(text_widget):
    line_numbers = tk.Text(root, width=4, padx=3, highlightthickness=0, bd=0, background='lightgrey', foreground='black', state='disabled')
    line_numbers.pack(side=tk.LEFT, fill=tk.Y)
    update_line_numbers(text_widget, line_numbers)
    text_widget.bind("<KeyRelease>", lambda event: update_line_numbers(text_widget, line_numbers))

def update_line_numbers(text_widget, line_numbers):
    line_numbers.config(state=tk.NORMAL)
    line_numbers.delete("1.0", tk.END)
    current_line = 1
    while True:
        line_info = text_widget.dlineinfo(f"{current_line}.0")
        if line_info is None:
            break
        line_numbers.insert(tk.END, f"{current_line}\n")
        current_line += 1
    line_numbers.config(state=tk.DISABLED)

# GUI Setup
root = tk.Tk()
root.title("JSON Compare Tool")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label1 = tk.Label(frame, text="JSON 1")
label1.grid(row=0, column=0)
label2 = tk.Label(frame, text="JSON 2")
label2.grid(row=0, column=1)

text1 = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=20)
text1.grid(row=1, column=0, padx=5)
text2 = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=20)
text2.grid(row=1, column=1, padx=5)

add_line_numbers(text1)
add_line_numbers(text2)

text1.tag_configure("highlight", background="yellow")
text2.tag_configure("highlight", background="yellow")

compare_btn = tk.Button(root, text="Compare JSON", command=on_compare)
compare_btn.pack(pady=10)

root.mainloop()
