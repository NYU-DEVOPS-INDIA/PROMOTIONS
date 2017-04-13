from behave import *
import json
import server_promotion as server


@when(u'I visit the "home page"')
def step_impl(context):
    context.resp = context.app.get('/')

@then(u'I should see "{message}"')
def step_impl(context, message):
    assert message in context.resp.data

@then(u'I should not see "{message}"')
def step_impl(context, message):
    assert message not in context.resp.data

@then(u'I should see no content in the response')
def step_impl(context):
    assert context.resp.data is ""

@given(u'the following promotions')
def step_impl(context):
    server.data_reset()
    url = '/promotions'
    for row in context.table:
        promotion = {'name': row['name'], 'kind': row ['kind'], 'description': row['description']}
        context.resp = context.app.post(url, data=json.dumps(promotion), content_type='application/json')

@when(u'I visit the "{url}"')
def step_impl(context, url):
    context.resp = context.app.get(url)
    assert context.resp.status_code == 200

@when(u'I visit the promotion "{url}" with id "{id}"')
def step_impl(context, url, id):
    target_url = url + '/' + id
    context.resp = context.app.get(target_url)
    assert context.resp.status_code == 200

@when(u'I visit the not present promotion "{url}" with id "{id}"')
def step_impl(context, url, id):
    target_url = url + '/' + id
    context.resp = context.app.get(target_url)
    assert context.resp.status_code == 404

@when(u'I visit the active promotions "{url}"')
def step_impl(context, url):
    context.resp = context.app.get(url)
    assert context.resp.status_code == 200

@when(u'I visit the inactive promotions "{url}"')
def step_impl(context, url):
    context.resp = context.app.get(url)
    assert context.resp.status_code == 200

@when(u'I visit the cancel a promotion with id "{url}"')
def step_impl(context, url):
    context.resp = context.app.put(url)
    assert context.resp.status_code == 200 

@when(u'I visit the cancel a not present promotion with id "{url}"')
def step_impl(context, url):
    context.resp = context.app.put(url)
    assert context.resp.status_code == 404 

@when(u'I change "{key}" to "{value}"')
def step_impl(context, key, value):
    data = json.loads(context.resp.data)
    new_data = {}
    new_data['name'] = data['name']
    new_data['kind'] = data['kind']
    new_data['description'] = data['description']
    new_data[key] = value
    context.resp.data = json.dumps(new_data)

@when(u'I update "{url}" with id "{id}"')
def step_impl(context, url, id):
    target_url = url + '/' + id
    context.resp = context.app.put(target_url, data=context.resp.data, content_type='application/json')
    assert context.resp.status_code == 200

@when(u'I update "{url}" with id "{id}" and invalid data')
def step_impl(context, url, id):
    target_url = url + '/' + id
    context.resp = context.app.put(target_url, data=context.resp.data, content_type='application/json')
    assert context.resp.status_code == 400

@when(u'I visit the promotion kind "{url}"')
def step_impl(context, url):
    context.resp = context.app.get(url)
    assert context.resp.status_code == 200

@when(u'I visit the not present promotion kind "{url}"')
def step_impl(context, url):
    context.resp = context.app.get(url)
    assert context.resp.status_code == 404

@when(u'I visit the delete the promotion "{url}" with id "{id}"')
def step_impl(context, url, id):
    target_url = url + '/' + id
    context.resp = context.app.delete(target_url)
    assert context.resp.status_code == 204
    