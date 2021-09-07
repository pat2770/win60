from datetime import datetime
from bs4 import BeautifulSoup
import requests,re,csv

class Item:
    def __init__(self, title, id, link, price, description, reviews, stars):
        self.title=title
        self.id=id
        self.link=link
        self.price=price
        self.description=description
        self.reviews=reviews
        self.stars=stars

    def __str__(self):
        return self.toString()

    def __unicode__(self):
        return self.toString()

    def __repr__(self):
        return self.toString()

    def toString(self):
        return "Title: {0}\nid: {1}\nLink: {2}\nPrice: {3}\nDescription: {4}\nStars: {5}\nReviews: {6}".format(self.title, self.id, self.link, self.price, self.description, self.reviews, self.stars)

def initSoup(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, 'lxml')

def extractItems(laptops,items):
    for l in laptops:
        title=l.find("a","title").get("title")
        link=l.find("a","title").get("href")
        regex_id=re.compile(".*/(\d+)")
        id=regex_id.match(link).group(1)
        price=l.find("h4","price").string
        description=l.find("p","description").string
        stars=len(l.find_all("span", "glyphicon-star"))
        regex_reviews=re.compile("(\d+) reviews")
        reviews=regex_reviews.match(l.find("div", "ratings").find(string=regex_reviews)).group(1)
        items.append(Item(title,id,link,price,description,reviews,stars))
 

def writeItemsToCsv(items):
    with open('bs4_laptops.csv', 'w', newline='') as csvfile:
        fieldnames = ['title', 'id', 'link', 'price', 'description', 'stars', 'reviews']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in items:
            writer.writerow({'title': i.title, 'id': i.id, 'link': i.link, 'price': i.price, 'description': i.description, 'stars': i.stars, 'reviews': i.reviews})

def main():
    startTime = datetime.now()
    soup=initSoup("https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops")
    laptops = soup.find_all("div","thumbnail")    
    items=[]
    extractItems(laptops,items)
    writeItemsToCsv(items)
    print(datetime.now() - startTime)

if __name__ == "__main__":
    main()

