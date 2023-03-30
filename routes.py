from flask import make_response, Blueprint, request

from handler import get_latest_engine_message, post_new_user_message

bp = Blueprint('convince_me_routes', __name__)


@bp.route("/")
def index():
    return "<p>Convince Me!</p>"


@bp.route("/get-latest-incoming-message/<string:uuid>/")
def get_latest_incoming_message(uuid):
    message = get_latest_engine_message(uuid)
    if message is None:
        return make_response('', 404)
    else:
        return make_response(message.to_json(), 200)


@bp.route("/post-new-outgoing-message/<string:uuid>/", methods=['POST'])
def post_outgoing_message(uuid):
    if post_new_user_message(uuid, request.json):
        return make_response('', 200)
    else:
        return make_response('', 404)
