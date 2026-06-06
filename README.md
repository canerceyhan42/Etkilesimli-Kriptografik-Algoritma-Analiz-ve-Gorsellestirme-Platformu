# CryptoVisualizer

## Etkileşimli Kriptografik Algoritma Analiz ve Görselleştirme Platformu

Bu proje, Kriptografi ve Uygulamaları dersi final projesi kapsamında geliştirilmiştir. Amaç, temel kriptografik algoritmaların çalışma prensiplerini görselleştirmek ve kullanıcıların bu algoritmaları etkileşimli olarak inceleyebilmesini sağlamaktır.

---

## Özellikler

### 🔐 AES (Advanced Encryption Standard)

* ✅ AES-128 şifreleme ve **deşifreleme**
* ✅ **Gerçek AES S-Box** kullanımı
* ✅ State Matrix gösterimi
* ✅ SubBytes görselleştirmesi
* ✅ ShiftRows görselleştirmesi
* ✅ MixColumns görselleştirmesi
* ✅ AddRoundKey görselleştirmesi
* ✅ **🎬 İnteraktif Adım Adım Görselleştirme**
  * ⏮ İlk adıma git
  * ◀ Geri / İleri ▶ butonları
  * ⏭ Son adıma git
  * ▶ Otomatik oynatma (hız ayarı: 500-5000 ms)
  * Adım göstergesi (1/6, 2/6...)
* ✅ Dosyadan metin yükleme
* ✅ Sonuçları kopyalama ve kaydetme

### 🔓 DES (Data Encryption Standard)

* ✅ DES şifreleme ve **deşifreleme**
* ✅ **Görselleştirme**: Initial Permutation, 16 Rounds, Final Permutation
* ✅ Feistel fonksiyonu açıklaması
* ✅ Binary gösterim

### 🔒 3DES (Triple DES)

* ✅ Triple DES şifreleme ve **deşifreleme**
* ✅ **Görselleştirme**: EDE (Encrypt-Decrypt-Encrypt) modu
* ✅ Üçlü anahtar sistemi gösterimi
* ✅ Güvenlik analizi

### 🔨 SHA-256 ve Hash Fonksiyonları

* ✅ SHA-256 hash üretimi
* ✅ **SHA-512, SHA-1, MD5** desteği
* ✅ **Algoritma karşılaştırması** (hız ve güvenlik)
* ✅ Hash değeri görüntüleme

### 📊 Avalanche Effect Analizi

* ✅ İki farklı girdinin hash sonuçlarını karşılaştırma
* ✅ Farklı bit sayısını hesaplama
* ✅ Değişim yüzdesini gösterme

### 🔑 HMAC-SHA256

* ✅ Anahtarlı mesaj doğrulama kodu üretimi
* ✅ HMAC formülü açıklaması

### ➗ GF(2^8) Galois Field İşlemleri

* ✅ GF(2^8) çarpma işlemi
* ✅ Adım adım işlem görselleştirmesi
* ✅ AES polinomu kullanımı
* ✅ **Detaylı docstring ve açıklamalar**

### 🎲 Random Bit Generator

* ✅ 128, 256, 512 bit rastgele değer üretimi
* ✅ **İstatistiksel analiz** (bit dağılımı, kalite değerlendirmesi)
* ✅ **PRNG vs CSPRNG karşılaştırması**
* ✅ Entropi kaynağı açıklaması
* ✅ Güvenlik özellikleri açıklaması


---

## Kullanılan Teknolojiler

* Python 3.8+
* Tkinter (GUI)
* PyCryptodome (Kriptografik algoritmalar)
* Pyperclip (Clipboard işlemleri)

---

## Kurulum

Gerekli kütüphaneleri yükleyin:

```bash
pip install -r requirements.txt
```

---

## Çalıştırma

```bash
python main.py
```

veya

```bash
cd Kriptoloji_Final_Projesi
python main.py
```

---

## Proje Yapısı

```text
Kriptoloji_Final_Projesi/
│
├── main.py                          # Ana GUI uygulaması
│
├── algorithms/                      # Algoritma modülleri
│   ├── aes_module.py               # AES-128 + S-Box + Görselleştirme
│   ├── des_module.py               # DES + Görselleştirme
│   ├── triple_des_module.py        # 3DES + EDE Görselleştirme
│   ├── hash_module.py              # SHA-256/512, MD5, SHA-1 + Karşılaştırma
│   ├── hmac_module.py              # HMAC-SHA256
│   ├── rbg_module.py               # RBG + İstatistik + PRNG vs CSPRNG
│   └── galois_module.py            # GF(2^8) + Detaylı Açıklamalar
│
├── requirements.txt                 # Bağımlılıklar
└── README.md                        # Bu dosya
```

---

## Kullanım Örnekleri

### AES Şifreleme
1. **AES** sekmesine gidin
2. Plaintext girin veya "📁 Dosyadan Yükle" butonuyla yükleyin
3. 16 karakterlik key girin
4. **Encrypt & Visualize** butonuna tıklayın
5. Sonuçları "📋 Kopyala" veya "💾 Kaydet" ile kaydedin

### Hash Karşılaştırması
1. **SHA-256** sekmesine gidin
2. "Algoritma Karşılaştırması" bölümüne bir metin girin
3. **Algoritmaları Karşılaştır** butonuna tıklayın
4. MD5, SHA-1, SHA-256, SHA-512 sonuçlarını ve hız karşılaştırmasını görün

### PRNG vs CSPRNG Analizi
1. **RBG** sekmesine gidin
2. **PRNG vs CSPRNG** butonuna tıklayın
3. Güvenli ve güvensiz rastgele sayı üreticilerinin farkını görün

---


## Eğitimsel Değer

Bu platform aşağıdaki kriptografik kavramları öğretir:

1. **Simetrik Şifreleme**: AES, DES, 3DES
2. **Hash Fonksiyonları**: SHA ailesi, avalanche effect
3. **Galois Field Matematiği**: GF(2^8) aritmetiği
4. **HMAC**: Mesaj kimlik doğrulama
5. **Rastgele Sayı Üretimi**: CSPRNG vs PRNG
6. **Güvenlik Prensipleri**: Collision, entropy, key management

---

## Geliştirici


* **Caner CEYHAN**
* **Yusuf ALP**

**Ders**: Kriptografi ve Uygulamaları  
**Kurum**: Osmaniye Korkut Ata Üniversitesi  
**Yıl**: 2025-2026

---



## Kaynaklar

1. FIPS 197 - Advanced Encryption Standard (AES)
2. FIPS 46-3 - Data Encryption Standard (DES)
3. FIPS 180-4 - Secure Hash Standard (SHS)
4. RFC 2104 - HMAC: Keyed-Hashing for Message Authentication
5. Python Cryptographic Authority - cryptography.io

---


