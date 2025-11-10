"""
TikTok Repost Remover
made by: ravejsreal
GitHub: https://github.com/ravejsreal/tiktok-repost-remover
"""

import os
import sys
import time
from pathlib import Path

missing_packages = []

try:
    import pyautogui
except Exception as e:
    missing_packages.append("pyautogui")

try:
    from colorama import Fore, Style, init
except Exception as e:
    missing_packages.append("colorama")

if missing_packages:
    print("=" * 60)
    print("ERROR: Missing required packages".center(60))
    print("=" * 60)
    print()
    print(f"Missing: {', '.join(missing_packages)}")
    print()
    print("Install with:")
    print("  pip install -r requirements.txt")
    print()

    install = input("Install missing packages now? (y/n): ").strip().lower()
    if install == 'y':
        print()
        print("Installing packages...")
        import subprocess
        result = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pyautogui", "colorama"],
                              capture_output=True, text=True)
        print(result.stdout)
        if result.returncode == 0:
            print("Installation complete! Restarting script...")
            print()
            input("Press Enter to restart...")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            print("Installation failed. Try running manually:")
            print("  pip install pyautogui colorama")
            print()
            input("Press Enter to exit...")
    else:
        input("Press Enter to exit...")
    sys.exit(1)

init(autoreset=True)
PURPLE = Fore.MAGENTA + Style.BRIGHT

class TikTokRemover:
    def __init__(self):
        self.click_x = 1318
        self.click_y = 318
        self.delay = 2.0
        self.count = 0

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        self.clear_screen()
        print(PURPLE + "=" * 60)
        print(PURPLE + "TIKTOK REPOST REMOVER".center(60))
        print(PURPLE + "made by ravejsreal".center(60))
        print(PURPLE + "github.com/ravejsreal/tiktok-repost-remover".center(60))
        print(PURPLE + "=" * 60)
        print()

    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def run(self):
        self.print_header()
        print(PURPLE + f"Click Position: X:{self.click_x} Y:{self.click_y}")
        print(PURPLE + f"Delay: {self.delay} seconds")
        print()
        print(PURPLE + "Starting in 5 seconds... Switch to TikTok window!")
        print()

        for i in range(5, 0, -1):
            print(PURPLE + f"Starting in {i}...", end='\r', flush=True)
            time.sleep(1)

        print()
        print(PURPLE + "Running... (Press Ctrl+C to stop)")
        print()

        start_time = time.time()

        try:
            while True:
                pyautogui.moveTo(self.click_x, self.click_y)
                time.sleep(0.1)
                pyautogui.click()
                self.count += 1

                elapsed = time.time() - start_time
                print(PURPLE + f"\rReposts removed: {self.count} | Time: {self.format_time(elapsed)}", end='', flush=True)

                time.sleep(self.delay)

                pyautogui.press('down')

                time.sleep(self.delay)

        except KeyboardInterrupt:
            elapsed = time.time() - start_time
            print()
            print()
            print(PURPLE + "=" * 60)
            print(PURPLE + f"Stopped!")
            print(PURPLE + f"Total reposts removed: {self.count}")
            print(PURPLE + f"Total time: {self.format_time(elapsed)}")
            print(PURPLE + "=" * 60)
            print()
            input(PURPLE + "Press Enter to exit...")


if __name__ == "__main__":
    remover = TikTokRemover()
    remover.run()
