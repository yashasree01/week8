import azure.functions as func
import pyodbc
import json
import os

app = func.FunctionApp()

# ---- Connection details pulled from environment/App Settings, NOT hardcoded ----
def get_db_connection():
    server = os.environ["SQL_SERVER"]        # e.g. cityuweek8yashasree.database.windows.net
    database = os.environ["SQL_DATABASE"]    # e.g. week8-yashasree
    username = os.environ["SQL_USERNAME"]    # e.g. yashasree-admin
    password = os.environ["SQL_PASSWORD"]

    return pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=" + server + ";"
        "DATABASE=" + database + ";"
        "UID=" + username + ";"
        "PWD=" + password + ";"
        "ENCRYPT=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

@app.route(route="login", methods=["GET"], auth_level=func.AuthLevel.FUNCTION)
def login(req: func.HttpRequest) -> func.HttpResponse:
    req_username = req.params.get("username")
    req_password = req.params.get("password")

    if not req_username or not req_password:
        return func.HttpResponse(
            json.dumps({"message": "Missing username or password"}),
            status_code=400,
            mimetype="application/json"
        )

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (req_username, req_password)
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"message": "Server error", "error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

    if result:
        return func.HttpResponse(
            json.dumps({"message": "Login Successful", "username": req_username}),
            status_code=200,
            mimetype="application/json"
        )
    else:
        return func.HttpResponse(
            json.dumps({"message": "Invalid credentials"}),
            status_code=401,
            mimetype="application/json"
        )
