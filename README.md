# TikTok Repost Remover

**made by ravejsreal**
[GitHub Repository](https://github.com/ravejsreal/tiktok-repost-remover)

Automatically removes all your TikTok reposts. Fast and efficient - removes about 12 reposts per minute (720 per hour).

## Features

✅ **Color detection** - searches for the repost button color (#efc546) in a defined area
✅ **Red rectangle overlay** - shows the search area while running
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

The script uses color detection to find the repost button. Here's what happens:

1. **Set position**: You position your mouse over the repost button and press 'O'
2. **Create search area**: A 40px wide × 200px tall rectangle is created centered on your position
3. **Color search**: Searches for the exact color #efc546 (yellow repost button) within the rectangle
4. **Click**: Instantly teleports cursor to the color and clicks
5. **Move left**: Moves cursor 100px to the left
6. **Scroll down**: Presses down arrow key to move to next repost
7. **Wait**: 2 second delay before next search
8. **Repeat**: Continues until you press 'q' to stop

The red rectangle overlay stays visible the entire time so you can see the search area. Shows you how many reposts have been removed and tracks total time running. When you stop it, generates a purple stats image.

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

All packages auto-install if missing when you run the script.
