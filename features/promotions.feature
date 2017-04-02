Feature: The Promotions service back-end
    As a Promotions Scheme Owner
    I need a RESTful catalog service
    So that I can keep track of all my promotions

Scenario: The server is running
    When I visit the "home page"
    Then I should see "Promotions REST API"
    Then I should not see "404 Not Found"

Scenario: List all promotions
    Given the following promotions
        |  name  |  kind  | description  |
        |  Buy one, get one free  |  sales-promotion1  |  Buy an item having a cost of atleast 20$ to get one free.Cost of the higher price product will be taken into account |
        |  Buy one, get two free  |  sales-promotion3  |  Buy an item having a cost of atleast 40$ to get two free.Cost of the higher price product will be taken into account |
        |  Buy one, get two free  |  sales-promotion3  |  Buy an item having a cost of atleast 60$ to get two free.Cost of the higher price product will be taken into account |

    When I visit the "/promotions"
    Then I should see "atleast 20$"
    Then I should see "atleast 40$"
    Then I should see "atleast 60$"
