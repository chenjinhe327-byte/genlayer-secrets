cat > genlayer_secrets/secrets.py << 'EOF'
from genlayer import *
from typing import Dict, Optional
from datetime import datetime

class SecureSecretManager(gl.Contract):
    """GenLayer 安全凭证管理器 - 核心类"""
    
    def __init__(self):
        self.secrets: Dict[str, str] = {}      # secret_name -> encrypted_blob
        self.metadata: Dict[str, dict] = {}    # secret_name -> metadata
        self.audit_log: list = []

    @gl.public.write
    def store_secret(self, name: str, encrypted_blob: str, expires_at: int = 0):
        """存储加密后的 Secret（客户端需提前加密）"""
        caller = gl.get_caller()
        self.secrets[name] = encrypted_blob
        self.metadata[name] = {
            "owner": caller,
            "expires_at": expires_at,
            "version": 1,
            "last_used": 0
        }
        self._log_audit(caller, name, "store")
        print(f"✅ Secret '{name}' 已安全存储")

    def _log_audit(self, caller: str, name: str, action: str):
        self.audit_log.append({
            "ts": int(datetime.now().timestamp()),
            "caller": caller,
            "secret": name,
            "action": action
        })

    def _inject_secret(self, name: str) -> Optional[str]:
        """仅在 validator 执行时安全注入（关键安全点）"""
        if name not in self.secrets:
            return None
        
        meta = self.metadata.get(name, {})
        if meta.get("expires_at", 0) > 0 and meta["expires_at"] < int(datetime.now().timestamp()):
            return None
            
        secret = self.secrets[name]
        self.metadata[name]["last_used"] = int(datetime.now().timestamp())
        self._log_audit(gl.get_caller(), name, "use")
        return secret   # 真实环境中在这里进行解密

    def make_secure_web_get(self, url: str, secret_name: str = "api_key", **kwargs):
        """使用 Secret 安全发起网页请求"""
        def nondet_block():
            secret = self._inject_secret(secret_name)
            if not secret:
                return {"error": "Secret invalid or expired"}
            
            headers = kwargs.get("headers", {})
            headers["Authorization"] = f"Bearer {secret}"
            
            return gl.nondet.web.get(url, headers=headers)
        
        return gl.eq_principle.execute(nondet_block)
EOF

echo "✅ secrets.py 已写入"