# ⚡ V2Ray Config Filter & Analyzer

A Python script to **analyze** and **filter** configuration strings used in some proxy formats (e.g. vmess, vless, ss, trojan) based on basic **ping reachability** and **parameter checks**.

> 🛑 **Important:** This tool does **not** provide, generate, promote, or facilitate VPN access or any circumvention services. It only analyzes text-based configuration strings already owned by the user.

---

## ✨ Features

- Parse `vmess`, `vless`, `trojan`, and `shadowsocks`-formatted strings
- Check basic server reachability using ICMP ping
- Detect basic encryption keywords (e.g. TLS)
- Export filtered lists to:
  - `valid_configs.txt` — configs that respond to ping
  - `secure_configs.txt` — configs with security flags (e.g. tls, secure ciphers)
  - `sub_file.txt` — base64-encoded version for personal use

---

## 🚀 Usage

### 1. Clone the repository

```bash
git clone https://github.com/Arash-GJ/v2ray-config-tester.git
cd v2ray-config-tester
```

### 2. Install dependencies

```bash
pip install ping3
```

### 3. Run the script

```bash
python check_configs.py
```

---

## 📂 Output Files

| File Name            | Description                                               |
|----------------------|-----------------------------------------------------------|
| `valid_configs.txt`  | Config strings that responded to ping                     |
| `secure_configs.txt` | Subset with TLS/secure ciphers for optional analysis      |
| `sub_file.txt`       | Base64-encoded version for importing into external tools  |

---

## 🧪 Sample Output

```
🔒 VMESS | my-server | 1.2.3.4 | 83 ms
⚠️  SS    | shadowsocks | 8.8.8.8 | 210 ms
❌ TROJAN | test         | 5.5.5.5 | No response
```

---

## 🔐 Security Note

This tool simply checks text-based input using regex and ping.  
It **does not establish any connections**, create proxy links, or bypass restrictions.

---

## ⚠️ Legal & Ethical Notice

This script is intended for:
- Educational purposes
- Local security testing
- Learning how proxy config formats are structured

> 📌 **This is NOT a VPN.**
> It does NOT provide or unlock VPN, tunnel, proxy, or bypass functionality.

Users are responsible for complying with **local laws** and **terms of service** of any third-party software they use.  
The author assumes no liability for any misuse.

---

## 📄 License

MIT License © 2025 [Arash Jahromi]
