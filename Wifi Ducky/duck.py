import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
import time
import digitalio
from board import *

def exe(Payload_Script):
    """Execute a Ducky Script payload"""
    
    duckyCommands = {
        'WINDOWS': Keycode.WINDOWS, 'GUI': Keycode.GUI,
        'APP': Keycode.APPLICATION, 'MENU': Keycode.APPLICATION, 'SHIFT': Keycode.SHIFT,
        'ALT': Keycode.ALT, 'CONTROL': Keycode.CONTROL, 'CTRL': Keycode.CONTROL,
        'DOWNARROW': Keycode.DOWN_ARROW, 'DOWN': Keycode.DOWN_ARROW, 'LEFTARROW': Keycode.LEFT_ARROW,
        'LEFT': Keycode.LEFT_ARROW, 'RIGHTARROW': Keycode.RIGHT_ARROW, 'RIGHT': Keycode.RIGHT_ARROW,
        'UPARROW': Keycode.UP_ARROW, 'UP': Keycode.UP_ARROW, 'BREAK': Keycode.PAUSE,
        'PAUSE': Keycode.PAUSE, 'CAPSLOCK': Keycode.CAPS_LOCK, 'DELETE': Keycode.DELETE,
        'END': Keycode.END, 'ESC': Keycode.ESCAPE, 'ESCAPE': Keycode.ESCAPE, 'HOME': Keycode.HOME,
        'INSERT': Keycode.INSERT, 'NUMLOCK': Keycode.KEYPAD_NUMLOCK, 'PAGEUP': Keycode.PAGE_UP,
        'PAGEDOWN': Keycode.PAGE_DOWN, 'PRINTSCREEN': Keycode.PRINT_SCREEN, 'ENTER': Keycode.ENTER,
        'SCROLLLOCK': Keycode.SCROLL_LOCK, 'SPACE': Keycode.SPACE, 'TAB': Keycode.TAB,
        'BACKSPACE': Keycode.BACKSPACE,
        'A': Keycode.A, 'B': Keycode.B, 'C': Keycode.C, 'D': Keycode.D, 'E': Keycode.E,
        'F': Keycode.F, 'G': Keycode.G, 'H': Keycode.H, 'I': Keycode.I, 'J': Keycode.J,
        'K': Keycode.K, 'L': Keycode.L, 'M': Keycode.M, 'N': Keycode.N, 'O': Keycode.O,
        'P': Keycode.P, 'Q': Keycode.Q, 'R': Keycode.R, 'S': Keycode.S, 'T': Keycode.T,
        'U': Keycode.U, 'V': Keycode.V, 'W': Keycode.W, 'X': Keycode.X, 'Y': Keycode.Y,
        'Z': Keycode.Z, 'F1': Keycode.F1, 'F2': Keycode.F2, 'F3': Keycode.F3,
        'F4': Keycode.F4, 'F5': Keycode.F5, 'F6': Keycode.F6, 'F7': Keycode.F7,
        'F8': Keycode.F8, 'F9': Keycode.F9, 'F10': Keycode.F10, 'F11': Keycode.F11,
        'F12': Keycode.F12,
    }

    def convertLine(line):
        """Convert a line of commands to keycodes"""
        newline = []
        print(f"Converting line: {line}")
        
        # Handle empty lines
        if not line.strip():
            return newline
            
        # Split the line into individual keys/commands
        for key in filter(None, line.split(" ")):
            key = key.upper().strip()
            if not key:
                continue
                
            # Find the keycode for the command
            command_keycode = duckyCommands.get(key, None)
            if command_keycode is not None:
                newline.append(command_keycode)
            elif hasattr(Keycode, key):
                newline.append(getattr(Keycode, key))
            else:
                print(f"Unknown key: <{key}>")
        
        print(f"Converted to: {newline}")
        return newline

    def runScriptLine(line):
        """Execute a line of keycodes"""
        if not line:
            return
            
        try:
            # Press all keys simultaneously
            for k in line:
                kbd.press(k)
            
            # Small delay to ensure keys are registered
            time.sleep(0.01)
            
            # Release all keys
            kbd.release_all()
            
            # Small delay between key combinations
            time.sleep(0.05)
            
        except Exception as e:
            print(f"Error executing key combination: {e}")

    def sendString(text):
        """Type a string"""
        if not text:
            return
            
        try:
            print(f"Typing: {text}")
            layout.write(text)
        except Exception as e:
            print(f"Error typing string '{text}': {e}")

    def parseLine(line):
        """Parse and execute a single line of Ducky Script"""
        if not line or not line.strip():
            return
            
        line = line.strip()
        print(f"Parsing line: {line}")
        
        try:
            if line.startswith("REM"):
                # Comment - ignore
                print(f"Comment: {line}")
                pass
            elif line.startswith("DELAY"):
                # Delay command
                try:
                    delay_ms = int(line.split()[1]) if len(line.split()) > 1 else 500
                    delay_seconds = delay_ms / 1000.0
                    print(f"Delaying {delay_seconds} seconds")
                    time.sleep(delay_seconds)
                except (ValueError, IndexError) as e:
                    print(f"Invalid DELAY command: {line}, error: {e}")
            elif line.startswith("STRING"):
                # String typing
                text = line[7:] if len(line) > 7 else ""
                sendString(text)
            elif line.startswith("DEFAULT_DELAY") or line.startswith("DEFAULTDELAY"):
                # Set default delay
                try:
                    if line.startswith("DEFAULT_DELAY"):
                        delay_ms = int(line.split()[1]) if len(line.split()) > 1 else 0
                    else:  # DEFAULTDELAY
                        delay_ms = int(line.split()[1]) if len(line.split()) > 1 else 0
                    
                    global defaultDelay
                    defaultDelay = delay_ms
                    print(f"Default delay set to: {defaultDelay}ms")
                except (ValueError, IndexError) as e:
                    print(f"Invalid DEFAULT_DELAY command: {line}, error: {e}")
            else:
                # Key combination
                newScriptLine = convertLine(line)
                if newScriptLine:
                    runScriptLine(newScriptLine)
                    
        except Exception as e:
            print(f"Error parsing line '{line}': {e}")

    # Initialize keyboard and layout
    try:
        print("Initializing USB HID keyboard...")
        kbd = Keyboard(usb_hid.devices)
        layout = KeyboardLayoutUS(kbd)
        print("Keyboard initialized successfully")
    except Exception as e:
        print(f"Failed to initialize keyboard: {e}")
        return False

    # Sleep at start to allow device recognition
    print("Waiting for device recognition...")
    time.sleep(0.5)

    # Initialize variables
    defaultDelay = 0
    previousLine = ""
    
    try:
        print(f"Starting script execution with {len(Payload_Script)} lines")
        
        for line_num, line in enumerate(Payload_Script, 1):
            if not line:
                continue
                
            line = line.rstrip()
            print(f"Line {line_num}: {line}")
            
            try:
                if line.startswith("REPEAT"):
                    # Repeat previous command
                    try:
                        repeat_count = int(line.split()[1]) if len(line.split()) > 1 else 1
                        print(f"Repeating previous command {repeat_count} times")
                        
                        for i in range(repeat_count):
                            if previousLine:
                                parseLine(previousLine)
                                if defaultDelay > 0:
                                    time.sleep(defaultDelay / 1000.0)
                    except (ValueError, IndexError) as e:
                        print(f"Invalid REPEAT command: {line}, error: {e}")
                else:
                    # Normal command
                    parseLine(line)
                    previousLine = line
                
                # Apply default delay
                if defaultDelay > 0:
                    time.sleep(defaultDelay / 1000.0)
                    
            except Exception as e:
                print(f"Error processing line {line_num} '{line}': {e}")
                continue

        print("Script execution completed successfully")
        return True
        
    except Exception as e:
        print(f"Fatal error during script execution: {e}")
        return False