# Copyright 2016 John Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class Promotion(object):

    def __init__(self, id, name, description, kind, status):
        self.id = id
        self.name = name
        self.description = description
        self.kind = kind
        self.status=status


    def save(self, redis):
        if self.id == 0:
            self.id = self.__next_index(redis)
        redis.hmset(self.id, self.serialize())

    def delete(self, redis):
        redis.delete(self.id)

    def __next_index(self, redis):
        redis.incr('index')
        index = redis.get('index')
        return index

    def serialize(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        # id is optional because it's a database key
        id = 0
        if data.has_key('id'):
            id = data['id']
        return Promotion(id, data['name'], data['description'], data['kind'], data['status'])

    @staticmethod
    def validate(data):
        valid = False
        try:
            name = data['name']
            kind = data['kind']
            description=data['description']
            valid = True
        except KeyError:
            valid = False
        except TypeError:
            valid = False
        return valid

    @staticmethod
    def all(redis):
        # results = [Pet.from_dict(redis.hgetall(key)) for key in redis.keys() if key != 'index']
        results = []
        for key in redis.keys():
            if key != 'index':  # filer out our id index
                data = redis.hgetall(key)
                results.append(Promotion.from_dict(data))
        return results

    @staticmethod
    def find(redis, id):
        if redis.exists(id):
            data = redis.hgetall(id)
            return Promotion.from_dict(data)
        else:
            return None

    @staticmethod
    def find_by_kind(redis, kind):
        results = []
        for key in redis.keys():
            if key != 'index':  # filer out our id index
                data = redis.hgetall(key)
                if data['kind'].upper() == kind:
                    results.append(Promotion.from_dict(data))
        return results

    @staticmethod
    def find_by_status(redis, status):
        results = []
        for key in redis.keys():
            if key != 'index':  # filer out our id index
                data = redis.hgetall(key)
                if data['status'].upper() == status:
                    results.append(Promotion.from_dict(data))
        return results
    @staticmethod
    def cancel_by_id(redis,id):
        if redis.exists(id):
            data = redis.hgetall(id)
            print 'data is', data
            data['status'] ='Inactive'
            print 'data now is', data
            return Promotion.from_dict(data)
        else:
            return None   