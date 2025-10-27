# ViewSonic Elite RGB Controller 🎨

Control your ViewSonic Elite monitor RGB lighting with USB HID, Razer Chroma SDK, or screen color sampling.

## 🚀 Quick Start

**See [`QUICK_START.md`](QUICK_START.md) for the fastest way to get started!**

### Three Ways to Control Your Monitor

1. **🎮 Official Razer Chroma** - Already installed! Works with 100+ games
2. **🖥️ Universal Screen Sampling** - Works with ANY game  
3. **🐍 Manual Python Control** - Direct USB HID control

## 📋 Features

- ✅ **Direct USB HID Control** - Control RGB via Python
- ✅ **Razer Chroma Integration** - Sync with Chroma-enabled games
- ✅ **Screen Color Sampling** - Universal game support
- ✅ **Multiple Modes** - Static, Rainbow, Breathing, Music-reactive, etc.
- ✅ **Dual-Zone Control** - Independent base & rear lighting
- ✅ **Multi-Monitor Support** - Control multiple ViewSonic displays

## 🔍 Discovery: Official Chroma Integration Exists!

**IMPORTANT:** Your ViewSonic monitor already has official Razer Chroma support via:

```
C:\ProgramData\Razer Chroma SDK\Apps\ViewSonicRGBController\ViewSonicRGBController.exe
```

This handles all Chroma RGB data automatically. See [`CHROMA_INTEGRATION_DISCOVERY.md`](CHROMA_INTEGRATION_DISCOVERY.md) for details.

## ⚡ Installation

### Prerequisites
- Windows 10/11
- Python 3.8+ (for Python scripts)
- ViewSonic Elite monitor (tested with XG270QC)

### Install Python Dependencies

```powershell
pip install -r requirements.txt
```

## 📖 Usage

### Option 1: Official Razer Chroma (Recommended)

```powershell
# Check if running
Get-Process ViewSonicRGBController

# Launch any Chroma-enabled game - it syncs automatically! ✨
```

### Option 2: Screen Color Sampling (Universal)

```powershell
# Works with ANY game, not just Chroma
python chroma_screen_sync.py
```

### Option 3: Manual USB HID Control

```powershell
# List devices
python set_mode.py --list

# Set static color (dual zone)
python set_mode.py --mode static --base FF0000 --rear 0000FF

# Effects
python set_mode.py --mode rainbow
python set_mode.py --mode breathing --base 00FF00
python set_mode.py --mode music
```

### Option 4: Python Chroma Client (Custom)

```powershell
# Custom Chroma SDK integration
python viewsonic_chroma_client.py
```

## 🛠️ Available Tools

| Tool | Purpose |
|------|---------|
| `set_mode.py` | Direct USB HID control |
| `chroma_screen_sync.py` | Screen color sampling for any game |
| `viewsonic_chroma_client.py` | Python Chroma SDK client |
| `monitor_chroma_traffic.py` | Chroma SDK diagnostics |
| `ViewSonicRGBController.exe` | Official Chroma integration |

## 🎮 Supported RGB Modes

- **Static** - Solid color (dual zone)
- **Rainbow** - Cycling rainbow effect
- **Breathing** - Pulsing effect with custom color
- **Stack** - Stacking color animation
- **Warp-speed** - Fast color transitions
- **Music** - Music-reactive (requires audio input)

## 🔧 Advanced Usage

### Multi-Monitor Control

```python
import set_mode

# Find all devices
devices = set_mode.find_viewsonic_devices()

# Control specific monitor
set_mode.set_mode("static", 
    color_base=(255, 0, 0), 
    color_rear=(0, 0, 255),
    device_index=0
)
```

### Custom Color Effects

```python
# Gradual color transitions
for i in range(256):
    set_mode.set_mode("static",
        color_base=(i, 0, 255-i),
        color_rear=(255-i, 0, i)
    )
    time.sleep(0.01)
```

## 🐛 Troubleshooting

### No ViewSonic devices found
1. Check USB connection
2. Verify monitor is powered on
3. Try different USB port
4. Run as Administrator

### Chroma SDK not responding
1. Install Razer Synapse 3
2. Start Razer Chroma SDK Service
3. Check: `netstat -ano | Select-String "54235"`

### ViewSonicRGBController not working
1. Check if running: `Get-Process ViewSonicRGBController`
2. Verify in Razer Synapse → Chroma Studio
3. Restart Razer Synapse

### Screen sampling colors incorrect
1. Adjust `COLOR_HISTORY_SIZE` in `chroma_screen_sync.py`
2. Try different sampling methods (edge/corner/dominant)
3. Increase/decrease `UPDATE_INTERVAL` for FPS

## 📚 Documentation

- [`QUICK_START.md`](QUICK_START.md) - Fast setup guide
- [`CHROMA_INTEGRATION_DISCOVERY.md`](CHROMA_INTEGRATION_DISCOVERY.md) - How Chroma integration works
- [`requirements.txt`](requirements.txt) - Python dependencies

## 🔬 Technical Details

### USB HID Protocol

```
Device:     VID:0x0543, PID:0xA002
Interface:  HID Feature Reports
Packet:     167 bytes
Format:     [mode, base_R, base_G, base_B, rear_R, rear_G, rear_B, ...]
```

### Razer Chroma SDK

```
Endpoint:   http://localhost:54235/razer/chromasdk
Protocol:   REST API (HTTP/JSON)
Auth:       None (localhost only)
```

### Screen Sampling

```
Method:     PIL screenshot → numpy color analysis
FPS:        30 (configurable)
Smoothing:  3-frame color history
```

## 🤝 Contributing

This project reverse-engineers the ViewSonic Elite RGB USB protocol. Contributions welcome!

### Discovered So Far
- ✅ USB HID protocol (167-byte packets)
- ✅ Color mode commands (static, rainbow, breathing, etc.)
- ✅ Official Chroma integration (ViewSonicRGBController.exe)
- ✅ Dual-zone control (base + rear)
- ⏳ Music-reactive sensitivity settings
- ⏳ Advanced timing/transition controls

## 📝 License

See LICENSE file.

## 🙏 Credits

- ViewSonic for the Elite series monitors
- Razer for Chroma SDK
- Community contributors at https://github.com/viewsonic-rgb

## ⚠️ Disclaimer

This is an unofficial third-party tool. Use at your own risk. Not affiliated with ViewSonic or Razer.