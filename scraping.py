import requests
from bs4 import BeautifulSoup
import re #for sanitizing the title
import time

#for sanitizing filename
def sanitize_filename(title):
    # Remove characters not allowed in filenames (Windows-safe)
    title = re.sub(r'[\\/*?:"<>|]', "", title)
    # Handle weird spacings
    return re.sub(r"\s+", " ", title).strip()

#getting response and parsing
url = "https://people.math.harvard.edu/~mpopa/papers.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

#get a list of html elements with link-title
links = soup.select("a")

for link in links:
    #get the title of the paper
    title = link.get_text(strip=True)
    title = sanitize_filename(title)
    filename = title + '.pdf'

    #get the url of the paper
    href = link["href"]
    pdf_url = requests.compat.urljoin(url, href)

    #download the paper
    print(f"Downloading: {title}")
    pdf_response = requests.get(pdf_url)
    with open(filename, "wb") as f:
        f.write(pdf_response.content)
    
    #sleep between requests
    time.sleep(1)

