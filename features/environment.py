from behave import *
import server_promotion as server

def before_all(context):
    context.app = server.app.test_client()
    server.inititalize_redis()
    context.server = server
