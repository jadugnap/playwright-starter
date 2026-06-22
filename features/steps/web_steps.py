import re
from behave import given, when, then
from playwright.sync_api import expect

@given('I navigate to the Python home page "{url}"')
def step_navigate_to_url(context, url):
    context.page.goto(url)

@when('I search for "{search_term}" in the search field')
def step_search_for_term(context, search_term):
    search_input = context.page.locator("#id-search-field")
    search_input.fill(search_term)
    context.page.locator("#submit").click()

@then('I should see search results related to "{search_term}"')
def step_verify_results(context, search_term):
    # Verify the results section header is visible
    results_heading = context.page.locator("h3:has-text('Results')")
    expect(results_heading).to_be_visible()
    
    # Verify we are on the search page with the correct query parameters
    expect(context.page).to_have_url(re.compile(rf"https://www\.python\.org/search/\?q={search_term}"))
    
    # Verify the results list is visible
    results_list = context.page.locator("ul.list-recent-events")
    expect(results_list).to_be_visible()

