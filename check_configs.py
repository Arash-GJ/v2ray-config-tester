#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ping3 import ping
import base64
import re
import json
import urllib.parse

# ------------------------------------------
# Read and decode subscription file
# Supports plain text or base64-encoded lines
# ------------------------------------------
def fetch_subscription_from_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = f.read()

        try:
            decoded_data = base64.b64decode(data.strip()).decode('utf-8')
        except Exception:
            print("⚠️ Input is not base64. Trying direct line parsing.")
            decoded_data = data

        return [line.strip() for line in decoded_data.splitlines() if line.strip().startswith(("vless://", "vmess://", "ss://", "trojan://"))]
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

# ------------------------------------------
# Parsers for different protocol types
# ------------------------------------------
def parse_vless(url):
    match = re.match(r"vless://([^@]+)@([^:]+):(\d+)\?(.*?)#(.*)", url)
    if match:
        uuid, host, port, params, remark = match.groups()
        secure = 'tls' in params.lower() or 'reality' in params.lower()
        return {"type": "vless", "host": host, "remark": urllib.parse.unquote(remark), "full": url, "secure": secure}
    return None

def parse_vmess(url):
    try:
        base64_payload = url[8:]
        padding = '=' * (-len(base64_payload) % 4)
        decoded = base64.b64decode(base64_payload + padding).decode('utf-8')
        cfg = json.loads(decoded)
        secure = cfg.get("tls", "").lower() == "tls" or cfg.get("security", "").lower() in ["tls", "reality"]
        return {"type": "vmess", "host": cfg.get("add"), "remark": cfg.get("ps", "no-remark"), "full": url, "secure": secure}
    except Exception:
        return None

def parse_ss(url):
    try:
        url = url[5:]
        if '@' not in url:
            decoded = base64.b64decode(url + '=' * (-len(url) % 4)).decode()
            url = decoded
        parts = url.split('@')
        if len(parts) != 2:
            return None
        cipher_info, host_port = parts
        cipher = cipher_info.split(':')[0].lower()
        host, port = host_port.split(':')
        secure = cipher in ['aes-256-gcm', 'chacha20-ietf-poly1305']
        return {"type": "ss", "host": host, "remark": "shadowsocks", "full": "ss://" + url, "secure": secure}
    except Exception:
        return None

def parse_trojan(url):
    match = re.match(r"trojan://[^@]+@([^:/?#]+):\d+", url)
    if match:
        host = match.group(1)
        remark = url.split('#')[-1] if '#' in url else 'trojan'
        secure = 'security=tls' in url.lower()
        return {"type": "trojan", "host": host, "remark": urllib.parse.unquote(remark), "full": url, "secure": secure}
    return None

# ------------------------------------------
# Ping test for host availability
# ------------------------------------------
def check_ping(host):
    try:
        latency = ping(host, timeout=2)
        return round(latency * 1000) if latency else None
    except:
        return None

# ------------------------------------------
# Main function
# ------------------------------------------
def main():
    filepath = input("Enter path to local subscription file: ").strip().strip('"')
    urls = fetch_subscription_from_file(filepath)
    print(f"Found {len(urls)} configs. Checking ping...\n")

    valid_configs = []

    # Parse and ping each config
    for url in urls:
        cfg = None
        if url.startswith("vless://"):
            cfg = parse_vless(url)
        elif url.startswith("vmess://"):
            cfg = parse_vmess(url)
        elif url.startswith("ss://"):
            cfg = parse_ss(url)
        elif url.startswith("trojan://"):
            cfg = parse_trojan(url)

        if cfg and cfg.get("host"):
            latency = check_ping(cfg["host"])
            if latency is not None:
                cfg["ping"] = latency
                secure_icon = "🔒" if cfg.get("secure") else "⚠️"
                print(f"{secure_icon} {cfg['type'].upper()} | {cfg['remark']} | {cfg['host']} | {latency} ms")
                valid_configs.append(cfg)
            else:
                print(f"❌ {cfg['type'].upper()} | {cfg['remark']} | {cfg['host']} | No response")
        else:
            print(f"⚠️ Cannot parse: {url[:50]}...")

    # Final summary
    print(f"\n✅ Valid configs ({len(valid_configs)}):")
    for cfg in valid_configs:
        secure_icon = "🔒" if cfg.get("secure") else "⚠️"
        print(f"{secure_icon} {cfg['type'].upper()} | {cfg['remark']} | {cfg['host']} | {cfg['ping']} ms")
        print(cfg["full"])
        print("-" * 40)

    # Save all valid configs
    with open("valid_configs.txt", "w", encoding="utf-8") as f_all:
        for cfg in valid_configs:
            f_all.write(cfg["full"] + "\n")

    # Save only secure configs
    secure_configs = [cfg for cfg in valid_configs if cfg.get("secure")]
    with open("secure_configs.txt", "w", encoding="utf-8") as f_secure:
        for cfg in secure_configs:
            f_secure.write(cfg["full"] + "\n")

    # Create base64-encoded subscription file (e.g. for V2RayNG or NapsternetV)
    if secure_configs:
        content = "\n".join(cfg["full"] for cfg in secure_configs)
        encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")
        with open("sub_file.txt", "w", encoding="utf-8") as f_sub:
            f_sub.write(encoded)
        print(f"🌐 Created base64 subscription file: 'sub_file.txt'")

    # Final results
    print(f"\n📝 Saved {len(valid_configs)} valid configs to 'valid_configs.txt'")
    print(f"🔐 Saved {len(secure_configs)} secure configs to 'secure_configs.txt'")

if __name__ == "__main__":
    main()
