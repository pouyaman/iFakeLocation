#! /usr/bin/python3

#    7-Eleven Python implementation. This program allows you to lock in a fuel price from your computer.
#    Copyright (C) 2019  Freyta
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <https://www.gnu.org/licenses/>.

# Used for requests to the price check script and for 7-Eleven stores
import requests, json
# Functions used for getting the OS environments from settings.py
import settings, os

'''''''''''''''''''''''''''
You can set or change any these environmental variables in settings.py
'''''''''''''''''''''''''''
PRICE_URL = os.getenv('PRICE_URL',settings.PRICE_URL)
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0"

fuel_types_dict = {
    'E10': 0,
    'U91': 1,
    'U95': 2,
    'U98': 3,
    'DSL': 4,
    'LPG': 5
}

def cheapestFuelAll():
    # Just a quick way to get fuel prices from a website that is already created.
    # Thank you to master131 for this.
    r = requests.get(PRICE_URL, headers={"user-agent":USER_AGENT})
    response = json.loads(r.text)

    # E10
    session['postcode0'] = response['regions'][0]['prices'][0]['postcode']
    session['price0']    = response['regions'][0]['prices'][0]['price']

    # Unleaded 91
    session['postcode1'] = response['regions'][0]['prices'][1]['postcode']
    session['price1']    = response['regions'][0]['prices'][1]['price']

    # Unleaded 95
    session['postcode2'] = response['regions'][0]['prices'][2]['postcode']
    session['price2']    = response['regions'][0]['prices'][2]['price']

    # Unleaded 98
    session['postcode3'] = response['regions'][0]['prices'][3]['postcode']
    session['price3']    = response['regions'][0]['prices'][3]['price']

    # Diesel
    session['postcode4'] = response['regions'][0]['prices'][4]['postcode']
    session['price4']    = response['regions'][0]['prices'][4]['price']

    # LPG
    session['postcode5'] = response['regions'][0]['prices'][5]['postcode']
    session['price5']    = response['regions'][0]['prices'][5]['price']

def cheapestFuel(fueltype):
    # Gets the cheapest fuel price for a certain type of fuel and the postcode
    # This is used for the automatic lock in
    r = requests.get(PRICE_URL, headers={"user-agent":USER_AGENT})
    response = json.loads(r.text)
    '''
    52 = Unleaded 91
    53 = Diesel
    54 = LPG
    55 = Unleaded 95
    56 = Unleaded 98
    57 = E10
    '''
    if(fueltype == "52"):
        fueltype = 1
    if(fueltype == "53"):
        fueltype = 4
    if(fueltype == "54"):
        fueltype = 5
    if(fueltype == "55"):
        fueltype = 2
    if(fueltype == "56"):
        fueltype = 3
    if(fueltype == "57"):
        fueltype = 0

    # Get the postcode and price
    postcode  = response['regions'][0]['prices'][fueltype]['postcode']
    price     = response['regions'][0]['prices'][fueltype]['price']
    latitude  = response['regions'][0]['prices'][fueltype]['lat']
    longitude = response['regions'][0]['prices'][fueltype]['lng']
    return postcode, price, latitude, longitude

def lockedPrices():
    # This function is used for getting our locked in fuel prices to display on the main page

    # Remove all of our previous error messages
    session.pop('ErrorMessage', None)


if __name__ == '__main__':
    print("This should be run through app.py")
