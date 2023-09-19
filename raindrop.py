import requests
import constants

# Retrieves the raindrop.io bookmarks
def retrieveRainDrops():
    try:
        response = requests.get(constants.GETRAINDROPURL, headers=constants.GETRAINDROPURLHEADERS)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error code %s" % response.status_code)
    except requests.exceptions.RequestException as e:
        print(e)

