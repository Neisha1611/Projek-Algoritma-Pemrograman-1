import csv 
import pandas as pd
import os

def cetak_selamat_datang():
    os.system("cls")
    print("=" * 115)
    print(r"""
                                          🌱  SELAMAT DATANG  🌱
          
                    ██████╗ ██╗██████╗ ██╗████████╗███████╗███╗   ███╗ █████╗ ██████╗ ████████╗
                    ██╔══██╗██║██╔══██╗██║╚══██╔══╝██╔════╝████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝
                    ██████╔╝██║██████╔╝██║   ██║   ███████╗██╔████╔██║███████║██████╔╝   ██║   
                    ██╔══██╗██║██╔══██╗██║   ██║   ╚════██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║   
                    ██████╔╝██║██████╔╝██║   ██║   ███████║██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   
                    ╚═════╝ ╚═╝╚═════╝ ╚═╝   ╚═╝   ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝                                                 
                                🌱  Solusi Cerdas untuk Penjualan Bibit  🌱
        """)
    print("=" * 115)
    print("Jangan lupa untuk registrasi terlebih dahulu jika belum mempunyai akun ya!".center(115))
    print("=== Silahkan pilih menu di bawah ini ya! ===".center(115))    

def main():
    cetak_selamat_datang()
    init_user_file()  
    while True:
        print("\nMenu:")
        print("[1] Registrasi Pengguna")
        print("[2] Login Pengguna")
        print("[3] Login Admin")
        print("[4] Keluar")
        pilihan = input("Pilih opsi ([1],[2],[3],[4]): ")

        if pilihan == '1':
            registrasi()
        elif pilihan == '2':
            user_login()
        elif pilihan == '3':
            admin_login()
        elif pilihan == '4':
            print("Terima kasih! Sampai jumpa.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

user_csv = "pengguna.csv"
def init_user_file():
    if not os.path.exists(user_csv):
        with open(user_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['nama', 'password', 'role'])
            writer.writerow(['petani', '24240', 'admin'])

def registrasi():
    print("=" * 54, "Registrasi", "=" * 54)
    while True:
        nama = input('Masukkan nama anda: ').strip().lower()
        password = input('Masukkan PIN (5 digit): ')

        if len(password) != 5 or not password.isdigit():
            print('PIN harus terdiri dari 5 digit angka.')
            if not lanjutkan_atau_keluar():
                return
            continue
        if not nama.isalpha():
            print("Nama harus berupa huruf.")
            if not lanjutkan_atau_keluar():
                return
            continue

        with open(user_csv, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == nama:
                    print("Nama sudah digunakan. Buat nama lain.")
                    if not lanjutkan_atau_keluar():
                        return
                    break
            else:
                with open(user_csv, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([nama, password, 'user'])
                print("\n===========| Berhasil Membuat Akun Baru |==========")
                return

def user_login():
    global nama_pengguna
    print("=" * 54, "Login User", "=" * 54)

    if not os.path.exists(user_csv):
        print("Anda belum melakukan registrasi. Silakan registrasi terlebih dahulu.")
        return

    while True:
        nama = input('Masukkan nama anda: ').strip().lower()
        password = input('Masukkan PIN: ')

        with open(user_csv, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 2:  
                    continue
                if row[0] == nama and row[1] == password:
                    print(f"Login berhasil! Selamat datang, {nama}.")
                    nama_pengguna = nama
                    menu_pengguna()
                    return  

            print("Nama atau PIN salah. Silakan coba lagi.")
            if not lanjutkan_atau_keluar():
                return

def admin_login():
    print("=" * 54, "Login Admin", "=" * 54)
    while True:
        nama = input('Masukkan nama admin: ').strip().lower()
        password = input('Masukkan PIN: ')

        if nama == 'petani' and password == '24240':
            print("Login admin berhasil!")
            menu_admin()
            return
        else:
            print("Nama atau PIN salah. Silakan coba lagi.")
            if not lanjutkan_atau_keluar():
                return

def lanjutkan_atau_keluar():
    while True:
        pilihan = input("Apakah Anda ingin mencoba lagi? (ya/tidak): ").strip().lower()
        if pilihan == 'ya':
            return True
        elif pilihan == 'tidak':
            print("Terima kasih, sampai jumpa!")
            os.system("cls")
            return False
        else:
            print("Pilihan tidak valid. Masukkan 'ya' untuk lanjut atau 'tidak' untuk keluar.")

def menu_pengguna():
    print("=" * 50,"Menu Pengguna","=" *50)
    print("1. Lihat Daftar Harga Bibit")
    print("2. Membeli")
    print("3. Riwayat Pembelian")
    print("4. Keluar")
    pilihan = input("Pilih menu (1/2/3/4): ")
    if pilihan == '1':
        lihat_daftar_harga()
    elif pilihan == '2':
        membeli()
    elif pilihan == '3':
        lihat_riwayat_pembelian()
    elif pilihan == '4':
        print("Terima kasih telah menggunakan layanan kami!")
        main()
    else:
        print("Pilihan tidak valid. Silakan coba lagi!")
        menu_pengguna ()

jenis_bibit = [ "Wortel", "Bayam", "Sawi", "Kangkung", "Pare", "Kentang"]
harga_standar = [20000, 25000, 18000, 22000, 24000, 26000]
harga_premium = [harga + 5000 for harga in harga_standar]
stok_standar = [30, 25, 40, 35, 50, 20]
stok_premium = [20, 15, 35, 30, 40, 25]
garis = "+-----+-------------+--------------+--------------+--------------+--------------+"

bibit_csv = "data_bibit.csv"
def simpan_data_bibit():
    with open(bibit_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["No", "Jenis Bibit", "Harga Standar", "Stok Standar", "Harga Premium", "Stok Premium"])
        for i in range(len(jenis_bibit)):
            writer.writerow([i + 1, jenis_bibit[i], harga_standar[i], stok_standar[i], harga_premium[i], stok_premium[i]])

def tampilkan_tabel():
    print(garis)
    print("| No  | Jenis Bibit | Harga Standar| Stok Standar | Harga Premium| Stok Premium |")
    print(garis)
    for i in range(len(jenis_bibit)):
        print("| {:<3} | {:<11} | {:<12} | {:<12} | {:<12} | {:<12} |".format(
            i + 1, jenis_bibit[i], harga_standar[i], stok_standar[i], harga_premium[i], stok_premium[i]))
    print(garis)

def lihat_daftar_harga ():
    os.system("cls")
    while True:
        tampilkan_tabel ()
        kembali = input("\nKetik 'ya' jika ingin kembali: ").lower().strip()
        if kembali == 'ya':
           menu_pengguna ()
        else:
            print("Input tidak valid. Silakan tekan 'ya' untuk kembali.")

nama_pengguna = None
laporan_pembelian_pengguna=[]
def membeli():
    diskon = {200000: 0.03, 400000: 0.05, 600000: 0.07}
    total_pembelian = 0
    transaksi = []  
    if nama_pengguna is None:
        pass
    while True:
        print("="*81)
        print("|                              MENU PEMBELIAN BIBIT                             |")
        print("="*81)
        tampilkan_tabel()
        try:
            pilihan_bibit = int(input("Pilih nomor jenis bibit yang ingin dibeli: "))
            if pilihan_bibit < 1 or pilihan_bibit > len(jenis_bibit):
                print("Pilihan tidak ada, silahkan coba lagi.")
                continue
        except ValueError:
            print("Masukkan angka yang valid, silahkan coba lagi.")
            continue
        nama_bibit = jenis_bibit[pilihan_bibit - 1]
        harga_bibit_standar = harga_standar[pilihan_bibit - 1]
        harga_bibit_premium = harga_premium[pilihan_bibit - 1]
        kualitas = input("Pilih kualitas bibit (Standar/Premium): ").lower().strip()
        if kualitas not in ["standar", "premium"]:
            print("Kualitas tidak tersedia, silahkan pilih kualitas yang ada.")
            continue
        stok = stok_standar if kualitas == "standar" else stok_premium
        harga_bibit = harga_bibit_standar if kualitas == "standar" else harga_bibit_premium
        if stok[pilihan_bibit - 1] == 0:
            print(f"Mohon maaf stok {nama_bibit} dengan kualitas {kualitas} sudah habis.")
            continue
        try:
            kuantitas = int(input(f"Masukkan jumlah bibit yang ingin dibeli (stok tersedia: {stok[pilihan_bibit - 1]}): "))
            if kuantitas <= 0:
                print("Kuantitas harus lebih dari nol, silakan coba lagi.")
                continue
            if kuantitas > stok[pilihan_bibit - 1]:
                print(f"Kuantitas yang diminta melebihi stok. Stok tersedia: {stok[pilihan_bibit - 1]} unit.")
                continue
        except ValueError:
            print("Masukkan jumlah yang valid, silakan coba lagi.")
            continue

        print(f"Bibit yang dibeli berupa {nama_bibit} dengan kualitas {kualitas} {kuantitas}")
        total_harga_bibit = harga_bibit * kuantitas
        total_pembelian += total_harga_bibit
        break
        
    diskon_persen = 0
    for batas, persen in diskon.items():
        if total_pembelian > batas:
            diskon_persen = persen
    jumlah_diskon = total_pembelian * diskon_persen
    total_setelah_diskon = total_pembelian - jumlah_diskon
    while True:
            konfirmasi = input("\nApakah Anda ingin melanjutkan ke pembayaran? (y/n): ").lower().strip()
            if konfirmasi == "y":
                break  
            elif konfirmasi == "n":
                print("Transaksi dibatalkan.")
                menu_pengguna()  
            else:
                print("Pilihan tidak valid. Silakan masukkan 'y' untuk melanjutkan atau 'n' untuk membatalkan.")
    try:
        pembayaran = int(input(f"Total belanja Anda: Rp {total_setelah_diskon:,}\nMasukkan jumlah uang (tanpa titik dan koma): Rp "))
        if pembayaran < total_setelah_diskon:
            print("Uang anda tidak cukup. Transaksi dibatalkan.")
            membeli()  
        else: 
            stok[pilihan_bibit - 1] -= kuantitas 
            transaksi.append((nama_bibit, kualitas, kuantitas, harga_bibit, total_harga_bibit))
    except ValueError:
        print("Masukkan jumlah yang valid. Transaksi dibatalkan.")
        membeli()

    laporan_csv = "laporan_pembelian_pengguna.csv"
    file_exists = os.path.exists(laporan_csv)

    with open(laporan_csv, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Nama Pembeli", "Jenis Bibit", "Kualitas", "Kuantitas", "Harga Pembelian", "Harga Pembelian Setelah Diskon"])
        for item in transaksi:
            writer.writerow([nama_pengguna, item[0], item[1], item[2], item[4], total_setelah_diskon])
    
    with open("struk_pembelian.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Nama Pengguna", nama_pengguna])
        writer.writerow(["Nama Bibit", "Kualitas", "Kuantitas", "Harga Satuan", "Total Harga"])
        for item in transaksi:
            writer.writerow(item)
        writer.writerow([])
        writer.writerow(["Total Harga", "", "", "", f"Rp {total_pembelian:,}"])
        writer.writerow(["Diskon", "", "", "", f"Rp {jumlah_diskon:,}"])
        writer.writerow(["Total Bayar", "", "", "", f"Rp {total_setelah_diskon:,}"])
        writer.writerow(["Pembayaran", "", "", "", f"Rp {pembayaran:,}"])
        kembalian = pembayaran - total_setelah_diskon
        writer.writerow(["Kembalian", "", "", "", f"Rp {kembalian:,}"])

    simpan_pembelian(nama_bibit, kualitas, kuantitas, total_harga_bibit)
    simpan_stok()

    print("="*47)
    print("|                STRUK PEMBELIAN              |")
    print("="*47)
    for item in transaksi:
        print(f"{item[0]} ({item[1]}) - {item[2]}  x Rp {item[3]:,} = Rp {item[4]:,}") 
    print("-"*47)
    print(f"Nama Pembeli     : {nama_pengguna}")
    print(f"Total Harga      : Rp {total_pembelian:,}")
    print(f"Diskon           : {diskon_persen*100:.0f}% (Rp {jumlah_diskon:,})")
    print("-"*47)
    print(f"Total Bayar      : Rp {total_setelah_diskon:,}")
    print(f"Uang Anda        : Rp {pembayaran:,}")
    print(f"Kembalian        : Rp {kembalian:,}")
    print("="*47)

    ada_ulasan()

def simpan_stok():
    with open("data_bibit.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["No", "Jenis Bibit", "Harga Standar", "Stok Standar", "Harga Premium", "Stok Premium"])
        for i in range(len(jenis_bibit)):
            writer.writerow([i + 1, jenis_bibit[i], harga_standar[i], stok_standar[i], harga_premium[i], stok_premium[i]])

def baca_stok():
    global stok_standar, stok_premium
    if os.path.exists("data_bibit.csv"):
        with open("data_bibit.csv", 'r') as file:
            reader = csv.reader(file)
            next(reader)
            stok_standar = []
            stok_premium = []
            for row in reader:
                if row:
                    stok_standar.append(int(row[3]))
                    stok_premium.append(int(row[5]))

ulasan_list=[]
def ada_ulasan():
    ulasan = input("Apakah Anda ingin memberikan ulasan? (Ya/Tidak): ").lower().strip()
    if ulasan == 'ya':
        isi_ulasan = input("Masukkan ulasan Anda: ").strip()
        if not isi_ulasan:
            print("Ulasan tidak boleh kosong.")
            ada_ulasan()
        else:
            ulasan_baru = {"nama": nama_pengguna, "ulasan": isi_ulasan}
            ulasan_list.append(ulasan_baru)
            simpan_ulasan_ke_csv(ulasan_baru) 
            print("Ulasan berhasil ditambahkan!")
            menu_pengguna()
    elif ulasan == 'tidak':
        print("Terimakasih sudah membeli produk kami!")
        menu_pengguna()
    else:
        print("Pilihan tidak tersedia. Silakan coba lagi!")
        ada_ulasan()

def simpan_ulasan_ke_csv(ulasan):
    file_csv = "data_ulasan.csv"
    file_exists = False
    
    try:
        with open(file_csv, 'r', newline='') as file:
            file_exists = True
    except FileNotFoundError:
        pass

    with open(file_csv, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Nama Pengguna", "Ulasan"])
        writer.writerow([ulasan["nama"], ulasan["ulasan"]])

nama_pembelian_csv = 'riwayat_pembelian.csv'
def lihat_riwayat_pembelian():
    os.system("cls")
    print("-" * 46, "Riwayat Pembelian", "-" * 46)
    if not os.path.exists(nama_pembelian_csv):
        print("Anda belum melakukan pembelian.")
        kembali = input("\nKetik 'ya' jika ingin kembali: ").lower().strip()
        if kembali == 'ya':
            menu_pengguna()
            return 
        else:
            print("Input tidak valid. Ketik 'ya' untuk kembali.")
            lihat_riwayat_pembelian()
    with open(nama_pembelian_csv, mode='r',) as file:
        reader = csv.reader(file)
        print(f"{'Nama Pengguna':<15} {'Bibit':<15} {'Kualitas':<15} {'Kuantitas':<10} {'Total Harga':<15}")
        print("-" * 115)
        ada_data = False
        for row in reader:
            if row[0] == nama_pengguna:
                ada_data = True
                print(f"{row[0]:<15} {row[1]:<15} {row[2]:<15} {row[3]:<10} {row[4]:<15}")

        if not ada_data:
            print("Anda belum melakukan pembelian.")
        
    print("=" * 115)
    kembali = input("\nKetik 'ya' jika ingin kembali: ").lower().strip()
    if kembali == 'ya':
        menu_pengguna()
    else:
        print("Input tidak valid. Ketik 'ya' untuk kembali.")
        lihat_riwayat_pembelian()

def simpan_pembelian(bibit, kualitas, kuantitas, total_harga):
    with open(nama_pembelian_csv, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([nama_pengguna, bibit, kualitas, kuantitas, total_harga])

def menu_admin():
    os.system("cls")
    while True:
        print("\n=== Menu Admin ===")
        print("1. Update Daftar Bibit")
        print("2. Laporan Pembelian")
        print("3. Lihat Ulasan")
        print("4. Keluar")
        pilihan = input("Pilih menu (1/2/3/4): ")
        if pilihan == "1": 
            menu_update()
        elif pilihan == "2":    
            laporan_pembelian()   
        elif pilihan == "3":
            lihat_ulasan()
        elif pilihan == "4":
            os.system("cls")
            main() 
        else: 
            print("Pilihan tidak tersedia. Silahkan coba lagi!")

def menu_update():
    while True:
        print("\nMenu Update:")
        print("1. Tambah Bibit")
        print("2. Hapus Bibit")
        print("3. Keluar")
        pilihan = input("Pilih menu (1/2/3): ")
        if pilihan == "1":
            tambah_bibit()
        elif pilihan == "2":
            hapus_bibit()
        elif pilihan == "3":
            print("Terima kasih telah berkunjung!")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih menu yang benar.")

def tambah_bibit():
    tampilkan_tabel()
    while True:
        nama_bibit = str(input("Masukkan nama bibit baru: "))
        if not nama_bibit.isalpha() or not nama_bibit.strip():
            print("Nama bibit harus berupa huruf dan tidak boleh kosong. Silakan coba lagi.")
            continue
        try:
            harga = int(input("Masukkan harga standar bibit: "))
            stok_standar_bibit = int(input("Masukkan stok standar bibit: "))
            stok_premium_bibit = int(input("Masukkan stok premium bibit: "))
        except ValueError:
            print("Harga dan stok harus berupa angka bulat. Silakan coba lagi.")
            continue
        
        harga_premium_bibit = harga + 5000
        jenis_bibit.append(nama_bibit)
        harga_standar.append(harga)
        harga_premium.append(harga_premium_bibit)
        stok_standar.append(stok_standar_bibit)
        stok_premium.append(stok_premium_bibit)
        
        with open('data_bibit.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(['Nama Pengguna', 'Nama Bibit', 'Harga Standar', 'Harga Premium', 'Stok Standar', 'Stok Premium'])
            writer.writerow([len(jenis_bibit), nama_bibit, harga, harga_premium_bibit, stok_standar_bibit, stok_premium_bibit])
        
        simpan_data_bibit()
        tampilkan_tabel()
        print(f"Bibit '{nama_bibit}' berhasil ditambahkan!")
        
        break

def hapus_bibit():
    tampilkan_tabel()
    try:
        no_bibit = int(input("Masukkan nomor bibit yang ingin dihapus: "))
        if no_bibit < 1 or no_bibit > len(jenis_bibit):
            print("Nomor bibit tidak valid!")
        else:
            jenis_bibit.pop(no_bibit - 1)
            harga_standar.pop(no_bibit - 1)
            harga_premium.pop(no_bibit - 1)
            stok_standar.pop(no_bibit - 1)
            stok_premium.pop(no_bibit - 1)
            
            with open('data_bibit.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Nama Pengguna', 'Nama Bibit', 'Harga Standar', 'Harga Premium', 'Stok Standar', 'Stok Premium'])
                for idx in range(len(jenis_bibit)):
                    writer.writerow([idx + 1, jenis_bibit[idx], harga_standar[idx], harga_premium[idx], stok_standar[idx], stok_premium[idx]])

            simpan_data_bibit()
            tampilkan_tabel()
            print(f"Bibit nomor {no_bibit} berhasil dihapus!")
    except ValueError:
        print("Masukkan nomor bibit yang valid.")

def simpan_data_bibit():
    with open(bibit_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["No", "Jenis Bibit", "Harga Standar", "Stok Standar", "Harga Premium", "Stok Premium"])
        for i in range(len(jenis_bibit)):
            writer.writerow([i + 1, jenis_bibit[i], harga_standar[i], stok_standar[i], harga_premium[i], stok_premium[i]])

def baca_data_bibit():
    global jenis_bibit, harga_standar, harga_premium, stok_standar, stok_premium
    if os.path.exists(bibit_csv):
        with open(bibit_csv, 'r') as file:
            reader = csv.DictReader(file)
            jenis_bibit = []
            harga_standar = []
            harga_premium = []
            stok_standar = [] 
            stok_premium = []
            for row in reader:
                if row:
                    jenis_bibit.append(row['Jenis Bibit'])
                    harga_standar.append(int(row['Harga Standar']))
                    harga_premium.append(int(row['Harga Premium']))
                    stok_standar.append(int(row['Stok Standar']))
                    stok_premium.append(int(row['Stok Premium']))

def laporan_pembelian():
    os.system("cls") 
    file_csv = "laporan_pembelian_pengguna.csv"
    if not os.path.exists(file_csv):
        print("Belum ada transaksi yang tercatat.")
        print("=" * 115)
        kembali = input("\nKetik 'ya' jika ingin kembali: ").lower().strip()
        if kembali == 'ya':
            menu_admin()
        else:
            print("Input tidak valid. Ketik 'ya' untuk kembali.")
            laporan_pembelian()
        return

    try:
        df_pembelian = pd.read_csv(file_csv)
        laporan_pembelian_pengguna = df_pembelian.to_dict('records')

        if not laporan_pembelian_pengguna:
            print("Belum ada transaksi yang tercatat.")
            print("=" * 115)
            kembali = input("\nKetik 'ya' jika ingin kembali: ").lower().strip()
            if kembali == 'ya':
               menu_admin()
            else:
                print("Input tidak valid. Ketik 'ya' untuk kembali.")
                laporan_pembelian()
            return
        
        print("=" * 115)
        print("Laporan Pembelian".center(115))
        print("=" * 115)
        print("+----------------+-------------+----------+------------+-----------------+--------------------------------+")
        print("| Nama Pembeli   | Jenis Bibit | Kualitas | Kuantitas  | Harga Pembelian | Harga Pembelian Setelah Diskon |")
        print("+----------------+-------------+----------+------------+-----------------+--------------------------------+")
        
        total_pembelian = 0
        total_pembelian_setelah_diskon = 0
        
        for pembelian in laporan_pembelian_pengguna:
            print("| {:<14} | {:<11} | {:<8} | {:<10} | {:<15,} | {:<30,} |".format(
                pembelian["Nama Pembeli"], pembelian["Jenis Bibit"],
                pembelian["Kualitas"], pembelian["Kuantitas"],
                pembelian["Harga Pembelian"], pembelian["Harga Pembelian Setelah Diskon"]))
            
            total_pembelian += pembelian["Harga Pembelian"]
            total_pembelian_setelah_diskon += pembelian["Harga Pembelian Setelah Diskon"]
        
        print("+----------------+-------------+----------+------------+-----------------+--------------------------------+")
        print(f"| Total Keseluruhan Pembelian :                        | Rp{total_pembelian:,.0f}       | Rp{total_pembelian_setelah_diskon:,.0f}                      |")
        print("=" * 115)
        
    except Exception as e:
        print(f"Terjadi kesalahan saat membaca file: {e}")
    
    kembali = input("\nKetik 'ya' jika ingin kembali: ").lower().strip()
    if kembali == 'ya':
        menu_admin()
    else:
        print("Input tidak valid. Ketik 'ya' untuk kembali.")
        laporan_pembelian()

def lihat_ulasan():
    os.system("cls") 
    print("=" * 54, "Ulasan Pengguna", "=" * 54)
    file_csv = "data_ulasan.csv"
    try:
        with open(file_csv, 'r', newline='') as file:
            reader = csv.reader(file)
            ulasan_data = list(reader)
            
            if len(ulasan_data) > 1:  
                for ulasan in ulasan_data[1:]:  
                    print(f"Nama: {ulasan[0]}, Ulasan: {ulasan[1]}")
            else:
                print("Belum ada ulasan yang diberikan.")
    except FileNotFoundError:
        print("Belum ada file ulasan. Tidak ada data yang dapat ditampilkan.")
    
    print("=" * 54)
    kembali = input("\nKetik 'ya' jika ingin kembali: ").lower().strip()
    if kembali == 'ya':
        menu_admin()
    else:
        print("Input tidak valid. Ketik 'ya' untuk kembali.")
        lihat_ulasan()

if __name__ == "__main__":
    baca_stok()
    baca_data_bibit()
    main()
