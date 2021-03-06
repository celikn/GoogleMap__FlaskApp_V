from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from sqlalchemy import (create_engine, MetaData, Column, Integer, String,func, select)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry
from sqlalchemy import func
from geoalchemy2.functions import GenericFunction

### EXAMPLE with Leaflet
appgeo = Flask(__name__, template_folder="templates")

engine = create_engine('postgresql://postgres:postgres@localhost/flaskgisdb', echo=True)
#"'postgresql://username:password@localhost/databasename'
metadata = MetaData(engine)
Base = declarative_base(metadata=metadata)

class Lake(Base):
   __tablename__ = 'lake'
   id = Column(Integer, primary_key=True)
   name = Column(String)
   geom = Column(Geometry('POLYGON'))


class Spot(Base):
    __tablename__ = 'spots'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    geom = Column(Geometry('POINT'))

class Road(Base):
        __tablename__ = 'roads'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        geom = Column(Geometry('LINESTRING'))

#
#
# metadata.drop_all()
# metadata.create_all()
#



session = sessionmaker(bind=engine)()
# Add objects.  We can use strings...
# session.add_all([
#          Road(name='Jeff Rd', geom='LINESTRING(191232 243118,191108 243242)'),
#          Road(name='Geordie Rd', geom='LINESTRING(189141 244158,189265 244817)'),
#          Road(name='Paul St', geom='LINESTRING(192783 228138,192612 229814)'),
#          Road(name='Graeme Ave', geom='LINESTRING(189412 252431,189631 259122)'),
#          Road(name='Phil Tce', geom='LINESTRING(190131 224148,190871 228134)'),
#          Spot(name='test 1',geom='POINT(39.9130572 32.7892743)'),
#      ])
#
# session.commit()
r2 = session.query(Road).filter_by(name='Paul St').first()

query = session.query(Road.name,
                      func.ST_Area(func.ST_Buffer(Road.geom, 2)) \
                      .label('bufferarea'))
for row in query:
    print ('%s: %f' % (row.name, row.bufferarea))


spotquery = session.query(Spot.name,
                      func.ST_X(Spot.geom).label('X'),func.ST_Y(Spot.geom).label('Y'))
spotCoordinates=[]
for row in spotquery:
    print ('%s: %f  , %f ' % (row.name, row.X, row.Y))
    spotCoordinates.append((row.X,row.Y))

print(spotCoordinates)
@appgeo.route("/")
def mapview():
      return render_template('indexgeo.html',spotCoordinates=spotCoordinates)

if __name__ == "__main__":
      appgeo.run(debug=True, host="127.0.0.1",port=5012)
