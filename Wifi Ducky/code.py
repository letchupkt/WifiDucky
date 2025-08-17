import socketpool
import wifi
import json
import time
import gc
import usb_hid
from duck import exe
from adafruit_httpserver import Server, Request, JSONResponse, POST, Response

# Configuration - Client Mode Only
client_ssid = ""
client_password = ""

# Status tracking
execution_count = 0
start_time = time.monotonic()

def initialize_wifi():
    """Initialize WiFi in Client Mode"""
    try:
        # Stop any existing connections
        try:
            wifi.radio.stop_ap()
        except:
            pass
        
        # Start station mode
        try:
            wifi.radio.start_station()
        except:
            pass
        
        time.sleep(1)
        
        # Connect to client network
        print(f"Connecting to {client_ssid}...")
        wifi.radio.connect(client_ssid, client_password)
        
        # Wait for connection with better status checking
        max_wait = 15
        connected = False
        
        while max_wait > 0 and not connected:
            try:
                # Try multiple ways to check connection
                if hasattr(wifi.radio, 'connected'):
                    connected = wifi.radio.connected
                elif hasattr(wifi.radio, 'ap_active'):
                    connected = not wifi.radio.ap_active  # In client mode, ap should be inactive
                else:
                    # Try to get IP address as connection indicator
                    try:
                        ip = wifi.radio.ipv4_address
                        connected = ip is not None and str(ip) != "0.0.0.0"
                    except:
                        connected = False
                
                if connected:
                    print(f"Successfully connected to {client_ssid}")
                    break
                    
            except Exception as e:
                print(f"Connection check error: {e}")
                connected = False
            
            max_wait -= 1
            time.sleep(1)
            print(f"Waiting for connection... {max_wait} attempts left")
        
        if connected:
            try:
                client_ip = wifi.radio.ipv4_address
                if client_ip and str(client_ip) != "0.0.0.0":
                    print(f"Client IP: {client_ip}")
                    return str(client_ip)
                else:
                    print("No valid IP obtained")
                    return None
            except Exception as e:
                print(f"IP retrieval error: {e}")
                return None
        else:
            print("Failed to connect to client network")
            return None
            
    except Exception as e:
        print(f"Client mode error: {e}")
        return None

# Initialize WiFi
device_ip = initialize_wifi()

# Create HTTP server
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=False)

@server.route("/")
def base(request: Request):
    try:
        # Try to load index.html from current directory
        with open("index.html", "r") as file:
            html_content = file.read()
        headers = {"Content-Type": "text/html"}
        return Response(request, html_content, headers=headers)
    except Exception as e:
        # Fallback error page
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>WiFi Ducky v2.0</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .error {{ color: red; }}
                .info {{ color: blue; }}
            </style>
        </head>
        <body>
            <h1>WiFi Ducky v2.0</h1>
            <p class="error">Error: Cannot load index.html</p>
            <p class="info">Device IP: {device_ip}</p>
            <p class="info">SSID: {client_ssid}</p>
            <p class="info">Password: {client_password}</p>
            <p>Please check file structure and try again.</p>
        </body>
        </html>
        """
        return Response(request, error_html, headers={"Content-Type": "text/html"})

@server.route("/api", POST, append_slash=True)
def api(request: Request):
    global execution_count
    if request.method == POST:
        try:
            req = request.json()
            payload = req.get("content", "")
            
            if not payload:
                return JSONResponse(request, {"status": "error", "message": "No payload"})
            
            payload_lines = payload.splitlines()
            exe(payload_lines)
            execution_count += 1
            
            return JSONResponse(request, {
                "status": "success",
                "message": f"Executed {len(payload_lines)} lines",
                "execution_id": execution_count
            })
            
        except Exception as e:
            return JSONResponse(request, {
                "status": "error", 
                "message": f"Execution failed: {str(e)}"
            })

@server.route("/status", append_slash=True)
def status(request: Request):
    """Get device status"""
    try:
        uptime = int(time.monotonic() - start_time)
        free_mem = gc.mem_free()
        
        # Check WiFi status safely
        wifi_status = "unknown"
        try:
            if hasattr(wifi.radio, 'connected'):
                wifi_status = "connected" if wifi.radio.connected else "disconnected"
            elif hasattr(wifi.radio, 'ap_active'):
                wifi_status = "connected" if wifi.radio.ap_active else "disconnected"
            else:
                wifi_status = "active"
        except:
            wifi_status = "active"
        
        status_data = {
            "status": "online",
            "device": "WiFi Ducky",
            "version": "2.0",
            "uptime": uptime,
            "executions": execution_count,
            "current_ssid": client_ssid,
            "wifi_status": wifi_status,
            "ip_address": device_ip,
            "free_memory": free_mem,
            "last_execution": None
        }
        
        return JSONResponse(request, status_data)
        
    except Exception as e:
        return JSONResponse(request, {
            "status": "error",
            "message": f"Status error: {str(e)}"
        })

@server.route("/config", append_slash=True)
def get_config(request: Request):
    """Get current configuration"""
    try:
        config_data = {
            "status": "success",
            "config": {
                "client_ssid": client_ssid,
                "client_password": "*" * len(client_password) if client_password else "",
            }
        }
        return JSONResponse(request, config_data)
    except Exception as e:
        return JSONResponse(request, {
            "status": "error",
            "message": f"Config error: {str(e)}"
        })

@server.route("/config", POST, append_slash=True)
def update_config(request: Request):
    """Update configuration"""
    global client_ssid, client_password
    try:
        req = request.json()
        config = req.get("config", {})
        
        new_client_ssid = config.get("client_ssid", "").strip()
        new_client_password = config.get("client_password", "").strip()
        
        if not new_client_ssid:
            return JSONResponse(request, {
                "status": "error",
                "message": "Client SSID cannot be empty"
            })
        
        if not new_client_password:
            return JSONResponse(request, {
                "status": "error",
                "message": "Client password cannot be empty"
            })
        
        client_ssid = new_client_ssid
        client_password = new_client_password
        
        return JSONResponse(request, {
            "status": "success",
            "message": "Settings saved successfully",
            "wifi_restart_required": False
        })
        
    except Exception as e:
        return JSONResponse(request, {
            "status": "error",
            "message": f"Failed to update config: {str(e)}"
        })

@server.route("/restart", POST, append_slash=True)
def restart_wifi(request: Request):
    """Restart WiFi with new settings"""
    global device_ip
    try:
        print(f"Restarting WiFi in Client mode...")
        
        device_ip = initialize_wifi()
        
        if device_ip:
            return JSONResponse(request, {
                "status": "success",
                "message": f"WiFi restarted successfully",
                "new_ip": device_ip
            })
        else:
            return JSONResponse(request, {
                "status": "error",
                "message": "WiFi restart failed"
            })
        
    except Exception as e:
        print(f"WiFi restart error: {e}")
        return JSONResponse(request, {
            "status": "error",
            "message": f"WiFi restart failed: {str(e)}"
        })

@server.route("/factory-reset", POST, append_slash=True)
def factory_reset(request: Request):
    """Factory reset to default settings"""
    global client_ssid, client_password, execution_count
    try:
        # Reset to default values
        client_ssid = ""
        client_password = ""
        execution_count = 0
        
        return JSONResponse(request, {
            "status": "success",
            "message": "Factory reset completed successfully",
            "config": {
                "client_ssid": client_ssid,
                "client_password": "*" * len(client_password) if client_password else "",
            }
        })
        
    except Exception as e:
        return JSONResponse(request, {
            "status": "error",
            "message": f"Factory reset failed: {str(e)}"
        })

@server.route("/test", append_slash=True)
def test_endpoint(request: Request):
    """Test endpoint to verify server is working"""
    try:
        # Test WiFi radio attributes
        wifi_info = {}
        try:
            wifi_info["enabled"] = wifi.radio.enabled
            wifi_info["mac_address"] = str(wifi.radio.mac_address)
        except Exception as e:
            wifi_info["error"] = str(e)
        
        return JSONResponse(request, {
            "message": "WiFi Ducky v2.0 is running",
            "time": time.monotonic(),
            "memory": gc.mem_free(),
            "mode": "Client",
            "stealth": False, # Stealth mode removed
            "wifi_info": wifi_info,
            "device_ip": device_ip
        })
    except Exception as e:
        return JSONResponse(request, {
            "error": f"Test failed: {str(e)}",
            "time": time.monotonic()
        })

@server.route("/debug", append_slash=True)
def debug_endpoint(request: Request):
    """Debug endpoint to check system compatibility"""
    try:
        debug_info = {
            "circuitpython_version": "Unknown",
            "wifi_radio_attributes": [],
            "wifi_radio_methods": [],
            "storage_attributes": [],
            "storage_methods": []
        }
        
        # Check CircuitPython version
        try:
            import sys
            debug_info["circuitpython_version"] = sys.version
        except:
            pass
        
        # Check WiFi radio attributes
        try:
            for attr in dir(wifi.radio):
                if not attr.startswith('_'):
                    debug_info["wifi_radio_attributes"].append(attr)
        except Exception as e:
            debug_info["wifi_radio_error"] = str(e)
        
        # Check storage attributes
        try:
            for attr in dir(storage):
                if not attr.startswith('_'):
                    debug_info["storage_attributes"].append(attr)
        except Exception as e:
            debug_info["storage_error"] = str(e)
        
        return JSONResponse(request, debug_info)
        
    except Exception as e:
        return JSONResponse(request, {
            "error": f"Debug failed: {str(e)}"
        })

# Start HTTP server
print(f"WiFi Ducky v2.0 starting...")
print(f"Client SSID: {client_ssid}")
print(f"Client Password: {client_password}")
print(f"IP Address: {device_ip}")
print(f"Mode: Client")
print(f"Stealth: Disabled")

try:
    server.serve_forever(device_ip, 80)
except KeyboardInterrupt:
    pass
except Exception as e:
    # Restart on error
    import supervisor
    supervisor.reload()