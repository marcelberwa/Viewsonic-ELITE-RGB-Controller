import hid
import time

# ViewSonic Elite XG270QC HID identifiers
VID = 0x0543
PID = 0xA002

# Base payload from Wireshark (Blue) — fill the rest to 167 bytes
BASE_PAYLOAD = [
    0x02, 0x01, 0x00, 0x53, 0xF7, 0x00, 0x0A, 0x00, 0x01
] + [0x00] * (167 - 9)

# Define 10 colors (R, G, B) as observed / example values
COLORS = [
    (0x00, 0x53, 0xF7),  # Blue
    (0x01, 0x4F, 0xFE),  # Cyan
    (0xFF, 0xF9, 0x4D),  # Yellow
    (0xF7, 0x00, 0x93),  # Magenta-like
    (0xFF, 0x00, 0x00),  # Red
    (0x00, 0xFF, 0x00),  # Green
    (0x00, 0x00, 0xFF),  # Pure Blue
    (0xFF, 0xFF, 0xFF),  # White
    (0x80, 0x80, 0x00),  # Olive
    (0x00, 0x80, 0x80),  # Teal
]

def set_color(r, g, b):
    """Send a color Feature Report to the monitor."""
    payload = BASE_PAYLOAD.copy()
    payload[2] = r
    payload[3] = g
    payload[4] = b

    dev = hid.device()
    dev.open(VID, PID)
    dev.send_feature_report(payload)
    dev.close()
    print(f"Set color to R={r} G={g} B={b}")

def main():
    for color in COLORS:
        r, g, b = color
        set_color(r, g, b)
        time.sleep(3)

if __name__ == "__main__":
    main()