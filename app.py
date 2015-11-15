import os
from flask import Flask
from flask import request
from flask import Response
import convert


app = Flask(__name__)

DOC = """
This API transforms coordinates in WGS-84 to GCJ02 and vice-versa, e.g.: 

WGS-84 to GCJ02:
  $ curl '{prefix}wgs84togcj02?lat=31.22222&lon=121.45806'
  31.221399,121.466258


GCJ02 to WGS-84:
  $ curl '{prefix}gcj02towgs84?lat=31.221399&lon=121.466258'
  31.222220,121.458062

- Changping Chen
"""

@app.route('/')
def hello():
    return Response(DOC.strip().format(prefix=request.url_root), mimetype="text/plain", status=200)


@app.route('/wgs84togcj02', methods=["GET", "POST"])
def wgs84togcj02():
    latitudes = request.values.get("lat", "").strip()
    longitudes = request.values.get("lon", "").strip()

    if len(latitudes) == 0 or len(longitudes) == 0:
        return Response("No input is given.", mimetype="text/plain", status=500)

    latitudes = latitudes.split(",")
    longitudes = longitudes.split(",")

    if len(latitudes) != len(longitudes):
        return Response("len(latitudes) != len(longitudes)", mimetype="text/plain", status=500)

    flat = [float(lat) for lat in latitudes]
    flon = [float(lon) for lon in longitudes]

    output = ""
    for lat, lon in zip(flat, flon):
        output += "%f,%f\n" % convert.wgs84togcj02(lat, lon)

    return Response(output, mimetype="text/plain", status=200)



@app.route('/gcj02towgs84', methods=["GET", "POST"])
def gcj02towgs84():
    latitudes = request.values.get("lat", "").strip()
    longitudes = request.values.get("lon", "").strip()

    if len(latitudes) == 0 or len(longitudes) == 0:
        return Response("No input is given.", mimetype="text/plain", status=500)

    latitudes = latitudes.split(",")
    longitudes = longitudes.split(",")

    if len(latitudes) != len(longitudes):
        return Response("len(latitudes) != len(longitudes)", mimetype="text/plain", status=500)

    flat = [float(lat) for lat in latitudes]
    flon = [float(lon) for lon in longitudes]

    output = ""
    for lat, lon in zip(flat, flon):
        output += "%f,%f\n" % convert.gcj02towgs84(lat, lon)

    return Response(output, mimetype="text/plain", status=200)


if __name__ == "__main__":
    app.debug = True
    app.run()
