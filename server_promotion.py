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
from flask import Flask, Response, jsonify, request, make_response, json, url_for, render_template
from flask_api import status    # HTTP Status Codes
from flasgger import Swagger
from redis import Redis
from redis.exceptions import ConnectionError
from promotion import Promotion

# Create Flask application
app = Flask(__name__)
app.config['LOGGING_LEVEL'] = logging.INFO

# Configure Swagger before initilaizing it
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "specs": [
        {
            "version": "1.0.0",
            "title": "DevOps Swagger Promotion App",
            "description": "This is a Promotion server.",
            "endpoint": 'v1_spec',
            "route": '/v1/spec'
        }
    ]
}

# Initialize Swagger after configuring it
Swagger(app)

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409

######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    return render_template('index.html')
    #promotion_url = request.base_url + "promotions"
    #return make_response(jsonify(name='Promotion REST API Service',version='1.0',url=promotion_url), HTTP_200_OK)

######################################################################
# LIST ALL PROMOTIONS
######################################################################
@app.route('/promotions', methods=['GET'])
def list_promotions():
    """
    Retrieve a list of all Promotions
    This endpoint will return all Promotions unless a query parameter on id or kind is specificed
    ---
    tags:
      - Promotions
    description: The Promotions endpoint allows you to query Promotion schemes
    parameters:
      - name: kind
        in: query
        description: the kind of Promotion scheme you are looking for
        required: false
        type: string
    responses:
      200:
        description: An array of Promotion schemes
        schema:
          type: array
          items:
            schema:
              id: Promotion
              properties:
                id:
                  type: integer
                  description: unique id assigned internally by service
                name:
                  type: string
                  description: the promotion scheme's name
                kind:
                  type: string
                  description: the kind of Promotion scheme (sales-promotion1, sale-senior-promotion, black-friday-promotion etc.)
                description:
                  type: string
                  description: the complete detail of the Promotion scheme and the criteria for the promotion.
                status:
                  type: string
                  description: the status of promotion scheme whether it is currently "Active" or "Inactive" 
      400:
        description: No promotion schemes found.             
    """
    results = []
    
    kind = request.args.get('kind')
    if kind:
        result = Promotion.find_by_kind(redis, kind)
    else:
        result = Promotion.all(redis)
    if len(result) > 0:
       results = [Promotion.serialize(promotion) for promotion in result]
       return make_response(jsonify(results), HTTP_200_OK)
    else:
       results = { 'error' : 'No promotions found'  }
       rc = HTTP_404_NOT_FOUND
       return make_response(jsonify(results), rc)

######################################################################
# LIST ALL ACTIVE PROMOTIONS
######################################################################
@app.route('/promotions/status/active', methods=['GET'])
def list_all_active_promotions():
    results = Promotion.find_by_status(redis, 'ACTIVE')
    if len(results) > 0:
        result = [Promotion.serialize(promotion) for promotion in results]
        rc = HTTP_200_OK
    else:
        result = { 'error' : 'No active promotions found'  }
        rc = HTTP_404_NOT_FOUND

    return make_response(jsonify(result), rc)

######################################################################
# RETRIEVE A PROMOTION
######################################################################
@app.route('/promotions/<int:id>', methods=['GET'])
def get_promotions(id):
    """
    Retrieve a single Promotion
    This endpoint will return a Promotion based on it's id
    ---
    tags:
      - Promotions
    produces:
      - application/json
    parameters:
      - name: id
        in: path
        description: ID of promotion to retrieve
        type: integer
        required: true
    responses:
      200:
        description: Promotion returned
        schema:
          id: Promotion
          properties:
            id:
              type: integer
              description: unique id assigned internally by service
            name:
              type: string
              description: name for the Promotion scheme
            kind:
              type: string
              description: the kind of Promotion scheme (sales-promotion1, sale-senior-promotion, black-friday-promotion etc.)
            description:
              type: string
              description: the complete detail of the Promotion scheme and the criteria for the promotion.
            status:
              type: string
              description: the status of promotion scheme whether it is currently "Active" or "Inactive"   
      404:
        description: Promotion not found
    """
    promotion = Promotion.find(redis, id)
    if promotion:
        message = promotion.serialize()
        rc = HTTP_200_OK
    else:
        message = { 'error' : 'Promotion with id: %s was not found' % str(id) }
        rc = HTTP_404_NOT_FOUND

    return make_response(jsonify(message), rc)

######################################################################
# RETRIEVE ALL PROMOTIONS BASED ON KIND
######################################################################
@app.route('/promotions/kind/<kind>', methods=['GET'])
def get_promotions_kind(kind):
 """
    Retrieve all promotions for one kind
    This endpoint will return a Promotion based on it's kind
    ---
    tags:
      - Promotions
    produces:
      - application/json
    parameters:
      - name: kind
        in: path
        description: the kind of Promotion scheme you are looking for
        type: string
        required: true
    responses:
      200:
        description: Promotion returned
        schema:
          id: Promotion
          properties:
            id:
              type: integer
              description: unique id assigned internally by service
            name:
              type: string
              description: name for the Promotion scheme
            kind:
              type: string
              description: the kind of Promotion scheme (sales-promotion1, sale-senior-promotion, black-friday-promotion etc.)
            description:
              type: string
              description: the complete detail of the Promotion scheme and the criteria for the promotion.
            status:
              type: string
              description: the status of promotion scheme whether it is currently "Active" or "Inactive"   
      404:
        description: Promotion not found
    """

    results = Promotion.find_by_kind(redis, kind.upper())
    if len(results) > 0:
        result = [Promotion.serialize(promotion) for promotion in results]
        rc = HTTP_200_OK
    else:
        result = { 'error' : 'Promotion with kind: %s was not found' % str(kind)  }
        rc = HTTP_404_NOT_FOUND

    return make_response(jsonify(result), rc)

######################################################################
# ACTION TO CANCEL THE PROMOTION
######################################################################
@app.route('/promotions/<int:id>/cancel', methods=['PUT'])
def cancel_promotions(id):
    """
    Cancel a single Promotion
    This endpoint will set the status of promotion as Inactive on success or return an error message if promotion is not found.
    ---
    tags:
      - Promotions
    parameters:
      - name: id
        in: path
        description: ID of promotion to cancel
        type: integer
        required: true
    responses:
      200:
        description: success message, 'Cancelled the promotion with given id'
      404:
        description: error message, 'Promotion with given id was not found'
    """
    promotion = Promotion.find(redis, id)
    if promotion:
        promotion = Promotion.cancel_by_id(redis,id)
        promotion.save(redis)
        message = {'Success' : 'Cancelled the Promotion with id ' + str(id)}
        rc = HTTP_200_OK
    else:
        message = { 'error' : 'Promotion %s was not found' % id }
        rc = HTTP_404_NOT_FOUND

    return make_response(jsonify(message), rc)

######################################################################
# ADD A NEW PROMOTION
######################################################################
@app.route('/promotions', methods=['POST'])
def create_promotions():
    """
    Creates a Promotion
    This endpoint will create a Promotion scheme based the data in the body that is posted
    ---
    tags:
      - Promotions
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: data
          required:
            - name
            - kind
            - description
          properties:
            name:
              type: string
              description: name for the Promotion scheme
            kind:
              type: string
              description: the kind of Promotion scheme (sales-promotion1, sale-senior-promotion, black-friday-promotion etc.)
            description:
              type: string
              description: the complete detail of the Promotion scheme and the criteria for the promotion.    
    responses:
      201:
        description: Promotion created
        schema:
          id: Promotion
          properties:
            id:
              type: integer
              description: unique id assigned internally by service
            name:
              type: string
              description: name for the Promotion scheme
            kind:
              type: string
              description: the kind of Promotion scheme (sales-promotion1, sale-senior-promotion, black-friday-promotion etc.)
            description:
              type: string
              description: the complete detail of the Promotion scheme and the criteria for the promotion.
            status:
              type: string
              description: the status of promotion scheme with the value "Active"    

      400:
        description: Bad Request (the posted data was not valid)
    """    
    id = 0
    payload = request.get_json()
    print payload
    if Promotion.validate(payload):
        promotion = Promotion(id, payload['name'], payload['description'], payload['kind'], 'Active')
        promotion.save(redis)
        id = promotion.id
        message = promotion.serialize()
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
# Can only update name/description/kind
@app.route('/promotions/<int:id>', methods=['PUT'])
def update_promotions(id):
    """
    Update a Promotion
    This endpoint will update a Promotion based the body that is posted
    ---
    tags:
      - Promotions
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - name: id
        in: path
        description: ID of promotion to retrieve
        type: integer
        required: true
      - in: body
        name: body
        schema:
          id: data
          required:
            - name
            - kind
            - description
          properties:
            name:
              type: string
              description: name for the Promotion scheme
            kind:
              type: string
              description: the kind of Promotion scheme (sales-promotion1, sale-senior-promotion, black-friday-promotion etc.)
            description:
              type: string
              description: the complete detail of the Promotion scheme and the criteria for the promotion. 
    responses:
      200:
        description: Promotion Updated
        schema:
          id: Promotion
          properties:
            id:
              type: integer
              description: unique id assigned internally by service
            name:
              type: string
              description: name for the Promotion scheme
            kind:
              type: string
              description: the kind of Promotion scheme (sales-promotion1, sale-senior-promotion, black-friday-promotion etc.)
            description:
              type: string
              description: the complete detail of the Promotion scheme and the criteria for the promotion.
            status:
              type: string
              description: the status of promotion scheme whether it is currently "Active" or "Inactive"   
      400:
        description: Bad Request (the posted data was not valid)
    """
    promotion = Promotion.find(redis, id)
    if promotion:
        payload = request.get_json()
        print 'payload is',payload
        if Promotion.validate(payload):
            promotion = Promotion(id, payload['name'], payload['description'], payload['kind'], promotion.status)
            promotion.save(redis)
            message = promotion.serialize()
            rc = HTTP_200_OK
        else:
            message = { 'error' : 'Promotion data was not valid' }
            rc = HTTP_400_BAD_REQUEST
    else:
        message = { 'error' : 'Promotion %s was not found' % id }
        rc = HTTP_404_NOT_FOUND
    return make_response(jsonify(message), rc)

######################################################################
# LIST ALL INACTIVE PROMOTIONS
######################################################################
@app.route('/promotions/status/inactive', methods=['GET'])
def list_all_inactive_promotions():
    results = Promotion.find_by_status(redis, 'INACTIVE')
    if len(results) > 0:
        result = [Promotion.serialize(promotion) for promotion in results]
        rc = HTTP_200_OK
    else:
        result = { 'error' : 'No inactive promotions found'  }
        rc = HTTP_404_NOT_FOUND
    return make_response(jsonify(result), rc)

######################################################################
# DELETE A PROMOTION
######################################################################
@app.route('/promotions/<int:id>', methods=['DELETE'])
def delete_promotions(id):
    """
    Delete a single Promotion
    This endpoint will return an empty response and delete the promotion in database
    ---
    tags:
      - Promotions
    parameters:
      - name: id
        in: path
        description: ID of promotion to delete
        type: integer
        required: true
    responses:
      204:
        description: no content
    """
    promotion = Promotion.find(redis, id)
    if promotion:
       promotion.delete(redis)
    return make_response('', HTTP_204_NO_CONTENT)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def data_load(payload):
    promotion = Promotion(0, payload['name'], payload['description'], payload['kind'],payload['status'])
    promotion.save(redis)

def data_reset():
    redis.flushall()

######################################################################
# Connect to Redis and catch connection exceptions
######################################################################
def connect_to_redis(hostname, port, password):
    redis = Redis(host=hostname, port=port, password=password)
    try:
        redis.ping()
    except ConnectionError:
        redis = None
    return redis


######################################################################
# INITIALIZE Redis
# This method will work in the following conditions:
#   1) In Bluemix with Redis bound through VCAP_SERVICES
#   2) With Redis running on the local server as with Travis CI
#   3) With Redis --link ed in a Docker container called 'redis'
######################################################################
def inititalize_redis():
    global redis
    redis = None
    # Get the crdentials from the Bluemix environment
    if 'VCAP_SERVICES' in os.environ:
        app.logger.info("Using VCAP_SERVICES...")
        VCAP_SERVICES = os.environ['VCAP_SERVICES']
        services = json.loads(VCAP_SERVICES)
        creds = services['rediscloud'][0]['credentials']
        app.logger.info("Conecting to Redis on host %s port %s" % (creds['hostname'], creds['port']))
        redis = connect_to_redis(creds['hostname'], creds['port'], creds['password'])
    else:
        app.logger.info("VCAP_SERVICES not found, checking localhost for Redis")
        redis = connect_to_redis('127.0.0.1', 6379, None)
        if not redis:
            app.logger.info("No Redis on localhost, using: redis")
            redis = connect_to_redis('redis', 6379, None)
    if not redis:
        # if you end up here, redis instance is down.
        app.logger.error('*** FATAL ERROR: Could not connect to the Redis Service')
        exit(1) 

debug = (os.getenv('DEBUG', 'False') == 'True')
inititalize_redis()
port = os.getenv('PORT', '5000')
######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    # Pull options from environment
    app.run(host='0.0.0.0', port=int(port), debug=debug)
