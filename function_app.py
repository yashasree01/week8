import json
import pymssql
import azure.fuctions as func

app = func.FunctionApp(http_auth_level=func.Authlevel.ANONYMOUS)

@app.route(route="hello")
def hello(req):
  return func.HttpResponse("Hello")
