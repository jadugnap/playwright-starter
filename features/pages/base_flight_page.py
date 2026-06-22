import os
import re
from playwright.sync_api import Page

class BaseFlightPage:
    def __init__(self, page: Page, context=None):
        self.page = page
        self.context = context

    def navigate(self, url: str):
        raise NotImplementedError

    def select_one_way(self):
        raise NotImplementedError

    def enter_origin_and_destination(self, origin: str, destination: str):
        raise NotImplementedError

    def select_departure_date(self, date: str):
        raise NotImplementedError

    def search_flights(self):
        raise NotImplementedError

    def verify_search_results(self):
        raise NotImplementedError

    def filter_by_nonstop(self):
        raise NotImplementedError

    def verify_nonstop_results(self):
        raise NotImplementedError

    def configure_passengers_and_class(self, adults_count: int, cabin_class: str):
        raise NotImplementedError

    def verify_passenger_and_class_config(self, adults_count: int, cabin_class: str):
        raise NotImplementedError

    def take_screenshot(self, default_step_name: str):
        import datetime
        
        feature_name = "unknown_feature"
        scenario_name = "unknown_scenario"
        step_name = default_step_name
        
        if self.context:
            if hasattr(self.context, "feature") and self.context.feature:
                filename = os.path.basename(self.context.feature.filename)
                feature_name = os.path.splitext(filename)[0]
            if hasattr(self.context, "scenario") and self.context.scenario:
                scen_name = self.context.scenario.name
                words = scen_name.split()
                if len(words) > 3:
                    lower_name = scen_name.lower().strip()
                    if "search flights" in lower_name:
                        scenario_name = "search_flights"
                    elif "filter flight results" in lower_name:
                        scenario_name = "filter_flights"
                    elif "change cabin class and passengers" in lower_name:
                        scenario_name = "change_passengers"
                    else:
                        stopwords = {"for", "on", "the", "a", "an", "in", "to", "of", "and", "is", "at"}
                        filtered = [w for w in words if w.lower() not in stopwords]
                        abbreviations = {
                            "documentation": "doc",
                            "development": "dev",
                            "configuration": "config",
                            "environment": "env",
                            "application": "app",
                            "information": "info"
                        }
                        shortened_words = []
                        for w in filtered:
                            w_clean = "".join(c for c in w.lower() if c.isalnum())
                            if w_clean in abbreviations:
                                shortened_words.append(abbreviations[w_clean])
                            elif w_clean:
                                shortened_words.append(w_clean)
                        scenario_name = "_".join(shortened_words[:3])
                else:
                    scenario_name = scen_name
            if hasattr(self.context, "step") and self.context.step:
                step_name = self.context.step.name
                
        def clean_name(s: str) -> str:
            return "".join(c for c in s if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
            
        feature_clean = clean_name(feature_name)
        scenario_clean = clean_name(scenario_name)
        step_clean = clean_name(step_name)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        filename = f"{feature_clean}_{scenario_clean}_{step_clean}_{timestamp}.png"
        
        os.makedirs("artifacts/screenshots", exist_ok=True)
        try:
            self.page.screenshot(path=f"artifacts/screenshots/{filename}", timeout=5000)
        except Exception as e:
            print(f"Skipping step screenshot (page or context may be closed): {e}")
