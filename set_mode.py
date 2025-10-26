import hid
import time
import sys

# ViewSonic Elite XG270QC HID identifiers
VID = 0x0543
PID = 0xA002

# Mode payloads (167 bytes each)
MODES = {
    "static": [
        0x02, 0x01, 0x00, 0x53, 0xf7, 0x00, 0x0a, 0x00, 0x01, 0x00, 0x53, 0xf7, 0x00, 0x0a, 0x00, 0x01
    ] + [0x00] * 151,
    
    "rainbow": [
        0x02, 0x07, 0x00, 0x00, 0x00, 0x00, 0x0a, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00, 0x0a, 0x00, 0x01
    ] + [0x00] * 151,
    
    "breathing": [
        0x02, 0x02, 0x00, 0x53, 0xf7, 0x00, 0x0a, 0x00, 0x02, 0x00, 0x53, 0xf7, 0x00, 0x0a, 0x00, 0x01
    ] + [0x00] * 151,
    
    "stack": [
        0x02, 0x09, 0x00, 0x53, 0xf7, 0x00, 0x0a, 0x00, 0x09, 0x00, 0x53, 0xf7, 0x00, 0x0a, 0x00, 0x01
    ] + [0x00] * 151,
    
    "warp-speed": [
        0x02, 0x06, 0x00, 0x00, 0x00, 0x00, 0x0a, 0x00, 0x06, 0x00, 0x00, 0x00, 0x00, 0x0a, 0x00, 0x01
    ] + [0x00] * 151,
    
    "music": [
        0x02, 0x12, 0x00, 0x53, 0xf7, 0x00, 0x0a, 0x00, 0x13, 0x00, 0x53, 0xf7, 0x00, 0x0a, 0x00, 0x01
    ] + [0x00] * 151,
    
    "music-pulse": [
        0x02, 0x12, 0x00, 0x53, 0xf7, 0x00, 0x0a, 0x00, 0x14, 0x00, 0x53, 0xf7, 0x00, 0x0a, 0x00, 0x01
    ] + [0x00] * 151,
}

# Color presets (R, G, B)
COLORS = {
    "blue": (0x00, 0x53, 0xF7),
    "cyan": (0x01, 0x4F, 0xFE),
    "yellow": (0xFF, 0xF9, 0x4D),
    "magenta": (0xF7, 0x00, 0x93),
    "red": (0xFF, 0x00, 0x00),
    "green": (0x00, 0xFF, 0x00),
    "pure-blue": (0x00, 0x00, 0xFF),
    "white": (0xFF, 0xFF, 0xFF),
    "olive": (0x80, 0x80, 0x00),
    "teal": (0x00, 0x80, 0x80),
}


def set_mode(mode_name, color_base=None, color_rear=None):
    """
    Set the display mode.
    
    Args:
        mode_name (str): Mode to set. Available modes: static, rainbow, breathing, stack, warp-speed, music, music-pulse
        color_base (tuple or str): Optional color for base zone (R, G, B) or color name.
        color_rear (tuple or str): Optional color for rear zone (R, G, B) or color name. If not provided, uses color_base.
    
    Returns:
        bool: True if successful, False otherwise
    """
    if mode_name.lower() not in MODES:
        print(f"Error: Mode '{mode_name}' not found. Available modes: {', '.join(MODES.keys())}")
        return False
    
    payload = MODES[mode_name.lower()].copy()
    
    # If only one color is provided, use it for both zones
    if color_rear is None:
        color_rear = color_base
    
    # Handle color_base parameter
    if color_base is not None:
        if isinstance(color_base, str):
            if color_base.lower() not in COLORS:
                print(f"Error: Color '{color_base}' not found. Available colors: {', '.join(COLORS.keys())}")
                return False
            r_base, g_base, b_base = COLORS[color_base.lower()]
        else:
            try:
                r_base, g_base, b_base = color_base
            except (TypeError, ValueError):
                print("Error: Color must be a tuple (R, G, B) or a color name string")
                return False
        
        # Set base zone color (bytes 2-4)
        payload[2] = r_base
        payload[3] = g_base
        payload[4] = b_base
    
    # Handle color_rear parameter
    if color_rear is not None:
        if isinstance(color_rear, str):
            if color_rear.lower() not in COLORS:
                print(f"Error: Color '{color_rear}' not found. Available colors: {', '.join(COLORS.keys())}")
                return False
            r_rear, g_rear, b_rear = COLORS[color_rear.lower()]
        else:
            try:
                r_rear, g_rear, b_rear = color_rear
            except (TypeError, ValueError):
                print("Error: Color must be a tuple (R, G, B) or a color name string")
                return False
        
        # Set rear zone color (bytes 9-11)
        payload[9] = r_rear
        payload[10] = g_rear
        payload[11] = b_rear
    
    try:
        dev = hid.device()
        dev.open(VID, PID)
        dev.send_feature_report(payload)
        dev.close()
        
        if color_base is not None:
            base_str = color_base if isinstance(color_base, str) else f"RGB({color_base[0]}, {color_base[1]}, {color_base[2]})"
            
            if color_rear is not None and color_rear != color_base:
                rear_str = color_rear if isinstance(color_rear, str) else f"RGB({color_rear[0]}, {color_rear[1]}, {color_rear[2]})"
                print(f"Set mode to '{mode_name}' with base zone: {base_str}, rear zone: {rear_str}")
            else:
                print(f"Set mode to '{mode_name}' with color {base_str} (both zones)")
        else:
            print(f"Set mode to '{mode_name}'")
        return True
    
    except Exception as e:
        print(f"Error communicating with device: {e}")
        return False


def list_modes():
    """List all available modes."""
    print("Available modes:")
    for mode in MODES.keys():
        print(f"  - {mode}")


def list_colors():
    """List all available color presets."""
    print("Available color presets:")
    for color_name, (r, g, b) in COLORS.items():
        print(f"  - {color_name}: RGB({r}, {g}, {b})")


def main():
    """
    CLI interface for setting modes and colors.
    
    Default behavior (no arguments): Cycles through all modes (5s each).
    With arguments: Set specific mode and optional colors for base and rear zones.
    
    Usage:
        python set_mode.py                                    # Cycle all modes
        python set_mode.py <mode>                             # Set mode with default colors
        python set_mode.py <mode> <color>                     # Set mode with same color on both zones
        python set_mode.py <mode> <color_base> <color_rear>   # Set mode with different colors per zone
        python set_mode.py <mode> <R> <G> <B>                 # Set mode with custom RGB (both zones)
        python set_mode.py <mode> <R1> <G1> <B1> <R2> <G2> <B2>  # Set mode with different RGB per zone
    """
    if len(sys.argv) >= 2:
        # User provided mode argument
        mode = sys.argv[1]
        color_base = None
        color_rear = None
        
        # Parse color arguments
        if len(sys.argv) >= 3:
            try:
                # Check for RGB format with two zones (7 arguments: mode + R1 G1 B1 R2 G2 B2)
                if len(sys.argv) == 8:
                    r1 = int(sys.argv[2])
                    g1 = int(sys.argv[3])
                    b1 = int(sys.argv[4])
                    r2 = int(sys.argv[5])
                    g2 = int(sys.argv[6])
                    b2 = int(sys.argv[7])
                    color_base = (r1, g1, b1)
                    color_rear = (r2, g2, b2)
                # Check for RGB format single color (5 arguments: mode + R G B)
                elif len(sys.argv) == 5:
                    r = int(sys.argv[2])
                    g = int(sys.argv[3])
                    b = int(sys.argv[4])
                    color_base = (r, g, b)
                # Check for two color names (4 arguments: mode + color1 + color2)
                elif len(sys.argv) == 4:
                    color_base = sys.argv[2]
                    color_rear = sys.argv[3]
                # Single argument after mode
                else:
                    color_base = sys.argv[2]
            except ValueError:
                # If conversion fails, treat as color names
                if len(sys.argv) == 4:
                    color_base = sys.argv[2]
                    color_rear = sys.argv[3]
                else:
                    color_base = sys.argv[2]
        
        set_mode(mode, color_base, color_rear)
    else:
        # Default behavior: cycle through all modes
        print("Cycling through all modes (5s each)...")
        print("Press Ctrl+C to stop\n")
        
        try:
            # Cycle through modes
            print("=== MODES ===")
            for mode_name in MODES.keys():
                print(f"Setting mode: {mode_name}")
                set_mode(mode_name)
                time.sleep(5)
            
            # Cycle through colors in static mode
            print("\n=== COLORS (Static Mode) ===")
            for color_name, (r, g, b) in COLORS.items():
                print(f"Setting color: {color_name} RGB({r}, {g}, {b})")
                set_mode("static", color_name)
                time.sleep(3)
            
            print("\nCycle complete!")
        
        except KeyboardInterrupt:
            print("\n\nCycle interrupted by user")
            sys.exit(0)


if __name__ == "__main__":
    main()
