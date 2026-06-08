from genlayer import *
from genlayer_secrets.secrets import SecureSecretManager

class WeatherSecureContract(gl.Contract):
    """使用 SecureSecretManager 的天气数据示例"""
    
    def __init__(self):
        self.secret_manager = SecureSecretManager()
        self.last_weather = ""

    @gl.public.write
    def store_api_key(self, encrypted_key: str):
        """开发者调用此方法存入加密后的 OpenWeatherMap API Key"""
        self.secret_manager.store_secret("weather_api", encrypted_key, expires_at=0)

    @gl.public.read
    def get_current_weather(self, city: str = "Hong Kong"):
        """安全调用天气 API"""
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=PLACEHOLDER&units=metric"
        
        result = self.secret_manager.make_secure_web_get(
            url=url,
            secret_name="weather_api"
        )
        
        self.last_weather = str(result)
        return result
