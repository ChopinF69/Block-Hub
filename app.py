from flask import Flask, make_response, redirect, render_template, request, url_for
from services.SessionManager import SessionManager
from services.UserManager import LoginStatus, RegisterStatus
from utils.Logger import Logger, LogLevel
import ecdsa


app = Flask(__name__)
logger = Logger("./logs.log")

session_manager = SessionManager()
lst_of_sessions = []
session_id, user_manager = session_manager.generate_session(["A", "B"], 1)
session_manager.set_session(user_manager)


@app.route("/")
def index():
    user_name = request.cookies.get("name")
    public_address = request.cookies.get("public_address")

    logger.Log(
        LogLevel.Information,
        f"User: {user_name}, with public_address: {public_address}",
    )
    print(user_name, public_address)
    return render_template(
        "index.html",
        peers=session_manager.get_session().get_network().get_peers(),
        user_name=user_name,
        public_address=public_address,
    )


@app.route("/createsession", methods=["GET"])
def createsession():
    logger.end()
    return render_template("create_session.html")


@app.route("/createsession", methods=["POST"])
def createsession_post():
    lst_of_names = [
        name.strip() for name in request.form.get("lst_of_names", "").split()
    ]
    difficulty = request.form.get("difficulty", "0")
    session_id, user_manager = session_manager.generate_session(
        lst_of_names, int(difficulty)
    )
    session_manager.set_session(user_manager)
    lst_of_sessions.append(session_id)

    # i need to save it in the cookie for the further requests
    response = make_response(redirect(url_for("index")))
    response.set_cookie("sesion_id", session_id, max_age=60 * 30)  # 30 minutes

    return response


@app.route("/register")
def register():
    logger.end()
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_post():
    name = request.form.get("name")
    if not name:
        logger.Log(LogLevel.Error, "Registration failed: Name is required.")
        return "Name is required", 400

    # status, password = userManager.register(name)
    status, password = session_manager.get_session().register(name)
    if status == RegisterStatus.AlreadyExists:
        logger.Log(
            LogLevel.Warning, f"Registration failed: User {name} already exists."
        )
        return "User already exists", 400

    logger.Log(LogLevel.Information, f"User {name} successfully registered.")
    return redirect(url_for("show_password_get", password=password))


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    public_address = request.form.get("public_address", "").strip()
    password = request.form.get("password", "").strip()

    # status = userManager.login(public_address, password)
    status = session_manager.get_session().login(public_address, password)

    if status == LoginStatus.WrongPassword:
        logger.Log(
            LogLevel.Warning, f"Login failed: Incorrect password for {public_address}."
        )
    elif status == LoginStatus.NoPublicAddress:
        logger.Log(
            LogLevel.Error,
            f"Login failed: No account found with public address {public_address}.",
        )
    elif status == LoginStatus.Success:
        # user_name = userManager.get_peer_by_address(public_address).get_name()
        user_name = (
            session_manager.get_session().get_peer_by_address(public_address).get_name()
        )
        logger.Log(LogLevel.Information, f"User {user_name} logged in successfully.")
        response = make_response(redirect(url_for("index")))
        response.set_cookie("public_address", public_address, max_age=60 * 60 * 24)
        response.set_cookie("name", user_name, max_age=60 * 60 * 24)  # 1 day
        return response

    return redirect(url_for("login"))


@app.route("/logout", methods=["POST"])
def logout():
    user_name = request.cookies.get("name")
    logger.Log(LogLevel.Information, f"User {user_name} logged out.")

    response = make_response(redirect(url_for("index")))
    response.delete_cookie("public_address")
    response.delete_cookie("name")
    return response


@app.route("/show_password", methods=["GET"])
def show_password_get():
    password = request.args.get("password", "No password available")
    logger.Log(LogLevel.Information, f"User is viewing password: {password}.")

    return render_template("show_password.html", password=password)


@app.route("/update_block_data/<int:peer_id>/<int:block_index>", methods=["POST"])
def update_block_data(peer_id, block_index):
    new_data = request.form.get("data")
    # _, service = network.get_peers()[peer_id]
    _, service = session_manager.get_session().get_network().get_peers()[peer_id]

    service.update_blocks_data(block_index, new_data)
    logger.Log(
        LogLevel.Information, f"Updating block {block_index} with new data: {new_data}"
    )

    return redirect(url_for("index"))


@app.route(
    "/update_transaction_data/<int:peer_id>/<int:block_index>/<int:transaction_index>",
    methods=["POST"],
)
def update_transaction_data(peer_id, block_index, transaction_index):
    new_amount = request.form.get("new_amount")
    if new_amount:
        new_amount = int(new_amount)

    # _, service = network.get_peers()[peer_id]
    _, service = session_manager.get_session().get_network().get_peers()[peer_id]
    logger.Log(
        LogLevel.Information,
        f"Updating transaction {transaction_index} with new amount: {new_amount}",
    )

    service.update_blocks_transaction_amount(block_index, new_amount, transaction_index)

    return redirect(url_for("index"))


@app.route("/allusers", methods=["GET"])
def allusers():
    logger.Log(LogLevel.Information, "User accessed all users page.")
    user_name = request.cookies.get("name")
    return render_template(
        "allusers.html",
        # list=userManager.get_users_public_addresses(),
        list=session_manager.get_session().get_users_public_addresses(),
        user_name=user_name,
    )


@app.route("/add_money", methods=["POST"])
def add_money():
    user_name = request.cookies.get("name")
    public_address = request.cookies.get("public_address")

    if not user_name or not public_address:
        logger.Log(LogLevel.Warning, "User is not logged in while trying to add money.")
        return redirect(url_for("login"))

    amount = request.form.get("amount", type=int)

    if amount and amount > 0:
        logger.Log(
            LogLevel.Information,
            f"Adding {amount} money to {user_name} ({public_address}).",
        )
        # userManager.add_money(public_address, amount)
        session_manager.get_session().add_money(public_address, amount)

    return redirect(url_for("myaccount"))


@app.route("/myaccount", methods=["GET"])
def myaccount():
    user_name = request.cookies.get("name")
    public_address = request.cookies.get("public_address")
    if not user_name or not public_address:
        logger.Log(
            LogLevel.Warning,
            f"User {user_name} is not logged in while accessing account page.",
        )
        return redirect(url_for("login"))
    # current_peer = userManager.get_peer_by_address(public_address)
    current_peer = session_manager.get_session().get_peer_by_address(public_address)
    logger.Log(
        LogLevel.Information, f"User {user_name} accessed their account details."
    )

    return render_template(
        "/myaccount.html",
        user_name=user_name,
        public_address=public_address,
        balance=current_peer.get_wallet().get_balance(),
        transactions=current_peer.get_wallet().get_transaction_history(),
    )


@app.route("/sendamount", methods=["POST"])
def sendamount():
    amount = request.form.get("amount", 0)
    public_address_to_send = request.form.get("public_address", "")
    data = request.form.get("data", "")
    own_public_address = request.cookies.get("public_address", "")
    logger.Log(
        LogLevel.Information,
        f"Sending {amount} to {public_address_to_send} from {own_public_address}.",
    )

    #    userManager.send_money(
    #        own_public_address, public_address_to_send, int(amount), data
    #    )
    session_manager.get_session().send_money(
        own_public_address, public_address_to_send, int(amount), data
    )
    return redirect(url_for("allusers"))


@app.route("/logs")
def logs():
    return render_template(
        "logs.html", logs=(line.strip() for line in open("./logs.log", "r"))
    )


@app.route("/getpublickey", methods=["GET"])
def get_public_key():
    return render_template("getpublickey.html")


@app.route("/getpublickey", methods=["POST"])
def get_public_key_post():
    private_key_hex = request.form.get("private_address", "").strip()
    try:
        private_key_bytes = bytes.fromhex(private_key_hex)

        sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)

        vk = sk.get_verifying_key()
        public_key_hex = vk.to_string().hex()

        logger.Log(LogLevel.Information, f"Derived public key: {public_key_hex}")
        return render_template("show_public_key.html", public_key=public_key_hex)

    except Exception as e:
        logger.Log(LogLevel.Error, f"Error retrieving public key: {str(e)}")
        return "Invalid private key", 400


if __name__ == "__main__":
    app.run(debug=True)
