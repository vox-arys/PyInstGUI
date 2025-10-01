import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import threading
import os
import sys

def browse_file():
    filename = filedialog.askopenfilename(
        filetypes=[("Python files", "*.py;*.pyw")],
        title="Select a Python file"
    )
    if filename:
        file_path.set(filename)
        dist_path.set(os.path.dirname(filename))

def browse_icon():
    filename = filedialog.askopenfilename(
        filetypes=[("Icon files", "*.ico")],
        title="Select an Icon"
    )
    if filename:
        icon_path.set(filename)

def browse_folder(var):
    folder = filedialog.askdirectory(title="Select Folder")
    if folder:
        var.set(folder)

def run_pyinstaller():
    if not file_path.get():
        messagebox.showerror("Error", "Please select a Python file first.")
        return
    cmd = ["pyinstaller"]
    if onefile_var.get(): cmd.append("--onefile")
    if windowed_var.get(): cmd.append("--windowed")
    if noconfirm_var.get(): cmd.append("--noconfirm")
    if clean_var.get(): cmd.append("--clean")
    if ascii_var.get(): cmd.append("--ascii")
    if icon_path.get(): cmd.append(f"--icon={icon_path.get()}")
    if dist_path.get(): 
        cmd.append(f"--distpath={dist_path.get()}")
        final_dist = dist_path.get()
    else:
        final_dist = "dist"
    if work_path.get(): cmd.append(f"--workpath={work_path.get()}")
    if spec_path.get(): cmd.append(f"--specpath={spec_path.get()}")
    if noupx_var.get(): cmd.append("--noupx")
    if upx_dir.get(): cmd.append(f"--upx-dir={upx_dir.get()}")
    if add_data.get(): cmd.append(f"--add-data={add_data.get()}")
    if hidden_import.get(): cmd.append(f"--hidden-import={hidden_import.get()}")
    if additional_hooks.get(): cmd.append(f"--additional-hooks-dir={additional_hooks.get()}")
    if runtime_hooks.get(): cmd.append(f"--runtime-hook={runtime_hooks.get()}")
    if collect_submodules.get(): cmd.append(f"--collect-submodules={collect_submodules.get()}")
    if collect_data.get(): cmd.append(f"--collect-data={collect_data.get()}")
    if collect_binaries.get(): cmd.append(f"--collect-binaries={collect_binaries.get()}")
    if collect_all.get(): cmd.append(f"--collect-all={collect_all.get()}")
    if noconsole_var.get(): cmd.append("--noconsole")
    if debug_var.get(): cmd.append("--debug=all")
    cmd.append(file_path.get())
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, "Running: " + " ".join(cmd) + "\n")

    def run():
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            for line in process.stdout:
                output_box.insert(tk.END, line)
                output_box.see(tk.END)
            process.wait()

            if not keep_spec_var.get():
                spec_file = os.path.splitext(os.path.basename(file_path.get()))[0] + ".spec"
                spec_path_full = os.path.join(spec_path.get() if spec_path.get() else os.getcwd(), spec_file)
                if os.path.exists(spec_path_full):
                    os.remove(spec_path_full)

            os.startfile(final_dist)

            messagebox.showinfo("Done", f"PyInstaller finished.\nOutput folder opened:\n{final_dist}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    threading.Thread(target=run, daemon=True).start()

root = tk.Tk()
root.title("PyInstaller GUI")
root.geometry("850x790")

file_path = tk.StringVar()
icon_path = tk.StringVar()
dist_path = tk.StringVar()
work_path = tk.StringVar()
spec_path = tk.StringVar()
upx_dir = tk.StringVar()
add_data = tk.StringVar()
hidden_import = tk.StringVar()
additional_hooks = tk.StringVar()
runtime_hooks = tk.StringVar()
collect_submodules = tk.StringVar()
collect_data = tk.StringVar()
collect_binaries = tk.StringVar()
collect_all = tk.StringVar()
keep_spec_var = tk.BooleanVar()

onefile_var = tk.BooleanVar(value=True)
windowed_var = tk.BooleanVar()
noconfirm_var = tk.BooleanVar()
clean_var = tk.BooleanVar()
ascii_var = tk.BooleanVar()
noupx_var = tk.BooleanVar()
noconsole_var = tk.BooleanVar()
debug_var = tk.BooleanVar()

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

tk.Label(frame, text="Python File:").grid(row=0, column=0, sticky="w")
tk.Entry(frame, textvariable=file_path, width=50).grid(row=0, column=1)
tk.Button(frame, text="Browse", command=browse_file).grid(row=0, column=2)

tk.Label(frame, text="Icon (optional):").grid(row=1, column=0, sticky="w")
tk.Entry(frame, textvariable=icon_path, width=50).grid(row=1, column=1)
tk.Button(frame, text="Browse", command=browse_icon).grid(row=1, column=2)

tk.Label(frame, text="Dist path:").grid(row=2, column=0, sticky="w")
tk.Entry(frame, textvariable=dist_path, width=50).grid(row=2, column=1)
tk.Button(frame, text="Browse", command=lambda: browse_folder(dist_path)).grid(row=2, column=2)

tk.Label(frame, text="Work path:").grid(row=3, column=0, sticky="w")
tk.Entry(frame, textvariable=work_path, width=50).grid(row=3, column=1)
tk.Button(frame, text="Browse", command=lambda: browse_folder(work_path)).grid(row=3, column=2)

tk.Label(frame, text="Spec path:").grid(row=4, column=0, sticky="w")
tk.Entry(frame, textvariable=spec_path, width=50).grid(row=4, column=1)
tk.Button(frame, text="Browse", command=lambda: browse_folder(spec_path)).grid(row=4, column=2)

tk.Checkbutton(frame, text="Onefile (--onefile)", variable=onefile_var).grid(row=5, column=0, sticky="w")
tk.Checkbutton(frame, text="Windowed (--windowed)", variable=windowed_var).grid(row=5, column=1, sticky="w")
tk.Checkbutton(frame, text="No Confirm (--noconfirm)", variable=noconfirm_var).grid(row=5, column=2, sticky="w")
tk.Checkbutton(frame, text="Clean (--clean)", variable=clean_var).grid(row=6, column=0, sticky="w")
tk.Checkbutton(frame, text="ASCII (--ascii)", variable=ascii_var).grid(row=6, column=1, sticky="w")
tk.Checkbutton(frame, text="No UPX (--noupx)", variable=noupx_var).grid(row=6, column=2, sticky="w")
tk.Checkbutton(frame, text="No Console (--noconsole)", variable=noconsole_var).grid(row=7, column=0, sticky="w")
tk.Checkbutton(frame, text="Debug (--debug=all)", variable=debug_var).grid(row=7, column=1, sticky="w")
tk.Checkbutton(frame, text="Keep Spec", variable=keep_spec_var).grid(row=7, column=2, sticky="w")

def add_entry(label, var, row):
    tk.Label(frame, text=label).grid(row=row, column=0, sticky="w")
    tk.Entry(frame, textvariable=var, width=50).grid(row=row, column=1, columnspan=2, sticky="we")

add_entry("UPX Dir:", upx_dir, 8)
add_entry("Add Data (--add-data):", add_data, 9)
add_entry("Hidden Import:", hidden_import, 10)
add_entry("Additional Hooks Dir:", additional_hooks, 11)
add_entry("Runtime Hook:", runtime_hooks, 12)
add_entry("Collect Submodules:", collect_submodules, 13)
add_entry("Collect Data:", collect_data, 14)
add_entry("Collect Binaries:", collect_binaries, 15)
add_entry("Collect All:", collect_all, 16)

tk.Button(frame, text="Build EXE", command=run_pyinstaller, bg="lightgreen").grid(row=17, column=0, columnspan=3, pady=10)

output_box = tk.Text(frame, height=20, width=100)
output_box.grid(row=18, column=0, columnspan=3, pady=5)

root.mainloop()
