from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from datetime import datetime
import re,csv

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
        return "Title: {0}\nid: {1}\nLink: {2}\nPrice: {3}\nDescription: {4}\nReviews: {5}\nStars: {6}".format(self.title, self.id, self.link, self.price, self.description, self.reviews, self.stars)

def runSelenium(url):
	driver = webdriver.Chrome()
	driver.get(url)
	items = []
	elem = driver.find_elements_by_xpath("//div[@class='thumbnail']")
	for e in elem:
		title=e.find_element_by_xpath(".//a[@class='title']").get_attribute('title')
		link=e.find_element_by_xpath(".//a[@class='title']").get_attribute('href')
		regex_id=re.compile(".*/(\d+)")
		id=regex_id.match(link).group(1)
		price=e.find_element_by_xpath(".//h4[@class='pull-right price']").get_attribute('innerHTML')
		description=e.find_element_by_xpath("//p[@class='description']").get_attribute('innerHTML')
		stars=len(e.find_elements_by_xpath(".//span[@class='glyphicon glyphicon-star']"))
		regex_reviews=re.compile("(\d+) reviews")
		reviews=regex_reviews.match(e.find_element_by_xpath(".//div[@class='ratings']").text).group(1)
		items.append(Item(title,id,link,price,description,reviews,stars))
	driver.close()
	return(items)

def writeItemsToCsv(items):
    with open('selenium_laptops.csv', 'w', newline='') as csvfile:
        fieldnames = ['title', 'id', 'link', 'price', 'description', 'stars', 'reviews']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in items:
            writer.writerow({'title': i.title, 'id': i.id, 'link': i.link, 'price': i.price, 'description': i.description, 'stars': i.stars, 'reviews': i.reviews})

def main():
    startTime = datetime.now()
    items=runSelenium("https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops")
    writeItemsToCsv(items)
    print(datetime.now() - startTime)

if __name__ == "__main__":
    main()
