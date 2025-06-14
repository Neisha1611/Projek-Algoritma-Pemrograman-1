import csv
import os
from datetime import datetime
from tabulate import tabulate

# Global variable untuk menyimpan username yang login
usernamelogin = ""

# ==================== FUNGSI UTILITAS ====================

def cekakun():
    """Membuat file akun.csv jika belum ada"""
    if not os.path.exists('akun.csv'):
        with open('akun.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Username', 'Password'])

def load_data_csv(file_path):
    """Load data dari file CSV"""
    if not os.path.exists(file_path):
        print(f"File '{file_path}' tidak ditemukan.")
        print(f"Pastikan file CSV sudah dibuat dengan nama yang tepat.")
        return []
    data = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'biaya' in row:
                    row['biaya'] = int(row['biaya'])
                if 'rating' in row:
                    row['rating'] = float(row['rating'])  # Tetap float untuk mendukung desimal
                data.append(row)
                
    except FileNotFoundError:
        print(f"File '{file_path}' tidak ditemukan.")
    except ValueError as e:
        print(f"Error dalam format data: {e}")
    return data

def simpan_data_csv(file_path, data, fieldnames):
    """Simpan data ke file CSV"""
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# ==================== ALGORITMA SELECTION SORT ====================

def selection_sort_rating_desc(data_list, key_func):
    """Selection sort untuk mengurutkan berdasarkan rating tertinggi"""
    n = len(data_list)
    for i in range(n):
        max_idx = i
        for j in range(i + 1, n):
            if key_func(data_list[j]) > key_func(data_list[max_idx]):
                max_idx = j
        data_list[i], data_list[max_idx] = data_list[max_idx], data_list[i]
    return data_list

def selection_sort_total_rating_desc(rekomendasi_list):
    """Selection sort untuk mengurutkan rekomendasi berdasarkan total rating tertinggi"""
    n = len(rekomendasi_list)
    for i in range(n):
        max_idx = i
        for j in range(i + 1, n):
            if rekomendasi_list[j]['total_rating'] > rekomendasi_list[max_idx]['total_rating']:
                max_idx = j
        rekomendasi_list[i], rekomendasi_list[max_idx] = rekomendasi_list[max_idx], rekomendasi_list[i]
    return rekomendasi_list

# ==================== FUNGSI RATING ====================

def simpan_rating(username, kota, tipe_tempat, nama_tempat, rating_baru):
    """Simpan rating yang diberikan customer"""
    now = datetime.now()
    
    # Cek apakah file rating sudah ada
    file_exists = os.path.exists('rating_history.csv')
    
    with open('rating_history.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['username', 'tanggal', 'waktu', 'kota', 'tipe_tempat', 'nama_tempat', 'rating_diberikan'])
        
        writer.writerow([
            username,
            now.strftime('%Y-%m-%d'),
            now.strftime('%H:%M'),
            kota,
            tipe_tempat,
            nama_tempat,
            rating_baru
        ])

def update_rating_tempat(file_path, nama_tempat, rating_baru):
    """Update rating di file CSV dengan rata-rata rating lama dan baru"""
    data = load_data_csv(file_path)
    
    for item in data:
        if item['nama'].lower() == nama_tempat.lower():
            # Hitung rating baru = (rating lama + rating baru) / 2
            rating_lama = float(item['rating'])
            rating_terbaru = (rating_lama + rating_baru) / 2
            item['rating'] = round(rating_terbaru, 1)  # Bulatkan ke 1 desimal
            
            # Simpan kembali ke file
            fieldnames = list(data[0].keys()) if data else ['nama', 'biaya', 'rating']
            simpan_data_csv(file_path, data, fieldnames)
            return rating_terbaru
    
    return None

def beri_rating():
    """Fungsi untuk customer memberikan rating"""
    print('==================================================')
    print('              BERIKAN RATING TEMPAT               ')
    print('==================================================')
    print('Kota yang tersedia: Ubud, Gianyar, Buleleng, Jimbaran, Denpasar, Uluwatu, Seminyak, Canggu, Nusadua, Tabanan')
    
    kota = input("Masukkan kota: ").strip()
    
    print("\nPilih tipe tempat:")
    print("1. Hotel")
    print("2. Wisata")
    
    while True:
        pilih_tipe = input("Pilih (1/2): ")
        if pilih_tipe == '1':
            tipe_tempat = 'hotel'
            file_path = f"hotel_{kota.lower()}.csv"
            break
        elif pilih_tipe == '2':
            tipe_tempat = 'wisata'
            file_path = f"wisata_{kota.lower()}.csv"
            break
        else:
            print("Pilihan tidak valid.")
    
    # Load data tempat
    data_tempat = load_data_csv(file_path)
    
    if not data_tempat:
        print(f"Data {tipe_tempat} untuk kota '{kota}' tidak ditemukan.")
        return
    
    print(f"\nDaftar {tipe_tempat.title()} di {kota.title()}:")
    for i, tempat in enumerate(data_tempat, 1):
        print(f"{i}. {tempat['nama']} - Rating saat ini: {tempat['rating']}/5")
    
    while True:
        try:
            pilih_tempat = int(input(f"\nPilih {tipe_tempat} (1-{len(data_tempat)}): ")) - 1
            if 0 <= pilih_tempat < len(data_tempat):
                break
            else:
                print("Nomor tidak valid.")
        except ValueError:
            print("Input harus berupa angka.")
    
    tempat_terpilih = data_tempat[pilih_tempat]
    
    print(f"\nAnda akan memberikan rating untuk: {tempat_terpilih['nama']}")
    print(f"Rating saat ini: {tempat_terpilih['rating']}/5")
    
    while True:
        try:
            rating_baru = float(input("Berikan rating Anda (1.0-5.0): "))
            if 1.0 <= rating_baru <= 5.0:
                break
            else:
                print("Rating harus antara 1.0-5.0")
        except ValueError:
            print("Rating harus berupa angka (contoh: 4.5)")
    
    # Konfirmasi
    konfirmasi = input(f"Yakin memberikan rating {rating_baru} untuk {tempat_terpilih['nama']}? (y/t): ").lower()
    
    if konfirmasi == 'y':
        # Update rating di file CSV
        rating_terbaru = update_rating_tempat(file_path, tempat_terpilih['nama'], rating_baru)
        
        if rating_terbaru:
            # Simpan ke history rating
            simpan_rating(usernamelogin, kota, tipe_tempat, tempat_terpilih['nama'], rating_baru)
            
            print(f"\nRating berhasil diberikan!")
            print(f"Rating lama: {tempat_terpilih['rating']}")
            print(f"Rating yang Anda berikan: {rating_baru}")
            print(f"Rating terbaru: {rating_terbaru:.1f}")
        else:
            print("Gagal mengupdate rating.")
    else:
        print("Rating dibatalkan.")
    
    input('\nTekan Enter untuk kembali...')

def lihat_history_rating():
    """Admin melihat siapa saja yang sudah memberikan rating"""
    print('==================================================')
    print('              HISTORY RATING CUSTOMER             ')
    print('==================================================')
    
    try:
        with open('rating_history.csv', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            history_data = list(reader)
            
            if not history_data:
                print('Belum ada customer yang memberikan rating.')
                return
            
            # Group by kota untuk tampilan yang lebih rapi
            kota_group = {}
            for row in history_data:
                kota = row['kota']
                if kota not in kota_group:
                    kota_group[kota] = []
                kota_group[kota].append(row)
            
            print(f"Total rating yang diberikan: {len(history_data)}")
            print("="*80)
            
            for kota, ratings in kota_group.items():
                print(f"\n🏙️  KOTA: {kota.upper()}")
                print("-" * 60)
                
                for i, rating in enumerate(ratings, 1):
                    print(f"{i}. Customer: {rating['username']}")
                    print(f"   Tanggal: {rating['tanggal']} {rating['waktu']}")
                    print(f"   Tempat: {rating['nama_tempat']} ({rating['tipe_tempat'].title()})")
                    print(f"   Rating diberikan: {rating['rating_diberikan']}/5")
                    print("-" * 40)
            
            # Statistik
            print(f"\n📊 STATISTIK:")
            unique_customers = set(row['username'] for row in history_data)
            print(f"Jumlah customer yang memberikan rating: {len(unique_customers)}")
            
            avg_rating = sum(float(row['rating_diberikan']) for row in history_data) / len(history_data)
            print(f"Rata-rata rating yang diberikan: {avg_rating:.1f}/5")
            
    except FileNotFoundError:
        print('Belum ada customer yang memberikan rating.')
    except Exception as e:
        print(f'Terjadi kesalahan saat membaca data rating: {e}')

# ==================== ALGORITMA KNAPSACK ====================

def knapsack_01(wisata_list, max_budget):
    """Algoritma Knapsack 0/1 untuk memilih wisata optimal"""
    n = len(wisata_list)
    if n == 0 or max_budget <= 0:
        return []
    
    # DP table
    dp = [[0 for _ in range(max_budget + 1)] for _ in range(n + 1)]
    
    # Fill DP table
    for i in range(1, n + 1):
        biaya = wisata_list[i-1]['biaya']
        rating = wisata_list[i-1]['rating']
        for w in range(max_budget + 1):
            if biaya <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - biaya] + rating)
            else:
                dp[i][w] = dp[i-1][w]

    # Backtrack untuk menemukan item yang dipilih
    selected = []
    w = max_budget
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected.append(wisata_list[i-1])
            w -= wisata_list[i-1]['biaya']
    
    return selected[::-1]  # Reverse untuk urutan yang benar

# ==================== FUNGSI REKOMENDASI ====================

def rekomendasi_paket(kota, budget):
    """Generate rekomendasi paket wisata berdasarkan kota dan budget"""
    hotel_file = f"hotel_{kota.lower()}.csv"
    wisata_file = f"wisata_{kota.lower()}.csv"
    
    hotel_list = load_data_csv(hotel_file)
    wisata_list = load_data_csv(wisata_file)

    if not hotel_list:
        print(f"Data hotel untuk kota '{kota}' tidak ditemukan.")
        return []
    
    if not wisata_list:
        print(f"Data wisata untuk kota '{kota}' tidak ditemukan.")
        return []

    rekomendasi = []
    
    # Sort hotel berdasarkan rating tertinggi menggunakan selection sort
    hotel_list_sorted = selection_sort_rating_desc(hotel_list.copy(), lambda x: x['rating'])
    
    for hotel in hotel_list_sorted:
        sisa_budget = budget - hotel['biaya']
        if sisa_budget <= 0:
            continue
            
        # Pilih wisata menggunakan knapsack
        wisata_terpilih = knapsack_01(wisata_list, sisa_budget)
        
        if len(wisata_terpilih) >= 3:  # Minimal 3 tempat wisata
            total_biaya = hotel['biaya'] + sum(w['biaya'] for w in wisata_terpilih)
            total_rating = hotel['rating'] + sum(w['rating'] for w in wisata_terpilih)
            
            rekomendasi.append({
                'hotel': hotel,
                'wisata': wisata_terpilih,
                'total_biaya': total_biaya,
                'total_rating': total_rating
            })

    # Sort berdasarkan total rating tertinggi menggunakan selection sort
    rekomendasi_sorted = selection_sort_total_rating_desc(rekomendasi)
    return rekomendasi_sorted[:5]  # Ambil 5 rekomendasi terbaik

def simpan_riwayat(username, kota, paket):
    """Simpan riwayat paket yang dipilih"""
    now = datetime.now()
    
    # Cek apakah file riwayat sudah ada
    file_exists = os.path.exists('riwayat.csv')
    
    with open('riwayat.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['username', 'tanggal', 'waktu', 'kota', 'hotel', 'biaya_hotel', 'rating_hotel', 'destinasi', 'total_biaya', 'total_rating'])
        
        destinasi_str = ';'.join([f"{w['nama']} (Rp{w['biaya']}, Rating:{w['rating']})" for w in paket['wisata']])
        writer.writerow([
            username,
            now.strftime('%Y-%m-%d'), 
            now.strftime('%H:%M'), 
            kota, 
            paket['hotel']['nama'], 
            paket['hotel']['biaya'],
            paket['hotel']['rating'],
            destinasi_str, 
            paket['total_biaya'],
            paket['total_rating']
        ])

def lihat_riwayat(username):
    """Lihat riwayat paket berdasarkan username dengan format tabel untuk destinasi"""
    try:
        with open('riwayat.csv', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            riwayat_user = [row for row in reader if row['username'] == username]
            
            if not riwayat_user:
                print('\nBelum ada riwayat yang tersimpan.')
                return
                
            print('\n' + '='*80)
            print('RIWAYAT PAKET WISATA'.center(80))
            print('='*80)
            
            for i, row in enumerate(riwayat_user, 1):
                print(f"\n📅 RIWAYAT #{i}")
                print(f"Tanggal & Waktu : {row['tanggal']} {row['waktu']}")
                print(f"Kota Tujuan     : {row['kota'].title()}")
                print(f"Hotel           : {row['hotel']}")
                print(f"Biaya Hotel     : Rp {int(row['biaya_hotel']):,}")
                print(f"Rating Hotel    : {row['rating_hotel']}/5")
                
                # Parse destinasi dan buat tabel
                destinasi_str = row['destinasi']
                destinasi_list = []
                
                # Split berdasarkan ';' untuk setiap destinasi
                for dest in destinasi_str.split(';'):
                    if dest.strip():  # Pastikan tidak kosong
                        # Extract nama, biaya, dan rating dari string seperti:
                        # "Nama Tempat (Rp123456, Rating:4.5)"
                        try:
                            # Pisahkan nama dan bagian dalam kurung
                            nama_part = dest.split(' (')[0].strip()
                            detail_part = dest.split(' (')[1].replace(')', '')
                            
                            # Extract biaya (hapus 'Rp' dan ambil angka)
                            biaya_part = detail_part.split(', ')[0].replace('Rp', '').strip()
                            biaya = int(biaya_part)
                            
                            # Extract rating
                            rating_part = detail_part.split('Rating:')[1].strip()
                            rating = float(rating_part)
                            
                            destinasi_list.append([
                                nama_part,
                                f"Rp {biaya:,}",
                                f"{rating}/5"
                            ])
                        except (IndexError, ValueError) as e:
                            # Jika parsing gagal, tampilkan data asli
                            destinasi_list.append([dest.strip(), "-", "-"])
                
                # Tampilkan tabel destinasi
                if destinasi_list:
                    print("\nDestinasi Wisata:")
                    headers = ["Nama Tempat", "Biaya", "Rating"]
                    print(tabulate(destinasi_list, headers=headers, tablefmt="grid"))
                
                print(f"\n💰 TOTAL BIAYA   : Rp {int(row['total_biaya']):,}")
                print(f"⭐ TOTAL RATING  : {float(row['total_rating'])}")
                print('-' * 80)
                
    except FileNotFoundError:
        print('\nBelum ada riwayat yang tersimpan.')
    except Exception as e:
        print(f'\nTerjadi kesalahan saat membaca riwayat: {e}')

# ==================== FUNGSI LOGIN & REGISTER ====================

def login():
    """Fungsi login untuk customer"""
    global usernamelogin
    os.system('cls' if os.name == 'nt' else 'clear')
    print('==================================================')
    print('                   LOGIN CUSTOMER                 ')
    print('==================================================')
    cekakun()
    username = input('Masukkan Username : ')
    password = input('Masukkan Password : ')

    loginsukses = False
    with open('akun.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Username'] == username and row['Password'] == password:
                loginsukses = True
                break

    if loginsukses:
        usernamelogin = username
        print('Login berhasil.')
        input('Tekan Enter untuk melanjutkan.')
        os.system('cls' if os.name == 'nt' else 'clear')
        menu_pengguna()
    else:
        print('Username atau Password salah.')
        input('Tekan Enter untuk mencoba lagi.')
        tampilanawal()

def register():
    """Fungsi register untuk customer baru"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print('==================================================')
    print('                    REGISTER                      ')
    print('==================================================')
    cekakun()
    
    # Load existing usernames
    with open('akun.csv', mode='r') as file:
        username_sama = {row['Username'] for row in csv.DictReader(file)}
    
    while True:
        username = input('Daftarkan Username anda : ')
        if len(username) < 2:
            print('Username minimal 2 huruf.')
            continue
        elif username in username_sama:
            print('Username sudah digunakan!')
            continue
        else:
            break
    
    while True:
        password = input('Masukkan Kata Sandi (minimal 8 karakter): ')
        if len(password) < 8:
            print('Password minimal 8 karakter.')
            continue
        else:
            break
    
    while True:
        cek = input('Apakah nama user dan password sudah sesuai (y/t): ').lower()
        if cek == 'y':
            with open('akun.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([username, password])
            print('Registrasi berhasil! Silahkan login.')
            input('Tekan Enter untuk melanjutkan.')
            tampilanawal()
            break
        elif cek == 't':
            register()
            break
        else:
            print('Input invalid, ulangi.')

def loginadmin():
    """Fungsi login untuk admin"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print('==================================================')
    print('                   LOGIN ADMIN                    ')
    print('==================================================')
    
    # Buat file admin jika belum ada
    if not os.path.exists('admin.csv'):
        with open('admin.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Username', 'Password'])
            writer.writerow(['admin', 'admin123'])

    username = input('Masukkan Username : ')
    password = input('Masukkan Password : ')

    login_sukses = False
    with open('admin.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Username'] == username and row['Password'] == password:
                login_sukses = True
                break

    if login_sukses:
        print("Login Admin Berhasil")
        input('Tekan Enter Untuk Melanjutkan')
        os.system('cls' if os.name == 'nt' else 'clear')
        menu_admin()
    else:
        print('Username atau Password salah')
        while True:
            cek = input('Apakah anda ingin melanjutkan (y/t) : ').lower()
            if cek == 'y':
                loginadmin()
                break
            elif cek == 't':
                tampilanawal()
                break
            else:
                print('Input invalid')

# ==================== MENU PENGGUNA ====================

def menu_pengguna():
    """Menu utama untuk customer"""
    while True:
        print('===========================================================')
        print('           SELAMAT DATANG DI SISTEM REKOMENDASI            ')
        print('          PAKET WISATA DENGAN OPTIMALISASI BUDGET          ')
        print('===========================================================')
        print(f'Selamat datang, {usernamelogin}!')
        print('Silahkan pilih menu yang anda butuhkan:')
        print("1. Cari Rekomendasi Paket Wisata")
        print("2. Lihat Riwayat Paket")
        print("3. Berikan Rating Hotel/Wisata")
        print('4. Lihat hotel yang tersedia')
        print('5. LIhat Destinasi tempat wisata')
        print("6. Logout")
        
        pilihan = input("Pilih menu (1/2/3/4): ")

        if pilihan == '1':
            cari_rekomendasi()
        elif pilihan == '2':
            lihat_riwayat(usernamelogin)
            input('\nTekan Enter untuk kembali ke menu...')
        elif pilihan == '3':
            beri_rating()
        elif pilihan == '4':
            kota = pilih_kota()
            if kota:
                file_path = f"hotel_{kota}.csv"
                tipe_data = 'HOTEL'
                lihat_data(file_path, tipe_data)
                input('Tekan Enter untuk melanjutkan...')
        elif pilihan == '5':
            kota = pilih_kota()
            if kota:
                file_path = f"wisata_{kota}.csv"
                tipe_data = 'WISATA'
                lihat_data(file_path, tipe_data)
                input('Tekan Enter untuk melanjutkan...')
        elif pilihan == '6':
            print('Logout berhasil.')
            input('Tekan Enter untuk kembali ke menu utama.')
            tampilanawal()
            break
        else:
            print("Pilihan tidak valid.")
            input('Tekan Enter untuk melanjutkan...')

def cari_rekomendasi():
    """Fungsi untuk mencari rekomendasi paket wisata"""
    print('==================================================')
    print('          CARI REKOMENDASI PAKET WISATA           ')
    print('==================================================')
    print('Kota yang tersedia: Ubud, Gianyar, Buleleng, Jimbaran, Denpasar, Uluwatu, Seminyak, Canggu, Nusadua, Tabanan')
    kota = input("Masukkan kota tujuan: ").strip()
    
    try:
        budget = int(input("Masukkan budget Anda: Rp "))
        if budget <= 0:
            print("Budget harus lebih dari 0.")
            return
    except ValueError:
        print("Input budget harus berupa angka.")
        return

    print(f"\nMencari rekomendasi untuk kota {kota.title()} dengan budget Rp {budget:,}")
    
    # Debug: tampilkan nama file yang dicari
    hotel_file = f"hotel_{kota.lower()}.csv"
    wisata_file = f"wisata_{kota.lower()}.csv"
    print(f"Mencari file: {hotel_file} dan {wisata_file}")
    
    print("Cek file hotel:", os.path.exists(hotel_file))
    print("Cek file wisata:", os.path.exists(wisata_file))
    
    paket_list = rekomendasi_paket(kota, budget)
    
    if not paket_list:
        print("Tidak ditemukan paket yang sesuai dengan budget Anda.")
        print("\nPastikan file CSV sudah dibuat dengan format:")
        print(f"- {hotel_file}")
        print(f"- {wisata_file}")
        input('Tekan Enter untuk kembali...')
        return

    print(f"\nDitemukan {len(paket_list)} rekomendasi paket:")
    print("="*80)
    
    for i, paket in enumerate(paket_list, 1):
        print(f"\nPAKET REKOMENDASI #{i}")
        print(f"Hotel: {paket['hotel']['nama']}")
        print(f"Biaya Hotel: Rp {paket['hotel']['biaya']:,}")
        print(f"Rating Hotel: {paket['hotel']['rating']}/5")
        print(f"Tempat Wisata ({len(paket['wisata'])} destinasi):")
        
        for j, wisata in enumerate(paket['wisata'], 1):
            print(f"  {j}. {wisata['nama']} - Rp {wisata['biaya']:,} (Rating: {wisata['rating']}/5)")
        
        print(f"TOTAL BIAYA: Rp {paket['total_biaya']:,}")
        print(f"TOTAL RATING: {paket['total_rating']:.1f}")  # Format dengan 1 desimal
        print("-" * 60)

    while True:
        pilih = input(f"\nSimpan paket ke riwayat? (1-{len(paket_list)} atau 0 untuk batal): ")
        if pilih == '0':
            break
        elif pilih.isdigit() and 1 <= int(pilih) <= len(paket_list):
            paket_terpilih = paket_list[int(pilih)-1]
            simpan_riwayat(usernamelogin, kota, paket_terpilih)
            print("Paket berhasil disimpan ke riwayat.")
            break
        else:
            print("Pilihan tidak valid.")
    
    input('Tekan Enter untuk kembali...')

# ==================== MENU ADMIN ====================

def pilih_kota():
    """Fungsi untuk memilih kota"""
    kota_list = ['Ubud', 'Gianyar', 'Buleleng', 'Jimbaran', 'Denpasar', 'Uluwatu', 'Seminyak', 'Canggu', 'Nusa Dua', 'Tabanan']
    print('\nPilih Kota:')
    for i, kota in enumerate(kota_list, 1):
        print(f"{i}. {kota}")
    
    while True:
        pilihan = input("Pilih kota (1-10): ")
        if pilihan.isdigit() and 1 <= int(pilihan) <= len(kota_list):
            return kota_list[int(pilihan) - 1].lower()
        else:
            print("Pilihan tidak valid.")

def tambah_data(file_path, fieldnames, tipe_data):
    """Tambah data baru"""
    judul = f'TAMBAH DATA {tipe_data.upper()}' 
    print('==================================================')
    print(judul.center(50))
    print('==================================================')
    data = load_data_csv(file_path)
    
    new_entry = {}
    for field in fieldnames:
        if field == 'biaya':
            while True:
                try:
                    value = int(input(f"Masukkan {field}: "))
                    new_entry[field] = value
                    break
                except ValueError:
                    print(f"{field} harus berupa angka.")
        elif field == 'rating':
            while True:
                try:
                    value = float(input(f"Masukkan {field} (0.0-5.0): "))
                    if not (0.0 <= value <= 5.0):
                        print("Rating harus antara 0.0-5.0")
                        continue
                    new_entry[field] = value
                    break
                except ValueError:
                    print("Rating harus berupa angka (bisa desimal, contoh: 4.5)")
        else:
            new_entry[field] = input(f"Masukkan {field}: ")
    
    data.append(new_entry)
    simpan_data_csv(file_path, data, fieldnames)
    print(f"Data {tipe_data} berhasil ditambahkan.")

def edit_data(file_path, fieldnames, tipe_data):
    """Edit data yang sudah ada"""
    judul = f'EDIT DATA {tipe_data.upper()}' 
    print('==================================================')
    print(judul.center(50))
    print('==================================================')
    data = load_data_csv(file_path)
    
    if not data:
        print("Data kosong.")
        return
    
    print("Data yang tersedia:")
    for i, item in enumerate(data, 1):
        print(f"{i}. {item['nama']} - Rp {item['biaya']:,} (Rating: {item['rating']})")
    
    while True:
        try:
            idx = int(input("Pilih nomor data yang akan diedit: ")) - 1
            if 0 <= idx < len(data):
                break
            else:
                print("Nomor tidak valid.")
        except ValueError:
            print("Input harus berupa angka.")
    
    print(f"\nMengedit data: {data[idx]['nama']}")
    for field in fieldnames:
        current_value = data[idx][field]
        if field == 'biaya':
            while True:
                new_val = input(f"{field} ({current_value}): ")
                if new_val == "":
                    break
                try:
                    new_val = int(new_val)
                    data[idx][field] = new_val
                    break
                except ValueError:
                    print(f"{field} harus berupa angka.")
        elif field == 'rating':
            while True:
                new_val = input(f"{field} ({current_value}) - masukkan 0.0-5.0: ")
                if new_val == "":
                    break
                try:
                    new_val = float(new_val)
                    if not (0.0 <= new_val <= 5.0):
                        print("Rating harus antara 0.0-5.0")
                        continue
                    data[idx][field] = new_val
                    break
                except ValueError:
                    print("Rating harus berupa angka (bisa desimal, contoh: 4.5)")
        else:
            new_val = input(f"{field} ({current_value}): ")
            if new_val:
                data[idx][field] = new_val
    
    simpan_data_csv(file_path, data, fieldnames)
    print(f"Data {tipe_data} berhasil diedit.")

def hapus_data(file_path, fieldnames, tipe_data):
    """Hapus data"""
    judul = f'HAPUS DATA {tipe_data.upper()}' 
    print('==================================================')
    print(judul.center(50))
    print('==================================================')
    data = load_data_csv(file_path)
    
    if not data:
        print("Data kosong.")
        return
    
    print("Data yang tersedia:")
    for i, item in enumerate(data, 1):
        print(f"{i}. {item['nama']} - Rp {item['biaya']:,} (Rating: {item['rating']})")
    
    while True:
        try:
            idx = int(input("Pilih nomor data yang akan dihapus: ")) - 1
            if 0 <= idx < len(data):
                break
            else:
                print("Nomor tidak valid.")
        except ValueError:
            print("Input harus berupa angka.")
    
    item_name = data[idx]['nama']
    konfirmasi = input(f"Yakin ingin menghapus '{item_name}'? (y/t): ").lower()
    
    if konfirmasi == 'y':
        del data[idx]
        simpan_data_csv(file_path, data, fieldnames)
        print(f"Data {tipe_data} '{item_name}' berhasil dihapus.")
    else:
        print("Penghapusan dibatalkan.")

def kelola_data(file_path, fieldnames, tipe_data):
    """Menu untuk mengelola data (hotel/wisata)"""
    while True:
        judul = f'KELOLAH DATA {tipe_data.upper()}' 
        print('==================================================')
        print(judul.center(50))
        print('==================================================')
        print("1. Tambah Data")
        print("2. Edit Data")
        print("3. Hapus Data")
        print("4. Lihat Data")
        print("5. Kembali")
        
        pilihan = input("Pilih menu: ")
        
        if pilihan == '1':
            tambah_data(file_path, fieldnames, tipe_data)
        elif pilihan == '2':
            edit_data(file_path, fieldnames, tipe_data)
        elif pilihan == '3':
            hapus_data(file_path, fieldnames, tipe_data)
        elif pilihan == '4':
            lihat_data(file_path, tipe_data)
        elif pilihan == '5':
            break
        else:
            print("Pilihan tidak valid.")
        
        input('Tekan Enter untuk melanjutkan...')

def lihat_data(file_path, tipe_data):
    """Lihat semua data"""
    judul = f'DATA {tipe_data.upper()}' 
    print('==================================================')
    print(judul.center(50))
    print('==================================================')
    data = load_data_csv(file_path)
    
    if not data:
        print("Data kosong.")
        return
    
    for i, item in enumerate(data, 1):
        print(f"{i}. {item['nama']}")
        print(f"   Biaya: Rp {item['biaya']:,}")
        print(f"   Rating: {item['rating']}/5")
        print("-" * 40)

def menu_admin():
    """Menu utama untuk admin"""
    while True:
        print('==================================================')
        print('                   MENU ADMIN                     ')
        print('==================================================')
        print("1. Kelola Data Hotel")
        print("2. Kelola Data Wisata") 
        print("3. Lihat History Rating Customer")  # Menu baru
        print("4. Logout")
        
        pilihan = input("Pilih menu: ")
        
        if pilihan == '1':
            kota = pilih_kota()
            if kota:
                file_path = f"hotel_{kota}.csv"
                kelola_data(file_path, ['nama', 'biaya', 'rating'], 'hotel')
        elif pilihan == '2':
            kota = pilih_kota()
            if kota:
                file_path = f"wisata_{kota}.csv"
                kelola_data(file_path, ['nama', 'biaya', 'rating'], 'wisata')
        elif pilihan == '3':
            lihat_history_rating()  # Panggil fungsi baru
            input('\nTekan Enter untuk kembali ke menu...')
        elif pilihan == '4':
            print('Logout berhasil.')
            input('Tekan Enter untuk kembali ke menu utama.')
            tampilanawal()
            break
        else:
            print("Pilihan tidak valid.")

# ==================== MENU UTAMA ====================

def tampilanawal():
    """Menu utama aplikasi"""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('===========================================================')
        print('           SELAMAT DATANG DI SISTEM REKOMENDASI            ')
        print('          PAKET WISATA DENGAN OPTIMALISASI BUDGET          ')
        print('===========================================================')
        print('Silahkan pilih menu login atau register')
        print('1. LOGIN CUSTOMER')
        print('2. LOGIN ADMIN')
        print('3. REGISTER')
        print('4. KELUAR')
        
        pilihan = input('Masukkan pilihan anda (1/2/3/4): ')
        
        if pilihan == '1':
            login()
        elif pilihan == '2':
            loginadmin()
        elif pilihan == '3':
            register()
        elif pilihan == '4':
            print('Terima kasih. Sampai jumpa.')
            break
        else:
            print('Pilihan tidak valid.')
            input('Tekan Enter untuk melanjutkan...')

# ==================== MAIN PROGRAM ====================

if __name__ == '__main__':
    tampilanawal()