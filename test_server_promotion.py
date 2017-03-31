# Test cases can be run with either of the following:
# python -m unittest discover
# nosetests -v --rednose --nologcapture

import unittest
import logging
import json
from flask_api import status    # HTTP Status Codes
import server_promotion

######################################################################
#  T E S T   C A S E S
######################################################################
class TestPromotionServer(unittest.TestCase):

    def setUp(self):
        # Only log criticl errors
        server_promotion.app.debug = True
        server_promotion.app.logger.addHandler(logging.StreamHandler())
        server_promotion.app.logger.setLevel(logging.CRITICAL)
        self.app = server_promotion.app.test_client()

    def tearDown(self):
        pass

    def test_index(self):
        resp = self.app.get('/')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )

    def test_get_promotion_list(self):
        resp = self.app.get('/promotions')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        promo_list = json.loads(resp.data)
        self.assertTrue( len(promo_list) > 0 )

    def test_get_promotion_active_list(self):
        resp = self.app.get('/promotions/status/active')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        active_list = json.loads(resp.data)
        self.assertTrue( len(active_list) > 0 )
        for i, data in enumerate(active_list):
            self.assertEqual( active_list[i]['status'], 'Active' )

    def test_get_promotion_inactive_list(self):
        resp = self.app.get('/promotions/status/inactive')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        inactive_list = json.loads(resp.data)
        self.assertTrue( len(inactive_list) > 0 )
        for i, data in enumerate(inactive_list):
            self.assertEqual( inactive_list[i]['status'], 'Inactive' )

    def test_get_promotion(self):
        resp = self.app.get('/promotions/2')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertTrue(data['id'] == 2)
        self.assertEqual (data['name'], 'Buy one, get two free')

    def test_get_promotion_not_found(self):
        resp = self.app.get('/promotions/99')
        self.assertEqual( resp.status_code, status.HTTP_404_NOT_FOUND )


######################################################################
# Utility functions
######################################################################


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()