# Copyright 2016, 2017 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging
from threading import Lock
from flask import Flask, Response, jsonify, request, make_response, json, url_for

# Create Flask application
app = Flask(__name__)
app.config['LOGGING_LEVEL'] = logging.INFO

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409

# Lock for thread-safe counter increment
lock = Lock()

# dummy data for testing
current_promotion_id = 2
promotions = [
    {
        'id': 0,
        'name': "Buy one, get one free",
        'description': 'Buy an item having a cost of atleast 30$ to get one free.Cost of the higher price product will be taken into account',
        'kind':'sales-promotion1'
    },
    {
        'id': 1,
        'name': "Buy one, get two free",
        'description': 'Buy an item having a cost of atleast 50$ to get two free.Cost of the highest price product will be taken into account',
        'kind':'sales-promotion2'
    },
    {
        'id': 2,
        'name': "Buy one, get two free",
        'description': 'Buy an item having a cost of atleast 50$ to get two free.Cost of the highest price product will be taken into account',
        'kind':'sales-promotion1'
    }
]

######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    promotion_url = request.base_url + "promotions"
    return make_response(jsonify(name='Promotion REST API Service',version='1.0',url=promotion_url), HTTP_200_OK)

######################################################################
# LIST ALL PROMOTIONS
######################################################################
@app.route('/promotions', methods=['GET'])
def list_promotions():
    results = []
    #kind = request.args.get('kind')
    if bool(promotions):
        results = [promotion for promotion in enumerate(promotions)]
        
    return make_response(jsonify(results), HTTP_200_OK)

######################################################################
# RETRIEVE A PROMOTION
######################################################################
@app.route('/promotions/<int:id>', methods=['GET'])
def get_promotions(id):
    index = [i for i, promotion in enumerate(promotions) if promotion['id'] == id]
    if len(index) > 0:
        message = promotions[index[0]]
        rc = HTTP_200_OK
    else:
        message = { 'error' : 'promotion with id: %s was not found' % str(id) }
        rc = HTTP_404_NOT_FOUND

    return make_response(jsonify(message), rc)

######################################################################
# RETRIEVE ALL PROMOTIONS BASED ON KIND
######################################################################
@app.route('/promotions/<kind>', methods=['GET'])
def get_promotions_kind(kind):
    results=[]
    for i,entry in enumerate(promotions):
      if entry['kind']==kind:
        print entry
        results.append(entry)
    rc = HTTP_200_OK
    if results == []:
     results = { 'error' : 'promotion with kind: %s was not found' % str(kind) }
     rc = HTTP_404_NOT_FOUND         
    return make_response(json.dumps(results), rc)






######################################################################
# ADD A NEW PROMOTION
######################################################################
@app.route('/promotions', methods=['POST'])
def create_promotions():
    payload = request.get_json()
    if is_valid(payload):
        id = next_index()
        promotion = {'id': id, 'name': payload['name'], 'description':payload['description'], 'kind': payload['kind']}
        promotions.append(promotion)
        message = promotion
        rc = HTTP_201_CREATED
    else:
        message = { 'error' : 'Data is not valid' }
        rc = HTTP_400_BAD_REQUEST

    response = make_response(jsonify(message), rc)
    if rc == HTTP_201_CREATED:
        response.headers['Location'] = url_for('get_promotions', id=id)
    return response

######################################################################
# UPDATE AN EXISTING PROMOTION
######################################################################
@app.route('/promotions/<int:id>', methods=['PUT'])
def update_promotions(id):
    index = [i for i, promotion in enumerate(promotions) if promotion['id'] == id]
    if len(index) > 0:
        payload = request.get_json()
        if is_valid(payload):
            promotions[index[0]] = {'id': id, 'name': payload['name'],'description':payload['description'], 'kind': payload['kind']}
            message = promotions[index[0]]
            rc = HTTP_200_OK
        else:
            message = { 'error' : 'Promotion data was not valid' }
            rc = HTTP_400_BAD_REQUEST
    else:
        message = { 'error' : 'Promotion %s was not found' % id }
        rc = HTTP_404_NOT_FOUND

    return make_response(jsonify(message), rc)

######################################################################
# DELETE A PROMOTION
######################################################################
#@app.route('/promotions/<int:id>', methods=['DELETE'])
#def delete_promotions(id):
#    index = [i for i, promotion in enumerate(promotions) if promotion['id'] == id]
#    if len(index) > 0:
#        del promotions[index[0]]
#    return make_response('', HTTP_204_NO_CONTENT)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def next_index():
    global current_promotion_id
    with lock:
        current_promotion_id += 1
    return current_promotion_id

def is_valid(data):
    valid = False
    try:
        name = data['name']
        kind = data['kind']
        description=data['description']
        valid = True
    except KeyError as err:
        app.logger.warn('Missing parameter error: %s', err)
    except TypeError as err:
        app.logger.warn('Invalid Content Type error: %s', err)

    return valid

@app.before_first_request
def setup_logging():
    if not app.debug:
        # In production mode, add log handler to sys.stderr.
        handler = logging.StreamHandler()
        handler.setLevel(app.config['LOGGING_LEVEL'])
        # formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
        #'%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter('[%(asctime)s] - %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)

######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    # Pull options from environment
    debug = (os.getenv('DEBUG', 'False') == 'True')
    port = os.getenv('PORT', '5000')
    app.run(host='192.168.33.10', port=int(port), debug=debug)
