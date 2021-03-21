from flask import Flask, render_template, url_for, redirect, session, request, jsonify
from client import MyClient
from threading import Thread, Event
import jsonpickle
import time


app = Flask(__name__)
app.secret_key = "Hello"

NAME_KEY = "name"
threads = {}
message = {}
CLIENTS = {}
threads_stop = {}

@app.route('/get_messages')
def get_message():
    if NAME_KEY in session and session[NAME_KEY] in message:
        return jsonify({"messages": message[session[NAME_KEY]]})
    else:
        return jsonify({"messages": []})


def disconnected():
    if NAME_KEY in session and session[NAME_KEY] in CLIENTS:
        client = CLIENTS[session[NAME_KEY]]
        client.disconnected()
        CLIENTS.pop(session[NAME_KEY])


@app.route("/login", methods=["POST", "GET"])
def login():

    def update_msg(client, name, stop):
        run = True
        while run:
            if stop[name]:
                run = False
            time.sleep(1)
            if client is None:
                continue
            new_msg = client.get_messages()
            print(client.name, new_msg)
            #message[name].extend(new_msg)
            for msg in new_msg:
                print(new_msg)
                if msg == "{quit}":
                    run = False
                    break
                if msg.split(' ')[0].replace(':', '') == client.name:
                    message[name].append("<div class='d-flex flex-column align-self-end'>" +
                                         "<p class='name'>Me</p><p class='self_msg'>" +
                                         ' '.join(msg.split(' ')[1:]) + "</p></div>")
                else:
                    message[name].append("<div class='d-flex flex-column'>" +
                                         "<p class='name'>" + client.name + "</p><p class='msg'>" +
                                         ' '.join(msg.split(' ')[1:]) + "</p></div>")
    if NAME_KEY in session:
        redirect(url_for("logout"))

    if request.method == "POST":
        session[NAME_KEY] = request.form["inputName"]
        client = MyClient(session[NAME_KEY])
        CLIENTS[session[NAME_KEY]] = client
        message[session[NAME_KEY]] = []
        stop_threads = False
        threads_stop[session[NAME_KEY]] = stop_threads
        thread = Thread(target=update_msg, args=[client, session[NAME_KEY], threads_stop])
        threads[session[NAME_KEY]] = thread
        thread.start()
        return redirect(url_for("home"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    disconnected()
    if NAME_KEY in session and session[NAME_KEY] in threads:
        threads_stop[session[NAME_KEY]] = True
        threads[session[NAME_KEY]].join()
        threads.pop(session[NAME_KEY])
    if NAME_KEY in session and session[NAME_KEY] in threads_stop:
        threads_stop.pop(session[NAME_KEY])
    if NAME_KEY in session and session[NAME_KEY] in message:
        message.pop(session[NAME_KEY])
    session.pop(NAME_KEY, None)

    return redirect(url_for("login"))


@app.route('/')
@app.route('/home')
def home():
    if NAME_KEY not in session:
        return redirect(url_for("login"))

    return render_template("index.html", page_login=True)


@app.route('/send_message', methods=["GET"])
def send_message():
    if session[NAME_KEY] in CLIENTS:
        ####PROBLEM#####
        client = CLIENTS[session[NAME_KEY]]
        msg = request.args.get("val")
        if client:
            client.send_messages(msg)
    return "none"


if __name__ == "__main__":
    app.run(debug=True)

