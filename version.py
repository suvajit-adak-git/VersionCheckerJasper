import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def compare_files():
    # Hide main window
    root.withdraw()

    # Prompt for the first file
    file1_path = filedialog.askopenfilename(
        title="Select the first Excel file (TC.xlsm)",
        filetypes=[("Excel Files", "*.xlsm *.xlsx *.xls")]
    )
    if not file1_path:
        messagebox.showerror("Error", "No file selected for the first Excel file.")
        return

    # Load the first Excel file
    xls1 = pd.ExcelFile(file1_path)
    df1 = xls1.parse("General", dtype=str)

    # Extract values that start with "CL " from any cell in the sheet
    cl_values = set()
    for col in df1.columns:
        cl_values.update(df1[col].dropna().astype(str).str.strip())

    cl_values = {val.replace("CL ", "").strip() for val in cl_values if val.startswith("CL ")}

    # No trimming now
    normalized_cl_values = cl_values

    # Prompt for the second file
    file2_path = filedialog.askopenfilename(
        title="Select the second Excel file (CIA.xlsm)",
        filetypes=[("Excel Files", "*.xlsm *.xlsx *.xls")]
    )
    if not file2_path:
        messagebox.showerror("Error", "No file selected for the second Excel file.")
        return

    # Load the second Excel file
    df2 = pd.read_excel(file2_path, sheet_name="HLR Change and Impact", header=3, dtype=str)

    hlr_id_col = "New HLR ID"
    if hlr_id_col in df2.columns:
        hlr_values = set(df2[hlr_id_col].dropna().astype(str).str.strip())
    else:
        messagebox.showerror("Error", "'New HLR ID' column not found in the second file.")
        return

    normalized_hlr_values = hlr_values

    # Prepare comparison results
    results = []
    for cl in normalized_cl_values:
        status = "OK" if cl in normalized_hlr_values else "NOK"
        results.append(f"{cl} - {status}")

    # Show results in a message box
    if results:
        result_text = "\n".join(results)
        messagebox.showinfo("Comparison Results", result_text)
    else:
        messagebox.showinfo("Comparison Results", "No CL values found to compare.")

# GUI setup
root = tk.Tk()
root.title("HLR Version comparison Tool")
root.geometry("300x150")

label = tk.Label(root, text="HLR version Compare",)
label.pack(pady=20)

compare_button = tk.Button(root, text="Select Files and Compare", command=compare_files,bg="lightblue", fg="black", font=("Arial", 14))
compare_button.pack(pady=10)

root.mainloop()
