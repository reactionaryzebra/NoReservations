# NoReservations-Flask-API

## Intro
This is an API serving the NoReservations app which can be found on my project partner Ethan Kaplan's Github [here](https://github.com/ethankaplan/NoReservations-React-Frontend).
The API was written RESTfully using Python and Flask.

## Endpoints

* api/v1/restaurants
  * A GET resuest to this endpoint will return a list of restaurants as a JSON object resembling:
  * [{
      "id": "1",
      
      "name": "Bestia",
      
      "cuisine": "Italian",
      
      "url": "http://www.bestia.com",
      
      "image_url": "http://www.images.com/bestia.jpg",
      
      "address": "1 main st\nLos Angeles, CA 90012",
      
      "phone": "(111)111-1111"
      
      }, ...]
      
* api/v1/restaurants/<restaurant_id>
  * A GET request to this endpoint will return a single restaurant as a JSON object in the same format as above

* api/v1/reservations
  * A GET request to this endpoint takes the following arguments as query strings:
    * api/v1/reservations?user_id={id}
      * This will return a list of all reservations being sold or bought by a particular user
    * api/v1/reservations?restaurant_id={id}
      * This will return a list of all reservations made at a particular restaurant
    * api/v1/reservations?restaurant_id={id}&date={YYYY-MM-DD}
      * This will return a list of all reservations made at a particular restaurant at a particular date
