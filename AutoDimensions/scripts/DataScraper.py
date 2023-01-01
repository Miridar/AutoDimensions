import requests
import os
import time
import webbrowser
from bs4 import BeautifulSoup

# Set the number of pages of the forum you want to scrape
number_of_pages = 39

# Set the URL of the forum you want to scrape
#forum_url = "https://forum.freecadweb.org/viewforum.php?f=35"
forum_url = "https://forum.freecadweb.org/viewforum.php?f=24"

# For cycle that goes through all the pages of the forum, each page has 25 topics
for i in range(0, number_of_pages):

    # Set the URL of the current page
    url = forum_url + "&start=" + str(i*25)
    domain = url.split("/viewforum.php")[0]

    # Set the directory where you want to save the .FCStd files and create the directory if it does not exist
    save_directory = "Desktop\Models"
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Send a request to the URL and get the HTML content
    response = requests.get(url)
    html = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Find all the links that contain '/viewtopic.php?f' and do not contain '&start=' or '&p='
    links = soup.find_all("a", href=lambda x: x is not None and "/viewtopic.php?f=" in x and "&t=" in x and "&start=" not in x and "&p=" not in x)

    # Extract the href values from the Tag objects
    page_urls = [link['href'] for link in links]

    # Remove duplicate href values from the list
    page_urls = list(set(page_urls))

    download_links = []
    # Iterate over the links and get the HTML content of each page
    for page_url in page_urls:
        # wait for 1 second to avoid overloading the server
        time.sleep(1)

        # Replace the first character of the URL with 'https://forum.freecadweb.org' to get the full URL
        page_url = domain + page_url[1:]
        print(page_url)
    
        # Send a request to the URL and get the HTML content
        page_response = requests.get(page_url)
        page_html = page_response.text
    
        # Parse the HTML content using BeautifulSoup
        page_soup = BeautifulSoup(page_html, "html.parser")

        # Find all the links that contain 'file.php' and add them to the download_links
        download_links.extend(page_soup.find_all("a", href=lambda x: x is not None and "file.php" in x))


    # Iterate over the links and download the files
    for dlink in download_links:
        # wait for 1 second to avoid overloading the server
        time.sleep(1)

        # Set the URL of the file you want to download
        file_url = domain + dlink["href"][1:]
        print(file_url)

        # Set the path to the Microsoft Edge executable
        edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

        # Open the URL in Microsoft Edge
        webbrowser.register('edge', None, webbrowser.BackgroundBrowser(edge_path))
        webbrowser.get('edge').open(file_url)

# Close Microsoft Edge
webbrowser.get("edge").close()

# print a message to the console to indicate that the script has finished
print("Finished")