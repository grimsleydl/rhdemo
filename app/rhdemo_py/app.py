#!/usr/bin/env python3
from flask import Flask, render_template, request
import pymysql
import socket
import os

app = Flask(__name__)

listen_address = os.getenv("APP_LISTEN", "0.0.0.0")
db_address = os.getenv("DB_LISTEN", "192.168.160.200")
db_pass = os.getenv("FLASK_DB_PASS")


config = {
    "host": db_address,
    "port": 3306,
    "user": "flask",
    "password": db_pass,
    "database": "rhdemo",
}


@app.route("/", methods=["GET"])
def hello():
    return "Hello, yes this is Flask"


@app.route("/index")
def index():
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    cur.execute("SELECT * FROM testtable")
    return render_template("index.html", data=cur.fetchall())


@app.route("/hostname")
def return_hostname():
    return "example flask app served from {} (fqdn: {}, ip: {}) to {} (xff {})<br>".format(
        socket.gethostname(),
        socket.getfqdn(),
        listen_address,
        request.remote_addr,
        *request.access_route
    )


def main():
    app.run(host=listen_address, port=5000)


if __name__ == "__main__":
    main()
