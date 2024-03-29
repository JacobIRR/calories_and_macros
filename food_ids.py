"""
# this is a list of food IDs from this API:
# https://ndb.nal.usda.gov/ndb/doc/index#
# https://ndb.nal.usda.gov/ndb/foods/show/01129?fgcd=&manu=&format=&count=&max=25&offset=&sort=default&order=asc&qlookup=HARD+BOILED+EGGS%2C+UPC%3A+812324023081&ds=&qt=&qp=&qa=&qn=&q=&ing=

0lIAZDhVt4xweOX3fbjBwUJCd6zZedU2Gh9wEDaX

You can start using this key to make web service requests. Simply pass your key in the URL when making a web request. Here's an example:

https://developer.nrel.gov/api/alt-fuel-stations/v1/nearest.json?api_key=0lIAZDhVt4xweOX3fbjBwUJCd6zZedU2Gh9wEDaX&location=Denver+CO
For additional support, please contact us. When contacting us, please tell us what API you're accessing and provide the following account details so we can quickly find you:

Account Email: jackobefranklin@gmail.com
Account ID: e38cc161-4e49-469e-abe5-34052aa44b35

search here:
https://ndb.nal.usda.gov/ndb/doc/apilist/API-SEARCH.md
example:
https://api.nal.usda.gov/ndb/search/?format=json&q=butter&sort=n&max=25&offset=0&api_key=0lIAZDhVt4xweOX3fbjBwUJCd6zZedU2Gh9wEDaX


once searched, use ids here in this API:
https://ndb.nal.usda.gov/ndb/doc/apilist/API-FOOD-REPORTV2.md
example:
https://api.nal.usda.gov/ndb/V2/reports?ndbno=01009&ndbno=01009&ndbno=45202763&ndbno=35193&type=b&format=json&api_key=DEMO_KEY

sample response:
{'api': 2.0,
 'count': 1,
 'foods': [{'food': {'desc': {'ds': 'Label Insight',
                              'manu': 'Wilcox Farms Inc.',
                              'name': 'WILCOX, ORGANIC HARD-BOILED EGGS, UPC: '
                                      '074483990011',
                              'ndbno': '45028794',
                              'ru': 'g'},
                     'footnotes': [],
                     'ing': {'desc': 'ORGANIC EGGS.', 'upd': '07/14/2017'},
                     'nutrients': [{'derivation': 'LCCS',
                                    'group': 'Proximates',
                                    'measures': [{'eqv': 45.0,
                                                  'eunit': 'g',
                                                  'label': 'EGGS',
                                                  'qty': 1.0,
                                                  'value': '70'}],
                                    'name': 'Energy',
                                    'nutrient_id': '208',
                                    'unit': 'kcal',
                                    'value': '156'},
                                   {'derivation': 'LCCS',
                                    'group': 'Proximates',
                                    'measures': [{'eqv': 45.0,
                                                  'eunit': 'g',
                                                  'label': 'EGGS',
                                                  'qty': 1.0,
                                                  'value': '6.00'}],
                                    'name': 'Protein',
                                    'nutrient_id': '203',
                                    'unit': 'g',
                                    'value': '13.33'},
                                   {'derivation': 'LCCS',
                                    'group': 'Proximates',
                                    'measures': [{'eqv': 45.0,
                                                  'eunit': 'g',
                                                  'label': 'EGGS',
                                                  'qty': 1.0,
                                                  'value': '4.50'}],
                                    'name': 'Total lipid (fat)',
                                    'nutrient_id': '204',
                                    'unit': 'g',
                                    'value': '10.00'},
                                   {'derivation': 'LCCS',
                                    'group': 'Proximates',
                                    'measures': [{'eqv': 45.0,
                                                  'eunit': 'g',
                                                  'label': 'EGGS',
                                                  'qty': 1.0,
                                                  'value': '1.00'}],
                                    'name': 'Carbohydrate, by difference',
                                    'nutrient_id': '205',
                                    'unit': 'g',
                                    'value': '2.22'},
                                   {'derivation': 'LCCD',
                                    'group': 'Proximates',
                                    'measures': [{'eqv': 45.0,
                                                  'eunit': 'g',
                                                  'label': 'EGGS',
                                                  'qty': 1.0,
                                                  'value': '0.0'}],
                                    'name': 'Fiber, total dietary',
                                    'nutrient_id': '291',
                                    'unit': 'g',
                                    'value': '0.0'},
                                   {'derivation': 'LCCS',
                                    'group': 'Proximates',
                                    'measures': [{'eqv': 45.0,
                                                  'eunit': 'g',
                                                  'label': 'EGGS',
                                                  'qty': 1.0,
                                                  'value': '0.00'}],
                                    'name': 'Sugars, total',
                                    'nutrient_id': '269',
                                    'unit': 'g',
                                    'value': '0.00'},
                                   {'derivation': 'LCCD',
                                    'group': 'Minerals',
                                    'measures': [{'eqv': 45.0,
                                                  'eunit': 'g',
                                                  'label': 'EGGS',
                                                  'qty': 1.0,
                                                  'value': '20'}],
                                    'name': 'Calcium, Ca',
                                    'nutrient_id': '301',
                                    'unit': 'mg',
                                    'value': '44'},
                                   {'derivation': 'LCCD',
                                    'group': 'Minerals',
                                    'measures': [{'eqv': 45.0,
                                                  'eunit': 'g',
                                                  'label': 'EGGS',
                                                  'qty': 1.0,
                                                  'value': '0.72'}],
                                    'name': 'Iron, Fe',
                                    'nutrient_id': '303',
                                    'unit': 'mg',
                                    'value': '1.60'},
                                   {'derivation': 'LCCS',
                                    'group': 'Minerals',
                                    'measures': [{'eqv': 45.0,
                                                  'eunit': 'g',
                                                  'label': 'EGGS',
                                                  'qty': 1.0,
                                                  'value': '65'}],
                                    'name': 'Sodium, Na',
                                    'nutrient_id': '307',
                                    'unit': 'mg',
                                    'value': '144'},
                                   {'derivation': 'LCCD',
                                    'group': 'Vitamins',
                                    'measures': [{'eqv': 45.0,
                                                  'eunit': 'g',
                                                  'label': 'EGGS',
                                                  'qty': 1.0,
                                                  'value': '0.0'}],
                                    'name': 'Vitamin C, total ascorbic acid',
                                    'nutrient_id': '401',
                                    'unit': 'mg',
                                    'value': '0.0'},
                                   {'derivation': 'LCCD',
                                    'group': 'Vitamins',
                                    'measures': [{'eqv': 45.0,
                                                  'eunit': 'g',
                                                  'label': 'EGGS',
                                                  'qty': 1.0,
                                                  'value': '300'}],
                                    'name': 'Vitamin A, IU',
                                    'nutrient_id': '318',
                                    'unit': 'IU',
                                    'value': '667'},
                                   {'derivation': 'LCCS',
                                    'group': 'Lipids',
                                    'measures': [{'eqv': 45.0,
                                                  'eunit': 'g',
                                                  'label': 'EGGS',
                                                  'qty': 1.0,
                                                  'value': '1.498'}],
                                    'name': 'Fatty acids, total saturated',
                                    'nutrient_id': '606',
                                    'unit': 'g',
                                    'value': '3.330'},
                                   {'derivation': 'LCCS',
                                    'group': 'Lipids',
                                    'measures': [{'eqv': 45.0,
                                                  'eunit': 'g',
                                                  'label': 'EGGS',
                                                  'qty': 1.0,
                                                  'value': '0.000'}],
                                    'name': 'Fatty acids, total trans',
                                    'nutrient_id': '605',
                                    'unit': 'g',
                                    'value': '0.000'},
                                   {'derivation': 'LCCS',
                                    'group': 'Lipids',
                                    'measures': [{'eqv': 45.0,
                                                  'eunit': 'g',
                                                  'label': 'EGGS',
                                                  'qty': 1.0,
                                                  'value': '215'}],
                                    'name': 'Cholesterol',
                                    'nutrient_id': '601',
                                    'unit': 'mg',
                                    'value': '478'}],
                     'sr': 'July, 2018',
                     'type': 'b'}}],
 'notfound': 0}

"""

FOOD_IDS = {
    "Boiled Egg": "45028794",
    "Bacon": "45172471",
    "Good Seed bread": "45027285",
    "Pineapple": "45226422",
    "Avocado": "09038",
    "Chicken Breast": "45257607",
    "Spinach": "45279549",
    "Mixed Nuts": "45274471",
    "Sweet Potato": "45215980",
    "Salmon": "45202301",
    "Brown Rice": "45009665",
    "Green Peas": "45209733",
    "Whole Milk": "45192730",
    # "Mass Gainer powder": "",  -  needs its own obj....
}

API_KEY = '0lIAZDhVt4xweOX3fbjBwUJCd6zZedU2Gh9wEDaX'

# Make this a struct/class/const ?
NUTRIENT_IDS = {
    'protein': '203',
    'fat': '204',
    'carbs': '205'
}
