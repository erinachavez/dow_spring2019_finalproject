from flask import Flask
from flask import json

from ChainAbstractions import ca_blueprint
from SynesthesiaSentences import ss_blueprint
from ARealPoem import arp_blueprint

import random

app = Flask(__name__)
app.register_blueprint(ca_blueprint)
app.register_blueprint(ss_blueprint)
app.register_blueprint(arp_blueprint)

@app.route('/random_color')
def random_color():
    data = {
        "r": random.randint(0,255),
        "g": random.randint(0,255),
        "b": random.randint(0,255)
    }

    response = app.response_class(
        response = json.dumps(data),
        status = 200,
        mimetype = 'application/json'
    )

    return response

if __name__ == "__main__":
    app.run(debug=True)
