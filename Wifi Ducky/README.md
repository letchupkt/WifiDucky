# WiFi Ducky v2.0

A powerful WiFi-enabled Rubber Ducky device built with Raspberry Pi Pico W, featuring multiple operation modes and stealth capabilities.

## 🚀 Features

### Core Functionality
- **Rubber Ducky Mode**: Execute Ducky Script payloads via web interface
- **BadUSB Mode**: Auto-execute scripts when device connects to computer
- **Web Interface**: Modern, responsive web UI accessible via WiFi

### Operation Modes

#### 1. Access Point Mode (Default)
- Creates a WiFi hotspot named "WIFI DUCK"
- Devices connect directly to the Pico W
- Access web interface at the device's IP address

#### 2. Client Mode
- Connects to existing WiFi networks
- Useful for remote access and stealth operations
- Web interface accessible from the same network

### Stealth Features
- **Storage Hiding**: Toggle to hide device storage from connected computers
- **USB Drive Concealment**: Device appears as HID keyboard only
- **Silent Operation**: All functions work without visible storage

### Network Access
- **Direct IP Access**: Connect via device IP address
- **Secure Web Interface**: Password-protected access point

## 🔧 Hardware Requirements

- Raspberry Pi Pico W
- Micro USB cable
- MicroSD card (optional, for storage)

## 📋 Software Requirements

### Required Libraries
```
adafruit_hid
adafruit_httpserver
```

### CircuitPython Version
- CircuitPython 8.0 or higher recommended

## 🚀 Quick Start

1. **Flash CircuitPython** to your Pico W
2. **Copy all files** to the device
3. **Connect via USB** or power via USB-C
4. **Connect to WiFi**:
   - **AP Mode**: Connect to "WIFI DUCK" network (password: "password")
   - **Client Mode**: Device connects to specified network
5. **Access Web Interface**:
   - Direct IP: `http://[device-ip]`

## 📱 Web Interface

### Payload Editor Tab
- Write and edit Ducky Scripts
- Load scripts from files
- Execute payloads immediately
- Template library for common tasks

### Settings Tab
- Switch between AP and Client modes
- Configure WiFi credentials
- Toggle stealth mode
- Device management (restart, factory reset)

### Reference Tab
- Complete Ducky Script command reference
- New features documentation
- Usage examples

## 🎯 Ducky Script Examples

### Basic Commands
```ducky
REM Basic Windows command prompt
GUI r
STRING cmd
ENTER
STRING ipconfig
ENTER
```

### Admin Access
```ducky
REM Open PowerShell as Administrator
GUI r
STRING powershell
ENTER
STRING Start-Process cmd -Verb runAs
ENTER
```

### System Control
```ducky
REM Lock workstation
GUI l

REM Show desktop
GUI d

REM Open Task Manager
CTRL SHIFT ESC
```

## ⚙️ Configuration

### Mode Switching
1. Go to **Settings** tab
2. Select desired mode (AP or Client)
3. Enter network credentials
4. Click **Save Settings**
5. Click **Restart WiFi** to apply changes

### Stealth Mode
1. Go to **Settings** tab
2. Toggle **Stealth Mode** switch
3. Storage will be hidden from connected computers
4. All functions remain operational

### BadUSB Mode
1. Go to **Payload Editor** tab
2. Write your script
3. Toggle **BadUSB Mode**
4. Script auto-executes when device connects

## 🔒 Security Features

- **Password Protection**: Default AP password can be changed
- **Stealth Operation**: Hide device identity
- **Secure Web Interface**: HTTPS-ready implementation
- **Access Control**: Configurable network access

## 🌐 Network Modes

### Access Point Mode
- **Use Case**: Direct device access, field operations
- **Pros**: No external network required, immediate access
- **Cons**: Limited range, manual connection required

### Client Mode
- **Use Case**: Remote access, network integration
- **Pros**: Extended range, network integration
- **Cons**: Requires existing network, network dependency

## 🛠️ Troubleshooting

### Common Issues

#### Device Not Accessible
1. Check WiFi connection
2. Verify device IP address
3. Ensure firewall allows connections
4. Try direct IP access instead of DNS

#### Scripts Not Executing
1. Verify USB connection
2. Check script syntax
3. Ensure target device recognizes HID device
4. Check execution status in web interface

#### WiFi Connection Issues
1. Verify credentials
2. Check network availability
3. Restart WiFi from settings
4. Perform factory reset if needed

### Factory Reset
1. Go to **Settings** tab
2. Click **Factory Reset**
3. Confirm action
4. Device restarts with default settings

## 🔄 Updates

### Version 2.0 Changes
- Added Client Mode for network integration
- Implemented Stealth Mode for storage hiding
- Enhanced mode management system
- Simplified network access via direct IP
- Improved web interface and user experience
- Better error handling and status reporting

## 📚 Advanced Usage

### Custom Scripts
- Support for all standard Ducky Script commands
- Custom delay timing
- Repeat functionality
- Comment support

### Network Integration
- Integration with existing network infrastructure
- Remote access capabilities
- Network monitoring and management

### Stealth Operations
- Concealed device operation
- Hidden storage access
- Silent payload execution

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📄 License

This project is open source. Please respect responsible disclosure practices.

## ⚠️ Disclaimer

This tool is for educational and authorized testing purposes only. Users are responsible for ensuring compliance with applicable laws and regulations.

## 📞 Support

For support and questions:
- GitHub Issues: [Project Repository]
- Documentation: See inline code comments
- Community: Check project discussions

---

**WiFi Ducky v2.0** - Power meets stealth in the palm of your hand.
