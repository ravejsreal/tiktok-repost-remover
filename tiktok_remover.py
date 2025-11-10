"""
TikTok Repost Remover
made by: ravejsreal
GitHub: https://github.com/ravejsreal/tiktok-repost-remover
"""

import os
import sys
import time
import threading
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

try:
    import keyboard
except Exception as e:
    missing_packages.append("keyboard")

try:
    from PIL import Image, ImageDraw, ImageFont
except Exception as e:
    missing_packages.append("pillow")

try:
    import win32gui
    import win32api
    import win32con
except Exception as e:
    missing_packages.append("pywin32")

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
        result = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pyautogui", "colorama", "keyboard", "pillow", "pywin32"],
                              capture_output=True, text=True)
        print(result.stdout)
        if result.returncode == 0:
            print("Installation complete! Restarting script...")
            print()
            input("Press Enter to restart...")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            print("Installation failed. Try running manually:")
            print("  pip install pyautogui colorama keyboard pillow pywin32")
            print()
            input("Press Enter to exit...")
    else:
        input("Press Enter to exit...")
    sys.exit(1)

init(autoreset=True)
PURPLE = Fore.MAGENTA + Style.BRIGHT

class TikTokRemover:
    def __init__(self):
        self.search_x = 1318
        self.search_y = 0
        self.search_y_start = 280
        self.search_y_end = 450
        self.delay = 2.0
        self.count = 0
        self.running = False
        self.start_time = 0
        self.stop_requested = False
        self.first_click = True

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

    def get_cursor_type(self):
        try:
            hcursor = win32gui.GetCursorInfo()[1]
            hand_cursor = win32api.LoadCursor(0, win32con.IDC_HAND)
            return hcursor == hand_cursor
        except:
            return False

    def find_clickable_position(self):
        current_x, current_y = pyautogui.position()

        start_y = min(current_y + 30, self.search_y_end)
        end_y = self.search_y_start

        for y in range(start_y, end_y, -2):
            pyautogui.moveTo(self.search_x, y, duration=0.01)
            time.sleep(0.02)

            if self.get_cursor_type():
                return self.search_x, y

        return None, None

    def set_position(self):
        self.print_header()
        print(PURPLE + "Move mouse EXACTLY over the repost button")
        print(PURPLE + "Tracking mouse position...")
        print()

        try:
            import msvcrt
            while True:
                x, y = pyautogui.position()
                print(PURPLE + f"\rCurrent position: X:{x:4d} Y:{y:4d} (Press 'O' to confirm)", end='', flush=True)

                if msvcrt.kbhit():
                    key = msvcrt.getch().decode('utf-8').lower()
                    if key == 'o':
                        self.search_x = x
                        self.search_y = y
                        break

                time.sleep(0.05)

        except KeyboardInterrupt:
            pass

        print()
        print()
        print(PURPLE + f"First click position: X:{self.search_x} Y:{self.search_y}")
        print(PURPLE + f"Will scan X:{self.search_x}, Y range: {self.search_y_start}-{self.search_y_end} for next clicks")
        print()
        input(PURPLE + "Press Enter to continue...")

    def display_thread(self):
        while self.running:
            elapsed = time.time() - self.start_time
            print(PURPLE + f"\rReposts removed: {self.count} | Time: {self.format_time(elapsed)}", end='', flush=True)
            time.sleep(0.1)

    def create_stats_image(self):
        script_dir = Path(__file__).parent
        output_path = script_dir / f"tiktok_stats_{int(time.time())}.png"

        img = Image.new('RGB', (800, 400), color=(138, 43, 226))
        draw = ImageDraw.Draw(img)

        try:
            font_large = ImageFont.truetype("arial.ttf", 48)
            font_medium = ImageFont.truetype("arial.ttf", 32)
            font_small = ImageFont.truetype("arial.ttf", 24)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()

        draw.text((400, 50), "TikTok Repost Remover", fill='white', anchor='mm', font=font_large)
        draw.text((400, 120), "Stats", fill='white', anchor='mm', font=font_medium)

        elapsed = time.time() - self.start_time
        draw.text((400, 200), f"Reposts Removed: {self.count}", fill='white', anchor='mm', font=font_medium)
        draw.text((400, 260), f"Total Time: {self.format_time(elapsed)}", fill='white', anchor='mm', font=font_medium)

        draw.text((400, 350), "made by ravejsreal", fill='white', anchor='mm', font=font_small)

        img.save(output_path)
        return output_path

    def on_q_pressed(self):
        self.stop_requested = True

    def run(self):
        self.set_position()

        self.print_header()
        print(PURPLE + f"Search X: {self.search_x}, Y Range: {self.search_y_start}-{self.search_y_end}")
        print(PURPLE + f"Delay: {self.delay} seconds")
        print()
        print(PURPLE + "Starting in 5 seconds... Switch to TikTok window!")
        print()

        for i in range(5, 0, -1):
            print(PURPLE + f"Starting in {i}...", end='\r', flush=True)
            time.sleep(1)

        print()
        print(PURPLE + "Running... (Press 'q' to stop)")
        print()

        keyboard.on_press_key('q', lambda _: self.on_q_pressed())

        self.running = True
        self.start_time = time.time()

        display = threading.Thread(target=self.display_thread, daemon=True)
        display.start()

        try:
            while not self.stop_requested:
                if self.first_click:
                    pyautogui.click(self.search_x, self.search_y)
                    self.count += 1
                    self.first_click = False
                else:
                    click_x, click_y = self.find_clickable_position()

                    if click_x and click_y:
                        pyautogui.click(click_x, click_y)
                        self.count += 1
                    else:
                        print(PURPLE + "\nButton not found, skipping...")

                for _ in range(int(self.delay * 10)):
                    if self.stop_requested:
                        break
                    time.sleep(0.1)

                if self.stop_requested:
                    break

                pyautogui.press('down')

                for _ in range(int(self.delay * 10)):
                    if self.stop_requested:
                        break
                    time.sleep(0.1)

        except KeyboardInterrupt:
            pass

        self.running = False
        keyboard.unhook_all()

        elapsed = time.time() - self.start_time
        print()
        print()
        print(PURPLE + "=" * 60)
        print(PURPLE + f"Stopped!")
        print(PURPLE + f"Total reposts removed: {self.count}")
        print(PURPLE + f"Total time: {self.format_time(elapsed)}")
        print(PURPLE + "=" * 60)
        print()

        print(PURPLE + "Creating stats image...")
        try:
            image_path = self.create_stats_image()
            print(PURPLE + f"Stats saved to: {image_path}")
            print()
            open_img = input(PURPLE + "Open stats image? (y/n): ").strip().lower()
            if open_img == 'y':
                os.startfile(image_path)
        except Exception as e:
            print(PURPLE + f"Error creating image: {e}")

        print()
        input(PURPLE + "Press Enter to exit...")


if __name__ == "__main__":
    remover = TikTokRemover()
    remover.run()
