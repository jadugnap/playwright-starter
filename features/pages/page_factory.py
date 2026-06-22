from features.pages.google_flights_page import GoogleFlightsPage
from features.pages.skyscanner_page import SkyscannerPage

class PageFactory:
    @staticmethod
    def get_page(url: str, page, context):
        url_lower = url.lower()
        if "google.com" in url_lower or "google.co" in url_lower:
            return GoogleFlightsPage(page, context)
        elif "skyscanner.com" in url_lower:
            return SkyscannerPage(page, context)
        else:
            # Default to Google Flights Page
            return GoogleFlightsPage(page, context)
