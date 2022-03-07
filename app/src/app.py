#!/usr/bin/env python3
from flask import Flask
import mariadb

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    return "Hello, yes this is Flask"

if __name__ == "__main__":
    app.run()
