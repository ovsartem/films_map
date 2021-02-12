import pandas as pd
import haversine
from geopy import Nominatim
import folium


def shortten(coordinate):
    """
    Helper function to reduce the place if get_coordinate
    isn't able to find it's coordinates
    """
    edited = coordinate.split(',')
    edited.pop(0)
    return ", ".join(edited)


def get_coordinate(coordinate):
    """
    Gets the coordinates of the place
    """
    flag = False
    while flag == False:
        try:
            geolocator = Nominatim(user_agent='artmanlike').geocode(coordinate)
            location = (geolocator.latitude, geolocator.longitude)
            flag = True
        except AttributeError:
            coordinate = shortten(coordinate)
    return location


def find_city(coordinates):
    """
    Finds the country
    """
    geolocator = Nominatim(user_agent="artmanlike")
    return geolocator.reverse(coordinates, language='en')[-2].split(",")[-1]


def get_distance(coord1, coord2):
    """
    Finds the distance between user place and films recorded nearby
    """
    return haversine.haversine(coord1, coord2)


def data(year, latitude, longitude, df):
    """
    Creates dataset of the closest films
    """
    coordinates = (latitude, longitude)
    place = find_city(coordinates)
    df = df[df["year"] == year]
    df = df[df["place"].str.contains(place) == True]
    df["coordinates"] = df["place"].apply(lambda x: get_coordinate(x))
    df.drop_duplicates(subset='coordinates', keep='first', inplace=True)
    df["distance"] = df.coordinates.apply(
        lambda x: get_distance(x, coordinates))
    df.sort_values(by='distance', ascending=True)
    return df[:10]


def map_creator(example, coords):
    """
    Generates the map
    """
    film_map = folium.Map(
        location=coords, tiles='cartodbpositron', zoom_start=9)
    folium.TileLayer('stamenterrain').add_to(film_map)
    film_map.add_child(folium.Marker(location=[
                       coords[0], coords[1]], popup="your location", icon=folium.Icon(color='darkblue', icon_color='white', icon='male', angle=0, prefix='fa')))
    for i in range(len(example)):
        market = example.iloc[i]
        data = list(market.iloc())
        film_map.add_child(folium.Marker(
            location=[data[3][0], data[3][1]], popup=data[0], icon=folium.Icon()))
    return film_map.save('Map_1.html')


if __name__ == '__main__':
    df = pd.read_csv("filtered_data.csv")
    year = int(input("Type the year: "))
    latitude = float(input("Type the latitude: "))
    longitude = float(input("Type the longitude: "))
    example = data(year, latitude, longitude, df)
    map_creator(example, (latitude, longitude))
    print("Check Map_1.html")
