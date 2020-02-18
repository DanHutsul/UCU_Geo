import folium
import pandas as pd

data = pd.read_csv('D:/Da/UCU/OP_2020/19.02/locations.csv',
                   error_bad_lines=False)
movies = data['movie']
years = data['year']
add_info = data['add_info']
location = data['location']


def main():
    """
    Main code part
    """
    print("Warning! Geopy method can have errors due to the\
           strain on the server")
    year = input("Please enter a year you would like to have a map for: ")
    coord = input("Please enter your location (format: lat, long): ")
    user_lt = coord.split(", ")[0]
    user_ln = coord.split()[1]
    # Create an empty list
    # Fill that list
    # (Difference, Index, latitude, longitude)
    # If list is full change the furthest location to the closest
    print("Please wait")
    locations = []
    i = 0
    while len(locations) <= 10:
        try:
            coords = locator(location[i])
            print(coords)
            lt = coords[0]
            ln = coords[1]
            dif = difference(user_lt, user_ln, lt, ln)
            if years[i] == year:
                locations.append((dif, i, lt, ln))
            i += 1
        except:
            pass
    # Sort by increasing
    z = i
    try:
        for i in range(z, 1000):
            locations.sort()
            coords = locator(location[i])
            print(coords)
            lt = coords[0]
            ln = coords[1]
            dif = difference(user_lt, user_ln, lt, ln)
            old_dif = locations[9][0]
            if dif < old_dif:
                locations[9] = (dif, i, lt, ln)
    except:
        pass

    map = folium.Map(location=[48.314775, 25.082925],
                     zoom_start=10)

    films = folium.FeatureGroup(name="Films")
    infos = folium.FeatureGroup(name="Additional info")
    for item in locations:
        lt = item[2]
        ln = item[3]
        index = item[1]
        name = movies[index]
        info = add_info[index]
        films.add_child(folium.CircleMarker(location=[lt, ln],
                                            radius=11,
                                            popup=name + "\n",
                                            fill_color='red',
                                            color='red',
                                            fill_opacity=0.5))

        infos.add_child(folium.CircleMarker(location=[lt, ln],
                                            radius=10,
                                            popup=info + "\n",
                                            fill_color='white',
                                            color='white',
                                            fill_opacity=0.2))

    map.add_child(infos)
    map.add_child(films)
    map.add_child(folium.LayerControl())
    map.save(year + '_map.html')
    print("Done!")
    print("Saved as " + year + "_map.html")


def locator(name):
    """ str -> tuple
    Finds the latitude and longtitude of the location
    >>> locator("London")
    (51.5074, 0.1278)
    """
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    from geopy.extra.rate_limiter import RateLimiter
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1,
                          max_retries=20)
    # Error occurs below
    location = geocode(name, timeout=None)
    lt = location.latitude
    ln = location.longitude
    return (lt, ln)


def difference(user_lt, user_ln, lt, ln):
    """int, int, int, int -> int
    Finds the summarical difference of inputted coordinates and city`s coordinates
    >>> difference(1.00, 1.00, 1.00, 1.00)
    0.0
    """
    # Finding difference in latitude
    dif_lt = float(user_lt) - lt
    if dif_lt < 0:
        dif_lt = -1*dif_lt
    # Finding difference in longitude
    dif_ln = float(user_ln) - ln
    if dif_ln < 0:
        dif_ln = -1*dif_ln
    dif_sum = dif_ln + dif_lt
    return dif_sum


if __name__ == "__main__":
    main()
