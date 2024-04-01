from flask import Flask, render_template, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from utils import generate_csrf_token, generate_auth_ticket, claim_auth_ticket

app = Flask(
    import_name=__name__,
    template_folder="web/templates",
    static_folder="web/static",
    static_url_path=""
)
limiter = Limiter(
    get_remote_address,
    app=app
)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/refresh", methods=["POST"])
@limiter.limit("2/minute")
def refresh():
    cookie = request.form.get("cookie")

    if not cookie or len(cookie) > 4096 or not isinstance(cookie, str):
        return jsonify({
            "error": True,
            "message": "invalid input"
        })
    
    csrf_token = generate_csrf_token(cookie)

    if not csrf_token:
        return jsonify({
            "error": True,
            "message": "csrf token failure"
        })
    
    auth_ticket = generate_auth_ticket(cookie, csrf_token)

    if not auth_ticket:
        return jsonify({
            "error": True,
            "message": "authentication ticket failure"
        })
    
    refresh_cookie = claim_auth_ticket(auth_ticket, csrf_token)

    return jsonify({
        "error": False,
        "cookie": refresh_cookie
    }) 

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
