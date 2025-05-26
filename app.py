import cmd
from flask import Flask, render_template, request
import subprocess
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    city = request.form['city']
    duration = request.form['duration']

    try:
        result = subprocess.run(
            ['C:/spark/bin/spark-submit.cmd', 'C:/Users/keyje/Desktop/BDA Project/Travel app/generate_itinerary.py', city, str(duration)],
            capture_output=True, text=True, check=True
        )
        data = json.loads(result.stdout)
        return render_template("result_day.html", output=data)

    except subprocess.CalledProcessError as e:
        return f"Spark job failed:<br><pre>{e.stderr}</pre>"
    except json.JSONDecodeError:
        return f"Error: Could not parse output.<br><br>Raw Output:<br><pre>{result.stdout}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
