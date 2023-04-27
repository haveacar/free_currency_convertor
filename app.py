import os
from datetime import datetime
import requests as requests
from flask import Flask, render_template, request, json

# api key and request url
API_KEY = "c66xOBOerxjgjCqRfbT3MzvIIqMoDm6e"
REQUEST_URL = "https://api.apilayer.com/fixer/latest?base=USD"

# path
CURRENT_PATH = os.path.dirname(__file__)
CURRENT_PATCH_JASON = os.path.join(CURRENT_PATH, "static")


class Currency:
    '''Currency convertor'''

    def __init__(self):
        pass

    def currency_convector(self):

        def receive_data():
            """
            Receive_data func check
            :return:  dict(collected_rates) or False
            """
            try:
                # receive data
                response_data = requests.get(REQUEST_URL, headers={"UserAgent": "XY", "apikey": API_KEY})
                collected_rates = json.loads(response_data.text)
                if collected_rates.get("success") == True: return collected_rates

            except:
                return False

        def reload_rates() -> dict:
            """
            Func Reload_data checks date from file
            if date!= date.now try upload
            :return: dict (rates), str(date)
            """
            time_now = datetime.now().strftime("%Y-%m-%d")
            # open rates from file
            with open(os.path.join(CURRENT_PATCH_JASON, "data_rates.json")) as f:
                rates_from_file = json.load(f)
            rates = rates_from_file

            # check from file current date
            if rates_from_file.get("date") != time_now:
                print("Uploading Data")
                rates = receive_data()

                # cannot receive data
                if rates == False:
                    print("Cannot update")
                    rates = rates_from_file
                else:
                    print("Uploading successful")
                    # create file
                    with open(os.path.join(CURRENT_PATCH_JASON, "data_rates.json"), "w") as f:
                        json.dump(rates, f, indent=4)
                        pass
            return rates

        all_rates = reload_rates()

        return all_rates


app = Flask(__name__)
conversion_rates = Currency()

# get current data rates
data = conversion_rates.currency_convector().get("date")
# list comprehension of keys rates
currencies = [key for key in conversion_rates.currency_convector().get("rates")]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        amount = float(request.form['amount'])
        from_currency = request.form['from_currency']
        to_currency = request.form['to_currency']
        # get conversion rate
        conversion_rate = conversion_rates.currency_convector().get("rates")[to_currency] / \
                          conversion_rates.currency_convector().get("rates")[from_currency]
        converted_amount = round(amount * conversion_rate, 2)
        # return template rates
        return render_template('index.html', data=data, amount=amount, from_currency=from_currency + " =",
                               converted_amount=converted_amount, to_currency=to_currency, currencies=currencies)
    else:
        return render_template('index.html', data=data, currencies=currencies)


if __name__ == '__main__':
    app.run(debug=True, port=5002)
