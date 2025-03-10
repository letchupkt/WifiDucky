# ** WiFi Ducky **

![Raspberry Pi Pico W](https://cdn.mos.cms.futurecdn.net/Xmn9ztSwKavDfzgX6x3g4g.jpg)

## **Project Overview**
WiFi Ducky is a **wireless keystroke injection tool** that emulates a **USB Rubber Ducky** over WiFi using the **Raspberry Pi Pico W**. This allows for remote execution of **Ducky Script payloads**, making it a powerful tool for **penetration testing, cybersecurity research, and automation**.

---
## **Features**
✅ **Remote Keystroke Injection** – Send payloads wirelessly to a connected device.

✅ **Ducky Script Support** – Execute pre-written Rubber Ducky scripts.

✅ **Web-Based Interface** – Simple UI for scripting and execution.

✅ **File Upload Support** – Run scripts from text files.

✅ **Cost-Effective** – Uses a single **Raspberry Pi Pico W** (~$6).

✅ **Hacker-Themed UI** – A dark, hacker-style interface for an immersive experience.


---
## **Getting Started**
### **Prerequisites**
- Raspberry Pi Pico W
- Micro-USB Cable
- Basic Knowledge of Ducky Script & CircuitPython

### **Installation**
#### **Step 1: Install CircuitPython**
1. Download **CircuitPython v8.0.0** [here](https://adafruit-circuit-python.s3.amazonaws.com/bin/raspberry_pi_pico_w/fr/adafruit-circuitpython-raspberry_pi_pico_w-fr-8.0.0.uf2).
2. Plug in your **Pico W** while holding the **BOOTSEL** button.
3. The device will appear as a drive named **RPI-RP2**.
4. Copy the **.uf2** file onto the drive. The device will reboot as **CIRCUITPY**.

#### **Step 2: Install Pico WiFi Duck Files**
1. Download the latest **release zip** from [here](https://github.com/letchupkt/wifi-ducky).
2. Extract the files.
3. Copy all files into the **CIRCUITPY** drive.

![File Copy](https://gcdnb.pbrd.co/images/WuZOVmyUAWF4.jpg?o=1)

---
## **How to Use**
1️⃣ Connect the **Raspberry Pi Pico W** to the target system via USB.
2️⃣ Connect to the **WiFi network** created by the Pico (**SSID:** WiFi Duck | **Password:** password).
3️⃣ Open a web browser and navigate to [192.168.4.1](http://192.168.4.1).
4️⃣ Write or upload a **Ducky Script** in the editor.
5️⃣ Click **RUN** to execute the script.

![Web Interface](https://gcdnb.pbrd.co/images/Qrj5szwW56B3.jpg?o=1)

---
## **Common Rubber Ducky Commands**
💾 **Basic Commands:**
- `DELAY 500` – Waits 500ms before executing the next command.
- `STRING Hello, World!` – Types 'Hello, World!' into the active window.
- `ENTER` – Simulates pressing Enter.
- `CTRL ALT DEL` – Simulates pressing Ctrl+Alt+Delete.

💡 **Example Script: Open Instagram**
```ducky
DELAY 1000
GUI r
DELAY 500
STRING https://www.instagram.com
ENTER
```

---
## **Disclaimer** 🚨
⚠️ This tool is intended for **educational and ethical hacking purposes only**. **Unauthorized use is illegal**. Always obtain **explicit permission** before testing on any system. ⚠️

---
## **Socials** 🔗
&copy; <span id="currentYear"></span> LetchuPkt | 
[GitHub](https://github.com/letchupkt) | 
[LinkedIn](https://linkedin.com/in/lakshmikanthank) | 
[Instagram](https://instagram.com/letchu_pkt)
