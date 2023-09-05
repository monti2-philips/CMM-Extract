import extract
import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog


def convert_name_2_excel(file_path):
    base_name = os.path.basename(file_path).split('.')[0]
    download_path = os.path.join(os.getenv('USERPROFILE'), 'Downloads')
    excel_path = os.path.join(download_path, base_name + '.xlsx')
    return excel_path


def run_offsets():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title='Select OFS File', filetypes=[('OFS', '.ofs')])

    tool_offset_excel_path = convert_name_2_excel(file_path)
    df = pd.read_table(file_path, sep=r"\n",
                       header=None, engine='python', names=['header'])

    with pd.ExcelWriter(tool_offset_excel_path) as writer:
        extract.extract_tools(df).to_excel(writer, sheet_name="Tool Offsets")
        extract.extract_offsets(df).to_excel(writer, sheet_name="Wear Offsets")

    print(f'OFFSET DATA STORED AT: {tool_offset_excel_path}')


def run_CMM():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title='Select CSV File', filetypes=[('CSV', '.csv')])

    cmm_excel_path = convert_name_2_excel(file_path)
    df = pd.read_csv(file_path)

    with pd.ExcelWriter(cmm_excel_path) as writer:
        extract.extract_CMM(df).to_excel(writer, sheet_name=os.path.basename(
            cmm_excel_path).split('.')[0], index=False)

    print(f'CMM DATA STORED AT: {cmm_excel_path}')


if __name__ == "__main__":
    choice = int(input(
        "[1] Run Tool/Wear Offsets Only\n[2] Run CMM Only\n[3] Run Both\nSELECTION: "))

    if choice == 1:
        run_offsets()
    elif choice == 2:
        run_CMM()
    elif choice == 3:
        run_offsets()
        run_CMM()
    else:
        print('Try Again, selected choice was not an option.')
