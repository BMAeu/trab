from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/nv_quest')
def showSignUp():
    return render_template('nv_quest.html')


if __name__ == "__main__":
    app.run()    