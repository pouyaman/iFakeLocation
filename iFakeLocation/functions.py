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
    fuel_info = {}

    # Just a quick way to get fuel prices from a website that is already created.
    # Thank you to master131 for this.
    r = requests.get(PRICE_URL, headers={"user-agent":USER_AGENT})
    response = json.loads(r.text)

    # E10
    fuel_info['E10'] = {}
    fuel_info['E10']['price']    = response['regions'][0]['prices'][0]['price']
    fuel_info['E10']['suburb']   = response['regions'][0]['prices'][0]['suburb']
    fuel_info['E10']['state']    = response['regions'][0]['prices'][0]['state']
    fuel_info['E10']['postcode'] = response['regions'][0]['prices'][0]['postcode']

    # Unleaded 91
    fuel_info['U91'] = {}
    fuel_info['U91']['price']    = response['regions'][0]['prices'][1]['price']
    fuel_info['U91']['suburb']   = response['regions'][0]['prices'][1]['suburb']
    fuel_info['U91']['state']    = response['regions'][0]['prices'][1]['state']
    fuel_info['U91']['postcode'] = response['regions'][0]['prices'][1]['postcode']

    # Unleaded 95
    fuel_info['U95'] = {}
    fuel_info['U95']['price']    = response['regions'][0]['prices'][2]['price']
    fuel_info['U95']['suburb']   = response['regions'][0]['prices'][2]['suburb']
    fuel_info['U95']['state']    = response['regions'][0]['prices'][2]['state']
    fuel_info['U95']['postcode'] = response['regions'][0]['prices'][2]['postcode']

    # Unleaded 98
    fuel_info['U98'] = {}
    fuel_info['U98']['price']    = response['regions'][0]['prices'][3]['price']
    fuel_info['U98']['suburb']   = response['regions'][0]['prices'][3]['suburb']
    fuel_info['U98']['state']    = response['regions'][0]['prices'][3]['state']
    fuel_info['U98']['postcode'] = response['regions'][0]['prices'][3]['postcode']

    # Diesel
    fuel_info['Diesel'] = {}
    fuel_info['Diesel']['price']    = response['regions'][0]['prices'][4]['price']
    fuel_info['Diesel']['suburb']   = response['regions'][0]['prices'][4]['suburb']
    fuel_info['Diesel']['state']    = response['regions'][0]['prices'][4]['state']
    fuel_info['Diesel']['postcode'] = response['regions'][0]['prices'][4]['postcode']

    # LPG
    fuel_info['LPG'] = {}
    fuel_info['LPG']['price']    = response['regions'][0]['prices'][5]['price']
    fuel_info['LPG']['suburb']   = response['regions'][0]['prices'][5]['suburb']
    fuel_info['LPG']['state']    = response['regions'][0]['prices'][5]['state']
    fuel_info['LPG']['postcode'] = response['regions'][0]['prices'][5]['postcode']
    return fuel_info, response

def cheapestFuelLocation(fueltype="U91", response=None):
    # Gets the cheapest fuel price for a certain type of fuel and the postcode
    # This is used for the automatic lock in

    assert fueltype in fuel_types_dict, "%s is not acceptable fuel type!" %fueltype
    f = fuel_types_dict[fueltype]

    if response is None:
        r = requests.get(PRICE_URL, headers={"user-agent":USER_AGENT})
        response = json.loads(r.text)

    # Get the postcode and price
    # price     = response['regions'][0]['prices'][f]['price']
    suburb    = response['regions'][0]['prices'][f]['suburb']
    state     = response['regions'][0]['prices'][f]['state']
    postcode  = response['regions'][0]['prices'][f]['postcode']
    location = "%s %s %s" %(suburb, state, postcode)
    return location

def print_fuel_dict(fuels_dict):
    style = "{:7} {:5} {:25} {:<6} {:<9}\r\n" #'Type', 'Price', 'Suburb', 'State', 'Postcode'
    msg = style.format('Type', 'Price', 'Suburb', 'State', 'Postcode')
    for f in fuels_dict:
        msg += style.format(f,
                            fuels_dict[f]['price'],
                            fuels_dict[f]['suburb'],
                            fuels_dict[f]['state'],
                            fuels_dict[f]['postcode'])
    return msg


if __name__ == '__main__':
    print("This should be run through an app")
