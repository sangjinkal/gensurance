from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
 return 'See you in TeroKarvinen.com!\n\n'

if __name__ == '__main__':
 app.run(host=localhost, port=5000)
