from genlayer import *
from genlayer_secrets.secrets import SecureSecretManager
from typing import Dict


class WeatherSecureContract(gl.Contract):
    """
    Secure Weather Contract using genlayer-secrets
    - Demonstrates safe external API call with encrypted credential
    """

    def __init__(self):
        self.secret_manager = SecureSecretManager()
        self.last_result: Dict = {}

    @gl.public.write
    def store_api_key(self, encrypted_key: str, expires_at: int = 0):
        """Store encrypted API key (never store plaintext!)"""
        self.secret_manager.store_secret(
            name="openweathermap_key",
            encrypted_blob=encrypted_key,
            expires_at=expires_at
        )

    @gl.public.read
    def get_current_weather(self, city: str = "Hong Kong") -> Dict:
        """Safe weather query using injected secret"""
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric"

        def nondet_block():
            # Safe secret injection only happens inside validator
            return self.secret_manager.make_secure_web_get(
                url=url,
                secret_name="openweathermap_key"
            )

        result = gl.eq_principle.execute(nondet_block)
        self.last_result = result
        return result


# For GenLayer Studio / CLI deployment
contract = WeatherSecureContract()