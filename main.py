import folium
import pandas as pd

data = pd.read_csv('locations.csv',
                   error_bad_lines=False)
movies = data['movie']
years = data['year']
add_info = data['add_info']
location = data['location']

city_data = pd.read_csv('worldcities.csv',
                        error_bad_lines=False)
cities = city_data['city_ascii']
lt = city_data['lat']
ln = city_data['lng']

def main():
    """
    Main code part
    """
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
        if years[i] == year:
            try:
                if years[i] == year:
                    coords = locator(location[i])
                    lt = coords[0]
                    ln = coords[1]
                    dif = difference(user_lt, user_ln, lt, ln)
                    locations.append((dif, i, lt, ln))
            except:
                pass
        i += 1
    # Sort by increasing
    z = i
    # The amount below can be changed
    for i in range(z, 30000):
        try:
            locations.sort()
            if years[i] == year:
                coords = locator(location[i])
                lt = coords[0]
                ln = coords[1]
                dif = difference(user_lt, user_ln, lt, ln)
                old_dif = locations[9][0]
                if dif < old_dif:
                    locations[9] = (dif, i, lt, ln)
        except:
            pass

    map = folium.Map(location=[user_lt, user_ln],
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
                                            radius=20,
                                            popup=name + "\n",
                                            fill_color='red',
                                            color='red',
                                            fill_opacity=0.5))

        infos.add_child(folium.CircleMarker(location=[lt, ln],
                                            radius=18,
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
    (51.5000, -0.1167)
    """
    for x in range(15490):
        if cities[x] in name:
            return(lt[x], ln[x])


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
