import re
from playwright.sync_api import expect
from features.pages.base_flight_page import BaseFlightPage

class SkyscannerPage(BaseFlightPage):
    def __init__(self, page, context=None):
        super().__init__(page, context)
        # Skyscanner selectors
        self.one_way_radio = page.locator("input[type='radio'][value='one-way'], #one-way-trip, label:has-text('One-way')")
        self.origin_input = page.locator("input[placeholder*='From'], input[placeholder*='Origin'], #origin-input")
        self.destination_input = page.locator("input[placeholder*='To'], input[placeholder*='Destination'], #destination-input")
        self.date_input = page.locator("input[placeholder*='Depart'], input[placeholder*='Date'], #departure-date")
        self.search_button = page.locator("button[type='submit'], .search-button, button:has-text('Search flights')")
        self.nonstop_filter = page.locator("input[type='checkbox'][value='direct'], label:has-text('Direct only'), label:has-text('Non-stop')")
        self.passenger_dropdown = page.locator(".passenger-selector, button:has-text('passenger'), button:has-text('Adult')")
        self.adult_increase_button = page.locator(".adults-control .increase, button[aria-label='Increase number of adults']")
        self.cabin_class_select = page.locator("select.cabin-class, .cabin-class-selector")

    def navigate(self, url: str):
        self.page.goto(url)
        self.take_screenshot("navigate")

    def select_one_way(self):
        if self.one_way_radio.is_visible():
            self.one_way_radio.first.click()
        self.take_screenshot("select_one_way")

    def enter_origin_and_destination(self, origin: str, destination: str):
        self.origin_input.fill(origin)
        self.origin_input.press("Tab")
        self.destination_input.fill(destination)
        self.destination_input.press("Tab")
        self.take_screenshot("enter_locations")

    def select_departure_date(self, date_val: str):
        self.date_input.fill(date_val)
        self.date_input.press("Enter")
        self.take_screenshot("select_date")

    def search_flights(self):
        self.search_button.click()
        self.take_screenshot("search_flights")

    def verify_search_results(self):
        expect(self.page).to_have_url(re.compile(r"search|results|flights"))
        self.take_screenshot("search_results")

    def filter_by_nonstop(self):
        self.nonstop_filter.first.check()
        self.take_screenshot("filter_nonstop")

    def verify_nonstop_results(self):
        expect(self.page).to_have_url(re.compile(r"direct=true|stops=0|non-stop"))
        self.take_screenshot("nonstop_results")

    def configure_passengers_and_class(self, adults_count: int, cabin_class: str):
        self.passenger_dropdown.click()
        for _ in range(adults_count - 1):
            if self.adult_increase_button.is_visible():
                self.adult_increase_button.click()
        if self.cabin_class_select.is_visible():
            self.cabin_class_select.select_option(label=cabin_class)
        self.take_screenshot("configure_passengers_and_class")

    def verify_passenger_and_class_config(self, adults_count: int, cabin_class: str):
        expect(self.page).to_have_url(re.compile(rf"adults={adults_count}"))
        expect(self.page).to_have_url(re.compile(rf"class={cabin_class.lower()}"))
        self.take_screenshot("verify_config")
