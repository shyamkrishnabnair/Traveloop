
# Travel Itinerary Generator using Apache Spark

## 📌 Project Overview

This project is a web-based **Travel Itinerary Generator** that leverages **Apache Spark** for data processing and **Hadoop HDFS** for distributed storage. It allows users to input a city and duration of stay and receive a customized itinerary with recommended places to visit. The system processes large travel datasets to offer intelligent recommendations based on user input.

---

## 🚀 Features

- Takes user input for city and duration.
- Analyzes city and tourism data stored in HDFS.
- Uses PySpark to recommend top-rated places dynamically.
- Returns an optimized travel itinerary as structured JSON.
- Renders results on a responsive web interface using Flask and Bootstrap.

---

## 🛠️ Tools and Technologies

### Frameworks & Libraries

- **Apache Spark**: For large-scale data processing using PySpark.
- **Hadoop HDFS**: Distributed file system used for storing cleaned datasets.
- **Flask**: Backend server to process inputs and serve results.
- **Bootstrap**: Frontend framework for building responsive UIs.
- **Python Libraries**:
  - `pandas`: Used during dataset cleaning and pre-processing.
  - `subprocess`: For executing PySpark scripts from Flask.

### Frontend

- **HTML5/CSS3**
- **Bootstrap 4**

### Backend

- **Python Flask**
- **PySpark**
- **Hadoop HDFS**

### Dataset Source

- Datasets were collected and adapted from [Kaggle](https://www.kaggle.com/).

---

## 🧹 Dataset Cleaning Process

- Used **pandas** to load and inspect raw data.
- Removed rows with missing or null values.
- Standardized header names and ensured UTF-8 encoding.
- Fixed inconsistent quoting and CSV structure issues.
- Saved cleaned files as `city_clean.csv` and `places_clean.csv`.

```python
# Example: Cleaning logic
df = pd.read_csv("raw_city.csv")
df.dropna(inplace=True)
df.columns = [col.strip().replace(" ", "_") for col in df.columns]
df.to_csv("city_clean.csv", index=False)
```

---

## 🗃️ HDFS Integration

```bash
# HDFS commands to create directories and upload files
hdfs dfs -mkdir -p /travel/data
hdfs dfs -put city_clean.csv /travel/data
hdfs dfs -put places_clean.csv /travel/data
```

---

## 🔄 Spark Script - Itinerary Generation

The `generate_itinerary.py` script does the following:

- Initializes SparkSession
- Loads `city_clean.csv` and `places_clean.csv` from HDFS
- Filters data based on the city input
- Recommends up to 3 places per day sorted by rating
- Handles edge cases and returns structured output

```python
# Load city and place data
city_df = spark.read.option("header", True).csv("hdfs://localhost:9000/travel/data/city_clean.csv")
places_df = spark.read.option("header", True).csv("hdfs://localhost:9000/travel/data/places_clean.csv")
```

---

## 🌐 Flask Integration

The Flask backend handles the web interface and execution logic:

- Receives user inputs from a form
- Runs Spark job using `subprocess.run()`
- Parses and displays the results in the frontend

```python
@app.route("/generate", methods=["POST"])
def generate():
    city = request.form["city"]
    duration = request.form["duration"]
    result = subprocess.run([...])
    return render_template("result.html", output=json.loads(result.stdout))
```

---

## 🎨 Frontend Display (HTML + Bootstrap)

The itinerary is displayed with styling and responsive layout.

```html
<h1>Itinerary for {{ output.City }}</h1>
<p>{{ output.Best_time_to_visit }}</p>
<p>{{ output.Duration_message }}</p>
{% for place in output.Places_to_visit %}
  <div>{{ place.Place }}</div>
{% endfor %}
```

---

## 🧑‍💻 Author Contribution

All tasks including dataset acquisition, cleaning, Spark integration, Flask backend development, HDFS configuration, and frontend design were completed by me as part of this academic project.

---

