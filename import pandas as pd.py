import csv
import pandas as pd
import os

# Fungsi untuk mencetak ucapan selamat datang
def cetak_selamat_datang():
    print("=" * 40)
    print("Selamat datang di BibitSmart".center(40))
    print("=" * 40)

# Fungsi untuk registrasi pengguna
def registrasi():
    print("=== Registrasi ===")
    while True:
        nama = str(input('Masukkan nama anda: ')).strip().lower()
        if not nama.isalpha():
            print("Nama harus berupa huruf")
            continue
        password = input('Masukkan PIN (5 digit): ')
        if len(password) != 5 or not password.isdigit():
            print('PIN harus terdiri dari 5 digit angka.')
        else:
            with open('pengguna.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([nama, password, 'user'])
            print("Registrasi berhasil!")
            break

# Fungsi untuk login pengguna
def login():
    global nama_pengguna
    print("=== Login ===")
    while True:
        nama = input('Masukkan nama anda: ').strip().lower()  
        password = input('Masukkan PIN: ')
       
        if not os.path.exists('pengguna.csv'):
            print("Anda belum melakukan registrasi. Silakan registrasi terlebih dahulu.")
            return None
        
        with open('pengguna.csv', 'r') as file:
            reader = csv.reader(file)
            ditemukan = False
            for row in reader:
                if row[0] == nama:
                    ditemukan = True  
                    if row[1] == password:
                        if nama == 'petani' and password == '24240':
                            print("Login admin berhasil!")
                            return 'admin'  
                        else:
                            print(f"Login berhasil! Selamat datang, {nama}.")
                            nama_pengguna = nama
                            return 'user' 
                    else:
                        print("PIN salah. Silakan coba lagi.")
                        return None  
            
            if not ditemukan:
                print(f"Nama '{nama}' tidak ditemukan. Anda belum melakukan registrasi.")
                return None  

# Menu utama yang menggabungkan registrasi dan login
def main():
    cetak_selamat_datang()
    while True:
        print("\n=== Menu ===")
        print("1. Registrasi")
        print("2. Login")
        pilihan = input("Pilih menu (1/2): ")

        if pilihan == '1':
            registrasi()
        elif pilihan == '2':
            hasil_login = login()
            if hasil_login == 'user':
                menu_pengguna()
            elif hasil_login == 'admin':
                menu_admin()
            elif hasil_login is None:
                continue  
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

# Data bibit dan fungsinya

jenis_bibit = [
    "Wortel", "Bayam", "Sawi", "Kangkung", "Pare", 
    "Kentang"
]
harga_standar = [20000, 25000, 18000, 22000, 24000, 26000]
harga_premium = [harga + 5000 for harga in harga_standar]
stok_standar = [30, 25, 40, 35, 50, 20]
stok_premium = [20, 15, 35, 30, 40, 25]
garis = "+-----+-------------+--------------+--------------+--------------+--------------+"

# Menampilkan tabel bibit
def tampilkan_tabel():
    print(garis)
    print("| No  | Jenis Bibit | Harga Standar| Stok Standar | Harga Premium| Stok Premium |")
    print(garis)
    for i in range(len(jenis_bibit)):
        print("| {:<3} | {:<11} | {:<12} | {:<12} | {:<12} | {:<12} |".format(
            i + 1, jenis_bibit[i], harga_standar[i], stok_standar[i], harga_premium[i], stok_premium[i]))
    print(garis)

# Fungsi untuk menu pembelian pengguna
nama_pengguna = None
laporan_pembelian_pengguna=[]
def menu_pengguna():
    tampilkan_tabel()
    diskon = {200000: 0.03, 400000: 0.05, 600000: 0.07}
    total_pembelian = 0
    transaksi = []  # mencatat detail pembelian
    if nama_pengguna is None:
        pass
    while True:
        print("="*35)
        print("|       MENU PEMBELIAN BIBIT      |")
        print("="*35)
        print("\tDaftar Jenis Bibit: ")
        nomor = 1
        for bibit in jenis_bibit:
            print(f"\t{nomor}. {bibit}")
            nomor += 1
        
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

        # Input kualitas bibit
        kualitas = input("Pilih kualitas bibit (Standar/Premium): ").lower()
        if kualitas not in ["standar", "premium"]:
            print("Kualitas tidak tersedia, silahkan pilih kualitas yang ada.")
            continue
        
        stok = stok_standar if kualitas == "standar" else stok_premium
        harga_bibit = harga_bibit_standar if kualitas == "standar" else harga_bibit_premium
        if stok[pilihan_bibit - 1] == 0:
            print(f"Mohon maaf stok {nama_bibit} dengan kualitas {kualitas} sudah habis.")
            continue

        # Input kuantitas
        try:
            kuantitas = int(input(f"Masukkan jumlah bibit yang ingin dibeli (stok tersedia: {stok[pilihan_bibit - 1]}): "))
            if kuantitas <= 0 or kuantitas > stok[pilihan_bibit - 1]:
                print("Kuantitas tidak valid, silahkan coba lagi.")
                continue
        except ValueError:
            print("Masukkan jumlah yang valid, silahkan coba lagi.")
            continue

        # Total harga untuk jenis bibit ini
        total_harga_bibit = harga_bibit * kuantitas
        total_pembelian += total_harga_bibit
        transaksi.append((nama_bibit, kualitas, kuantitas, harga_bibit, total_harga_bibit))
        
        stok[pilihan_bibit - 1] -= kuantitas  # Mengurangi stok
        
        # Menanyakan apakah ingin menambah pembelian
        tambah = input("Apakah anda ingin menambah pembelian bibit? (Ya/Tidak): ").lower()
        if tambah == "tidak":
            break
    
    # Diskon
    diskon_persen = 0
    for batas, persen in diskon.items():
        if total_pembelian > batas:
            diskon_persen = persen
    jumlah_diskon = total_pembelian * diskon_persen
    total_setelah_diskon = total_pembelian - jumlah_diskon

    # Input pembayaran
    try:
        pembayaran = int(input(f"Total belanja Anda: Rp {total_setelah_diskon:,}\nMasukkan jumlah uang: Rp "))
        if pembayaran < total_setelah_diskon:
            print("Uang anda tidak cukup. Transaksi dibatalkan.")
            return
        kembalian = pembayaran - total_setelah_diskon
    except ValueError:
        print("Masukkan jumlah yang valid. Transaksi dibatalkan.")
        return

    for item in transaksi :
        laporan_pembelian_pengguna.append({
        "Nama Pembeli"   : nama_pengguna,
        "Jenis Bibit"    : item[0],
        "Kualitas"       : item[1],
        "Kuantitas"      : item[2],
        "Total Pembelian": item[4],
    })

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
        writer.writerow(["Kembalian", "", "", "", f"Rp {kembalian:,}"])

    df_pembelian = pd.DataFrame(laporan_pembelian_pengguna)
    df_pembelian.to_csv("laporan_pembelian_pengguna.csv", index=False)

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
  
def menu_admin():
    print("\n=== Menu Admin ===")
    print("1. Update Daftar Bibit")
    print("2. Laporan Pembelian")
    print("3. Keluar")
    pilihan = input("Pilih menu (1/2/3): ")

    if pilihan == "1": 
        menu_update()
    elif pilihan == "2":    
        laporan_pembelian()   
    elif pilihan == "3":
        os.system("cls")
        main() 
    else: 
        print("Pilihan tidak tersedia. Silahkan coba lagi!")
    menu_admin()

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
            print(f"Bibit nomor {no_bibit} berhasil dihapus!")
    except ValueError:
        print("Masukkan nomor bibit yang valid.")


def laporan_pembelian():
    if not laporan_pembelian_pengguna:
        print("Belum ada transaksi yang dilakukan.")
        return

    print("="*115)
    print("Laporan Pembelian".center(115))
    print("="*115)

    print("+----------------+-------------+----------+------------+-----------------+")
    print("| Nama Pembeli   | Jenis Bibit | Kualitas | Kuantitas  | Total Pembelian |")
    print("+----------------+-------------+----------+------------+-----------------+")
    total_pembelian=0
    for pembelian in laporan_pembelian_pengguna:
        print("| {:<14} | {:<11} | {:<8} | {:<10} | {:<15} |".format(
            pembelian["Nama Pembeli"], pembelian["Jenis Bibit"],
            pembelian["Kualitas"], pembelian["Kuantitas"],
            pembelian["Total Pembelian"]))
        total_pembelian += pembelian["Total Pembelian"]
    print("+----------------+-------------+----------+------------+-----------------+")
    print(f"Total pembelian bibit : Rp{total_pembelian:}")

    df_pembelian = pd.DataFrame(laporan_pembelian_pengguna)
    df_pembelian.to_csv("Laporan Pembelian.csv", index=False)
    df_pembelian = pd.read_csv("Laporan Pembelian.csv")
# Menjalankan program
# if __name__ == "_main_":
main()