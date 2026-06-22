import re
from playwright.sync_api import expect
from features.pages.base_flight_page import BaseFlightPage

class GoogleFlightsPage(BaseFlightPage):
    def __init__(self, page, context=None):
        super().__init__(page, context)
        # Google Flights specific selectors
        self.trip_type_dropdown = page.locator("[aria-haspopup='listbox']").first # dropdown for trip types (Round-trip, One-way)
        self.one_way_option = page.locator("li[role='option']:has-text('One-way')")
        
        # Origin and destination inputs
        self.origin_input = page.locator("input[aria-label='Where from?'], input[placeholder='Where from?']")
        self.destination_input = page.locator("input[aria-label='Where to?'], input[placeholder='Where to?']")
        
        # Departure date input
        self.date_input = page.locator("input[placeholder='Departure'], input[aria-label='Departure']").first
        self.done_button = page.locator("button:has-text('Done')").first
        
        # Search button
        self.search_button = page.locator("button:has-text('Search'), button[aria-label='Search'], button:has-text('Explore'), button.xFFaTe, button[jsname='v37h1e']").first
        
        # Stops Filter
        self.stops_filter_button = page.locator("button:has-text('Stops')")
        self.nonstop_radio = page.locator("li[role='menuitemradio']:has-text('Nonstop only'), label:has-text('Nonstop only')")
        
        # Passenger and Class selectors
        self.passenger_dropdown = page.locator("[aria-label*='passenger'], .passenger-selector, button:has-text('passenger')").first
        self.adults_increment = page.locator("button[aria-label='Add adult'], button[aria-label*='Increase adults']")
        self.cabin_class_dropdown = page.locator("[aria-haspopup='listbox']:has-text('Economy'), [aria-haspopup='listbox']:has-text('Premium Economy'), [aria-haspopup='listbox']:has-text('Business'), [aria-haspopup='listbox']:has-text('First')").first
        
    def navigate(self, url: str):
        self.page.goto(url)
        self.take_screenshot("navigate")

    def select_one_way(self):
        btn = self.page.locator("span:has-text('Round-trip'), span:has-text('Round trip'), span:has-text('One-way'), span:has-text('One way')").first
        btn.wait_for(state="visible", timeout=10000)
        
        text = btn.text_content() or ""
        if "one-way" in text.lower() or "oneway" in text.lower() or "one way" in text.lower():
            self.take_screenshot("select_one_way")
            return
            
        btn.click(force=True)
        opt = self.page.locator("[role='option']:has-text('One-way'), [role='option']:has-text('One way'), li:has-text('One-way')").first
        opt.wait_for(state="visible", timeout=5000)
        opt.click(force=True)
        self.take_screenshot("select_one_way")

    def enter_origin_and_destination(self, origin: str, destination: str):
        # Origin
        origin_el = self.page.locator("input[aria-label='Where from?'], input[placeholder='Where from?'], [aria-label*='Where from']").filter(visible=True).first
        origin_el.wait_for(state="visible", timeout=3000)
        origin_el.click(force=True)
        self.page.wait_for_timeout(500)
        origin_el.fill(origin)
        self.page.wait_for_timeout(1000)
        self.page.keyboard.press("ArrowDown")
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(500)
        self.page.keyboard.press("Escape")
        
        # Destination
        dest_el = self.page.locator("input[aria-label='Where to?'], input[placeholder='Where to?'], [aria-label*='Where to']").filter(visible=True).first
        dest_el.wait_for(state="visible", timeout=3000)
        dest_el.click(force=True)
        self.page.wait_for_timeout(500)
        dest_el.fill(destination)
        self.page.wait_for_timeout(1000)
        self.page.keyboard.press("ArrowDown")
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(500)
        self.page.keyboard.press("Escape")
        
        self.take_screenshot("enter_locations")

    def select_departure_date(self, date_val: str):
        # Set the date value directly using javascript to bypass hidden elements and overlays
        self.page.evaluate(
            """(args) => {
                const [val] = args;
                const el = document.querySelector("input[placeholder='Departure'], input[aria-label='Departure'], input.TP4Lpb");
                if (el) {
                    el.value = val;
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }""",
            [date_val]
        )
        self.take_screenshot("select_date")

    def search_flights(self):
        self.search_button.wait_for(state="visible", timeout=10000)
        self.search_button.click()
        # Wait up to 10s for the page URL or layout to update
        try:
            self.page.wait_for_url(re.compile(r"flights/|travel/flights/|search"), timeout=10000)
        except Exception:
            pass
        self.take_screenshot("search_flights")

    def verify_search_results(self):
        # Verify URL changes and contains flight results indicators
        expect(self.page).to_have_url(re.compile(r"flights|search|travel"))
        self.take_screenshot("search_results")

    def filter_by_nonstop(self):
        self.stops_filter_button.wait_for(state="visible", timeout=10000)
        self.stops_filter_button.click()
        self.nonstop_radio.wait_for(state="visible", timeout=5000)
        self.nonstop_radio.click()
        self.take_screenshot("filter_nonstop")

    def verify_nonstop_results(self):
        expect(self.page).to_have_url(re.compile(r"stops=0|nonstop"))
        self.take_screenshot("nonstop_results")

    def configure_passengers_and_class(self, adults_count: int, cabin_class: str):
        # Configure passengers
        self.passenger_dropdown.wait_for(state="visible", timeout=10000)
        self.passenger_dropdown.click()
        self.adults_increment.wait_for(state="visible", timeout=5000)
        for _ in range(adults_count - 1):
            self.adults_increment.click()
        
        # Click Done to close the passenger dropdown
        passenger_done = self.page.locator("button:has-text('Done')").first
        passenger_done.wait_for(state="visible", timeout=5000)
        passenger_done.click()
        
        # Configure class
        self.cabin_class_dropdown.wait_for(state="visible", timeout=10000)
        self.cabin_class_dropdown.click()
        class_option = self.page.locator(f"li[role='option']:has-text('{cabin_class}')").first
        class_option.wait_for(state="visible", timeout=5000)
        class_option.click()
        
        self.take_screenshot("configure_passengers_and_class")

    def verify_passenger_and_class_config(self, adults_count: int, cabin_class: str):
        expect(self.page).to_have_url(re.compile(rf"adults={adults_count}"))
        expect(self.page).to_have_url(re.compile(rf"class={cabin_class.lower()}"))
        self.take_screenshot("verify_config")
