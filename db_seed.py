import requests
import config

restaurants = [{
    "name": "Le Comptoir",
    "url": "https://www.lecomptoirla.com/"
}, {
    "name": "Perch",
    "url": "https://perchla.com/"
}, {
    "name": "Bestia",
    "url": "https://bestiala.com/"
}, {
    "name": "Majordomo",
    "url": "https://www.majordomo.la/"
}, {
    "name": "Providence",
    "url": "https://providencela.com/"
}, {
    "name": "Sushi Ginza Onodera",
    "url": "https://onodera-group.com/sushi-la/"
}, {
    "name": "Spago",
    "url": "https://wolfgangpuck.com/dining/spago-2/"
}, {
    "name": "CUT",
    "url": "https://wolfgangpuck.com/dining/cut-beverly-hills/"
}, {
    "name": "El Cid",
    "url": "https://www.elcidsunset.com/"
}, {
    "name": "Nobu",
    "url": "https://www.noburestaurants.com/losangeles/home/"
}, {
    "name": "n/naka",
    "url": "https://n-naka.com/"
}, {
    "name": "Trois Familia",
    "url": "https://www.troisfamilia.com/"
}, {
    "name": "Catch",
    "url": "https://catchrestaurants.com/catchla/"
}, {
    "name": "Jon and Vinny",
    "url": "https://www.jonandvinnys.com/"
}, {
    "name": "Felix",
    "url": "https://felixla.com/"
}, {
    "name": "Kismet",
    "url": "https://www.kismetlosangeles.com/"
}, {
    "name": "Orsa and Winston",
    "url": "http://www.orsaandwinston.com/home/"
}, {
    "name": "71above",
    "url": "https://www.71above.com/"
}, {
    "name": "Bavel",
    "url": "https://baveldtla.com/"
}, {
    "name": "Broken Spanish",
    "url": "https://brokenspanish.com/"
}, {
    "name": "Otium",
    "url": "https://otiumla.com/"
}, {
    "name": "The Exchange",
    "url": "https://freehandhotels.com/los-angeles/the-exchange/"
}, {
    "name": "Best Girl",
    "url": "https://www.bestgirldtla.com/"
}, {
    "name": "Maude",
    "url": "https://www.mauderestaurant.com/"
}, {
    "name": "Mastro's Ocean Club",
    "url": "https://www.mastrosrestaurants.com/"
}, {
    "name": "Chateau Marmont",
    "url": "http://www.chateaumarmont.com/therestaurant.php"
}, {
    "name": "Gjelina",
    "url": "https://www.gjelina.com/"
}, {
    "name": "Hatchet Hall",
    "url": "https://www.hatchethallla.com/"
}]

for restaurant in restaurants:
    data = requests.get('https://api.yelp.com/v3/businesses/search?term={term}&location=Los Angeles&limit=1'.format(
        term=restaurant['name']), headers={"Authorization": "Bearer {}".format(config.YELP_KEY)})
    parsed_data = data.json()
    restaurant['image_url'] = parsed_data['businesses'][0]['image_url']
    restaurant['address'] = parsed_data['businesses'][0]['location']['display_address']
    restaurant['phone'] = parsed_data['businesses'][0]['display_phone']
    restaurant['cuisine'] = parsed_data['businesses'][0]['categories'][0]['title']

print(restaurants)
