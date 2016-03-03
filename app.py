from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

app = Flask(__name__, template_folder="templates")
GoogleMaps(app)

@app.route("/")
def mapview():
    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=39.9130572,
        lng=32.7892743,
        markers=[(37.4419, -122.1419)]
    )
    sndmap = Map(
        identifier="sndmap",
        lat=39.9130572,
        lng=32.7892743,
        markers={'http://maps.google.com/mapfiles/ms/icons/green-dot.png':[(37.4419, -122.1419)],
                 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png':[(37.4300, -122.1400)]}
    )
    return render_template('index.html', mymap=mymap, sndmap=sndmap)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1",port=5010)