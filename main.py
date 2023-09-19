import json
import constants
from . import raindrop, todoist

# Adds the new bookmarks to the archive
def updateArchive(filtered_bookmarks, processed_data):
    processed_data['items'].extend(filtered_bookmarks)
    with open(constants.ARCHIVEPATH, 'w') as archive:
        json.dump(processed_data, archive, indent=4)

# Finds the new bookmarks
def findNewBookmarks(response_json):
    processed_titles, processed_links, processed_data = filterOldBookmarks()
    filtered_bookmarks = [article for article in response_json['items'] if article['title']
                         not in processed_titles or article['link'] not in processed_links]
    return filtered_bookmarks, processed_data

# Filters bookmarks that have already been processed
def filterOldBookmarks():
    try:
        with open(constants.ARCHIVEPATH, 'r') as processed_file:
            processed_data = json.load(processed_file)
            processed_titles = {item['title']
                                for item in processed_data['items']}
            processed_links = {item['link']
                               for item in processed_data['items']}
    except FileNotFoundError:
        processed_titles = set()
        processed_links = set()
    return processed_titles, processed_links, processed_data


def main():
    response_json = raindrop.retrieveRainDrops()
    bookmarks, data = findNewBookmarks(response_json)
    if todoist.createTasks(bookmarks):
        updateArchive(bookmarks, data)


if __name__ == "__main__":
    main()
