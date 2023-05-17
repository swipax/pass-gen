import random
import keyboard
from colorama import Fore, Style
import colorama
colorama.init()
import time
import os
import sqlite3
os.system('cls' if os.name == 'nt' else 'clear') 

charset = ["A", "S", "D", "F", "G", "H", "J", "K", "L", "M", "N", "B", "X", "V", "Z", "O", "P", "U", "P", "Q", "W", "E", "T", "Y", "C", "a", "c", "t", "y", "s", "d", "f", "g", "z", "o", "u", "h", "j", "k", "l", "m", "n", "b", "v", "c", "x", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "!", "@", "#", "$", "_", "+", ":"]
logo =Fore.MAGENTA + """,------.  ,---.   ,---.   ,---.         ,----.   ,------.,--.  ,--. 
|  .--. '/  O  \ '   .-' '   .-',-----.'  .-./   |  .---'|  ,'.|  | 
|  '--' |  .-.  |`.  `-. `.  `-.'-----'|  | .---.|  `--, |  |' '  | 
|  | --'|  | |  |.-'    |.-'    |      '  '--'  ||  `---.|  | `   | 
`--'    `--' `--'`-----' `-----'        `------' `------'`--'  `--'
                                            github:swipax                  """
print(logo)
print("\n")
class Slow:
    @classmethod
    def slowType(cls, text: str, speed: float, color=None, newLine=True):
        for i in text:
            print((color or "") + i, end="", flush=True)
            time.sleep(speed)
        if newLine:
            print()

def generate_password():
    platform = input(Fore.BLUE + "\n" + "Platform: " + Style.NORMAL)
    uzunluk = int(input(Fore.CYAN + "\n" + "Şifre uzunluğu: " + Style.NORMAL))

    randpass = ""
    prevchar = ""
    for i in range(uzunluk):
        while True:
            char = random.choice(charset)
            if char != prevchar:
                randpass += char
                prevchar = char
                break

    print(f"Oluşturulan şifre: {randpass}" + "\n")

    database_type = input(Fore.YELLOW + "Veritabanı türünü seçin (1: TXT, 2: SQLite): " + Style.NORMAL)

    if database_type == "1":
        with open("pass.txt", "a") as f:
            f.write(f"Platform: {platform}\n")
            f.write(f"password: {randpass}\n")
            f.write("-------------------------------------\n")
        print("Şifre pass.txt dosyasına kaydedildi.")
    elif database_type == "2":
        conn = sqlite3.connect("passwords.db")
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS passwords
                     (platform TEXT, password TEXT)''')

        c.execute("INSERT INTO passwords VALUES (?, ?)", (platform, randpass))
        conn.commit()
        conn.close()

        print("Şifre SQLite veritabanına kaydedildi.")
    else:
        print("Geçersiz veritabanı türü seçildi.")

    print("\n")

def delete_password():
    platform = input(Fore.BLUE + "\n" + "Silinecek şifrenin platformu: " + Style.NORMAL)
    database_type = input(Fore.YELLOW + "Veritabanı türünü seçin (1: TXT, 2: SQLite): " + Style.NORMAL)

    if database_type == "1":
        with open("pass.txt", "r") as f:
            lines = f.readlines()

        found = False
        for i in range(len(lines)):
            if "Platform: " + platform in lines[i]:
                found = True
                start_index = i
                break

        if not found:
            print(Fore.RED + "Şifre bulunamadı." + Style.NORMAL)
            return

        end_index = start_index
        while end_index < len(lines) and lines[end_index].strip() != "-------------------------------------":
            end_index += 1

        with open("pass.txt", "w") as f:
            f.writelines(lines[:start_index] + lines[end_index + 1:])

        print(Fore.GREEN + "Şifre başarıyla silindi." + Style.NORMAL)
    elif database_type == "2":
        conn = sqlite3.connect("passwords.db")
        c = conn.cursor()

        c.execute("DELETE FROM passwords WHERE platform = ?", (platform,))
        conn.commit()
        conn.close()

        print(Fore.GREEN + "Şifre başarıyla silindi." + Style.NORMAL)
    else:
        print("Geçersiz veritabanı türü seçildi.")

       
def show_passwords():
    try:
        print("pass.txt Şifreleri:")
        print("-"*37)
        with open("pass.txt", "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("pass.txt dosyası bulunamadı.")

    try:
        print("passwords.db Şifreleri:")
        print("-"*37)
        conn = sqlite3.connect("passwords.db")
        c = conn.cursor()

        c.execute("SELECT * FROM passwords")
        rows = c.fetchall()
        for row in rows:
            platform, password = row
            print("Platform:", platform)
            print("Password:", password)
            print("-------------------------------------")

        conn.close()
    except sqlite3.Error:
        print("passwords.db veritabanı bulunamadı.")

while True:
    Slow.slowType("1) Yeni şifre oluşturma""\n",0.02,color=Fore.GREEN,newLine=True)
    Slow.slowType("2) Şifrelerimi göster""\n",0.02,color=Fore.CYAN)
    Slow.slowType("3) Şifre silme""\n",0.02,color=Fore.YELLOW)
    Slow.slowType("Programdan Çıkmak için 'q' basınız""\n",0.02,color=Fore.RED)   
    choice = input(Fore.YELLOW + "Seçim yapınız (1-3): " + Style.NORMAL)
    
    if choice == 'q':
        print("Programdan Çıkılıyor...")
        break 
    
    if choice == "1":
        generate_password()
    elif choice == "2":
        show_passwords()
    elif choice == "3":
        delete_password()
    else:
        print("Geçersiz Seçim")

    print(Fore.WHITE + "Menüye dönmek için ENTER tuşuna basın."+ Style.NORMAL)
    input()
    os.system('cls' if os.name == 'nt' else 'clear')

    print(logo)
