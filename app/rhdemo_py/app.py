#!/usr/bin/env python3
from flask import Flask, render_template, request
import mariadb
import socket

app = Flask(__name__)
app.debug = True


config = {
    "host": "192.168.150.200",
    "port": 3306,
    "user": "flask",
    "password": "PnWJ9abAq3EAfEeqy7e",
    "database": "rhdemo",
}


@app.route("/", methods=["GET"])
def main():
    return "Hello, yes this is Flask"


@app.route("/index")
def index():
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    cur.execute("SELECT * FROM testtable")
    return render_template("index.html", data=cur.fetchall())


@app.route("/hostname")
def return_hostname():
    return "example flask app served from {} (fqdn: {}) to {}".format(
        socket.gethostname(), socket.getfqdn(), request.remote_addr
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
