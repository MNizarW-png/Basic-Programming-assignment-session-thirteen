# generate_dummy.py
import pandas as pd

# 1. Data untuk sheet 'subjects'
data_subjects = {
    'kode subject': ['CS101', 'CS102', 'MAT201'],
    'subject name': ['Intro to Programming', 'Database Systems', 'Calculus II'],
    'sks': [3, 4, 3]
}

# 2. Data untuk sheet 'students'
data_students = {
    'student_id': [1001, 1002, 1003],
    'student name': ['Ali Perkasa', 'Budi Santoso', 'Citra Lestari'],
    'group': ['A', 'A', 'B']
}

# 3. Data untuk sheet 'raw_scores'
data_raw_scores = {
    'id': [1, 2, 3, 4, 5, 6],
    'subject code': ['CS101', 'CS102', 'CS101', 'MAT201', 'CS102', 'MAT201'],
    'student id': [1001, 1001, 1002, 1002, 1003, 1003],
    'score': [88, 78, 60, 85, 45, 90] # Nilai angka mahasiswa
}

# Membuat DataFrames
df_subjects = pd.DataFrame(data_subjects)
df_students = pd.DataFrame(data_students)
df_scores = pd.DataFrame(data_raw_scores)

# Menyimpan ke satu file Excel dengan 3 sheet berbeda
with pd.ExcelWriter('data_input.xlsx', engine='openpyxl') as writer:
    df_subjects.to_excel(writer, sheet_name='subjects', index=False)
    df_students.to_excel(writer, sheet_name='students', index=False)
    df_scores.to_excel(writer, sheet_name='raw_scores', index=False)

print("✅ File 'data_input.xlsx' berhasil dibuat otomatis dengan data contoh!")