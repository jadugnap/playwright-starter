import os
from playwright.sync_api import sync_playwright

def before_all(context):
    # Start Playwright
    context.playwright = sync_playwright().start()
    
    # Configure browser configuration based on environment variables
    headless = os.getenv("PLAYWRIGHT_HEADLESS", "true").lower() == "true"
    browser_type = os.getenv("BROWSER", "chromium").lower()
    
    if browser_type == "firefox":
        context.browser = context.playwright.firefox.launch(headless=headless)
    elif browser_type == "webkit":
        context.browser = context.playwright.webkit.launch(headless=headless)
    else:
        context.browser = context.playwright.chromium.launch(headless=headless)

def before_scenario(context, scenario):
    # Create an isolated browser context and page for each scenario
    context.page_context = context.browser.new_context(
        viewport={"width": 1280, "height": 720}
    )
    context.page = context.page_context.new_page()

def after_scenario(context, scenario):
    # Capture screenshot if a scenario fails
    if scenario.status == "failed" or (hasattr(scenario, "status") and scenario.status.name == "failed"):
        os.makedirs("screenshots", exist_ok=True)
        # Handle status object (behave uses Status enum/object in newer versions)
        scenario_name_clean = "".join(c for c in scenario.name if c.isalnum() or c in (" ", "_", "-")).rstrip()
        scenario_name_clean = scenario_name_clean.replace(" ", "_")
        screenshot_path = f"screenshots/{scenario_name_clean}_failed.png"
        try:
            context.page.screenshot(path=screenshot_path)
            print(f"Scenario failed. Screenshot saved to {screenshot_path}")
        except Exception as e:
            print(f"Failed to capture screenshot: {e}")

    # Clean up page and context
    context.page.close()
    context.page_context.close()

def after_all(context):
    # Clean up browser and Playwright
    context.browser.close()
    context.playwright.stop()
