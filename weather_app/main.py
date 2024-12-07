import weather
from flask import Flask, request, render_template

app = Flask(__name__)

api_key = "E2D2L0W3qMB9buETGgbVPGNrPAPXx6Yv"




@app.route("/", methods=["GET", "POST"])
def menu():
    if request.method == "POST":
        start_city_lat = request.form.get("start_lat")
        start_city_lon = request.form.get("start_lon")

        coordinates_start = (start_city_lat, start_city_lon)

        end_city_lat = request.form.get("end_lat")
        end_city_lon = request.form.get("end_lon")

        coordinates_end = (end_city_lat, end_city_lon)
        try:
            start_city_code = weather.get_location_key_by_coors(coordinates_start, api_key)
            end_city_code = weather.get_location_key_by_coors(coordinates_end, api_key)
        except Exception as e:
            return render_template("error.html", error=e)

        start_weather = weather.request(api_key, start_city_code)
        end_weather = weather.request(api_key, end_city_code)

        conditions_check_start = weather.check_bad_weather(start_weather)
        conditions_check_end = weather.check_bad_weather(end_weather)

        return render_template("result.html", start_city=coordinates_start, end_city=coordinates_end,
                               start_weather_list=conditions_check_start,
                               end_weather=conditions_check_end)

    return render_template("menu.html")


@app.route("/result")
def result():
    return render_template("result.html")




if __name__ == '__main__':
    app.run(debug=True)
