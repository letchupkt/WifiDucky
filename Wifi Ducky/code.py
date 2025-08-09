import socketpool
import wifi
import json
import time
import gc
from duck import exe
from adafruit_httpserver import Server, Request, JSONResponse, POST, Response






"""--------------------------------------------------------------------------------------"""
# Configuration
ssid = "WIFI DUCK"
password = "password"

# Status tracking
execution_count = 0
start_time = time.monotonic()

print("Creating access point", ssid)
wifi.radio.stop_station()
wifi.radio.start_ap(ssid, password)
print("Access point created!")
print(f"IP Address: {wifi.radio.ipv4_address_ap}")

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

"""--------------------------------------------------------------------------------------"""
@server.route("/")
def base(request: Request):
    try:
        with open("index.html", "r") as file:
            html_content = file.read()
        headers = {"Content-Type": "text/html"}
        return Response(request, html_content, headers=headers)
    except Exception as e:
        error_html = f"<h1>Error</h1><p>Cannot load index.html: {str(e)}</p>"
        return Response(request, error_html, headers={"Content-Type": "text/html"})

"""--------------------------------------------------------------------------------------"""
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
            print(f"Executing {len(payload_lines)} lines")
            
            exe(payload_lines)
            execution_count += 1
            
            return JSONResponse(request, {
                "status": "success",
                "message": f"Executed {len(payload_lines)} lines",
                "execution_id": execution_count
            })
            
        except Exception as e:
            print(f"API Error: {e}")
            return JSONResponse(request, {
                "status": "error", 
                "message": f"Execution failed: {str(e)}"
            })

"""--------------------------------------------------------------------------------------"""
@server.route("/status", append_slash=True)
def status(request: Request):
    """Get device status"""
    try:
        uptime = int(time.monotonic() - start_time)
        free_mem = gc.mem_free()
        
        status_data = {
            "status": "online",
            "device": "WiFi Ducky",
            "version": "1.0",
            "uptime": uptime,
            "executions": execution_count,
            "current_ssid": ssid,
            "wifi_status": "active",
            "ip_address": str(wifi.radio.ipv4_address_ap),
            "free_memory": free_mem,
            "last_execution": None
        }
        
        print(f"Status request: {status_data}")
        return JSONResponse(request, status_data)
        
    except Exception as e:
        print(f"Status Error: {e}")
        return JSONResponse(request, {
            "status": "error",
            "message": f"Status error: {str(e)}"
        })

"""--------------------------------------------------------------------------------------"""
@server.route("/config", append_slash=True)
def get_config(request: Request):
    """Get current configuration"""
    try:
        config_data = {
            "status": "success",
            "config": {
                "ssid": ssid,
                "password": "*" * len(password)
            }
        }
        print(f"Config request: {config_data}")
        return JSONResponse(request, config_data)
    except Exception as e:
        print(f"Config Error: {e}")
        return JSONResponse(request, {
            "status": "error",
            "message": f"Config error: {str(e)}"
        })

"""--------------------------------------------------------------------------------------"""
@server.route("/config", POST, append_slash=True)
def update_config(request: Request):
    """Update configuration"""
    global ssid, password
    try:
        req = request.json()
        config = req.get("config", {})
        
        new_ssid = config.get("ssid", "").strip()
        new_password = config.get("password", "").strip()
        
        # Validation
        if not new_ssid:
            return JSONResponse(request, {
                "status": "error",
                "message": "SSID cannot be empty"
            })
        
        if len(new_ssid) > 32:
            return JSONResponse(request, {
                "status": "error",
                "message": "SSID cannot be longer than 32 characters"
            })
        
        if not new_password:
            return JSONResponse(request, {
                "status": "error",
                "message": "Password cannot be empty"
            })
        
        if len(new_password) < 8 or len(new_password) > 63:
            return JSONResponse(request, {
                "status": "error",
                "message": "Password must be 8-63 characters long"
            })
        
        # Update global variables
        old_ssid = ssid
        ssid = new_ssid
        password = new_password
        
        wifi_restart_required = (old_ssid != new_ssid)
        
        return JSONResponse(request, {
            "status": "success",
            "message": "Settings saved successfully",
            "wifi_restart_required": wifi_restart_required
        })
        
    except Exception as e:
        print(f"Config Update Error: {e}")
        return JSONResponse(request, {
            "status": "error",
            "message": f"Failed to update config: {str(e)}"
        })

"""--------------------------------------------------------------------------------------"""
@server.route("/restart", POST, append_slash=True)
def restart_wifi(request: Request):
    """Restart WiFi with new settings"""
    try:
        print(f"Restarting WiFi with SSID: {ssid}")
        
        # Stop current AP
        wifi.radio.stop_ap()
        time.sleep(1)
        
        # Start new AP with updated settings
        wifi.radio.start_ap(ssid, password)
        
        return JSONResponse(request, {
            "status": "success",
            "message": "WiFi restarted successfully",
            "new_ssid": ssid
        })
        
    except Exception as e:
        print(f"WiFi Restart Error: {e}")
        return JSONResponse(request, {
            "status": "error",
            "message": f"WiFi restart failed: {str(e)}"
        })

"""--------------------------------------------------------------------------------------"""
@server.route("/factory-reset", POST, append_slash=True)
def factory_reset(request: Request):
    """Factory reset to default settings"""
    global ssid, password, execution_count
    try:
        # Reset to default values
        ssid = "WIFI DUCK"
        password = "password"
        execution_count = 0
        
        print("Factory reset completed")
        
        return JSONResponse(request, {
            "status": "success",
            "message": "Factory reset completed successfully",
            "config": {
                "ssid": ssid,
                "password": "*" * len(password)
            }
        })
        
    except Exception as e:
        print(f"Factory Reset Error: {e}")
        return JSONResponse(request, {
            "status": "error",
            "message": f"Factory reset failed: {str(e)}"
        })

"""--------------------------------------------------------------------------------------"""
@server.route("/test", append_slash=True)
def test_endpoint(request: Request):
    """Test endpoint to verify server is working"""
    return JSONResponse(request, {
        "message": "Test endpoint working!",
        "time": time.monotonic(),
        "memory": gc.mem_free()
    })

"""--------------------------------------------------------------------------------------"""
print("Starting server...")
print(f"Connect to: {ssid}")
print(f"Password: {password}")
print(f"Navigate to: http://{wifi.radio.ipv4_address_ap}")
print("Test endpoint: http://{}/test".format(wifi.radio.ipv4_address_ap))

try:
    server.serve_forever(str(wifi.radio.ipv4_address_ap), 80)
except KeyboardInterrupt:
    print("\nServer stopped")
except Exception as e:
    print(f"Server error: {e}")