from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

TOKEN = "CHANGE_THIS_TOKEN"

devices = {}
commands = {}
results = {}

def auth(req):
    return req.headers.get("Token") == TOKEN

@app.route("/")
def panel():
    html = """
    <h2>Python Remote Panel</h2>
    <form method="post" action="/send">
      Device ID:<br>
      <input name="device"><br><br>

      Command:<br>
      <select name="cmd">
        <option value="INFO">INFO</option>
        <option value="LIST_FILES">LIST_FILES</option>
        <option value="SCREENSHOT">SCREENSHOT</option>
      </select><br><br>

      <button type="submit">Send</button>
    </form>

    <hr>
    <h3>Devices</h3>
    <pre>{{devices}}</pre>

    <h3>Results</h3>
    <pre>{{results}}</pre>
    """
    return render_template_string(html, devices=devices, results=results)

@app.route("/send", methods=["POST"])
def send():
    device = request.form.get("device")
    cmd = request.form.get("cmd")
    commands[device] = cmd
    return "Command Sent ✔ <br><a href='/'>Back</a>"

@app.route("/poll", methods=["POST"])
def poll():
    if not auth(request):
        return jsonify({"error": "unauthorized"}), 403

    device = request.json.get("device")
    devices[device] = "online"

    cmd = commands.get(device, "")
    commands[device] = ""
    return jsonify({"cmd": cmd})

@app.route("/result", methods=["POST"])
def result():
    if not auth(request):
        return jsonify({"error": "unauthorized"}), 403

    device = request.json.get("device")
    res = request.json.get("result")
    results[device] = res
    return {"ok": True}

app.run(host="0.0.0.0", port=8080)
