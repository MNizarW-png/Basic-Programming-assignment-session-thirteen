# main.py
import pandas as pd
from gpa_calculator.data_handler import load_excel_data, save_to_excel
from gpa_calculator.calculator import calculate_gpa
INPUT_FILE = "data_input.xlsx"

def show_data(df, title):
    print(f"\n=== DATA {title.upper()} ===")
    if df.empty:
        print("(Data Kosong)")
    else:
        print(df.to_string(index=True)) # Menampilkan index untuk memudahkan update/delete
    print("=" * 20)

def crud_menu(df, sheet_name, columns):
    while True:
        print(f"\n--- Menu CRUD: Sheet [{sheet_name}] ---")
        print("1. Tampilkan Data (Read)")
        print("2. Tambah Data Baru (Create)")
        print("3. Ubah Data (Update)")
        print("4. Hapus Data (Delete)")
        print("5. Kembali ke Menu Utama")

        pilihan = input("Pilih aksi (1-5): ").strip()

        if pilihan == '1':
            show_data(df, sheet_name)

        elif pilihan == '2':
            print(f"\n[CREATE] Tambah data baru untuk {sheet_name}:")
            new_row = {}
            for col in columns:
                val = input(f"Masukkan {col}: ").strip()
                # Konversi otomatis jika kolom berupa angka (seperti SKS, Score, ID)
                if val.isdigit():
                    val = int(val)
                new_row[col] = val

            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            print("🎉 Data berhasil ditambahkan secara sementara!")

        elif pilihan == '3':
            show_data(df, sheet_name)
            if df.empty: continue
            try:
                idx = int(input("\n[UPDATE] Masukkan nomor indeks baris yang ingin diubah: "))
                if idx in df.index:
                    print("*(Kosongkan/langsung Enter jika tidak ingin mengubah kolom tersebut)*")
                    for col in columns:
                        old_val = df.at[idx, col]
                        val = input(f"Ubah {col} ({old_val}) menjadi: ").strip()
                        if val:
                            if val.isdigit(): val = int(val)
                            df.at[idx, col] = val
                    print("🎉 Data berhasil diperbarui secara sementara!")
                else:
                    print("❌ Indeks tidak ditemukan!")
            except ValueError:
                print("❌ Input harus berupa angka indeks!")

        elif pilihan == '4':
            show_data(df, sheet_name)
            if df.empty: continue
            try:
                idx = int(input("\n[DELETE] Masukkan nomor indeks baris yang ingin dihapus: "))
                if idx in df.index:
                    df = df.drop(idx).reset_index(drop=True)
                    print("🎉 Data berhasil dihapus secara sementara!")
                else:
                    print("❌ Indeks tidak ditemukan!")
            except ValueError:
                print("❌ Input harus berupa angka indeks!")

        elif pilihan == '5':
            # Kembalikan dataframe yang sudah dimodifikasi
            return df
        else:
            print("❌ Pilihan tidak valid!")

def main():
    print("=" * 45)
    print("   APP GPA CALCULATOR dengan Fitur CRUD   ")
    print("=" * 45)

    # Load data awal
    try:
        subjects_df, students_df, scores_df = load_excel_data(INPUT_FILE)
    except FileNotFoundError:
        print(f"❌ File '{INPUT_FILE}' tidak ditemukan.")
        print("Silakan jalankan 'generate_dummy.py' terlebih dahulu untuk membuat data awal.")
        return
    except Exception as e:
        print(f"❌ Gagal memuat data: {e}")
        return

    while True:
        print("\n===== MENU UTAMA =====")
        print("1. Kelola Data Tabel 'subjects'")
        print("2. Kelola Data Tabel 'students'")
        print("3. Kelola Data Tabel 'raw_scores'")
        print("4. Hitung & Cetak Laporan GPA (Excel)")
        print("5. Keluar & Simpan Perubahan Data Input")

        pilihan_utama = input("Pilih menu (1-5): ").strip()

        if pilihan_utama == '1':
            subjects_df = crud_menu(subjects_df, 'subjects', ['kode subject', 'subject name', 'sks'])

        elif pilihan_utama == '2':
            students_df = crud_menu(students_df, 'students', ['student_id', 'student name', 'group'])

        elif pilihan_utama == '3':
            scores_df = crud_menu(scores_df, 'raw_scores', ['id', 'subject code', 'student id', 'score'])

        elif pilihan_utama == '4':
            print("\n[Proses] Menghitung GPA...")
            try:
                result_df = calculate_gpa(subjects_df, students_df, scores_df)
                print("\n--- PREVIEW LAPORAN GPA ---")
                print(result_df.to_string(index=False))
                print("---------------------------")

                output_file = "gpa_report_output.xlsx"
                save_to_excel(result_df, output_file)
            except Exception as e:
                print(f"❌ Gagal menghitung GPA, periksa kembali relasi data Anda: {e}")

        elif pilihan_utama == '5':
            print(f"\n[Proses] Menyimpan semua perubahan ke {INPUT_FILE}...")
            try:
                with pd.ExcelWriter(INPUT_FILE, engine='openpyxl') as writer:
                    subjects_df.to_excel(writer, sheet_name='subjects', index=False)
                    students_df.to_excel(writer, sheet_name='students', index=False)
                    scores_df.to_excel(writer, sheet_name='raw_scores', index=False)
                print("💾 Semua perubahan data input BERHASIL disimpan!")
            except Exception as e:
                print(f"❌ Gagal menyimpan data input: {e}")

            print("Terima kasih telah menggunakan aplikasi ini. Sampai jumpa!")
            break
        else:
            print("❌ Pilihan tidak valid!")

if __name__ == "__main__":
    main()