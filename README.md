# ⚡ V2Ray Config Tester & Exporter

A Python script to **parse**, **ping**, **analyze**, and **export** V2Ray configurations (`vmess`, `vless`, `ss`, `trojan`) to a base64-encoded subscription file for clients like **V2RayNG** and **NapsternetV**.

---

## ✨ Features

- ✅ Parse `vmess`, `vless`, `trojan`, and `shadowsocks` configs  
- 📶 Check server availability using `ping`  
- 🔐 Detect secure configs (TLS, Reality, or modern ciphers)  
- 📝 Export useful files:
  - `valid_configs.txt` — all reachable configs
  - `secure_configs.txt` — only secure configs
  - `sub_file.txt` — base64-encoded subscription for V2RayNG / NPV Tunnel

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

| File Name            | Description                                           |
|----------------------|-------------------------------------------------------|
| `valid_configs.txt`  | All configs that responded to ping                    |
| `secure_configs.txt` | Only configs with TLS/Reality or secure cipher       |
| `sub_file.txt`       | Base64 version ready for import   |

---

## 🛡️ What is a "Secure" Config?

A config is marked as **secure** if:

- `vless`, `vmess`, or `trojan` includes `tls` or `reality` in the parameters.
- `shadowsocks` uses secure ciphers such as:
  - `aes-256-gcm`
  - `chacha20-ietf-poly1305`

---

## 🧪 Sample Output

```
🔒 VMESS | my-server | 1.2.3.4 | 83 ms
⚠️  SS    | shadowsocks | 8.8.8.8 | 210 ms
❌ TROJAN | test         | 5.5.5.5 | No response

✅ Valid configs (2):
🔒 VMESS | my-server | 1.2.3.4 | 83 ms
⚠️  SS    | shadowsocks | 8.8.8.8 | 210 ms
```

---

## ⚠️ Disclaimer

This tool is for **educational and diagnostic purposes only**.  
The author is **not responsible** for how this script is used.

> 📌 **Warning for restricted regions (e.g. Iran):**
> This script does not give you access to VPN in any way and is merely a security testing tool.
> Using, sharing, or distributing VPN tools may be subject to **legal risks** under local laws. Use this script **at your own risk** and responsibility.

---

## 📄 License

[MIT License](LICENSE) © 2025 [Arash Jahromi]
