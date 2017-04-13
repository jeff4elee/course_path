from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

if __name__ == 'main':
	app.run(debug=True)

from home import views