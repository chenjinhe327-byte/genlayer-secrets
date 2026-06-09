from genlayer import *
from typing import Dict, Optional
from datetime import datetime


class SecureSecretManager(gl.Contract):
    """
    Secure Secret Manager for GenLayer Intelligent Contracts
    - Secrets are stored encrypted on-chain
    - Only injected safely inside validator nondet execution
    """

    def __init__(self):
        self.secrets: Dict[str, str] = {}        # name -> encrypted_blob
        self.metadata: Dict[str, dict] = {}      # name -> metadata
        self.audit_log: list = []

    @gl.public.write
    def store_secret(self, name: str, encrypted_blob: str, expires_at: int = 0):
        """Store encrypted secret (client must encrypt before calling)"""
        caller = gl.get_caller()
        
        self.secrets[name] = encrypted_blob
        self.metadata[name] = {
            "owner": caller,
            "expires_at": expires_at,
            "version": 1,
            "last_used": 0,
            "stored_at": int(datetime.now().timestamp())
        }
        self._log_audit(caller, name, "store")
        print(f"✅ Secret '{name}' stored securely.")

    def _log_audit(self, caller: str, name: str, action: str):
        self.audit_log.append({
            "ts": int(datetime.now().timestamp()),
            "caller": caller,
            "secret": name,
            "action": action
        })

    def _inject_secret(self, name: str) -> Optional[str]:
        """Internal method - only safe to call inside nondet block"""
        if name not in self.secrets:
            return None

        meta = self.metadata.get(name, {})
        if meta.get("expires_at", 0) > 0 and meta["expires_at"] < int(datetime.now().timestamp()):
            return None

        # In real validator environment, decryption happens here
        secret = self.secrets[name]
        self.metadata[name]["last_used"] = int(datetime.now().timestamp())
        self._log_audit(gl.get_caller(), name, "use")
        return secret

    @gl.public.read
    def make_secure_web_get(self, url: str, secret_name: str = "api_key", **kwargs):
        """Safe web request with injected secret"""
        def nondet_block():
            secret = self._inject_secret(secret_name)
            if not secret:
                return {"error": "Secret invalid or expired"}

            headers = kwargs.get("headers", {})
            headers["Authorization"] = f"Bearer {secret}"   # 根据实际 API 调整

            return gl.nondet.web.get(url, headers=headers)

        return gl.eq_principle.execute(nondet_block)