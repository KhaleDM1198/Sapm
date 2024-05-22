from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Alive"

def keep_alive():
    app.run(debug=False, host='0.0.0.0', port=8080)

# If this script is run directly, start the Flask server
if __name__ == "__main__":
    keep_alive()

