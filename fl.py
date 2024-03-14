import os
from flask import Flask

# Initialize Flask app
app = Flask(__name__)

# Define route to run Streamlit app
@app.route("/")
def run_streamlit():
    # Run Streamlit app using os.system
    os.system("streamlit run sl.py")
    return ""

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
