# Test cases can be run with either of the following:
# python -m unittest discover
# nosetests -v --rednose --nologcapture

import unittest
import logging
import json
from flask_api import status    # HTTP Status Codes
import server_promotion as server

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
    
    def test_cancel_promotions_not_present(self):
        resp = self.app.put('/promotions/4/cancel')
        self.assertEqual( resp.status_code, status.HTTP_404_NOT_FOUND )
    
    def test_cancel_promotions_present(self):
        resp = self.app.put('/promotions/3/cancel')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
    
    
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
