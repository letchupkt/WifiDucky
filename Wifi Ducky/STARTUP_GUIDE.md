# WiFi Ducky v2.0 Startup Guide

## Quick Start

### 1. **Power On Device**
- Connect Pico W via USB or power supply
- Wait for device to boot up

### 2. **Connect to WiFi**
- Look for "WIFI DUCK" network in WiFi settings
- Connect with password: `password`

### 3. **Access Web Interface**
- Open any web browser
- Navigate to: `http://192.168.4.1` (default IP)
- Or check serial console for actual IP address

### 4. **Start Using**
- **Payload Editor**: Write and execute Ducky Scripts
- **Settings**: Configure WiFi and modes
- **Reference**: View available commands

## Features

### **Rubber Ducky Mode**
- Execute Ducky Scripts via web interface
- Support for all standard commands
- Real-time execution feedback

### **Client Mode**
- Connect to existing WiFi networks
- Access from same network
- Useful for remote operations

### **Stealth Mode**
- Hide device storage from computers
- Device appears as HID keyboard only
- All functions remain operational

## Troubleshooting

### **WiFi Not Working**
1. Check CircuitPython 8.0+ is installed
2. Verify all libraries are in `lib/` folder
3. Ensure Pico W (not regular Pico) is used
4. Check USB cable and power supply

### **Web Interface Not Loading**
1. Verify device IP address
2. Check if connected to correct network
3. Try different browser
4. Check firewall settings

### **Scripts Not Executing**
1. Ensure USB connection to target computer
2. Check script syntax
3. Verify target recognizes HID device
4. Check execution status in web interface

## File Structure

```
Wifi Ducky/
├── code.py              # Main application
├── duck.py              # Script execution engine
├── index.html           # Web interface
├── config.json          # Configuration
├── lib/                 # Required libraries
│   ├── adafruit_hid/
│   └── adafruit_httpserver/
└── README.md            # Full documentation
```

## Access Methods

- **Primary**: `http://[device-ip]`
- **Default**: `http://192.168.4.1`
- **Network**: Same network as device

---

**WiFi Ducky v2.0** - Ready to use out of the box!
