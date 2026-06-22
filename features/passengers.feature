Feature: Passenger and Class Configuration

  Scenario: Change cabin class and passengers for flight search
    Given I navigate to the travel agency website "https://www.google.com/travel/flights"
    And I select one-way flight option
    And I configure passenger details to "2" Adults and cabin class to "Business"
    And I enter origin "Singapore" and destination "Tokyo"
    And I select departure date "2026-07-20"
    When I click on the search button
    Then the search results page should show flights matching "2" Adults and "Business" class
