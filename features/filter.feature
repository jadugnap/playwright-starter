Feature: Flight Search Filtering

  Scenario: Filter flight results by non-stop option
    Given I navigate to the travel agency website "https://www.google.com/travel/flights"
    And I select one-way flight option
    And I enter origin "Singapore" and destination "Tokyo"
    And I select departure date "2026-07-20"
    And I click on the search button
    When I filter the results by non-stop flights
    Then I should see only non-stop flight results on the page
