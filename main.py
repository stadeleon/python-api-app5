from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/v1/<station>/<date>')
def get_station(station, date):
    temperature = 23

    return {
        "station": station,
        "date": date,
        "temperature": temperature
        }

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
