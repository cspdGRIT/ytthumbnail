import os
from flask import Flask
from flask_cors import CORS
# Initialize Flask app
app = Flask(__name__)
CORS(app)
# Define route to run Streamlit app
@app.route("/")
def run_streamlit():
    # Run Streamlit app using os.system
    os.system("streamlit run sl_app.py")
    return ""

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)

# python3 __init__.py