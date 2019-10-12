import pandas as pd
import numpy as np
import os
from flask import Flask, request, make_response, jsonify


# flask app for webhook
app = Flask(__name__)
log = app.logger


@app.route('/', methods=['GET'])
def webhook():
    return '''<h>The Heroku App is up and running <h\>'''



if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 80)
