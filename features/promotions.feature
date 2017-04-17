Feature: The Promotions service back-end
    As a Promotions Scheme Owner
    I need a RESTful catalog service
    So that I can keep track of all my promotions

Scenario: The server is running
    When I visit the "home page"
    Then I should see "Promotions REST API"
    Then I should not see "404 Not Found"

Scenario: Create a promotion
    Given I create a promotion called "Buy 1 get 1 free" And I describe it as "Buy an item and get another of the same item for free" And I set the kind to "discount"
    When I visit the "/promotions"
    Then I should see a promotion called "Buy 1 get 1 free" that is a "discount" and has status "Active"

Scenario: Create a promotion with no name
    Given I create a promotion with no name And I describe it as "Buy an item and get another of the same item for free" And I set the kind to "discount"
    When I visit the "/promotions" with no promotions
    Then I should see ""error": "No promotions found""
    Then I should not see a promotion that is a "discount" and has status "Active"


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

Scenario: List inactive promotions
    Given the following promotions
        |  name  |  kind  | description  |
        |  Buy one, get one free  |  sales-promotion1  |  Buy an item having a cost of atleast 20$ to get one free.Cost of the higher price product will be taken into account |
        |  Buy one, get two free  |  sales-promotion3  |  Buy an item having a cost of atleast 40$ to get two free.Cost of the higher price product will be taken into account |
        |  Buy one, get two free  |  sales-promotion3  |  Buy an item having a cost of atleast 60$ to get two free.Cost of the higher price product will be taken into account |

    When I visit the cancel a promotion with id "/promotions/1/cancel"
    Then I should see ""Success": "Cancelled the Promotion with id 1""
    When I visit the inactive promotions "/promotions/status/inactive"
    Then I should see "atleast 20$"   
    Then I should not see "atleast 40$"   
    Then I should not see "atleast 60$"  


Scenario: Retrieve promotion(present) with kind
    Given the following promotions
        |  name  |  kind  | description  |
        |  Buy one, get one free  |  sales-promotion1  |  Buy an item having a cost of atleast 20$ to get one free.Cost of the higher price product will be taken into account |
        |  Buy one, get two free  |  sales-promotion3  |  Buy an item having a cost of atleast 40$ to get two free.Cost of the higher price product will be taken into account |
        |  Buy one, get two free  |  sales-promotion3  |  Buy an item having a cost of atleast 60$ to get two free.Cost of the higher price product will be taken into account |

    When I visit the promotion kind "/promotions/kind/sales-promotion1"
    Then I should see "atleast 20$"
    Then I should not see "atleast 40$"
    Then I should not see "atleast 60$"


Scenario: Retrieve promotion(not present) with kind
    Given the following promotions
        |  name  |  kind  | description  |
        |  Buy one, get one free  |  sales-promotion1  |  Buy an item having a cost of atleast 20$ to get one free.Cost of the higher price product will be taken into account |
        |  Buy one, get two free  |  sales-promotion3  |  Buy an item having a cost of atleast 40$ to get two free.Cost of the higher price product will be taken into account |
        |  Buy one, get two free  |  sales-promotion3  |  Buy an item having a cost of atleast 60$ to get two free.Cost of the higher price product will be taken into account |

    When I visit the not present promotion kind "/promotions/kind/sales-promotion8"
    Then I should see "Promotion with kind: sales-promotion8 was not found"
    Then I should not see "atleast 20$"
    Then I should not see "atleast 40$"
    Then I should not see "atleast 60$"


Scenario: Delete a promotion given the id
    Given the following promotions
        |  name  |  kind  | description  |
        |  Buy one, get one free  |  sales-promotion1  |  Buy an item having a cost of atleast 20$ to get one free.Cost of the higher price product will be taken into account |
        |  Buy one, get two free  |  sales-promotion3  |  Buy an item having a cost of atleast 40$ to get two free.Cost of the higher price product will be taken into account |
        |  Buy one, get two free  |  sales-promotion3  |  Buy an item having a cost of atleast 60$ to get two free.Cost of the higher price product will be taken into account |
    
    When I visit the "/promotions"
    Then I should see "atleast 20$"
    And I should see "atleast 40$"
    And I should see "atleast 60$" 
    When I visit the delete the promotion "/promotions" with id "1"
    Then I should see no content in the response
    When I visit the "/promotions"
    Then I should see "atleast 40$"
    And I should see "atleast 60$"
    And I should not see "atleast 20$"
   
Scenario: Update a promotion (present) given the id
    Given the following promotions
        |  name  |  kind  | description  |
        |  Buy one, get one free  |  sales-promotion1  |  Buy an item having a cost of atleast 20$ to get one free.Cost of the higher price product will be taken into account |
        |  Buy one, get two free  |  sales-promotion3  |  Buy an item having a cost of atleast 40$ to get two free.Cost of the higher price product will be taken into account |
        |  Buy one, get two free  |  sales-promotion3  |  Buy an item having a cost of atleast 60$ to get two free.Cost of the higher price product will be taken into account |

    When I visit the promotion "/promotions" with id "3"
    And I change "kind" to "sales-promotion8"
    And I update "/promotions" with id "3"
    Then I should see "atleast 60$"   

Scenario: Update a promotion (not present) given the id
    Given the following promotions
        |  name  |  kind  | description  |
        |  Buy one, get one free  |  sales-promotion1  |  Buy an item having a cost of atleast 20$ to get one free.Cost of the higher price product will be taken into account |
        |  Buy one, get two free  |  sales-promotion3  |  Buy an item having a cost of atleast 40$ to get two free.Cost of the higher price product will be taken into account |
        |  Buy one, get two free  |  sales-promotion3  |  Buy an item having a cost of atleast 60$ to get two free.Cost of the higher price product will be taken into account |
    
    When I visit the not present promotion "/promotions" with id "4"
    Then I should see "Promotion with id: 4 was not found"
    And I should not see "atleast 20$"
    And I should not see "atleast 40$"
    And I should not see "atleast 60$"

Scenario: Update a promotion (present) given the id and invalid data
    Given the following promotions
        |  name  |  kind  | description  |
        |  Buy one, get one free  |  sales-promotion1  |  Buy an item having a cost of atleast 20$ to get one free.Cost of the higher price product will be taken into account |
        |  Buy one, get two free  |  sales-promotion3  |  Buy an item having a cost of atleast 40$ to get two free.Cost of the higher price product will be taken into account |
        |  Buy one, get two free  |  sales-promotion3  |  Buy an item having a cost of atleast 60$ to get two free.Cost of the higher price product will be taken into account |

    When I visit the promotion "/promotions" with id "3"
    And I change "status" to "inactive"
    And I update "/promotions" with id "3" and invalid data
    Then I should see ""error": "Promotion data was not valid""
