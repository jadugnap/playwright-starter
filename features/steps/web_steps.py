from behave import given, when, then
from features.pages.page_factory import PageFactory

@given('I navigate to the travel agency website "{url}"')
def step_navigate_to_travel_agency(context, url):
    context.ota_page = PageFactory.get_page(url, context.page, context)
    context.ota_page.navigate(url)

@given('I select one-way flight option')
def step_select_one_way(context):
    context.ota_page.select_one_way()

@when('I enter origin "{origin}" and destination "{destination}"')
@given('I enter origin "{origin}" and destination "{destination}"')
def step_enter_locations(context, origin, destination):
    context.ota_page.enter_origin_and_destination(origin, destination)

@when('I select departure date "{date}"')
@given('I select departure date "{date}"')
def step_select_date(context, date):
    context.ota_page.select_departure_date(date)

@when('I click on the search button')
@given('I click on the search button')
def step_click_search(context):
    context.ota_page.search_flights()

@then('I should see search results page loading')
def step_verify_results_page(context):
    context.ota_page.verify_search_results()

@when('I filter the results by non-stop flights')
def step_filter_nonstop(context):
    context.ota_page.filter_by_nonstop()

@then('I should see only non-stop flight results on the page')
def step_verify_nonstop_results(context):
    context.ota_page.verify_nonstop_results()

@given('I configure passenger details to "{adults}" Adults and cabin class to "{cabin_class}"')
def step_configure_passengers(context, adults, cabin_class):
    context.ota_page.configure_passengers_and_class(int(adults), cabin_class)

@then('the search results page should show flights matching "{adults}" Adults and "{cabin_class}" class')
def step_verify_passenger_and_class(context, adults, cabin_class):
    context.ota_page.verify_passenger_and_class_config(int(adults), cabin_class)
