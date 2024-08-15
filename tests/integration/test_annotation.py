import playwright.sync_api

base_url = "http://localhost:8000"


def test_annotation(page: playwright.sync_api.Page):
    page.goto(base_url)
    page.locator(".md-tooltip >> text=Code annotations should still work").wait_for(state="hidden")
    page.locator("aside").click()
    page.locator(".md-tooltip >> text=Code annotations should still work").wait_for()
