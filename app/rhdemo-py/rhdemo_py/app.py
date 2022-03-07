#!/usr/bin/env python3
from flask import Flask
import mariadb

app = Flask(__name__)


@app.route("/", methods=["GET"])
def main():
    return "Hello, yes this is Flask"


if __name__ == "__main__":
    app.run()



# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'jay'
app.config['MYSQL_DATABASE_PASSWORD'] = 'jay'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
