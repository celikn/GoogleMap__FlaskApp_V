from flask import *
app = Flask(__name__)
from flask import *

from flask import Flask, render_template

##Source:http://geoscript.org/tutorials/web-flask-py/index.html#tutorials-web-flask-py
app = Flask(__name__, template_folder="templates")

@app.route("/")
def wms():
     ##use python wms.py
     return render_template('wms2.html')



if __name__ == "__main__":
  app.run(debug=True, host="127.0.0.1",port=5011)
