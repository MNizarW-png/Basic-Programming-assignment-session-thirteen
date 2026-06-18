# gpa_calculator/calculator.py
import pandas as pd

def score_to_grade_points(score):
    """Mengubah skor angka menjadi bobot nilai (skala 4.0)"""
    if score >= 85: return 4.0   # A
    elif score >= 75: return 3.0 # B
    elif score >= 60: return 2.0 # C
    elif score >= 50: return 1.0 # D
    else: return 0.0             # E

def calculate_gpa(subjects_df, students_df, scores_df):
    """Menghitung total SKS dan GPA untuk setiap mahasiswa"""

    # 1. Gabungkan data skor dengan sks matakuliah
    merged_scores = scores_df.merge(subjects_df, left_on='subject code', right_on='kode subject', how='left')

    # 2. Hitung bobot nilai untuk setiap skor angka
    merged_scores['grade_point'] = merged_scores['score'].apply(score_to_grade_points)

    # 3. Hitung (Bobot * SKS) untuk tiap baris nilai
    merged_scores['total_points'] = merged_scores['grade_point'] * merged_scores['sks']

    # 4. Agregasi total SKS dan total poin per mahasiswa
    student_summary = merged_scores.groupby('student id').agg(
        total_sks=('sks', 'sum'),
        grand_points=('total_points', 'sum')
    ).reset_index()

    # 5. Hitung GPA (Total Poin / Total SKS)
    student_summary['gpa'] = (student_summary['grand_points'] / student_summary['total_sks']).round(2)

    # 6. Gabungkan hasil akhir dengan data profil mahasiswa agar lengkap
    final_report = students_df.merge(student_summary, left_on='student_id', right_on='student id', how='left')

    # Hapus kolom bantuan yang tidak diperlukan di laporan akhir
    final_report = final_report.drop(columns=['student id', 'grand_points'])

    # Isi mahasiswa yang tidak punya nilai (NaN) dengan 0
    final_report['total_sks'] = final_report['total_sks'].fillna(0).astype(int)
    final_report['gpa'] = final_report['gpa'].fillna(0.0)

    return final_report