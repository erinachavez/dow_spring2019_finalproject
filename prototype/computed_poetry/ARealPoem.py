from flask import Blueprint

import random

arp_blueprint = Blueprint('a_real_poem', __name__)

@arp_blueprint.route('/a_real_poem')
def a_real_poem():
    return "A Real Poem!"
