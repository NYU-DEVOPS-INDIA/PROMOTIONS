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

Scenario: Retrieve promotion(present) with id
    Given the following promotions
        |  name  |  kind  | description  |
        |  Buy one, get one free  |  sales-promotion1  |  Buy an item having a cost of atleast 20$ to get one free.Cost of the higher price product will be taken into account |
        |  Buy one, get two free  |  sales-promotion3  |  Buy an item having a cost of atleast 40$ to get two free.Cost of the higher price product will be taken into account |
        |  Buy one, get two free  |  sales-promotion3  |  Buy an item having a cost of atleast 60$ to get two free.Cost of the higher price product will be taken into account |

    When I visit the promotion "/promotions" with id "1"
    Then I should see "atleast 20$"
    Then I should not see "atleast 40$"
    Then I should not see "atleast 60$"

Scenario: Retrieve promotion(not present) with id
    Given the following promotions
        |  name  |  kind  | description  |
        |  Buy one, get one free  |  sales-promotion1  |  Buy an item having a cost of atleast 20$ to get one free.Cost of the higher price product will be taken into account |
        |  Buy one, get two free  |  sales-promotion3  |  Buy an item having a cost of atleast 40$ to get two free.Cost of the higher price product will be taken into account |
        |  Buy one, get two free  |  sales-promotion3  |  Buy an item having a cost of atleast 60$ to get two free.Cost of the higher price product will be taken into account |

    When I visit the not present promotion "/promotions" with id "4"
    Then I should see "Promotion with id: 4 was not found"
    Then I should not see "atleast 20$"
    Then I should not see "atleast 40$"
    Then I should not see "atleast 60$"

Scenario: List active promotions
    Given the following promotions
        |  name  |  kind  | description  |
        |  Buy one, get one free  |  sales-promotion1  |  Buy an item having a cost of atleast 20$ to get one free.Cost of the higher price product will be taken into account |
        |  Buy one, get two free  |  sales-promotion3  |  Buy an item having a cost of atleast 40$ to get two free.Cost of the higher price product will be taken into account |
        |  Buy one, get two free  |  sales-promotion3  |  Buy an item having a cost of atleast 60$ to get two free.Cost of the higher price product will be taken into account |

    When I visit the active promotions "/promotions/status/active"
    Then I should see "atleast 20$"
    Then I should see "atleast 40$"
    Then I should see "atleast 60$"

Scenario: Cancel a promotion given the id
    Given the following promotions
        |  name  |  kind  | description  |
        |  Buy one, get one free  |  sales-promotion1  |  Buy an item having a cost of atleast 20$ to get one free.Cost of the higher price product will be taken into account |
        |  Buy one, get two free  |  sales-promotion3  |  Buy an item having a cost of atleast 40$ to get two free.Cost of the higher price product will be taken into account |
        |  Buy one, get two free  |  sales-promotion3  |  Buy an item having a cost of atleast 60$ to get two free.Cost of the higher price product will be taken into account |

    When I visit the cancel a promotion with id "/promotions/1/cancel"
    Then I should see ""Success": "Cancelled the Promotion with id 1""
    When I visit the cancel a not present promotion with id "/promotions/4/cancel"
    Then I should see ""error": "Promotion 4 was not found""