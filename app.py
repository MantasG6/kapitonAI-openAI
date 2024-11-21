from flask import Flask
from flask_cors import CORS
from prompt import get_result
import pandas as pd

LOCAL_DATE_TIME = '2024-11-13 10:55'

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

locations = pd.read_csv("./data/locations.csv", sep=";")
loc = locations.iloc[0]

@app.route('/data')
def get_data():
    
    data = get_result(loc, LOCAL_DATE_TIME)
    # Returning the data as JSON
    return data

if __name__ == '__main__':
    app.run(port=5000, debug=True)