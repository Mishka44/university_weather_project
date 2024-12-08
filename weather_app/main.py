import weather
from flask import Flask, request, render_template
from api_key import API_KEY

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def menu():
    if request.method == "POST":

        start_city = request.form.get("start_city")
        end_city = request.form.get("end_city")

        try:
            start_city_code = weather.get_location_key_by_name(API_KEY, start_city)
            end_city_code = weather.get_location_key_by_name(API_KEY, end_city)
        except Exception as e:
            return render_template("error.html", error=e)

        start_weather = weather.request(API_KEY, start_city_code)
        end_weather = weather.request(API_KEY, end_city_code)

        conditions_check_start = weather.check_bad_weather(start_weather)
        conditions_check_end = weather.check_bad_weather(end_weather)

        return render_template("result.html", start_city=start_city, end_city=end_city,
                               start_weather_list=conditions_check_start,
                               end_weather=conditions_check_end)

    return render_template("menu.html")


@app.route("/result")
def result():
    return render_template("result.html")


if __name__ == '__main__':
    app.run(debug=True)
