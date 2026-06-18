# gpa_calculator/data_handler.py
import pandas as pd
import os

def load_excel_data(file_path):
    """Membaca 3 sheet dari file Excel input"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} tidak ditemukan!")

    try:
        # Membaca masing-masing sheet sesuai spesifikasi
        subjects = pd.read_excel(file_path, sheet_name='subjects')
        students = pd.read_excel(file_path, sheet_name='students')
        raw_scores = pd.read_excel(file_path, sheet_name='raw_scores')
        return subjects, students, raw_scores
    except Exception as e:
        raise Exception(f"Gagal membaca sheet. Pastikan nama sheet sesuai: {e}")

def save_to_excel(df, output_path):
    """Menyimpan hasil laporan ke file Excel baru"""
    try:
        df.to_excel(output_path, index=False, sheet_name='GPA Report')
        print(f"[Sukses] Data berhasil disimpan di: {output_path}")
    except Exception as e:
        print(f"[Error] Gagal menyimpan file: {e}")