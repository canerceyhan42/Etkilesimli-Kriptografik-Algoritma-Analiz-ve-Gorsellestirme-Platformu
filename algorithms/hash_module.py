"""
Hash fonksiyonları ve avalanche effect analizi modülü.

Bu modül SHA-256, SHA-512, MD5, SHA-1 hash fonksiyonlarını ve 
avalanche effect analizini içerir.
"""

import hashlib
from typing import Dict
import time


class HashVisualizer:
    """Çoklu hash fonksiyonları ve analiz araçları."""

    def sha256(self, text: str) -> str:
        """
        Metni SHA-256 ile hashler.
        
        Args:
            text: Hashlenecek metin
            
        Returns:
            Hex formatında hash değeri
        """
        return hashlib.sha256(
            text.encode()
        ).hexdigest()

    def sha512(self, text: str) -> str:
        """
        Metni SHA-512 ile hashler.
        
        Args:
            text: Hashlenecek metin
            
        Returns:
            Hex formatında hash değeri
        """
        return hashlib.sha512(
            text.encode()
        ).hexdigest()

    def sha1(self, text: str) -> str:
        """
        Metni SHA-1 ile hashler (Güvenli DEĞİL - sadece demo).
        
        Args:
            text: Hashlenecek metin
            
        Returns:
            Hex formatında hash değeri
        """
        return hashlib.sha1(
            text.encode()
        ).hexdigest()

    def md5(self, text: str) -> str:
        """
        Metni MD5 ile hashler (Güvenli DEĞİL - sadece demo).
        
        Args:
            text: Hashlenecek metin
            
        Returns:
            Hex formatında hash değeri
        """
        return hashlib.md5(
            text.encode()
        ).hexdigest()

    def compare_algorithms(self, text: str) -> str:
        """
        Farklı hash algoritmalarını karşılaştırır.
        
        Args:
            text: Hashlenecek metin
            
        Returns:
            Karşılaştırma raporu
        """
        report = ""
        report += "=" * 70 + "\n"
        report += "HASH ALGORİTMALARI KARŞILAŞTIRMASI\n"
        report += "=" * 70 + "\n\n"
        
        report += f"Metin: {text}\n\n"
        
        # MD5
        start = time.perf_counter()
        md5_hash = self.md5(text)
        md5_time = (time.perf_counter() - start) * 1000
        
        report += "1. MD5 (Güvenli DEĞİL)\n"
        report += f"   Hash: {md5_hash}\n"
        report += f"   Uzunluk: 128 bit\n"
        report += f"   Süre: {md5_time:.4f} ms\n"
        report += "   Durum: Collision bulundu, kullanılmamalı!\n\n"
        
        # SHA-1
        start = time.perf_counter()
        sha1_hash = self.sha1(text)
        sha1_time = (time.perf_counter() - start) * 1000
        
        report += "2. SHA-1 (Güvenli DEĞİL)\n"
        report += f"   Hash: {sha1_hash}\n"
        report += f"   Uzunluk: 160 bit\n"
        report += f"   Süre: {sha1_time:.4f} ms\n"
        report += "   Durum: Collision bulundu, kullanılmamalı!\n\n"
        
        # SHA-256
        start = time.perf_counter()
        sha256_hash = self.sha256(text)
        sha256_time = (time.perf_counter() - start) * 1000
        
        report += "3. SHA-256 (ÖNERİLEN)\n"
        report += f"   Hash: {sha256_hash}\n"
        report += f"   Uzunluk: 256 bit\n"
        report += f"   Süre: {sha256_time:.4f} ms\n"
        report += "   Durum: Güvenli, yaygın kullanımda\n\n"
        
        # SHA-512
        start = time.perf_counter()
        sha512_hash = self.sha512(text)
        sha512_time = (time.perf_counter() - start) * 1000
        
        report += "4. SHA-512 (ÇOK GÜVENLİ)\n"
        report += f"   Hash: {sha512_hash}\n"
        report += f"   Uzunluk: 512 bit\n"
        report += f"   Süre: {sha512_time:.4f} ms\n"
        report += "   Durum: En güvenli, yüksek güvenlik gereken uygulamalar için\n\n"
        
        report += "=" * 70 + "\n"
        report += "NOT: MD5 ve SHA-1 collision saldırılarına karşı savunmasızdır.\n"
        report += "     Kriptografik uygulamalar için SHA-256 veya SHA-512 kullanın.\n"
        report += "=" * 70 + "\n"
        
        return report

    def avalanche_effect(
            self,
            text1: str,
            text2: str
    ) -> Dict[str, any]:
        """
        İki metin arasında avalanche effect analizini yapar.
        
        Avalanche effect: Girdide küçük bir değişiklik, çıktıda
        büyük değişikliklere yol açmalıdır (ideal: ~50% bit değişimi).
        
        Args:
            text1: İlk metin
            text2: İkinci metin
            
        Returns:
            Hash değerleri, farklı bit sayısı ve değişim yüzdesi
        """
        hash1 = self.sha256(text1)
        hash2 = self.sha256(text2)

        bits1 = bin(
            int(hash1, 16)
        )[2:].zfill(256)

        bits2 = bin(
            int(hash2, 16)
        )[2:].zfill(256)

        diff = 0

        for a, b in zip(bits1, bits2):

            if a != b:
                diff += 1

        percentage = round(
            (diff / 256) * 100,
            2
        )

        return {
            "hash1": hash1,
            "hash2": hash2,
            "different_bits": diff,
            "percentage": percentage
        }