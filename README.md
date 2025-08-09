# WiFi Ducky 🚀

![Raspberry Pi Pico W](https://img.thingsboard.io/devices-library/raspberry-pi-pico-w.jpg)
*Empowering hackers with wireless ducky magic – quack your way into systems!*

## **Project Overview** 🦆
WiFi Ducky is a **cutting-edge wireless keystroke injection tool** that brings the power of a **USB Rubber Ducky** to the airwaves using the affordable **Raspberry Pi Pico W**. Execute **Ducky Script payloads** remotely over WiFi, perfect for **red teaming, penetration testing, automation scripts, and ethical hacking adventures**. Turn your Pico W into a stealthy, wireless attack vector – no cables, no limits!

Built with **CircuitPython** for simplicity and speed, this project lets you inject keystrokes from afar, mimicking keyboard input on the target machine. Whether you're testing security, automating tasks, or just having fun, WiFi Ducky is your go-to gadget.

**Why WiFi Ducky?** Because who wouldn't want a duck that flies wirelessly? 🕊️

---
## **Features** 🔥
✅ **Wireless Freedom** – Inject keystrokes remotely via WiFi, no physical connection needed after setup.

✅ **Full Ducky Script Compatibility** – Supports all standard Rubber Ducky commands like `STRING`, `DELAY`, `GUI`, and more.

✅ **Intuitive Web Dashboard** – Hacker-themed interface with real-time script editing, templates, and execution logs.

✅ **Script Upload & Templates** – Load payloads from files or use built-in templates for quick attacks.

✅ **Device Status Monitoring** – Track uptime, executions, memory, and WiFi details from the UI.

✅ **Configurable WiFi AP** – Custom SSID/password, restart, and factory reset options.

✅ **Secure & Portable** – Low-cost (~$6 for Pico W), compact, and easy to deploy.

✅ **Advanced Security** – Optional filesystem locking and encrypted interface for production use.

✅ **Community-Driven** – Open-source, with room for contributions and custom mods.

---
## **Demo Video** 🎥
Watch WiFi Ducky in action:  
[![WiFi Ducky Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)  


---
## **Getting Started** 🛠️
### **Prerequisites**
- **Hardware**: Raspberry Pi Pico W (with WiFi capabilities).
- **Cable**: Micro-USB for initial setup and flashing.
- **Software**: Basic familiarity with Ducky Script, CircuitPython, and a web browser.
- **Optional**: Soldering tools for custom pins or enclosures.

### **Installation**
#### **Step 1: Flash CircuitPython**
1. Download the latest **CircuitPython** (v8.0.0) from [Adafruit's site](https://circuitpython.org/board/raspberry_pi_pico_w/).
2. Hold the **BOOTSEL** button on your Pico W while plugging it into your PC via USB.
3. The Pico will mount as a drive called **RPI-RP2**.
4. Drag the downloaded **.uf2** file onto the RPI-RP2 drive. The Pico will reboot and appear as **CIRCUITPY**.

#### **Step 2: Install WiFi Ducky Files**
1. Clone this repository:
   ```
   git clone https://github.com/letchupkt/wifi-ducky.git
   ```
   Or download the ZIP from the [releases page](https://github.com/letchupkt/wifi-ducky/releases).
2. Navigate to the **Wifi Ducky** folder in the repo.
3. Copy all files from the **Wifi Ducky** folder to the root of your **CIRCUITPY** drive.
4. Safely eject the Pico – it's ready to quack!

#### **Step 3: Library Dependencies**
- Ensure CircuitPython libraries like `adafruit_httpserver` and `socketpool` are in the `/lib` folder on CIRCUITPY. Download from [Adafruit's library bundle](https://circuitpython.org/libraries) if missing.

---
## **How to Use** ⚡
1️⃣ **Hardware Setup**: Plug the Pico W into the target machine's USB port (it acts as a HID keyboard).

2️⃣ **Connect to WiFi**: Scan for networks – join **WiFi Duck** (default SSID) with password **password**.

3️⃣ **Access the Dashboard**: Open a browser and go to [http://192.168.4.1](http://192.168.4.1).

4️⃣ **Craft Your Payload**: Use the editor for custom Ducky Scripts, or upload a .txt file.

5️⃣ **Execute**: Hit **RUN** and watch the magic – keystrokes inject wirelessly!

6️⃣ **Customize Settings**: Update SSID/password, restart WiFi, or factory reset via the Settings tab.

![Web Interface Screenshot](https://github.com/user-attachments/assets/51c25369-f8c1-4a74-b633-7f8bf8a44b0e)

### **Advanced Tips**
- **Payload Templates**: Quick-start with built-in examples like "Hello World" or "Admin Shell".
- **Debug Mode**: Connect via serial REPL for logs (e.g., `screen /dev/ttyACM0 115200`).
- **Security Mode**: Enable filesystem encryption or USB drive disabling in `main.py` for stealth ops.
- **Custom Scripts**: Experiment with multi-stage payloads for complex attacks.

---
## **Common Rubber Ducky Commands** 📜
💾 **Basic Commands:**
- `DELAY 500` – Pause for 500ms (essential for timing-sensitive ops).
- `STRING Hello, World!` – Types the string as keyboard input.
- `ENTER` – Hits Enter key.
- `CTRL ALT DEL` – Opens security screen (Windows).

💡 **Pro Commands:**
- `GUI r` – Opens Run dialog (Windows).
- `ALT F4` – Closes active window.
- `REPEAT 5` – Repeats the previous command 5 times.
- `REM Comment` – Adds non-executing notes.

💡 **Example Script: Rickroll Prank**
```ducky
DELAY 1000
GUI r
DELAY 500
STRING https://www.youtube.com/watch?v=dQw4w9WgXcQ
ENTER
```

💡 **Example Script: System Info Dump**
```ducky
GUI r
DELAY 500
STRING cmd
ENTER
DELAY 1000
STRING systeminfo > C:\systeminfo.txt
ENTER
```

---
## **Troubleshooting** 🔧
- **No WiFi AP?** Check serial logs for errors in `main.py` – ensure Pico W firmware is up-to-date.
- **Interface Not Loading?** Verify `index.html` is copied correctly; try clearing browser cache.
- **Script Not Executing?** Ensure the Pico is recognized as a HID device on the target (test with simple `STRING` command).
- **USB Drive Visible?** Add `storage.disable_usb_drive()` in `boot.py` (see code for details).
- **Need Help?** Open an issue on GitHub or check the Discussions tab.

---
## **Contributing** 🤝
We love contributions! Fork the repo, make your changes, and submit a pull request.
- **Ideas**: Add new features like multi-payload queuing or BLE support.
- **Bugs**: Report issues with detailed logs.
- **Code Style**: Follow PEP8 for Python; keep markdown clean.

---
## **License** 📄
Licensed under the MIT License. See [LICENSE](LICENSE) for details.

---
## **Disclaimer** 🚨
⚠️ This tool is for **educational and ethical purposes only**. **Unauthorized use is illegal and unethical**. Always get **explicit permission** before running payloads on any system. The authors are not responsible for misuse. ⚠️

---
## **Socials** 🔗
&copy; 2025 LetchuPkt | 
[GitHub](https://github.com/letchupkt) | 
[LinkedIn](https://linkedin.com/in/lakshmikanthank) | 
[Instagram](https://instagram.com/letchu_pkt)  
*Star the repo if you quack it up! ⭐*
