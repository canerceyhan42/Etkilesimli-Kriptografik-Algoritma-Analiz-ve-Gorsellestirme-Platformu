"""
Rastgele bit üretici modülü.

Kriptografik güvenli rastgele sayı üretimi için secrets modülünü kullanır.
PRNG vs CSPRNG karşılaştırması ve basit istatistiksel testler içerir.
"""

import secrets
import random
from typing import Dict


class RandomBitGenerator:
    """Kriptografik güvenli rastgele bit üreticisi."""

    def generate(self, bits: int) -> str:
        """
        Belirtilen uzunlukta kriptografik güvenli rastgele değer üretir.
        
        Args:
            bits: Üretilecek bit sayısı (128, 256, 512 vb.)
            
        Returns:
            Hex formatında rastgele değer
            
        Raises:
            ValueError: Geçersiz bit sayısı
        """
        if bits <= 0 or bits % 8 != 0:
            raise ValueError("Bit sayısı pozitif ve 8'in katı olmalıdır")

        bytes_count = bits // 8

        return secrets.token_hex(
            bytes_count
        )

    def generate_with_analysis(self, bits: int) -> str:
        """
        Rastgele bit üretir ve istatistiksel analiz yapar.
        
        Args:
            bits: Üretilecek bit sayısı
            
        Returns:
            Detaylı analiz raporu
        """
        random_hex = self.generate(bits)
        
        # Hex'i binary'e çevir
        random_int = int(random_hex, 16)
        random_bits = bin(random_int)[2:].zfill(bits)
        
        # İstatistiksel analiz
        ones = random_bits.count('1')
        zeros = random_bits.count('0')
        ones_percent = (ones / bits) * 100
        zeros_percent = (zeros / bits) * 100
        
        report = ""
        report += "=" * 70 + "\n"
        report += f"KRIPTOGRAFIK GÜVENLI RASTGELE BIT ÜRETIMI ({bits} bit)\n"
        report += "=" * 70 + "\n\n"
        
        report += "1. ENTROPI KAYNAĞI\n"
        report += "   • secrets.token_hex() kullanılıyor\n"
        report += "   • İşletim sistemi entropi havuzundan beslenir\n"
        report += "   • Kriptografik uygulamalar için güvenli\n\n"
        
        report += "2. ÜRETILEN DEĞER\n"
        report += f"   Hex: {random_hex}\n"
        report += f"   Binary (ilk 64 bit): {random_bits[:64]}...\n\n"
        
        report += "3. İSTATİSTİKSEL ANALİZ\n"
        report += f"   • Toplam bit sayısı: {bits}\n"
        report += f"   • 1'ler: {ones} ({ones_percent:.2f}%)\n"
        report += f"   • 0'lar: {zeros} ({zeros_percent:.2f}%)\n"
        report += f"   • İdeal dağılım: 50% / 50%\n"
        report += f"   • Sapma: {abs(50 - ones_percent):.2f}%\n\n"
        
        # Randomness quality assessment
        deviation = abs(50 - ones_percent)
        if deviation < 2:
            quality = "Mükemmel"
        elif deviation < 5:
            quality = "Çok İyi"
        elif deviation < 10:
            quality = "İyi"
        else:
            quality = "Orta"
        
        report += f"   Kalite Değerlendirmesi: {quality}\n\n"
        
        report += "4. GÜVENLİK ÖZELLİKLERİ\n"
        report += "   ✓ Tahmin edilemez (unpredictable)\n"
        report += "   ✓ Tekrar üretilemez (non-reproducible)\n"
        report += "   ✓ Backward/forward secrecy\n"
        report += "   ✓ Kriptografik standartlara uygun\n\n"
        
        report += "=" * 70 + "\n"
        
        return report

    def compare_prng_vs_csprng(self, count: int = 100) -> str:
        """
        PRNG (random modülü) ile CSPRNG (secrets modülü) karşılaştırması.
        
        Args:
            count: Üretilecek sayı adedi
            
        Returns:
            Karşılaştırma raporu
        """
        report = ""
        report += "=" * 70 + "\n"
        report += "PRNG vs CSPRNG KARŞILAŞTIRMASI\n"
        report += "=" * 70 + "\n\n"
        
        # PRNG (random modülü)
        random.seed(12345)  # Sabit seed - tahmin edilebilir!
        prng_values = [random.randint(0, 255) for _ in range(count)]
        prng_bits = ''.join(bin(x)[2:].zfill(8) for x in prng_values[:10])
        prng_ones = prng_bits.count('1')
        prng_ones_percent = (prng_ones / len(prng_bits)) * 100
        
        report += "1. PRNG (Pseudo Random Number Generator)\n"
        report += "   Modül: random\n"
        report += f"   İlk 10 değer: {prng_values[:10]}\n"
        report += f"   Binary (80 bit): {prng_bits}\n"
        report += f"   1'ler: %{prng_ones_percent:.1f}\n\n"
        
        report += "   ❌ DEZAVANTAJLAR:\n"
        report += "   • Deterministic (seed bilinirse tahmin edilebilir)\n"
        report += "   • Kriptografik uygulamalar için GÜVENSİZ\n"
        report += "   • Aynı seed → Aynı sonuçlar\n\n"
        
        report += "   ✓ AVANTAJLAR:\n"
        report += "   • Hızlı\n"
        report += "   • Test ve simulation için uygun\n"
        report += "   • Tekrar üretilebilir (reproducible)\n\n"
        
        # CSPRNG (secrets modülü)
        csprng_values = [secrets.randbelow(256) for _ in range(count)]
        csprng_bits = ''.join(bin(x)[2:].zfill(8) for x in csprng_values[:10])
        csprng_ones = csprng_bits.count('1')
        csprng_ones_percent = (csprng_ones / len(csprng_bits)) * 100
        
        report += "2. CSPRNG (Cryptographically Secure PRNG)\n"
        report += "   Modül: secrets\n"
        report += f"   İlk 10 değer: {csprng_values[:10]}\n"
        report += f"   Binary (80 bit): {csprng_bits}\n"
        report += f"   1'ler: %{csprng_ones_percent:.1f}\n\n"
        
        report += "   ✓ AVANTAJLAR:\n"
        report += "   • Kriptografik olarak güvenli\n"
        report += "   • Tahmin edilemez\n"
        report += "   • OS entropi havuzundan beslenir\n"
        report += "   • Anahtar üretimi için uygun\n\n"
        
        report += "   ❌ DEZAVANTAJLAR:\n"
        report += "   • PRNG'ye göre daha yavaş\n"
        report += "   • Tekrar üretilemez\n\n"
        
        report += "=" * 70 + "\n"
        report += "SONUÇ:\n"
        report += "• Şifreleme anahtarları için: secrets (CSPRNG) ✓\n"
        report += "• Token/password üretimi için: secrets (CSPRNG) ✓\n"
        report += "• Oyun/simulation için: random (PRNG) ✓\n"
        report += "• Test data için: random (PRNG) ✓\n"
        report += "=" * 70 + "\n"
        
        return report