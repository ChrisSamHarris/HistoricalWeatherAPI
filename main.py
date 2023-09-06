from flask import Flask, render_template, jsonify, request
import pandas as pd 

app = Flask(__name__)

df = pd.read_csv("data/stations.txt", skiprows=17)
stations = df[['STAID','STANAME                                 ']]

@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html(index=False))

@app.route("/api/v1/<station>/<date>")
def about(station, date):
    filename = f"data/TG_STAID{str(station).zfill(6)}.txt"
    # formatted_date = date[:4] + "-" + date[4:6] + "-" + date[6:]
    # parse_dates = 18600105 -> 1860-01-05
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    # temp = df.station(date)
    temperature = df.loc[df['    DATE']==date]['   TG'].squeeze() / 10
    
    return jsonify({
    "station": station,
    "date": date,
    "temperature": f"{temperature} C"
})

@app.route("/api/v1/<station>")
def all_station_data(station):
    filename = f"data/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient="records")
    return result

@app.route("/api/v1/yearly/<station>/<year>")
def spec_year_station_data(station, year):
    filename = f"data/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    return result

@app.errorhandler(Exception)
def handle_error(e):
    return jsonify({
        "error": "Error loading file, have you entered a correct station and date?",
        "details": str(e)
    }), 500

# @app.errorhandler(Exception)
# def handle_error(e):
#     if request.path.startswith('/api/'):
#         return jsonify({
#             "error": "Error loading file, have you entered a correct station and date?",
#             "details": str(e)
#         }), 500  # 500 is the status code for Internal Server Error
#     else:
#         # handle non-API errors differently
#         return "An unexpected error occurred.", 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)