import os
import json
import constants
import raindrop
import todoist

# Function to construct the correct path based on the script's location
def get_file_path(filename):
    script_directory = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(script_directory, filename)

# Adds the new bookmarks to the archive
def updateArchive(filtered_bookmarks, processed_data):
    archive_path = get_file_path(constants.ARCHIVEFILENAME)

    processed_data['items'].extend(filtered_bookmarks)
    with open(archive_path, 'w') as archive:
        json.dump(processed_data, archive, indent=4)

# Finds the new bookmarks
def findNewBookmarks(response_json):
    processed_titles, processed_links, processed_data = filterOldBookmarks()
    filtered_bookmarks = [article for article in response_json['items'] if article['title']
                         not in processed_titles or article['link'] not in processed_links]
    return filtered_bookmarks, processed_data

# Filters bookmarks that have already been processed
def filterOldBookmarks():
    archive_path = get_file_path(constants.ARCHIVEFILENAME)

    processed_data = {}  # Initialize processed_data
    try:
        with open(archive_path, 'r') as processed_file:
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