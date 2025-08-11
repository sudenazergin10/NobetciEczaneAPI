import requests

iller = {
    "Ankara": ["Yenimahalle", "Çankaya", "Etimesgut"],
    "İstanbul": ["Kadıköy", "Büyükçekmece", "Beylikdüzü"],
    "Tekirdağ": ["Çorlu", "Değirmenaltı", "Saray"],
    "Antalya": ["Konyaaltı", "Serik", "Aksu"],
    "Muğla": ["Bodrum", "Fethiye", "Milas"],
    "Bursa": ["Mudanya", "Gemlik", "Osmangazi"],
    "Balıkesir": ["Altıeylül", "Karesi", "Edremit"],
    "İzmir": ["Konak", "Bornova", "Karşıyaka"],
    "Denizli": ["Pamukkale", "Merkezefendi", "Çivril"],
    "Eskişehir": ["Odunpazarı", "Tepebaşı", "Sivrihisar"]
}

# Collect api üzerinden alınan API Anahtarı buraya girilir.
API_KEY = "XXXX"
HEADERS = {
    "content-type": "application/json",
    "authorization": f"apikey {API_KEY}"
}

def secim_al(prompt, secenekler):
    #Kullanıcıdan seçim alır, geçerli olana kadar tekrar sorar.
    while True:
        secim = input(prompt).strip()
        if secim in secenekler:
            return secim    #secim dogruysa döngü biter
        print(f"Geçersiz seçim! Lütfen {', '.join(secenekler)} seçeneklerinden birini girin.")

def numarali_secim(prompt, liste):
    #Listedeki elemanlardan numara ile seçim yapmaya olanak verir.
    while True:
        print(prompt)
        for i, eleman in enumerate(liste, 1):    #liste öğeleri 1’den başlayarak numaralandırılır.
            print(f"{i}. {eleman}")
        secim = input("Seçiminiz (numara ile): ").strip()    #Kullanıcıdan bir sayı girmesi istenir.
        if secim.isdigit() and 1 <= int(secim) <= len(liste):    #girilen sayı listede buluyor mu diye bakıyoruz.
            return liste[int(secim) - 1]     #!Liste indeksleri 0’dan başlar, o yüzden -1 
        print("Geçersiz numara! Lütfen tekrar deneyin.")

def api_get(url, params):
    #API'den GET isteği yapar ve sonucu döner, hata durumlarını yönetir.
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()      #Eğer istek başarısız olduysa hata fırlat!
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Ağ veya API hatası: {e}")
    except ValueError as e:
        print(f"API yanıtı JSON olarak işlenemedi: {e}")
    except Exception as e:
        print(f"Bilinmeyen hata: {e}")
    return None

def listele_nobetci_eczane(il, ilce):
    url = "https://api.collectapi.com/health/dutyPharmacy"
    params = {"il": il, "ilce": ilce}
    print("\nNöbetçi eczane bilgileri çekiliyor...")
    data = api_get(url, params)    #API'den gelen cevap data içine kaydedilir.
    if data and data.get("success"):     #veri geldiyse devam edilir.
        eczaneler = data.get("result", [])     #eczane bilgileri alınır.
        print(f"\n🔎 {il}/{ilce} için bulunan nöbetçi eczaneler:")
        print("="*60)
        if eczaneler:
            for eczane in eczaneler:
                print(f"🏪 İsim   : {eczane.get('name', 'Bilgi yok')}")
                print(f"📍 Adres  : {eczane.get('address', 'Bilgi yok')}")
                print(f"📞 Telefon: {eczane.get('phone', 'Bilgi yok')}")
                print("-"*60)
        else:
            print("Bölgede nöbetçi eczane bulunamadı.")
    else:
        print(f"API yanıtı başarısız oldu: {data.get('message', 'Bilinmeyen hata') if data else 'Yanıt alınamadı'}")

def toplam_nobetci_eczane(il):
    url = "https://api.collectapi.com/health/districtList"
    params = {"il": il}      #parametre sadece il
    print(f"\n{il} ilindeki toplam nöbetçi eczane sayısı çekiliyor...")
    data = api_get(url, params)
    if data and data.get("success"):
        eczaneler = data.get("result", [])
        print(f"\n📊 {il} ilinde toplam {len(eczaneler)} adet nöbetçi eczane bulunmaktadır.")
    else:
        print(f"API yanıtı başarısız oldu: {data.get('message', 'Bilinmeyen hata') if data else 'Yanıt alınamadı'}")

def main():
    print("    NÖBETÇİ ECZANE SORGULAMA    ")
    while True:
        print("\nYapmak istediğiniz işlemi seçin:")
        print("1. Nöbetçi eczaneleri listele (il ve ilçe seçerek)")
        print("2. Bir ildeki toplam nöbetçi eczane sayısını öğren")

        islem = secim_al("\nSeçiminiz (1 veya 2): ", ["1", "2"])

        secilen_il = numarali_secim("\nİller:", list(iller.keys()))
        print(f"\nSeçilen il: {secilen_il}")

        if islem == "1":    #işlem 1 ise API'den veri cekilir ekrana yazdırılır.
            secilen_ilce = numarali_secim(f"\n{secilen_il} ilçeleri:", iller[secilen_il])
            print(f"\nSeçilen ilçe: {secilen_ilce}")
            listele_nobetci_eczane(secilen_il, secilen_ilce)
        else:
            toplam_nobetci_eczane(secilen_il)

        devam = secim_al("\nAna menüye dönmek ister misiniz? (Evet/Hayır): ", ["evet", "hayır"])
        if devam == "hayır":
            print("\nProgram sonlandırılıyor. İyi günler!")
            break

if __name__ == "__main__":
    main()     #çalıştığında direkt main fonksiyonunun başlamasını sağlar.
