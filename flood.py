from playwright.sync_api import sync_playwright
import time

BASE_URL = "https://play.blooket.com/play"
TABS_PER_WINDOW = 6
ACTION_DELAY = 0.2


def run_browser(start_player, num_tabs, game_id, base_name, headless):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            viewport={'width': 800, 'height': 600},
            java_script_enabled=True,
            ignore_https_errors=True
        )

        pages = []
        for _ in range(num_tabs):
            page = context.new_page()
            pages.append(page)

        # Game ID sequence
        for i, page in enumerate(pages):
            try:
                page.goto(BASE_URL, wait_until='networkidle')
                page.fill("input[type='tel']", game_id)
                page.click("button[type='submit']")
                print(f"Tab {i + 1}: ID entered")
            except Exception as e:
                print(f"Tab {i + 1} ID error: {str(e)[:50]}")

        # Nickname sequence
        for i, page in enumerate(pages):
            try:
                page.wait_for_selector("input[type='text'][maxlength='15']")
                page.fill("input[type='text'][maxlength='15']", f"{base_name}{start_player + i}")
                page.click("div[type='submit']")
                print(f"Player {start_player + i} joined")
            except Exception as e:
                print(f"Tab {i + 1} join error: {str(e)[:50]}")

        time.sleep(1)
        browser.close()


def start_game(game_id, total_players, headless, base_name):
    num_windows = -(-total_players // TABS_PER_WINDOW)

    for window in range(num_windows):
        start_player = (window * TABS_PER_WINDOW) + 1
        num_tabs = min(TABS_PER_WINDOW, total_players - (window * TABS_PER_WINDOW))
        print(f"\nBrowser {window + 1}: {num_tabs} tabs")
        run_browser(start_player, num_tabs, game_id, base_name, headless)


if __name__ == "__main__":
    game_id = input("Game ID: ")
    base_name = input("Base name: ")
    total_players = int(input("Players: "))
    headless = input("Headless (y/n): ").lower() == 'y'

    start_game(game_id, total_players, headless, base_name)
