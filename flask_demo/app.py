from flask import Flask, render_template

app = Flask(__name__)


@app.route('/404')
def not_found():
    return render_template("404.html")


@app.route('/blank')
def blank():
    return render_template("blank.html")


@app.route('/buttons')
def buttons():
    return render_template("404.html")


@app.route('/cards')
def cards():
    return render_template("404.html")


@app.route('/charts')
def charts():
    return render_template("404.html")


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/tables')
def tables():
    return render_template("tables.html")


@app.route('/utilities-animation')
def utilities_animation():
    return render_template("utilities-animation.html")


@app.route('/utilities-border')
def utilities_border():
    return render_template("utilities-border.html")


@app.route('/utilities-color')
def utilities_color():
    return render_template("utilities-color.html")


@app.route('/utilities-other')
def utilities_other():
    return render_template("utilities-other.html")


if __name__ == '__main__':
    # TODO  [ECharts, WordCloud]
    app.run(debug=True)
