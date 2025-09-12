import requests

def get_weather(city="kathmandu"):
    try: 
        url = f"https://wttr.in/{city}?format=3"
        res = requests.get(url)
        if res.status_code == 200:
            return res.text.strip()
        else:
            return f"Could not get weather for {city}."
    except Exception as e:
        return f"Weather tool error: {str(e)}"
    

def get_exchange_rate(from_currency="USD", to_currency="CAD"):
    try:
        url = f"https://api.frankfurter.app/latest?from={from_currency}&to={to_currency}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            rate = data['rates'].get(to_currency)
            if rate:
                return f"1 {from_currency} = {rate} {to_currency}"
            else:
                return f"Could not get exchange rate for {from_currency} to {to_currency}."
        else:
            return f"Exchange rate API error."
    except Exception as e:
        return f"Exchange rate tool error: {str(e)}"
    

