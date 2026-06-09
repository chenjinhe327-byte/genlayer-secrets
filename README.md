# genlayer-secrets

**🔐 Secure Secrets & Credential Manager for GenLayer Intelligent Contracts**

Never hardcode API keys again. Store encrypted secrets on-chain and inject them safely **only during validator execution**.

## ✨ Features
- Encrypted secrets stored on-chain
- Secrets never exposed to callers or frontend
- Support for expiration time + audit log
- CLI one-click template generation
- Easy to integrate with any Intelligent Contract
- Works with `gl.nondet.web.get()`

## Quick Start

```bash
pip install -e .

# Generate secure template
genlayer-secrets