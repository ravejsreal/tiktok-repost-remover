# TikTok Repost Remover

**made by ravejsreal**
[GitHub Repository](https://github.com/ravejsreal/tiktok-repost-remover)

Automatically removes all your TikTok reposts. Fast and efficient - removes about 12 reposts per minute (720 per hour).

## Features

✅ **Smart button detection** - finds the button even if it moves
✅ **Live counter** - shows reposts removed and time elapsed
✅ **Global hotkey (q)** - stop from any window
✅ **Stats image** - generates a purple stats image when done
❌ Can **not** run in the background while you do other stuff

## Speed

⚡ ~12 reposts per minute
⚡ ~720 reposts per hour
⚡ 2 second delay between actions (safe and won't get flagged)

## Installation

```bash
pip install -r requirements.txt
```

## How to Use

1. Open TikTok in your browser
2. Navigate to your reposts page
3. Run the script:

```bash
python tiktok_remover.py
```

4. Position your mouse exactly on the repost button
5. Press 'O' to confirm the position
6. You have 5 seconds to switch to your TikTok window
7. Script will automatically find and click the repost button, then scroll down
8. Press 'q' from anywhere to stop

## How It Works

The script uses smart cursor detection to find clickable elements. Here's what happens:

1. **First click**: Clicks at the exact position you set
2. **Subsequent clicks**: Scans vertically to find the button using cursor type detection (hand pointer)
3. **Scrolls down**: Presses down arrow key to move to next repost
4. **Repeats**: Continues with 2 second delays between actions

Shows you how many reposts have been removed and tracks total time running. When you stop it, generates a purple stats image.

## Example

When you run it you'll see:

```
============================================================
               TIKTOK REPOST REMOVER
                   made by ravejsreal
       github.com/ravejsreal/tiktok-repost-remover
============================================================

Move mouse EXACTLY over the repost button
Tracking mouse position...

Current position: X:1318 Y:350 (Press 'O' to confirm)
```

Then while running:

```
Running... (Press 'q' to stop)

Reposts removed: 12 | Time: 00:01:00
```

Perfect for cleaning up your TikTok profile when you've got dozens (or thousands) of reposts to remove. Just set it and let it run.

## Requirements

- Python 3.x
- pyautogui
- colorama
- keyboard
- pillow
- pywin32

All packages auto-install if missing when you run the script.
