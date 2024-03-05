from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/user/<username>')
def show_user_profile(username):
    return f'User: {username}'


@app.route('/simple_web')
def fun_simple_web():  # put application's code here
    return render_template('web1.html', message='Flask is awesome!')


if __name__ == '__main__':
    app.run()
