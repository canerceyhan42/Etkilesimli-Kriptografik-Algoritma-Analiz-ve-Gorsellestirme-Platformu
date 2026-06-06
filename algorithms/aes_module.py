"""
AES (Advanced Encryption Standard) modülü.

AES-128 şifreleme ve görselleştirme fonksiyonlarını içerir.
"""

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii
from typing import List


class AESVisualizer:
    """AES-128 şifreleme ve görselleştirme sınıfı."""

    # Gerçek AES S-Box
    SBOX = [
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
    ]

    def __init__(self):
        pass

    def sbox_lookup(self, byte_val: int) -> int:
        """
        AES S-Box lookup işlemi.
        
        Args:
            byte_val: Giriş byte değeri (0-255)
            
        Returns:
            S-Box'tan dönen değer
        """
        return self.SBOX[byte_val]

    def text_to_matrix(self, text: bytes) -> List[List[str]]:
        """
        Byte dizisini 4x4 hex matrisine dönüştürür.
        
        Args:
            text: 16 byte'lık veri
            
        Returns:
            4x4 hex değerler matrisi
        """
        matrix = []

        for i in range(0, 16, 4):

            row = []

            for j in range(4):
                row.append(hex(text[i + j])[2:].zfill(2))

            matrix.append(row)

        return matrix

    def matrix_to_string(self, matrix: List[List[str]]) -> str:
        """
        Matrisi string formatına dönüştürür.
        
        Args:
            matrix: 4x4 hex matrisi
            
        Returns:
            Formatlanmış string
        """
        output = ""

        for row in matrix:
            output += " ".join(row)
            output += "\n"

        return output

    def sub_bytes_demo(self, matrix: List[List[str]]) -> List[List[str]]:
        """
        SubBytes işlemi - Gerçek AES S-Box kullanır.
        
        Her byte S-Box tablosundan geçirilir.
        
        Args:
            matrix: 4x4 hex matrisi
            
        Returns:
            Dönüştürülmüş matris
        """
        result = []

        for row in matrix:

            new_row = []

            for value in row:

                byte = int(value, 16)

                # Gerçek S-Box kullan
                transformed = self.sbox_lookup(byte)

                new_row.append(
                    hex(transformed)[2:].zfill(2)
                )

            result.append(new_row)

        return result

    def shift_rows_demo(self, matrix):

        shifted = []

        for i, row in enumerate(matrix):

            shifted.append(
                row[i:] + row[:i]
            )

        return shifted

    def mix_columns_demo(self, matrix):

        mixed = []

        for row in matrix:

            new_row = []

            for value in row:

                byte = int(value, 16)

                mixed_value = ((byte << 1) & 0xFF)

                new_row.append(
                    hex(mixed_value)[2:].zfill(2)
                )

            mixed.append(new_row)

        return mixed

    def add_round_key_demo(self, matrix):

        result = []

        for row in matrix:

            new_row = []

            for value in row:

                byte = int(value, 16)

                transformed = byte ^ 0x0F

                new_row.append(
                    hex(transformed)[2:].zfill(2)
                )

            result.append(new_row)

        return result

    def visualize(self, plaintext: str) -> str:
        """
        AES şifreleme adımlarını görselleştirir (1 round demo).
        
        Args:
            plaintext: Görselleştirilecek metin
            
        Returns:
            Adım adım görselleştirme raporu
        """
        data = plaintext.encode()

        data = pad(data, 16)

        block = data[:16]

        matrix = self.text_to_matrix(block)

        report = ""

        report += "=" * 60 + "\n"
        report += "AES-128 ŞİFRELEME ADIMLARI (Round 1 Demo)\n"
        report += "=" * 60 + "\n\n"

        report += "0. INITIAL STATE (Plaintext)\n"
        report += self.matrix_to_string(matrix)
        report += "\n"

        sub = self.sub_bytes_demo(matrix)

        report += "1. SUB BYTES (S-Box Substitution)\n"
        report += "   Her byte, AES S-Box tablosundan geçirilir.\n"
        report += "   S-Box: Doğrusal olmayan dönüşüm sağlar.\n\n"
        report += self.matrix_to_string(sub)
        report += "\n"

        shift = self.shift_rows_demo(sub)

        report += "2. SHIFT ROWS (Satır Kaydırma)\n"
        report += "   • Satır 0: Kaydırma yok\n"
        report += "   • Satır 1: 1 byte sola\n"
        report += "   • Satır 2: 2 byte sola\n"
        report += "   • Satır 3: 3 byte sola\n\n"
        report += self.matrix_to_string(shift)
        report += "\n"

        mix = self.mix_columns_demo(shift)

        report += "3. MIX COLUMNS (Sütun Karıştırma)\n"
        report += "   Her sütun GF(2^8) üzerinde matris çarpımı ile\n"
        report += "   dönüştürülür (son round'da yapılmaz).\n\n"
        report += self.matrix_to_string(mix)
        report += "\n"

        add = self.add_round_key_demo(mix)

        report += "4. ADD ROUND KEY (Anahtar Ekleme)\n"
        report += "   State ile round key XOR edilir.\n\n"
        report += self.matrix_to_string(add)
        report += "\n"

        report += "=" * 60 + "\n"
        report += "NOT: AES-128'de 10 round vardır.\n"
        report += "     Son round'da MixColumns adımı yapılmaz.\n"
        report += "     Her round için farklı round key kullanılır.\n"
        report += "=" * 60 + "\n"

        return report

    def get_visualization_steps(self, plaintext: str) -> list:
        """
        AES adımlarını liste olarak döndürür (ileri/geri sarma için).
        
        Args:
            plaintext: Görselleştirilecek metin
            
        Returns:
            (başlık, içerik) tuple'larından oluşan liste
        """
        data = plaintext.encode()
        data = pad(data, 16)
        block = data[:16]
        
        steps = []
        
        # Adım 0: Initial State
        matrix = self.text_to_matrix(block)
        content = "PLAINTEXT\n\n"
        content += self.matrix_to_string(matrix)
        content += "\nBu, şifrelenecek verinin 4x4 state matrix formatında gösterimidir."
        steps.append(("0. INITIAL STATE", content))
        
        # Adım 1: SubBytes
        sub = self.sub_bytes_demo(matrix)
        content = "S-BOX SUBSTITUTION\n\n"
        content += "Her byte, AES S-Box tablosundan geçirilir.\n"
        content += "S-Box: Doğrusal olmayan dönüşüm sağlar.\n\n"
        content += "ÖNCE:\n"
        content += self.matrix_to_string(matrix)
        content += "\nSONRA:\n"
        content += self.matrix_to_string(sub)
        steps.append(("1. SUB BYTES", content))
        
        # Adım 2: ShiftRows
        shift = self.shift_rows_demo(sub)
        content = "SHIFT ROWS (Satır Kaydırma)\n\n"
        content += "• Satır 0: Kaydırma yok\n"
        content += "• Satır 1: 1 byte sola kaydırılır\n"
        content += "• Satır 2: 2 byte sola kaydırılır\n"
        content += "• Satır 3: 3 byte sola kaydırılır\n\n"
        content += "ÖNCE:\n"
        content += self.matrix_to_string(sub)
        content += "\nSONRA:\n"
        content += self.matrix_to_string(shift)
        steps.append(("2. SHIFT ROWS", content))
        
        # Adım 3: MixColumns
        mix = self.mix_columns_demo(shift)
        content = "MIX COLUMNS (Sütun Karıştırma)\n\n"
        content += "Her sütun GF(2^8) üzerinde matris çarpımı ile dönüştürülür.\n"
        content += "Son round'da bu adım yapılmaz.\n\n"
        content += "ÖNCE:\n"
        content += self.matrix_to_string(shift)
        content += "\nSONRA:\n"
        content += self.matrix_to_string(mix)
        steps.append(("3. MIX COLUMNS", content))
        
        # Adım 4: AddRoundKey
        add = self.add_round_key_demo(mix)
        content = "ADD ROUND KEY (Anahtar Ekleme)\n\n"
        content += "State matrisi ile round key XOR edilir.\n"
        content += "Bu adım, şifrelemenin güvenliğini sağlar.\n\n"
        content += "ÖNCE:\n"
        content += self.matrix_to_string(mix)
        content += "\nSONRA:\n"
        content += self.matrix_to_string(add)
        steps.append(("4. ADD ROUND KEY", content))
        
        # Final
        content = "AES-128 ŞİFRELEME TAMAMLANDI\n\n"
        content += "Final State:\n"
        content += self.matrix_to_string(add)
        content += "\n\nNOT:\n"
        content += "• AES-128'de toplam 10 round vardır\n"
        content += "• Bu görselleştirme 1. round'u göstermektedir\n"
        content += "• Her round için farklı round key kullanılır\n"
        content += "• Son round'da MixColumns adımı yapılmaz"
        steps.append(("5. SONUÇ", content))
        
        return steps

    def encrypt(self, plaintext: str, key: str) -> str:
        """
        AES-128 ile metni şifreler.
        
        Args:
            plaintext: Şifrelenecek metin
            key: Şifreleme anahtarı (minimum 16 karakter önerilir)
            
        Returns:
            Hex formatında şifreli metin
            
        Raises:
            Exception: Şifreleme hatası
        """
        key = key.encode()

        if len(key) < 16:
            key = key.ljust(16, b'0')

        key = key[:16]

        cipher = AES.new(key, AES.MODE_ECB)

        encrypted = cipher.encrypt(
            pad(
                plaintext.encode(),
                AES.block_size
            )
        )

        return binascii.hexlify(
            encrypted
        ).decode()

    def decrypt(self, ciphertext: str, key: str) -> str:
        """
        AES-128 ile şifreli metni çözer.
        
        Args:
            ciphertext: Şifreli metin (hex formatında)
            key: Deşifreleme anahtarı
            
        Returns:
            Çözülmüş plaintext
            
        Raises:
            ValueError: Geçersiz şifreli metin formatı
        """
        from Crypto.Util.Padding import unpad
        
        try:
            key = key.encode()

            if len(key) < 16:
                key = key.ljust(16, b'0')

            key = key[:16]

            cipher = AES.new(key, AES.MODE_ECB)

            encrypted_bytes = binascii.unhexlify(ciphertext)
            
            decrypted = cipher.decrypt(encrypted_bytes)
            
            decrypted = unpad(decrypted, AES.block_size)

            return decrypted.decode()
            
        except Exception as e:
            raise ValueError(f"Deşifreleme hatası: {str(e)}")