from pyspark.sql import SparkSession
import json
import sys
from pyspark.sql.functions import col

def generate_itinerary(city_name, stay_duration):
    spark = SparkSession.builder.appName("TravelItinerary").getOrCreate()

    # Read cleaned CSVs from HDFS
    city_df = spark.read.option("header", True).option("multiLine", True).option("quote", "\"").option("escape", "\"").csv("hdfs://localhost:9000/travel/data/city_clean.csv")
    places_df = spark.read.option("header", True).option("multiLine", True).option("quote", "\"").option("escape", "\"").csv("hdfs://localhost:9000/travel/data/places_clean.csv")



    # Filter city info
    city_filtered = city_df.filter(col("City") == city_name)
    if city_filtered.count() == 0:
        spark.stop()
        return {"error": f"City '{city_name}' not found"}

    city_info = city_filtered.collect()[0].asDict()

    # Validate and convert stay_duration to int
    try:
        stay_duration = int(stay_duration)
    except ValueError:
        stay_duration = 1  # default to 1 day if invalid input

    # Get min and max days from city info
    min_days = int(city_info.get('min_days') or 0)
    max_days = int(city_info.get('max_days') or 0)

    # Duration message logic
    if min_days and stay_duration < min_days:
        duration_msg = f"Your stay ({stay_duration} days) is shorter than the ideal minimum ({min_days} days)."
    elif max_days and stay_duration > max_days:
        duration_msg = f"Your stay ({stay_duration} days) is longer than the ideal maximum ({max_days} days)."
    else:
        duration_msg = "Your stay fits within the ideal duration."

    # Get places for the city, order by Ratings descending
    places_filtered = places_df.filter(col("City") == city_name).orderBy(col("Ratings").desc())

    # Limit places recommended: 3 places per day of stay
    max_places = stay_duration * 3
    places_list = [row.asDict() for row in places_filtered.limit(max_places).collect()]

    itinerary = {
        "City": city_info["City"],
        "Ratings": city_info["Ratings"],
        "Ideal_duration": city_info["Ideal_duration"],
        "User_stay_duration": stay_duration,
        "Duration_message": duration_msg,
        "Best_time_to_visit": city_info["Best_time_to_visit"],
        "City_desc": city_info["City_desc"],
        "Places_to_visit": places_list
    }

    spark.stop()
    return itinerary


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: spark-submit generate_itinerary.py <city_name> <duration_days>")
        sys.exit(1)

    city = sys.argv[1]
    duration = sys.argv[2]

    result = generate_itinerary(city, duration)
    print(json.dumps(result))  # Output for Flask
