import hid
import binascii

# ViewSonic Elite XG270QC HID identifiers
VID = 0x0543
PID = 0xA002

# 167-byte HID Feature Report from Wireshark (frame 4539)
# You can replace the bytes here to change color/mode.
data_hex = """
02 01 93 17 ff 00 0a 00 01 93 17 ff 00 0a 00 01 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
"""

data = bytes.fromhex(' '.join(data_hex.strip().split()))

# open the device
dev = hid.device()
dev.open(VID, PID)

# optional: print device info
print(f"Opened {dev.get_manufacturer_string()} {dev.get_product_string()}")

# Send the feature report
# Report ID is 2 (from Wireshark: wValue 0x0302)
report_id = 2

# hidapi expects full report: [report_id, <payload>]
# if data already starts with 0x02, it's okay to send as-is.
dev.send_feature_report(data)

print("Feature report sent!")

# close device
dev.close()
