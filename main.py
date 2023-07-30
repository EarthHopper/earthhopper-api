import os
import openai
from dotenv import load_dotenv
import pprint
import json
import googlemaps
import pprint
from fastapi import FastAPI
load_dotenv()

app = FastAPI()
maps_key = os.getenv("GOOGLE_MAPS")

gmaps = googlemaps.Client(key=maps_key)

def search_place(query):
    places = gmaps.places(query)

    return places["results"]

openai.api_key = os.getenv("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")

@app.get("/itinerary")
async def generate_itinerary(city: str, days_staying: int):
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f'You are the API of an eco-conscious travel company. Give me, in JSON format, a travel itinerary for a user traveling to {city} and arriving at {city} airport. Give me the carbon emissions in kgs that each activity has, and give me the exact hourly schedule. This user is staying for 2 days, his arrival being at 12:00PM. The JSON should only have 3 fields: the "itinerary" field, which is a list of dictionaries each containing an activity, the start time, and the carbon emissions, the field "carbon_emissions" with the numerical value of the total carbon emissions by the traveler in kgs, and the "normal_emissions" field, that has the carbon emissions comparison in kgs that a normal, non-eco-friendly traveler would produce.  Include a field named "hotel" that has the name of a popular hotel located in {city}. Also, in the list of activities, include when the user goes to sleep and wakes up if there is a next day. Give me a max of 6 activities. DO NOT write "Popular hotel". Write a real hotel name.'}
    ]
    )
    response = json.loads(completion.choices[0].message["content"])
    places_to_visit = []
    for activity in response["itinerary"]:
        place = activity["activity"] + f" in {city}"
        place_location = search_place(place)[0]
        places_to_visit.append({"place_name": place_location["name"], "place_coordinates": place_location["geometry"]["location"]})
    final_response = {"recommendations": response["itinerary"], "locations": places_to_visit, "earthhopper_emissions": response["carbon_emissions"], "average_emissions": response["normal_emissions"], "hotel_recommendation": response["hotel"]}
    return final_response
