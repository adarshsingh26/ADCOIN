from flask import Flask, jsonify, request, render_template   # Importing flask Class
from werkzeug.utils import secure_filename
from PIL import Image
from pyzbar.pyzbar import decode
import pyqrcode, os, time
from flask_cors import CORS
from wallet import Wallet
from blockchain import Blockchain

UPLOAD_FOLDER = 'img/'
ALLOWED_EXTENSIONS = set(['png'])

app = Flask(__name__)       # Creating a flask object i.e WSGI application(__name__ tells flask in which context it run)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

qr_public_key = ""
qr_amount = ""


@app.route("/get_qr_code", methods=["POST"])
def generate_qr_code():
    files = os.listdir(os.getcwd() + "\\static")
    for file in files:
        if "qr_code" in file:
            print(os.getcwd() + "\\static\\" + file)
            try:
                os.remove(os.getcwd() + "\\static\\" + file)
                print("success file deleted")
            except FileNotFoundError:
                print("error file not deleted")
                continue
        else:
            continue
    data = request.get_json()
    qrobj = pyqrcode.create('{}/{}'.format(data["public_key"], data["amount"]))
    # qrobj = pyqrcode.create('{}/{}'.format(data["public_key"], data["amount"]))
    qrobj.png('static/qr_code{}.png'.format(data["amount"]), scale=2)
    response = {
        "message": "QR CODE generated successfully",
        "address": str(request.remote_addr),
    }
    return jsonify(response), 201


# @app.route("/static/qr_code.png",methods=["GET"])
# def get_file():
#     return send_from_directory("static","qr_code.png"), 200

@app.route("/upload_data", methods=["POST"])
def decode_qr_code():
    try:
        data = request.files["qrCode"]
        filename = secure_filename(data.filename)
        data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data = decode(Image.open('img/{}'.format(data.filename)))
        decoded_data = data[0][0].decode("UTF-8")
        public_key, amount = decoded_data.split("/")
        response = {
            "message": "QR scanned successfully",
            "public_key": public_key,
            "amount": amount          # "{0:.2f}".format(amount)
        }
        return jsonify(response), 200
    except:
        response = {
            "message": "Error scanning QR code, upload correct qr code",
        }
        return jsonify(response), 400

# @app.route("/data/<public_key>/<amount>", methods=["GET"])
# def get_qr_data(public_key, amount):
#     global qr_public_key
#     global qr_amount
#     qr_public_key = public_key
#     qr_amount = amount
#     response = {
#         "message": "QR CODE scanned successfully."
#     }
#     return jsonify(response), 201
#     # return render_template("node.html", public_key=public_key, amount=amount)


# @app.route("/get_data", methods=["GET"])
# def send_data():
#     global qr_public_key
#     global qr_amount
#     while (qr_public_key == "" and qr_amount == ""):
#         time.sleep(2)
#     else:
#         response = {
#             "message": "QR data recieved successfully",
#             "public_key": qr_public_key,
#             "amount": qr_amount
#         }
#     qr_public_key = ""
#     qr_amount = ""
#     return jsonify(response), 201


@app.route("/", methods=["GET"])             # route maps the url to the function
def get_node_ui():
    return render_template("node.html")


@app.route("/network", methods=["GET"])
def get_network_ui():
    return render_template("network.html")


@app.route('/wallet', methods=["DELETE"])
def remove_wallet():
    try:
        os.remove(os.getcwd() + "/wallet-{}.txt".format(port))
        os.remove(os.getcwd() + "/blockchain-{}.txt".format(port))
        if (os.path.isfile(os.getcwd() + "/wallet-{}.txt".format(port)) or os.path.isfile(os.getcwd() + "/blockchain-{}.txt".format(port))):
            response = {
                "message": "Wallet deletion failed",
            }
            return jsonify(response), 500
        else:
            response = {
                "message": "Wallet deleted successfully"
            }
            return jsonify(response), 200
    except:
        response = {
            "message": "Wallet dosen't exist"
        }
        return jsonify(response), 500



@app.route("/wallet", methods=["POST"])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key, port)
        response = {
            "public_key": wallet.public_key,
            "private_key": wallet.private_key,
            "funds": blockchain.get_balance()
        }
        return jsonify(response), 201         # 201 --> Created
    else:
        response = {
            "message": "Wallet creation failed"
        }
        return jsonify(response), 500           # 500 --> Server error


@app.route("/wallet", methods=["GET"])
def load_keys():
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key, port)
        response = {
            "public_key": wallet.public_key,
            "private_key": wallet.private_key,
            "funds": blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            "message": "Loading keys failed. Create a wallet or load a wallet if it exists"
        }
        return jsonify(response), 500


@app.route("/balance", methods=["GET"])
def get_balance():
    balance = blockchain.get_balance()
    if balance != None:
        response = {
            "message": "Fetched balance successfully",
            "funds": balance
        }
        return jsonify(response), 200           # 200 --> OK
    else:
        response = {
            "message": "Loading balance Failed",
            "wallet_set_up": wallet.public_key != None
        }
        return jsonify(response), 500


@app.route("/broadcast_transaction", methods=["POST"])
def broadcast_transaction():
    values = request.get_json()
    if not values:
        response = {
            "message": "No data found"
        }
        return jsonify(response), 400
    required = ["sender", "recipient", "amount", "signature"]
    if not all(key in values for key in required):
        response = {
            "message": "Some data is missing"
        }
        return jsonify(response), 400
    success = blockchain.add_transaction(values["recipient"], values["sender"], values["signature"], values["amount"],
                                         is_receiving=True)
    if success:
        response = {
            "message": "Successfully added transaction",
            "transaction": {
                "sender": values["sender"],
                "recipient": values["recipient"],
                "amount": values["amount"],
                "signature": values["signature"]
            }
        }
        return jsonify(response), 201
    else:
        response = {
            "message": "Creating a transaction failed"
        }
        return jsonify(response), 500


@app.route("/broadcast_block", methods=["POST"])
def broadcast_block():
    values = request.get_json()
    if not values:
        response = {
            "message": "No data found"
        }
        return jsonify(response), 400
    if "block" not in values:
        response = {
            "message": "Some data is missing"
        }
        return jsonify(response), 400
    block = values["block"]
    if block["index"] == blockchain.chain[-1].index + 1:
        if blockchain.add_block(block):
            response = {"message": "Block added"}
            return jsonify(response), 201
        else:
            response = {"message": "Block seems invalid"}
            return jsonify(response), 409
    elif block["index"] > blockchain.chain[-1].index:
        response = {"message": "Blockchain seems to differ from local blockchain"}
        blockchain.resolve_conflicts = True
        return jsonify(response), 200
    else:
        response = {"message": "Blockchain seems to be shorter, block not added"}
        return jsonify(response), 409


@app.route("/transaction", methods=["POST"])
def add_transaction():
    if wallet.public_key == None:
        response = {
            "message": "No wallet setup"
        }
        return jsonify(response), 400    # 400 --> Client Error
    values = request.get_json()  # Gets json data from the client request
    if not values:
        response = {
            "message": "No data found"
        }
        return jsonify(response), 400
    required_fields = ["recipient", "amount"]
    if not all(field in values for field in required_fields):
        response = {"message": "Required data is missing"}
        return jsonify(response), 400
    recipient = values["recipient"]
    amount = values["amount"]

    signature = wallet.sign_transaction(wallet.public_key, recipient, amount)
    success = blockchain.add_transaction(recipient, wallet.public_key, signature, amount)
    if success:
        response = {
            "message": "Successfully added transaction",
            "transaction": {
                "sender": wallet.public_key,
                "recipient": recipient,
                "amount": amount,
                "signature": signature
            },
            "funds": blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            "message": "Creating a transaction failed"
        }
        return jsonify(response), 500


@app.route("/mine", methods=["POST"])
def mine():
    if blockchain.resolve_conflicts:
        response = {"message": "Resolve conflicts first, block not added"}
        return jsonify(response), 409
    block = blockchain.mine_block()
    if block != None:
        dict_block = block.__dict__.copy()
        dict_block["transactions"] = [tx.__dict__ for tx in dict_block["transactions"]]
        response = {
            "message": "Block added successfully",
            "block": dict_block,
            "funds": blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            "message": "Adding a block failed",
            "wallet_set_up": wallet.public_key != None
        }
        return jsonify(response), 500


@app.route("/resolve-conflicts", methods=["POST"])
def resolve_conflicts():
    replaced = blockchain.resolve()
    if replaced:
        response = {"message": "Chain was replaced"}
    else:
        response = {"message": "Local Chain kept"}
    return jsonify(response), 200

@app.route("/transactions", methods=["GET"])
def get_open_transaction():
    transactions = blockchain.get_open_transactions()
    dict_transactions = [tx.__dict__ for tx in transactions]
    return jsonify(dict_transactions), 200


@app.route("/chain", methods=["GET"])
def get_chain():
    chain_snapshot = blockchain.chain
    dict_chain = [block.__dict__.copy() for block in chain_snapshot]
    for dict_block in dict_chain:
        dict_block["transactions"] = [tx.__dict__ for tx in dict_block["transactions"]]
    return jsonify(dict_chain), 200    # return takes data and HTTP status code


@app.route("/node", methods=["POST"])
def add_node():
    values = request.get_json()
    if not values:
        response = {
            "message": "No data found"
        }
        return jsonify(response), 400
    if "node" not in values:
        response = {
            "message": "Send node data"
        }
        return jsonify(response), 400
    node = values["node"]
    blockchain.add_peer_node(node)
    response = {
        "message": "Node added successfully",
        "all_nodes": blockchain.get_peer_nodes()
    }
    return jsonify(response), 201


@app.route('/node/<node_url>', methods=["DELETE"])
def remove_node(node_url):
    if node_url == "" or node_url == None:
        response = {
            "message": "No node found"
        }
        return jsonify(response), 400
    blockchain.remove_peer_node(node_url)
    response = {
        "message": "Node removed",
        "all_nodes": blockchain.get_peer_nodes()
    }
    return jsonify(response), 200


@app.route("/nodes", methods=["GET"])
def get_nodes():
    nodes = blockchain.get_peer_nodes()
    response = {
        "all_nodes": nodes
    }
    return jsonify(response), 200


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=5000)
    args = parser.parse_args()
    port = args.port
    wallet = Wallet(port)
    blockchain = Blockchain(wallet.public_key, port)
    app.run("0.0.0.0", port=port)  # Run the web app (Use "0.0.0.0" for external connectivity and "127.0.0.1" for local)
