# TikTok Repost Remover

**made by ravejsreal**
[GitHub Repository](https://github.com/ravejsreal/tiktok-repost-remover)

Automated tool to remove TikTok reposts. Clicks the remove button and scrolls down automatically with a 2 second delay between actions.

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

4. You have 5 seconds to switch to your TikTok window
5. Script will automatically click at position X:1318 Y:318 then press down arrow
6. Press Ctrl+C to stop when done

## What It Does

The script repeats this cycle with a 2 second delay between each action:
1. Move mouse to X:1318 Y:318
2. Click
3. Wait 2 seconds
4. Press down arrow key
5. Wait 2 seconds
6. Repeat

Shows you how many reposts have been removed and tracks total time running.

## Example

When you run it you'll see:

```
============================================================
               TIKTOK REPOST REMOVER
                   made by ravejsreal
       github.com/ravejsreal/tiktok-repost-remover
============================================================

Click Position: X:1318 Y:318
Delay: 2.0 seconds

Starting in 5 seconds... Switch to TikTok window!

Running... (Press Ctrl+C to stop)

Reposts removed: 42 | Time: 00:03:24
```

The counter and timer update in real-time as it works.
"# tiktok-repost-remover" 
