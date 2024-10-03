from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Função para coletar dados de uma API financeira pública e criptomoedas
def get_market_data():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    data = response.json()

    # Filtrar apenas USD, BRL, EUR
    filtered_data = {key: data['rates'][key] for key in ['USD', 'BRL', 'EUR'] if key in data['rates']}

    # Adicionar informações de BTC e ETH usando a CoinGecko API
    crypto_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    crypto_response = requests.get(crypto_url)
    crypto_data = crypto_response.json()

    # Adicionar criptomoedas
    filtered_data['BTC'] = crypto_data['bitcoin']['usd']
    filtered_data['ETH'] = crypto_data['ethereum']['usd']

    return filtered_data

@app.route('/', methods=['GET', 'POST'])
def index():
    data = get_market_data()
    converted_value = None

    # Se o método for POST, significa que um valor foi inserido para conversão
    if request.method == 'POST':
        input_value = float(request.form['amount'])
        currency_from = request.form['currency_from']
        currency_to = request.form['currency_to']
        
        # Converter o valor da moeda de origem para a moeda de destino
        converted_value = input_value * data[currency_to] / data[currency_from]
        
    return render_template('index.html', data=data, converted_value=converted_value)

if __name__ == "__main__":
    app.run(debug=True)