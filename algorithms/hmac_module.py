"""
HMAC (Hash-based Message Authentication Code) modülü.

HMAC, mesaj bütünlüğü ve kimlik doğrulama için kullanılır.
"""

import hmac
import hashlib


class HMACVisualizer:
    """HMAC-SHA256 implementasyonu."""

    def generate(
            self,
            message: str,
            key: str
    ) -> str:
        """
        Mesaj için HMAC-SHA256 değeri üretir.
        
        HMAC = H((K ⊕ opad) || H((K ⊕ ipad) || message))
        
        Args:
            message: HMAC hesaplanacak mesaj
            key: Gizli anahtar
            
        Returns:
            Hex formatında HMAC değeri
        """
        return hmac.new(
            key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()