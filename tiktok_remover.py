"""
TikTok Repost Remover

A Python automation tool that automatically removes TikTok reposts from your profile.
This script uses intelligent cursor detection and GUI automation to efficiently remove
multiple reposts with minimal user intervention.

Features:
    - Smart button detection using cursor type checking
    - Live statistics display (count and elapsed time)
    - Global hotkey support to stop from any window
    - Automatic stats image generation
    - Auto-install missing dependencies

Author: ravejsreal
GitHub: https://github.com/ravejsreal/tiktok-repost-remover
License: MIT

Usage:
    python tiktok_remover.py

Requirements:
    - Python 3.6+
    - Windows OS (uses win32 APIs for cursor detection)
    - See requirements.txt for package dependencies
"""

import os
import sys
import time
import threading
from pathlib import Path
from typing import Optional, Tuple

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
    """
    Main automation class for removing TikTok reposts.

    This class handles the entire automation workflow including position detection,
    button clicking, scrolling, and statistics tracking. It uses cursor type detection
    to intelligently locate clickable elements on the screen.

    Attributes:
        search_x (int): X coordinate for button search
        search_y (int): Initial Y coordinate for first click
        search_y_start (int): Starting Y coordinate for vertical search range
        search_y_end (int): Ending Y coordinate for vertical search range
        delay (float): Delay in seconds between actions
        count (int): Number of reposts removed
        running (bool): Flag indicating if automation is currently running
        start_time (float): Timestamp when automation started
        stop_requested (bool): Flag to signal stop request
        first_click (bool): Flag to track if this is the first click
    """

    def __init__(self):
        """Initialize the TikTokRemover with default settings."""
        self.search_x = 1318  # Default X position for button
        self.search_y = 0  # Will be set by user
        self.search_y_start = 280  # Top of vertical search range
        self.search_y_end = 450  # Bottom of vertical search range
        self.delay = 2.0  # Safe delay to avoid rate limiting
        self.count = 0  # Reposts removed counter
        self.running = False  # Automation state
        self.start_time = 0  # Session start time
        self.stop_requested = False  # Stop signal
        self.first_click = True  # First click uses user-defined position

    def clear_screen(self):
        """Clear the terminal screen (cross-platform)."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """Display the application header with branding."""
        self.clear_screen()
        print(PURPLE + "=" * 60)
        print(PURPLE + "TIKTOK REPOST REMOVER".center(60))
        print(PURPLE + "made by ravejsreal".center(60))
        print(PURPLE + "github.com/ravejsreal/tiktok-repost-remover".center(60))
        print(PURPLE + "=" * 60)
        print()

    def format_time(self, seconds: float) -> str:
        """
        Convert seconds to HH:MM:SS format.

        Args:
            seconds (float): Time in seconds

        Returns:
            str: Formatted time string in HH:MM:SS format
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def get_cursor_type(self) -> bool:
        """
        Check if the cursor is currently displaying as a hand pointer.

        This method uses Windows API to detect if the cursor has changed to a hand
        pointer, which typically indicates a clickable element.

        Returns:
            bool: True if cursor is a hand pointer, False otherwise
        """
        try:
            hcursor = win32gui.GetCursorInfo()[1]
            hand_cursor = win32api.LoadCursor(0, win32con.IDC_HAND)
            return hcursor == hand_cursor
        except:
            return False

    def find_clickable_position(self) -> Tuple[Optional[int], Optional[int]]:
        """
        Scan vertically to find a clickable button position.

        This method moves the cursor vertically along a predefined X coordinate,
        checking for hand pointer cursor changes that indicate a clickable element.

        Returns:
            Tuple[Optional[int], Optional[int]]: (x, y) coordinates if button found,
                                                  (None, None) otherwise

        Note:
            Scans upward from current position + 30px to search_y_start in 2px steps
        """
        current_x, current_y = pyautogui.position()

        # Start slightly below current position, scan upward
        start_y = min(current_y + 30, self.search_y_end)
        end_y = self.search_y_start

        # Scan upward in 2-pixel increments
        for y in range(start_y, end_y, -2):
            pyautogui.moveTo(self.search_x, y, duration=0.01)
            time.sleep(0.02)

            # Check if cursor changed to hand pointer (clickable element)
            if self.get_cursor_type():
                return self.search_x, y

        return None, None

    def set_position(self):
        """
        Interactive setup to capture the initial button position from user.

        Displays real-time mouse coordinates and waits for user to press 'O'
        to confirm the position when hovering over the repost button.

        Side effects:
            Sets self.search_x and self.search_y based on confirmed position
        """
        self.print_header()
        print(PURPLE + "Move mouse EXACTLY over the repost button")
        print(PURPLE + "Tracking mouse position...")
        print()

        try:
            import msvcrt
            while True:
                x, y = pyautogui.position()
                print(PURPLE + f"\rCurrent position: X:{x:4d} Y:{y:4d} (Press 'O' to confirm)", end='', flush=True)

                # Check for 'O' key press to confirm position
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
        """
        Background thread that continuously updates the statistics display.

        Runs while self.running is True, updating the console with current
        repost count and elapsed time every 100ms.
        """
        while self.running:
            elapsed = time.time() - self.start_time
            print(PURPLE + f"\rReposts removed: {self.count} | Time: {self.format_time(elapsed)}", end='', flush=True)
            time.sleep(0.1)

    def create_stats_image(self) -> Path:
        """
        Generate a purple stats image with session statistics.

        Creates an 800x400 PNG image with purple background displaying:
        - Total reposts removed
        - Total time elapsed
        - Branding information

        Returns:
            Path: Path to the generated stats image

        Note:
            Image is saved in the same directory as the script with timestamp
        """
        script_dir = Path(__file__).parent
        output_path = script_dir / f"tiktok_stats_{int(time.time())}.png"

        # Create purple background image
        img = Image.new('RGB', (800, 400), color=(138, 43, 226))
        draw = ImageDraw.Draw(img)

        # Load fonts (fallback to default if Arial not available)
        try:
            font_large = ImageFont.truetype("arial.ttf", 48)
            font_medium = ImageFont.truetype("arial.ttf", 32)
            font_small = ImageFont.truetype("arial.ttf", 24)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # Draw header
        draw.text((400, 50), "TikTok Repost Remover", fill='white', anchor='mm', font=font_large)
        draw.text((400, 120), "Stats", fill='white', anchor='mm', font=font_medium)

        # Draw statistics
        elapsed = time.time() - self.start_time
        draw.text((400, 200), f"Reposts Removed: {self.count}", fill='white', anchor='mm', font=font_medium)
        draw.text((400, 260), f"Total Time: {self.format_time(elapsed)}", fill='white', anchor='mm', font=font_medium)

        # Draw footer
        draw.text((400, 350), "made by ravejsreal", fill='white', anchor='mm', font=font_small)

        img.save(output_path)
        return output_path

    def on_q_pressed(self):
        """Callback function for 'q' key press to signal stop request."""
        self.stop_requested = True

    def run(self):
        """
        Main automation loop.

        This method orchestrates the entire automation process:
        1. Captures initial button position from user
        2. Displays 5-second countdown
        3. Starts automation loop that:
           - Clicks repost button (first click uses exact position, subsequent use scanning)
           - Waits configured delay
           - Scrolls down to next repost
           - Repeats until user presses 'q'
        4. Generates and optionally displays stats image

        The automation can be stopped at any time by pressing 'q' from any window.
        """
        # Interactive setup to get button position
        self.set_position()

        # Display configuration
        self.print_header()
        print(PURPLE + f"Search X: {self.search_x}, Y Range: {self.search_y_start}-{self.search_y_end}")
        print(PURPLE + f"Delay: {self.delay} seconds")
        print()
        print(PURPLE + "Starting in 5 seconds... Switch to TikTok window!")
        print()

        # 5-second countdown to allow window switching
        for i in range(5, 0, -1):
            print(PURPLE + f"Starting in {i}...", end='\r', flush=True)
            time.sleep(1)

        print()
        print(PURPLE + "Running... (Press 'q' to stop)")
        print()

        # Register global hotkey for stopping
        keyboard.on_press_key('q', lambda _: self.on_q_pressed())

        # Start automation
        self.running = True
        self.start_time = time.time()

        # Start background stats display thread
        display = threading.Thread(target=self.display_thread, daemon=True)
        display.start()

        try:
            while not self.stop_requested:
                # Click repost button
                if self.first_click:
                    # Use exact user-defined position for first click
                    pyautogui.click(self.search_x, self.search_y)
                    self.count += 1
                    self.first_click = False
                else:
                    # Scan for button position
                    click_x, click_y = self.find_clickable_position()

                    if click_x and click_y:
                        pyautogui.click(click_x, click_y)
                        self.count += 1
                    else:
                        print(PURPLE + "\nButton not found, skipping...")

                # Wait with interruptible delay
                for _ in range(int(self.delay * 10)):
                    if self.stop_requested:
                        break
                    time.sleep(0.1)

                if self.stop_requested:
                    break

                # Scroll to next repost
                pyautogui.press('down')

                # Wait with interruptible delay
                for _ in range(int(self.delay * 10)):
                    if self.stop_requested:
                        break
                    time.sleep(0.1)

        except KeyboardInterrupt:
            pass

        # Cleanup
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
