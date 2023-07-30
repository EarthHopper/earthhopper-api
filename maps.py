import googlemaps
import pprint

API_KEY = 'AIzaSyDlp2yGurVp3IJV_st_XlBkQxur47ScIpM'

gmaps = googlemaps.Client(key=API_KEY)

def search_place(query):
    places = gmaps.places(query)

    return places["results"]

if __name__ == "__main__":
    search_query = input("Enter a place you want to search for: ")
    pprint.pprint({"name": search_place(search_query)[0]})