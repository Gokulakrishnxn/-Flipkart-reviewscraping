import requests
from bs4 import BeautifulSoup
import csv
import matplotlib.pyplot as plt
from wordcloud import STOPWORDS, WordCloud
import plotly.graph_objects as go


main_url = "https://www.flipkart.com/cmf-nothing-buds-pro-2-50-db-anc-hi-res-ldac-smart-dial-spatial-audio-dual-drivers-bluetooth/product-reviews/itm30c0d780a4c6c?pid=ACCHFZ2FPSFBD9UT&lid=LSTACCHFZ2FPSFBD9UTMQZQP0&marketplace=FLIPKART"
stopwords = STOPWORDS

all_positive_comments = ""
all_negative_comments = ""

# for overall review stats
def all_stars():
    star_arr = []
    response = requests.get(main_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_stars = soup.find_all(class_='BArk-j')
    for i in all_stars:
        star_arr.append(i.text.strip())
    print(star_arr)
    
    stars = ["5 star", "4 star", "3 star", "2 star", "1 star"]
    values = [6384, 2053, 472, 241, 770] # Convert strings to integers

    fig = go.Figure(data=[go.Bar(x=stars, y=values)])

    fig.update_layout(
        title="Star Rating Distribution",
        xaxis_title="Star Ratings",
        yaxis_title="Number of Reviews",
        template="plotly_white",
        yaxis_range=[0, 1000] # Set the y-axis range
    )

    fig.show()



def scrape_positive_reviews(page_num, filename):
    global all_positive_comments
    
    url = f'{main_url}&page={page_num}&sortOrder=POSITIVE_FIRST'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    paragraphs = soup.find_all('p', class_='z9E0IG')
    stars = soup.find_all(class_='XQDdHH Ga3i8K')
    comments = soup.find_all(class_='ZmyHeo')

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(['Star', 'Paragraph', 'Comment'])
        
        for star, paragraph, comment in zip(stars, paragraphs, comments):
            review_text = comment.text.strip()
            all_positive_comments += review_text + " " 
            writer.writerow([star.text.strip(), paragraph.text.strip(), review_text])

    print(f"Data from page {page_num} for positive reviews has been successfully written to {filename}")


def scrape_negative_reviews(page_num, filename):
    global all_negative_comments

    url = f'{main_url}&page={page_num}&sortOrder=NEGATIVE_FIRST'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    paragraphs = soup.find_all('p', class_='z9E0IG')
    stars = soup.find_all(class_='XQDdHH Js30Fc Ga3i8K')
    comments = soup.find_all(class_='ZmyHeo')

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        if file.tell() == 0:
            writer.writerow(['Star', 'Paragraph', 'Comment'])

        for star, paragraph, comment in zip(stars, paragraphs, comments):
            review_text = comment.text.strip()
            all_negative_comments += review_text + " "  
            writer.writerow([star.text.strip(), paragraph.text.strip(), review_text])

    print(f"Data from page {page_num} for negative reviews has been successfully written to {filename}")


def scrape_positive_pages(num_pages, filename):
    for page_num in range(1, num_pages + 1):
        scrape_positive_reviews(page_num, filename)


def scrape_negative_pages(num_pages, filename):
    for page_num in range(1, num_pages + 1):
        scrape_negative_reviews(page_num, filename)

def wordcloud_positive():
    wc = WordCloud(background_color="white", stopwords=stopwords, height=700, width=500)
    wc.generate(all_positive_comments)
    wc.to_file("wordcloud_positive.png")

def wordcloud_negative():
    wc = WordCloud(background_color="white", stopwords=stopwords, height=700, width=500)
    wc.generate(all_negative_comments)
    wc.to_file("wordcloud_negative.png")

num_pages_to_scrape = int(input("Enter the number of pages to scrape from the URL: "))

print("Scraping positive reviews...")
scrape_positive_pages(num_pages_to_scrape, 'positive_reviews.csv')

print("Scraping negative reviews...")
scrape_negative_pages(num_pages_to_scrape, 'negative_reviews.csv')

print("\nScraping complete.")

print("Wordcloud created for Positive review")
wordcloud_positive()

print("Wordcloud created for Negative review")
wordcloud_negative()

all_stars()