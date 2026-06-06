"""
Triple DES (3DES) modülü.

3DES şifreleme, deşifreleme ve görselleştirme fonksiyonlarını içerir.
"""

from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
import binascii


class TripleDESVisualizer:
    """3DES şifreleme ve görselleştirme sınıfı."""

    def encrypt(
            self,
            plaintext,
            key
    ):
        """
        3DES ile metni şifreler.
        
        Args:
            plaintext: Şifrelenecek metin
            key: 24 karakterlik anahtar
            
        Returns:
            Şifreli metin (hex format)
        """
        key = key.encode()

        if len(key) < 24:
            key = key.ljust(24, b'0')

        key = key[:24]

        cipher = DES3.new(
            key,
            DES3.MODE_ECB
        )

        encrypted = cipher.encrypt(
            pad(
                plaintext.encode(),
                8
            )
        )

        return binascii.hexlify(
            encrypted
        ).decode()

    def decrypt(
            self,
            ciphertext,
            key
    ):
        """
        3DES ile şifreli metni çözer.
        
        Args:
            ciphertext: Şifreli metin (hex formatında)
            key: 24 karakterlik anahtar
            
        Returns:
            Çözülmüş plaintext
            
        Raises:
            ValueError: Geçersiz şifreli metin
        """
        try:
            key = key.encode()

            if len(key) < 24:
                key = key.ljust(24, b'0')

            key = key[:24]

            cipher = DES3.new(
                key,
                DES3.MODE_ECB
            )

            encrypted_bytes = binascii.unhexlify(ciphertext)
            
            decrypted = cipher.decrypt(encrypted_bytes)
            
            decrypted = unpad(decrypted, 8)

            return decrypted.decode()
            
        except Exception as e:
            raise ValueError(f"3DES deşifreleme hatası: {str(e)}")

    def visualize(self, plaintext, key):
        """
        3DES şifreleme adımlarını görselleştirir.
        
        Args:
            plaintext: Şifrelenecek metin
            key: 24 karakterlik anahtar
            
        Returns:
            Görselleştirme raporu
        """
        key_bytes = key.encode()
        if len(key_bytes) < 24:
            key_bytes = key_bytes.ljust(24, b'0')
        key_bytes = key_bytes[:24]
        
        # 3 anahtarı ayır
        k1 = key_bytes[:8]
        k2 = key_bytes[8:16]
        k3 = key_bytes[16:24]
        
        report = ""
        report += "=" * 60 + "\n"
        report += "3DES (TRIPLE DES) ŞİFRELEME GÖRSELLEŞTİRMESİ\n"
        report += "=" * 60 + "\n\n"
        
        report += "3DES = EDE (Encrypt-Decrypt-Encrypt) Modu\n\n"
        
        # Keys
        report += "1. ÜÇLÜ ANAHTAR SİSTEMİ (168-bit efektif)\n"
        report += f"   K1 (64-bit): {binascii.hexlify(k1).decode()}\n"
        report += f"   K2 (64-bit): {binascii.hexlify(k2).decode()}\n"
        report += f"   K3 (64-bit): {binascii.hexlify(k3).decode()}\n\n"
        
        # Plaintext
        data = plaintext.encode()
        data = pad(data, 8)
        block = data[:8]
        
        report += "2. PLAINTEXT\n"
        report += f"   Metin: {plaintext[:8]}\n"
        report += f"   Hex: {binascii.hexlify(block).decode()}\n\n"
        
        # 3DES Process
        report += "3. ÜÇLÜ ŞİFRELEME SÜRECİ\n"
        report += "   ┌─────────────────────────────────────┐\n"
        report += "   │  Plaintext                          │\n"
        report += "   └──────────────┬──────────────────────┘\n"
        report += "                  ▼\n"
        report += "   ┌─────────────────────────────────────┐\n"
        report += "   │  DES ENCRYPT (K1)                   │\n"
        report += "   │  • 16 rounds Feistel Network        │\n"
        report += "   └──────────────┬──────────────────────┘\n"
        report += "                  ▼\n"
        report += "            Intermediate 1\n"
        report += "                  ▼\n"
        report += "   ┌─────────────────────────────────────┐\n"
        report += "   │  DES DECRYPT (K2)                   │\n"
        report += "   │  • 16 rounds (ters sıra)            │\n"
        report += "   └──────────────┬──────────────────────┘\n"
        report += "                  ▼\n"
        report += "            Intermediate 2\n"
        report += "                  ▼\n"
        report += "   ┌─────────────────────────────────────┐\n"
        report += "   │  DES ENCRYPT (K3)                   │\n"
        report += "   │  • 16 rounds Feistel Network        │\n"
        report += "   └──────────────┬──────────────────────┘\n"
        report += "                  ▼\n"
        report += "   ┌─────────────────────────────────────┐\n"
        report += "   │  Ciphertext                         │\n"
        report += "   └─────────────────────────────────────┘\n\n"
        
        # Result
        encrypted = self.encrypt(plaintext, key)
        report += "4. SONUÇ (CIPHERTEXT)\n"
        report += f"   Hex: {encrypted}\n\n"
        
        report += "=" * 60 + "\n"
        report += "GÜVENLİK ANALİZİ:\n"
        report += "• Efektif anahtar uzunluğu: 168 bit (DES'in 56 bit'ine karşı)\n"
        report += "• Brute force saldırılara karşı son derece dirençli\n"
        report += "• DES'in geriye uyumlu alternatifi (K1=K2=K3 ise DES)\n"
        report += "• EDE modu: Encrypt(K1) → Decrypt(K2) → Encrypt(K3)\n"
        report += "=" * 60 + "\n"
        
        return report