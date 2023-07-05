import datetime

from flask import Flask, render_template
import pandas as pd
from datetime import datetime

# requested_date = datetime.strptime('18600101', '%Y%m%d')
# st_id = "{:06d}".format(1)
# df = pd.read_csv(f"data_small/TG_STAID{st_id}.txt", skiprows=20)
# # df = pd.read_csv(f"data_small/TG_STAID000001.txt", skiprows=20, parse_dates=["    DATE"])
# row = df.loc[df["    DATE"] == requested_date]['   TG'].squeeze() / 10
# print(f"TG_STAID{st_id}.txt")
# print(requested_date)
# print(row)
# exit()


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/stations')
def get_stations_list():
    df = pd.read_csv('data_small/stations.txt', skiprows=17)
    # df[10:20][['STAID', 'STANAME                                 ']].to_html()
    return render_template('stations.html', df=df)


@app.route('/stations/<station_id>')
def get_station_data(station_id):
    df = pd.read_csv(f"data_small/TG_STAID{station_id.zfill(6)}.txt", skiprows=20, parse_dates=["    DATE"])
    return df[10:30].to_dict(orient='records')


@app.route('/api/v1/stations/<station>/<date>')
def get_station_temperature(station, date):
    requested_date = datetime.strptime(date, '%Y%m%d')
    st_id = "{:06d}".format(int(station))
    df = pd.read_csv(f"data_small/TG_STAID{st_id}.txt", skiprows=20, parse_dates=["    DATE"])

    try:
        temperature = df.loc[df["    DATE"] == requested_date]['   TG'].squeeze() / 10
        if temperature.empty:
            raise Exception()
    except Exception:
        return "Date or Temperature Not Found"

    return {
        "station": st_id,
        "date": requested_date,
        "temperature": temperature
    }


@app.route('/api/v1/stations/<station_id>/year/<year>')
def get_station_year_data(station_id, year):
    df = pd.read_csv(f"data_small/TG_STAID{station_id.zfill(6)}.txt",
                     skiprows=20)
    df['    DATE'] = df['    DATE'].astype(str)
    df1 = df[df['    DATE'].str.startswith(str(year))]
    return df1[10:30].to_dict(orient='records')


@app.route('/api/v1/dictionary/<search>')
def pillow_is(search):
    df = pd.read_csv('dictionary.csv')
    row = df.loc[df['word'] == search]

    if not len(row.word):
        return '404'

    return {"word": row.word.squeeze(),
            "definition": row.definition.squeeze()}


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
