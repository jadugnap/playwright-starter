Feature: Python.org Website Search

  Scenario: Search for documentation on Python.org
    Given I navigate to the Python home page "https://www.python.org/"
    When I search for "pep" in the search field
    Then I should see search results related to "pep"
