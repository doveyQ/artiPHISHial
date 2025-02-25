import requests
from bs4 import BeautifulSoup
import request
import colors
import logo

def main(url, name):
    domain = url.split("//")[1].split("/")[0]
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    try:
        # Find the URL of the CSS file
        css_link = None
        for link in soup.find_all("link"):
            if link.get("rel") == ["stylesheet"]:
                css_link = link.get("href")
                break

        if css_link is not None:
            # Check if the css link contains a whole url or not
            if "http" in css_link:
                css_url = css_link
            else:
                css_url = f"{url}{css_link}"

            # Remove "//" except after "http" and "https"
            if "//" in css_url and not css_url.startswith("http://") and not css_url.startswith("https://"):
                css_url = css_url.replace("//", "/")

            # Get css content
            css_response = requests.get(css_url)
            css_content = css_response.content.decode()

            print("Extracting Colors from website ...")
            #Call the function to get the colors
            colors.extract_colors(url, css_content)
    except Exception as e:
        print("An error occurred trying to get the colors:", e)

    try:
        print("Loading image from website ...")
        # Call the function to get the logo
        logo.extract_logo(domain)
        print("Logo successfully pulled")


    except Exception as e:
        print("An error occurred trying to pull the logo:", e)

    request.generatepage(domain, name)
