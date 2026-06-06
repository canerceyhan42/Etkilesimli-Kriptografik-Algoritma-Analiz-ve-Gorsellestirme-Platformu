"""
DES (Data Encryption Standard) modülü.

DES şifreleme, deşifreleme ve görselleştirme fonksiyonlarını içerir.
"""

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import binascii


class DESVisualizer:
    """DES şifreleme ve görselleştirme sınıfı."""

    def encrypt(
            self,
            plaintext,
            key
    ):
        """
        DES ile metni şifreler.
        
        Args:
            plaintext: Şifrelenecek metin
            key: 8 karakterlik anahtar
            
        Returns:
            Şifreli metin (hex format)
        """
        key = key.encode()

        if len(key) < 8:
            key = key.ljust(8, b'0')

        key = key[:8]

        cipher = DES.new(
            key,
            DES.MODE_ECB
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
        DES ile şifreli metni çözer.
        
        Args:
            ciphertext: Şifreli metin (hex formatında)
            key: 8 karakterlik anahtar
            
        Returns:
            Çözülmüş plaintext
            
        Raises:
            ValueError: Geçersiz şifreli metin
        """
        try:
            key = key.encode()

            if len(key) < 8:
                key = key.ljust(8, b'0')

            key = key[:8]

            cipher = DES.new(
                key,
                DES.MODE_ECB
            )

            encrypted_bytes = binascii.unhexlify(ciphertext)
            
            decrypted = cipher.decrypt(encrypted_bytes)
            
            decrypted = unpad(decrypted, 8)

            return decrypted.decode()
            
        except Exception as e:
            raise ValueError(f"DES deşifreleme hatası: {str(e)}")

    def visualize(self, plaintext, key):
        """
        DES şifreleme adımlarını görselleştirir.
        
        Args:
            plaintext: Şifrelenecek metin
            key: 8 karakterlik anahtar
            
        Returns:
            Görselleştirme raporu
        """
        data = plaintext.encode()
        data = pad(data, 8)
        block = data[:8]
        
        key_bytes = key.encode()
        if len(key_bytes) < 8:
            key_bytes = key_bytes.ljust(8, b'0')
        key_bytes = key_bytes[:8]
        
        report = ""
        report += "=" * 60 + "\n"
        report += "DES ŞİFRELEME ADIMLARI GÖRSELLEŞTİRMESİ\n"
        report += "=" * 60 + "\n\n"
        
        # Plaintext
        report += "1. PLAINTEXT (64-bit)\n"
        report += f"   Metin: {plaintext[:8]}\n"
        report += f"   Hex: {binascii.hexlify(block).decode()}\n"
        report += f"   Binary: {bin(int(binascii.hexlify(block), 16))[2:].zfill(64)}\n\n"
        
        # Key
        report += "2. KEY (64-bit, 56-bit efektif)\n"
        report += f"   Key: {key[:8]}\n"
        report += f"   Hex: {binascii.hexlify(key_bytes).decode()}\n\n"
        
        # Initial Permutation
        report += "3. INITIAL PERMUTATION (IP)\n"
        report += "   64-bit veri IP tablosu ile permüte edilir\n"
        report += "   L0 (32-bit) | R0 (32-bit) oluşturulur\n\n"
        
        # 16 Rounds
        report += "4. 16 ROUND İŞLEMLERİ\n"
        report += "   Her round'da Feistel fonksiyonu uygulanır:\n"
        report += "   • Li = Ri-1\n"
        report += "   • Ri = Li-1 ⊕ f(Ri-1, Ki)\n\n"
        
        report += "   Feistel Fonksiyonu f(R, K):\n"
        report += "   a) Expansion (E): 32-bit → 48-bit\n"
        report += "   b) Key Mixing: E(R) ⊕ K\n"
        report += "   c) S-Box: 48-bit → 32-bit (8 S-Box)\n"
        report += "   d) Permutation (P): 32-bit permütasyon\n\n"
        
        report += "   Round 1: L1, R1 hesaplanır\n"
        report += "   Round 2: L2, R2 hesaplanır\n"
        report += "   ...\n"
        report += "   Round 16: L16, R16 hesaplanır\n\n"
        
        # Final Permutation
        report += "5. FINAL PERMUTATION (FP = IP^-1)\n"
        report += "   R16 | L16 birleştirilir ve FP uygulanır\n\n"
        
        # Result
        encrypted = self.encrypt(plaintext, key)
        report += "6. SONUÇ (CIPHERTEXT)\n"
        report += f"   Hex: {encrypted}\n"
        report += f"   Binary: {bin(int(encrypted, 16))[2:].zfill(64)}\n\n"
        
        report += "=" * 60 + "\n"
        report += "NOT: DES, 64-bit bloklar üzerinde 16 round Feistel\n"
        report += "     Network yapısı kullanır. Her round için farklı\n"
        report += "     bir 48-bit subkey üretilir.\n"
        report += "=" * 60 + "\n"
        
        return report