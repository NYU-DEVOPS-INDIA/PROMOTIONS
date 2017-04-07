# Test cases can be run with either of the following:
# python -m unittest discover
# nosetests -v --rednose --nologcapture

import unittest
import logging
import json
from flask_api import status    # HTTP Status Codes
import server_promotion as server
from promotion import Promotion

######################################################################
#  T E S T   C A S E S
######################################################################
class TestPromotionServer(unittest.TestCase):

    def setUp(self):
        server.app.debug = True
        server.app.logger.addHandler(logging.StreamHandler())
        server.app.logger.setLevel(logging.CRITICAL)

        self.app = server.app.test_client()
        server.inititalize_redis()
        server.data_reset()
        server.data_load({"name": "Buy one, get one free","description": "Buy an item having a cost of atleast 20$ to get one free.Cost of the higher price product will be taken into account", "kind": "sales-promotion1","status": "Active"})
        server.data_load({"name": "Buy one, get two free","description": "Buy an item having a cost of atleast 40$ to get three free.Cost of the higher price product will be taken into account", "kind": "sales-promotion3","status": "Active"})
        server.data_load({"name": "Buy one, get two free","description": "Buy an item having a cost of atleast 60$ to get three free.Cost of the higher price product will be taken into account", "kind": "sales-promotion3","status": "Active"})

    def test_index(self):
        resp = self.app.get('/')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        self.assertTrue ('Promotions REST API' in resp.data)

    def test_get_promotion_list(self):
        resp = self.app.get('/promotions')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertTrue( len(data) > 0 )

    def test_get_promotion(self):
        resp = self.app.get('/promotions/2')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertEqual (data['name'], 'Buy one, get two free')

    def test_get_nonexisting_promotion(self):
        resp = self.app.get('/promotions/5')
        self.assertEqual( resp.status_code, status.HTTP_404_NOT_FOUND )

    def test_get_active_promotion(self):
        resp = self.app.get('/promotions/status/active')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        active_promotions = json.loads(resp.data)
        self.assertTrue( len(active_promotions) > 0 )
        for data in active_promotions:
         self.assertEqual( data['status'], 'Active')

    def test_get_promotion_kind(self):
        resp = self.app.get('/promotions/kind/sales-promotion3')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertTrue(len(data) > 0)
        for abc in data:
         self.assertEqual(abc['name'], 'Buy one, get two free')
         
    def test_query_promotion_kind(self):
        resp = self.app.get('/promotions?kind=sales-promotion1')
        print 'resp data is',resp.data
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertTrue(len(data) > 0)

    def test_get_nonexisting_promotionkind(self):
        resp = self.app.get('/promotions/kind/sales')
        self.assertEqual( resp.status_code, status.HTTP_404_NOT_FOUND )     
    
    def test_cancel_promotions_not_present(self):
        resp = self.app.put('/promotions/4/cancel')
        self.assertEqual( resp.status_code, status.HTTP_404_NOT_FOUND )
    
    def test_cancel_promotions_present(self):
        resp = self.app.put('/promotions/3/cancel')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
 
    def test_update_promotions_not_present(self):
        resp = self.app.put('/promotions/4')
        self.assertEqual( resp.status_code, status.HTTP_404_NOT_FOUND )

    def test_update_promotions_with_no_data(self):
        resp = self.app.put('/promotions/3', data=None, content_type='application/json')
        self.assertEqual( resp.status_code, status.HTTP_400_BAD_REQUEST )

    def test_update_promotions_present_valid_data(self):
        updated_promotion = {"name": "Buy one, get two free","description": "Buy an item having a cost of atleast 90$ to get three free.Cost of the higher price product will be taken into account", "kind": "sales-promotion3"}
        data = json.dumps(updated_promotion)
        resp = self.app.put('/promotions/3', data=data, content_type='application/json')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertTrue("atleast 90$" in data['description'])
        self.assertEqual(data['kind'], 'sales-promotion3')
        self.assertEqual (data['name'], 'Buy one, get two free')

    def test_update_promotions_present_invalid_data(self):
        updated_promotion = {"name": "Buy one, get two free","description": "Buy an item having a cost of atleast 90$ to get three free.Cost of the higher price product will be taken into account", "status": "Active"}
        data = json.dumps(updated_promotion)
        resp = self.app.put('/promotions/3', data=data, content_type='application/json')
        self.assertEqual( resp.status_code, status.HTTP_400_BAD_REQUEST )

    def test_delete_promotion(self):
        # save the current number of promotion for later comparrison
        promotion_count = self.get_promotion_count()
        # delete a promotion
        resp = self.app.delete('/promotions/2', content_type='application/json')
        self.assertEqual( resp.status_code, status.HTTP_204_NO_CONTENT )
        self.assertEqual( len(resp.data), 0 )
        new_count = self.get_promotion_count()
        self.assertEqual( new_count, promotion_count - 1)

        def test_create_promotion(self):
        # save the current number of promotions for later comparrison
        promotion_count = self.get_promotion_count()
        # add a new pet
        new_promotion = {"name": "Buy one, get two free","description": "Buy an item having a cost of atleast 60$ to get three free.Cost of the higher price product will be taken into account", "kind": "sales-promotion3"}
        data = json.dumps(new_promotion)
        resp = self.app.post('/promotions', data=data, content_type='application/json')
        self.assertEqual( resp.status_code, status.HTTP_201_CREATED )
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertTrue( location != None)
        # Check the data is correct
        new_json = json.loads(resp.data)
        self.assertEqual (new_json['name'], 'Buy one, get two free')
        # check that count has gone up and includes sammy
        resp = self.app.get('/promotions')
        # print 'resp_data(2): ' + resp.data
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK )
        self.assertEqual(len(data), promotion_count + 1 )
        self.assertIn(new_json,data)        
    
    def test_create_promotion_with_no_name(self):
        new_promotion = {"description": "Buy an item having a cost of atleast 80$ to get four free.Cost of the higher price product will be taken into account", "kind": "sales-promotion4"}
        data = json.dumps(new_promotion)
        resp = self.app.post('/promotions', data=data, content_type='application/json')
        self.assertEqual( resp.status_code, status.HTTP_400_BAD_REQUEST )

    def test_create_promotion_with_no_kind(self):
        new_promotion = {"name": "Buy one, get two free","description": "Buy an item having a cost of atleast 60$ to get three free.Cost of the higher price product will be taken into account"}
        data = json.dumps(new_promotion)
        resp = self.app.post('/promotions', data=data)
        self.assertEqual( resp.status_code, status.HTTP_400_BAD_REQUEST )


    def test_validate(self):
        lack_arguments_input = {"name": "Buy one, get two free", "kind": "sales-promotion1"}
        self.assertFalse(Promotion.validate(lack_arguments_input))
        incorrect_type_input = {"name": 1, "description" : "empty", "kind": "sales-promotion3"}
        self.assertFalse(Promotion.validate(incorrect_type_input))
        correct_input = {"name": "Buy one, get two free","description": "Buy an item having a cost of atleast 90$ to get three free.Cost of the higher price product will be taken into account", "kind": "sales-promotion3"}
        self.assertTrue(Promotion.validate(correct_input))
    
######################################################################
# Utility functions
######################################################################

    def get_promotion_count(self):
        # save the current number of promotion schemes
        resp = self.app.get('/promotions')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        data = json.loads(resp.data)
        return len(data)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
