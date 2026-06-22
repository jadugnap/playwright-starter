Feature: Flight Search functionality

  Scenario: Search flights on Online Travel Agency website
    Given I navigate to the travel agency website "https://www.google.com/travel/flights"
    And I select one-way flight option
    When I enter origin "Singapore" and destination "Tokyo"
    And I select departure date "2026-07-20"
    And I click on the search button
    Then I should see search results page loading
