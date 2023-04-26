from flask import Flask, render_template, request

app = Flask(__name__)


conversion_rates = {
    'USD': 1.0,
    'EUR': 0.83,
    'GBP': 0.72,
    'JPY': 109.44,
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        from_currency = request.form['from_currency']
        to_currency = request.form['to_currency']
        conversion_rate = conversion_rates[to_currency] / conversion_rates[from_currency]
        converted_amount = amount * conversion_rate
        return render_template('index.html', converted_amount=converted_amount)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5002)
