# TikTok Repost Remover

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

**A smart automation tool that removes TikTok reposts quickly and efficiently using intelligent cursor detection.**

Made with ❤️ by [ravejsreal](https://github.com/ravejsreal)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Performance](#performance)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Manually removing hundreds or thousands of TikTok reposts is tedious and time-consuming. **TikTok Repost Remover** automates this process using smart cursor detection to find and click the repost button, then scrolls to the next one. Set it up once and let it clean your profile automatically.

Perfect for users who want to:
- Clean up their TikTok profile
- Remove bulk reposts efficiently
- Save hours of manual clicking

---

## Features

### Core Features

✅ **Smart Button Detection** - Uses Windows cursor API to intelligently locate clickable elements, even when button positions change

✅ **Live Statistics** - Real-time counter showing reposts removed and time elapsed

✅ **Global Hotkey Support** - Press `q` from any window to stop the automation safely

✅ **Stats Image Generation** - Creates a shareable purple stats image when finished

✅ **Auto-Dependency Installation** - Automatically detects and offers to install missing packages

✅ **Configurable Delays** - Safe 2-second default delay prevents rate limiting

### What It Can't Do

❌ **Background Operation** - Must run in the foreground; you cannot use your computer for other tasks while it runs

---

## Performance

| Metric | Value |
|--------|-------|
| **Reposts per Minute** | ~12 |
| **Reposts per Hour** | ~720 |
| **Default Delay** | 2 seconds |
| **Detection Method** | Cursor type scanning |

These values ensure safe operation without triggering TikTok's rate limiting or anti-automation measures.

---

## Prerequisites

### System Requirements

- **Operating System**: Windows (uses `win32` APIs for cursor detection)
- **Python**: Version 3.6 or higher
- **Browser**: Any browser that supports TikTok

### Python Packages

All packages will auto-install if missing when you first run the script:

- `pyautogui` - GUI automation
- `colorama` - Colored terminal output
- `keyboard` - Global hotkey detection
- `pillow` - Stats image generation
- `pywin32` - Windows API access for cursor detection

---

## Installation

### Quick Install

1. **Clone the repository**
   ```bash
   git clone https://github.com/ravejsreal/tiktok-repost-remover.git
   cd tiktok-repost-remover
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Or let the script auto-install them on first run!

### Manual Installation

If you prefer to install packages manually:

```bash
pip install pyautogui colorama keyboard pillow pywin32
```

---

## Usage

### Step-by-Step Guide

1. **Open TikTok in your browser**
   - Navigate to your profile
   - Go to your reposts page
   - Make sure the repost button is visible on screen

2. **Run the script**
   ```bash
   python tiktok_remover.py
   ```

3. **Position your mouse**
   - Move your mouse cursor exactly over the repost button
   - The terminal will show real-time coordinates: `X:1318 Y:350`
   - Press `O` when positioned correctly

4. **Confirm and start**
   - Press `Enter` to confirm the position
   - You have **5 seconds** to switch to your TikTok window
   - The automation starts automatically

5. **Monitor progress**
   ```
   Running... (Press 'q' to stop)

   Reposts removed: 42 | Time: 00:03:30
   ```

6. **Stop when done**
   - Press `q` from anywhere to stop
   - View your statistics summary
   - Optionally generate and view a stats image

### Example Session

```
============================================================
               TIKTOK REPOST REMOVER
                   made by ravejsreal
       github.com/ravejsreal/tiktok-repost-remover
============================================================

Move mouse EXACTLY over the repost button
Tracking mouse position...

Current position: X:1318 Y:350 (Press 'O' to confirm)

First click position: X:1318 Y:350
Will scan X:1318, Y range: 280-450 for next clicks

Press Enter to continue...

Search X: 1318, Y Range: 280-450
Delay: 2.0 seconds

Starting in 5 seconds... Switch to TikTok window!

Running... (Press 'q' to stop)

Reposts removed: 156 | Time: 00:26:00
```

---

## How It Works

### Technical Overview

The automation uses a sophisticated cursor detection algorithm:

1. **Initial Click**
   - Uses the exact (X, Y) coordinates you provide
   - Clicks the repost button at this position

2. **Intelligent Scanning**
   - For subsequent reposts, scans vertically along the X coordinate
   - Checks cursor type at each position (normal vs. hand pointer)
   - When cursor changes to hand pointer, button is detected
   - Clicks at the detected position

3. **Scrolling**
   - Presses the down arrow key to navigate to next repost
   - Waits the configured delay (default: 2 seconds)

4. **Repeat**
   - Continues the cycle until you press `q` or no more reposts exist

### Algorithm Details

```python
# Vertical scan algorithm
for y in range(start_y, end_y, -2):
    move_cursor_to(x, y)
    if cursor_is_hand_pointer():
        click(x, y)
        break
```

The 2-pixel increment provides fast scanning while maintaining accuracy.

---

## Configuration

### Default Settings

You can modify these values in `tiktok_remover.py`:

```python
class TikTokRemover:
    def __init__(self):
        self.search_x = 1318          # X coordinate for scanning
        self.search_y_start = 280     # Top of scan range
        self.search_y_end = 450       # Bottom of scan range
        self.delay = 2.0              # Delay between actions (seconds)
```

### Adjusting the Delay

For faster removal (at your own risk):
```python
self.delay = 1.0  # 1 second delay
```

For safer operation on slower connections:
```python
self.delay = 3.0  # 3 second delay
```

### Adjusting the Scan Range

If buttons appear outside the default range:
```python
self.search_y_start = 200  # Scan higher on screen
self.search_y_end = 600    # Scan lower on screen
```

---

## Troubleshooting

### Common Issues

#### "Button not found, skipping..."

**Cause**: The cursor detection couldn't find a clickable element in the scan range.

**Solutions**:
- Verify TikTok window is active and visible
- Check that reposts are still available
- Adjust `search_y_start` and `search_y_end` values
- Make sure browser zoom is at 100%

#### Script clicks wrong position

**Cause**: Screen resolution or browser zoom affects coordinates.

**Solutions**:
- Set browser zoom to 100%
- Re-run and carefully position mouse when prompted
- Check that TikTok's layout hasn't changed

#### ImportError or ModuleNotFoundError

**Cause**: Missing Python packages.

**Solutions**:
- Run `pip install -r requirements.txt`
- Or let the script auto-install on first run
- Make sure you're using Python 3.6+

#### Nothing happens after starting

**Cause**: TikTok window not in focus or coordinates incorrect.

**Solutions**:
- Make sure you clicked into the TikTok window during the 5-second countdown
- Verify the initial position you set was correct
- Check that the repost button is visible on screen

#### Stats image not opening

**Cause**: No default image viewer or permission issues.

**Solutions**:
- Manually open the generated PNG from the script directory
- Check file permissions
- Look for `tiktok_stats_[timestamp].png` in the script folder

---

## FAQ

### Is this safe to use?

Yes, the script uses safe delays (2 seconds) to avoid triggering anti-automation measures. However, use at your own discretion and according to TikTok's Terms of Service.

### Can I use this on Mac or Linux?

No, this version requires Windows because it uses `win32` APIs for cursor detection. A cross-platform version could be developed using alternative methods.

### Will this get my account banned?

The script is designed with safe delays and natural behavior patterns. However, any automation carries inherent risk. Use responsibly and don't abuse it.

### Can I run this in the background?

No, the automation requires the TikTok window to be visible and in focus for cursor detection and clicking to work.

### How do I stop it in an emergency?

Press `q` from any window - it's a global hotkey that works even if TikTok window is focused.

### Can I adjust the speed?

Yes, modify the `self.delay` value in the code. Lower values = faster, but increased risk of rate limiting.

### Does this work with TikTok mobile app?

No, this is designed for browser-based TikTok only.

---

## Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Ideas for Contributions

- Cross-platform support (macOS, Linux)
- GUI interface
- Browser extension version
- Customizable themes for stats images
- Better error handling
- Configuration file support
- Pause/resume functionality

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Creator**: [ravejsreal](https://github.com/ravejsreal)
- **Repository**: [tiktok-repost-remover](https://github.com/ravejsreal/tiktok-repost-remover)

---

## Disclaimer

This tool is for educational and personal use only. Use it responsibly and in accordance with TikTok's Terms of Service. The author is not responsible for any consequences resulting from the use of this tool.

---

## Support

If you find this tool helpful, consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs in the Issues section
- 💡 Suggesting new features
- 🔄 Sharing with others who might find it useful

---

**Happy cleaning! 🧹✨**
