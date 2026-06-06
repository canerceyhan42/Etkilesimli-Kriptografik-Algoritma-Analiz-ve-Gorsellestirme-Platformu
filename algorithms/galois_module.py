"""
Galois Field GF(2^8) işlemleri modülü.

AES'te kullanılan GF(2^8) aritmetiğini implemente eder.
Tüm işlemler AES polinomu (x^8 + x^4 + x^3 + x + 1) üzerinde yapılır.
"""

from typing import Tuple, List


class GaloisField:
    """GF(2^8) Galois Field işlemleri."""

    AES_POLY = 0x1B  # x^8 + x^4 + x^3 + x + 1 = 0x11B, modulodan sonra 0x1B

    def add(self, a: int, b: int) -> int:
        """
        GF(2^8) toplama işlemi (XOR).
        
        Args:
            a: İlk byte
            b: İkinci byte
            
        Returns:
            a + b (GF(2^8) üzerinde)
        """
        return a ^ b

    def multiply(self, a: int, b: int) -> Tuple[int, List[str]]:
        """
        GF(2^8) çarpma işlemi.
        
        Peasant çarpma algoritması kullanılır:
        - b'nin en düşük biti 1 ise sonuca a eklenir
        - a bir bit sola kaydırılır
        - a >= 0x100 ise AES polinomu ile modulo alınır
        - b bir bit sağa kaydırılır
        
        Args:
            a: İlk byte
            b: İkinci byte
            
        Returns:
            (sonuç, adım_listesi) tuple'ı
        """
        result = 0

        steps = []

        original_a = a
        original_b = b

        for i in range(8):

            steps.append(
                f"Adım {i+1}: a={hex(a)} b={hex(b)} result={hex(result)}"
            )

            if b & 1:
                result ^= a

            carry = a & 0x80

            a <<= 1

            if carry:
                a ^= self.AES_POLY

            a &= 0xFF

            b >>= 1

        steps.append(
            f"\nSonuç = {hex(result)}"
        )

        return result, steps

    def visualize_multiplication(self, a_hex: str, b_hex: str) -> str:
        """
        GF(2^8) çarpma işlemini adım adım görselleştirir.
        
        Args:
            a_hex: İlk byte (hex string)
            b_hex: İkinci byte (hex string)
            
        Returns:
            Görselleştirme raporu
            
        Raises:
            ValueError: Geçersiz hex değeri
        """
        try:
            a = int(a_hex, 16)
            b = int(b_hex, 16)
        except ValueError:
            raise ValueError("Geçersiz hex değeri. Örnek: 'A3' veya '5F'")

        if not (0 <= a <= 255 and 0 <= b <= 255):
            raise ValueError("Değerler 0x00-0xFF aralığında olmalıdır")

        result, steps = self.multiply(a, b)

        report = ""

        report += "GF(2^8) ÇARPMA İŞLEMİ\n"
        report += "=" * 40 + "\n\n"

        report += f"A = {a_hex}\n"
        report += f"B = {b_hex}\n\n"

        report += "\n".join(steps)

        return report