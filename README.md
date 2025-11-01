# WiFind 📡

**Wi-Fi Profile Reporter** is a secure Windows tool to view saved Wi-Fi profiles, encryption types, and connection info. Optionally reveal passwords with `--reveal` and send full reports to Telegram. Simple, Unicode/Persian-friendly, perfect for network pros and security enthusiasts.

---

![Python Version](https://img.shields.io/badge/python-3.11-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows-blue)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram&logoColor=white)
![Persian Support](https://img.shields.io/badge/%D9%81%D8%A7%D8%B1%D8%B3%DB%8C-%D9%BE%D8%B4%D8%AA%DB%8C%D8%A8%D8%A7%D9%86%DB%8C-green)

---

## 🚀 Features

- View all saved Wi-Fi profiles on Windows  
- Display encryption type, connection mode, and network type  
- Optional password reveal with `--reveal`  
- Gather active network interface info and signal strength  
- Send full **HTML reports** to Telegram with `--send-telegram`  
- Full **Unicode & Persian support**  
- Ideal for network professionals, security enthusiasts, and automation  

---

## ⚡ Requirements

- **OS:** Windows  
- **Python:** 3.8+  
- **Library:** `requests` (for Telegram)

```bash
pip install -r requirements.txt

🛠️ Installation
bashgit clone https://github.com/IM-KOBRA/WiFind.git
cd WiFind
pip install -r requirements.txt
Optional: Set up Telegram (for --send-telegram)
powershell# PowerShell
setx WIFI_BOT_TOKEN "YOUR_BOT_TOKEN"
setx WIFI_CHAT_ID "YOUR_CHAT_ID"

Or add them directly in code or .env file.


💻 Usage

























CommandDescriptionpython wifi_reporter.pyView local reportpython wifi_reporter.py --revealShow passwordspython wifi_reporter.py --send-telegramSend report to Telegrampython wifi_reporter.py --reveal --send-telegramShow + send with passwords

🎨 Sample Output
textSSID               : HomeWiFi
Authentication     : WPA2-Personal
Encryption         : CCMP
Connection Mode    : auto
Network Type       : Infrastructure
Signal             : 87%
Password           : MySecretPass123   (only with --reveal)

Telegram reports are sent in rich HTML format.


🛡️ Security & Privacy

Passwords are only shown with --reveal
Runs 100% locally — no data sent without your command
Telegram sending is optional and fully configurable


📄 License
textMIT License © 2025 IM-KOBRA

🏷️ Tags
Wi-Fi Network Security Windows Python Telegram Bot Automation Persian Unicode WiFi Password Netsh Cybersecurity

🤝 Contributing
Found a bug? Have an idea? Submit a Pull Request!
See CONTRIBUTING.md for guidelines.

⭐ Star This Project!
If you find WiFind useful, give it a star ⭐ to help others discover it!


  Made with ❤️ by IM-KOBRA

```
