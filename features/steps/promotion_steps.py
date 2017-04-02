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
