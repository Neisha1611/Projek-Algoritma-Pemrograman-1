import pandas as pd
import csv
import os

def cetak_selamat_datang():
    print("=" * 40)
    print("Selamat datang di SmartBibit".center(40))
    print("=" * 40)

def registrasi():
    print("=== Registrasi ===")
    while True:
        nama = input('Masukkan nama anda: ').strip().lower() 
        password = input('Masukkan PIN (5 digit): ')
        if len(password) != 5 or not password.isdigit():
            print('PIN harus terdiri dari 5 digit angka.')
        else:
            with open('pengguna.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([nama, password, 'user'])
            print("Registrasi berhasil!")
            break

def login_pengguna():
    print("=== Login Pengguna ===")
    while True:
        nama = input('Masukkan nama anda: ').strip().lower()  
        password = input('Masukkan PIN: ')
        
        with open('pengguna.csv', 'r') as file:
            reader = csv.reader(file)
            ditemukan = False
            for row in reader:
                if row[0] == nama and row[1] == password:
                    print(f"Login berhasil! Selamat datang, {nama}.")
                    ditemukan = True
                    menu_pengguna()
                    break
            
            if ditemukan:
                return True
            else:
                print("Login gagal. Silakan coba lagi.")
                keluar = input("Apakah Anda ingin keluar? (y/n): ").strip().lower()
                if keluar == 'y':
                    return False
                
def menu_pengguna():
    print("\n=== Menu ===")
    print("1. Daftar Bibit")
    print("4. Keluar")
    pilihan = input("Pilih menu (1/2):")

    if pilihan == "1": 
        tampilkan_daftar_bibit()
    elif pilihan == "2":
        main() 
    else: 
        print("Pilihan tidak tersedia. Silahkan coba lagi!")
        menu_admin()

def tampilkan_daftar_bibit():
    print("\n=== Daftar Bibit ===")
    print(daftarBibit.to_string(index=False))  # Menampilkan DataFrame tanpa indeks

daftarBibit = {
    "Jenis Bibit" : ["Wortel","Wortel", "Bayam","Bayam", "Sawi", "Sawi", "Kangkung", "Kangkung", "Pare", "Pare", "Kentang", "Kentang"],
    "Kualitas" : ["Standart", "Premium", "Standart", "Premium", "Standart", "Premium", "Standart", "Premium", "Standart", "Premium", "Standart", "Premium"],
    "Harga" : [10000, 15000,10000, 15000,10000, 15000,10000, 15000,10000, 15000,10000, 15000],
    "Stok" :[10,10,10,10,10,10,10,10,10,10,10,10]
    }

daftarBibit = pd.DataFrame(daftarBibit)
daftarBibit.to_csv("daftarBibit.csv", index=False)
daftarBibit = pd.read_csv("daftarBibit.csv")
print(daftarBibit)

def login_admin():
    print("=== Login Admin ===")
    while True:
        nama_admin = input('Masukkan nama admin: ').strip().lower()  
        password = input('Masukkan PIN (password admin): ')
        
        if nama_admin == 'petani' and password == '24240':
            print("Login admin berhasil!")
            menu_admin()
            return True
        else:
            print("Login admin gagal. Silakan coba lagi.")
            keluar = input("Apakah Anda ingin keluar? (iya/tidak): ").strip().lower()
            if keluar == 'iya':
                return False
            
def menu_admin():
    print("\n=== Menu Admin ===")
    print("1. Update Stok Bibit")
    print("2. Update Daftar Bibit")
    print("3. Riwayat Pembelian")
    print("4. Keluar")
    pilihan = input("Pilih menu (1/2/3/4): ")

    if pilihan == "1": 
        update_stok() 
    elif pilihan == "2":
        update_daftar_bibit()
    elif pilihan == "3":    
        riwayat_pembelian()   
    elif pilihan == "4":
        main() 
    else: 
        print("Pilihan tidak tersedia. Silahkan coba lagi!")
        menu_admin()

# def update_stok():
#     print("\n=== Update Stok Bibit ===")
#     print("Pilih bibit : ")
#     urutanbibit = 0
#     liststok = []
#     with open("Daftar Stok Bibit.csv","r") as file:
#         reader = csv.reader(file)


# def update_daftar_bibit():

# def riwayat_pembelian():
#     print("\n=== Riwayat Pembelian Bibit ===")
#     df = pd.read_csv("Riwayat Pembelian.csv", sep=';', header=0, index_col="nama")
#     # with open("Riwayat Pembelian.csv","r") as riwayat:
#     #     reader = csv.reader(riwayat)
#     #     nomorriwayat = 0
#     #     for row in reader:
#     #         nomorriwayat += 1
#     #         print(f"{nomorriwayat}. Nama Pembeli : {row[1]}\n Jenis Bibit : {row[2]}\n Kualitas Bibit : {row[3]}\n Harga Bibit : {row[4]}\n Jumlah Pembelian Bibit : {row[5]}\n Total Harga Pembelian : {row[6]}")
#     pilihan = input("1. Kembali ke Menu Admin \n2. Keluar \nPilih Menu (1/2) : ")

#     if pilihan == "1":
#         menu_admin()
#     elif pilihan == "2":
#         main()
#     else:
#         print("Pilihan tidak tersedia. Coba lagi!")
#         riwayat_pembelian()

def main():
    cetak_selamat_datang()
    while True:
        print("\n=== Menu ===")
        print("1. Registrasi")
        print("2. Login Pengguna")
        print("3. Login Admin")
        print("4. Keluar")
        pilihan = input("Pilih menu (1/2/3/4): ")

        if pilihan == '1':
            registrasi()
        elif pilihan == '2':
            if not os.path.exists('pengguna.csv'):
                print("Anda belum registrasi. Silakan registrasi terlebih dahulu.")
            else:
                if not login_pengguna():
                    continue  
        elif pilihan == '3':
            if not login_admin():
                continue  
        elif pilihan == '4':
            print("Terima kasih! Sampai jumpa.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()