"""
ViewSonic RGB Controller - Razer Chroma SDK Support
Uses pywinusb for HID communication
"""

import time
import sys
import threading

try:
    import pywinusb.hid as hid
except ImportError:
    print("ERROR: pywinusb not installed!")
    print("Run: pip install pywinusb")
    sys.exit(1)

# ViewSonic Vendor ID and supported PIDs
VIEWSONIC_VID = 0x0543
SUPPORTED_PIDS = [0xA002]  # ViewSonic Elite XG270QC

VID = VIEWSONIC_VID
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

# Music mode flag
_music_stop_flag = False


def find_viewsonic_devices():
    """Find all connected ViewSonic devices"""
    devices = []
    
    try:
        all_devices = hid.find_all_hid_devices()
        
        for i, device in enumerate(all_devices):
            if device.vendor_id == VIEWSONIC_VID and device.product_id in SUPPORTED_PIDS:
                devices.append({
                    'index': len(devices),
                    'device': device,
                    'vendor_id': device.vendor_id,
                    'product_id': device.product_id,
                    'product': device.product_name or 'ViewSonic Monitor',
                    'serial': device.serial_number or 'Unknown',
                    'manufacturer': 'ViewSonic',
                    'path': str(device)  # Use string representation for path
                })
    except Exception as e:
        print(f"Error finding devices: {e}", file=sys.stderr)
    
    return devices


def list_viewsonic_devices():
    """Print all connected ViewSonic devices"""
    devices = find_viewsonic_devices()
    
    if not devices:
        print("\nNo ViewSonic devices found!")
        return
    
    print(f"\nFound {len(devices)} ViewSonic device(s):\n")
    print(f"{'Index':<8} {'Device':<30} {'Serial':<20} {'Manufacturer':<15}")
    print("-" * 73)
    
    for device in devices:
        print(
            f"{device['index']:<8} "
            f"{device['product']:<30} "
            f"{device['serial']:<20} "
            f"{device['manufacturer']:<15}"
        )


def get_device_by_index(index):
    """Get device info by index"""
    devices = find_viewsonic_devices()
    if 0 <= index < len(devices):
        return devices[index]
    return None


def set_mode(mode_name, color_base=None, color_rear=None, device_index=None):
    """
    Set RGB mode on device
    
    Args:
        mode_name: static, rainbow, breathing, stack, warp-speed, music, music-pulse
        color_base: (R, G, B) tuple for base zone (or color name string)
        color_rear: (R, G, B) tuple for rear zone (or color name string)
        device_index: Which device to control (None = all devices)
    """
    
    if mode_name not in MODES:
        print(f"ERROR: Unknown mode '{mode_name}'")
        print(f"Available modes: {', '.join(MODES.keys())}")
        return False
    
    # Convert color names to RGB tuples
    if isinstance(color_base, str):
        color_base = COLORS.get(color_base.lower())
    if isinstance(color_rear, str):
        color_rear = COLORS.get(color_rear.lower())
    
    # Get list of devices to control
    if device_index is None:
        devices = find_viewsonic_devices()
        device_indices = [d['index'] for d in devices]
    else:
        device_indices = [device_index]
    
    if not device_indices:
        print("ERROR: No ViewSonic devices found!")
        return False
    
    success = True
    
    for idx in device_indices:
        try:
            device_info = get_device_by_index(idx)
            if not device_info:
                print(f"ERROR: Device #{idx} not found")
                success = False
                continue
            
            payload = MODES[mode_name].copy()
            
            # Set colors if applicable
            if mode_name in ["static", "breathing", "stack"]:
                if color_base:
                    payload[2] = color_base[0]
                    payload[3] = color_base[1]
                    payload[4] = color_base[2]
                
                if color_rear:
                    payload[9] = color_rear[0]
                    payload[10] = color_rear[1]
                    payload[11] = color_rear[2]
            
            # Send feature report
            device = device_info['device']
            device.open()
            device.send_feature_report(payload)
            device.close()
            
            # Print confirmation
            if color_base and color_rear:
                print(f"Set {device_info['product']} (#{idx}) to {mode_name} "
                      f"(base: RGB{color_base}, rear: RGB{color_rear})")
            elif color_base:
                print(f"Set {device_info['product']} (#{idx}) to {mode_name} "
                      f"(RGB{color_base})")
            else:
                print(f"Set {device_info['product']} (#{idx}) to {mode_name}")
                
        except Exception as e:
            print(f"ERROR setting mode on device #{idx}: {e}", file=sys.stderr)
            success = False
    
    return success


def set_music_mode(variant, duration=None, device_index=None):
    """Start music visualization mode"""
    global _music_stop_flag
    
    if variant not in ["music", "music-pulse"]:
        print(f"ERROR: Invalid music variant '{variant}'")
        return False
    
    # First set the mode
    set_mode(variant, device_index=device_index)
    
    # Start music streaming
    _music_stop_flag = False
    thread = threading.Thread(
        target=_music_stream_worker,
        args=(variant, duration, device_index),
        daemon=True
    )
    thread.start()
    
    if duration:
        thread.join(timeout=duration)
        stop_music_mode()
    
    return True


def stop_music_mode():
    """Stop music mode streaming"""
    global _music_stop_flag
    _music_stop_flag = True


def _music_stream_worker(variant, duration, device_index):
    """Background worker for music mode streaming"""
    global _music_stop_flag
    import math
    
    devices = find_viewsonic_devices()
    if device_index is not None:
        devices = [d for d in devices if d['index'] == device_index]
    
    if not devices:
        print("ERROR: No devices for music streaming")
        return
    
    start_time = time.time()
    tick = 0
    
    try:
        while not _music_stop_flag:
            if duration and (time.time() - start_time) > duration:
                break
            
            # Generate audio-like data
            bass = int(128 + 127 * math.sin(tick * 0.02))
            freq_l = int(128 + 100 * math.sin(tick * 0.03))
            freq_r = int(128 + 100 * math.cos(tick * 0.03))
            
            # Music packet (64 bytes)
            payload = [0x01, 0xC0, 0x00, bass, freq_l, freq_r] + [0x00] * 58
            
            # Send to all devices
            for device_info in devices:
                try:
                    device = device_info['device']
                    device.open()
                    device.write(payload)
                    device.close()
                except Exception:
                    pass
            
            tick += 1
            time.sleep(0.01)  # ~100Hz update rate
            
    except KeyboardInterrupt:
        pass
    finally:
        print("Music mode stopped")


def main():
    """Main CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='ViewSonic RGB Controller - Razer Chroma SDK Support',
        prog='set_mode.py'
    )
    
    parser.add_argument(
        'command',
        nargs='?',
        default='list',
        help='Command: list, rainbow, breathing, stack, warp-speed, music, music-pulse, static'
    )
    
    parser.add_argument(
        '--device',
        type=int,
        default=None,
        help='Device index (default: all devices)'
    )
    
    parser.add_argument(
        'colors',
        nargs='*',
        help='Color name(s) or RGB values'
    )
    
    args = parser.parse_args()
    
    if args.command == 'list':
        list_viewsonic_devices()
        return
    
    # Parse colors
    color_base = None
    color_rear = None
    
    if args.colors:
        first = args.colors[0]
        if first in COLORS:
            color_base = COLORS[first]
        else:
            try:
                if len(args.colors) >= 3:
                    color_base = (int(args.colors[0]), int(args.colors[1]), int(args.colors[2]))
                    if len(args.colors) >= 6:
                        color_rear = (int(args.colors[3]), int(args.colors[4]), int(args.colors[5]))
            except ValueError:
                print(f"ERROR: Invalid color format '{first}'")
                return
    
    # Execute command
    if args.command in MODES:
        set_mode(args.command, color_base, color_rear, args.device)
    elif args.command == 'music' or args.command == 'music-pulse':
        duration = None
        if args.colors and args.colors[0].isdigit():
            duration = int(args.colors[0])
        set_music_mode(args.command, duration, args.device)
    else:
        print(f"ERROR: Unknown command '{args.command}'")
        print(f"Available commands: list, {', '.join(MODES.keys())}")


if __name__ == "__main__":
    main()