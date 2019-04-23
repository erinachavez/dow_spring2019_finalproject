from flask import Blueprint

ss_blueprint = Blueprint('synesthesia_sentences', __name__)

@ss_blueprint.route('/synesthesia_sentences')
def synesthesia_sentences():
    return "Synesthesia Sentences!"
