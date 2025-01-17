import requests
import csv
from textblob import TextBlob
import re

class Review:
    def __init__(self, movie, title, content, rate, upvotes, downvotes):
        self.movie = movie
        self.title = title
        self.content = content
        self.rate = rate
        self.upvotes = upvotes
        self.downvotes = downvotes
        blob = TextBlob(content);
        self.polarity = blob.polarity
        self.subjectivity = blob.subjectivity


endcur = "";
reviews = [];


def clean_text(raw_text):
    """
    Clean text by removing HTML tags, HTML entities, and bracketed content.
    """
    # Remove HTML tags
    no_html_tags = re.sub(r'<.*?>', '', raw_text)

    # Remove HTML entities (e.g., &#39;)
    no_html_entities = re.sub(r'&[#\w]+;', '', no_html_tags)

    # Remove special numeric entities (e.g., &#39)
    no_numeric_entities = re.sub(r'&#\d+;', '', no_html_entities)

    # Remove content inside brackets (e.g., (text))
    no_brackets = re.sub(r'\(.*?\)', '', no_numeric_entities)

    # Remove extra whitespace
    cleaned_text = " ".join(no_brackets.split())

    return cleaned_text

def get_reviews_data(movie):
    url = (
    'https://caching.graphql.imdb.com/'
    '?operationName=TitleReviewsRefine&variables={{"after":"g4u6bermtizcsyid7cux7mjvqlr4qcbt3ykdz4pqcwb32vtjnerkic25mjohjvzwhoo3gvxwvklw5fwr3dfh4",'
    '"const":"{movie}","filter":{{}},"first":25,"locale":"zh-CN",'
    '"sort":{{"by":"HELPFULNESS_SCORE","order":"DESC"}}}}'
    '&extensions={{"persistedQuery":{{"sha256Hash":"89aff4cd7503e060ff1dd5aba91885d8bac0f7a21aa1e1f781848a786a5bdc19","version":1}}}}'
    ).format(movie=movie)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "content-type": "application/json"
    }
    res = requests.get(url, headers=headers)
    # print(res.text)
    data = res.json()
    total = data["data"]["title"]["reviews"]["total"]
    print("Total reviews:", total)
    times = 0;
    while endcur != "END":
        print("Fetching... ", times * 50, "/", total)
        get_part_review(movie)
        times = times + 1

    print("Collected reviews:", len(reviews))

def get_part_review(movie):
    global endcur
    url = (
    'https://caching.graphql.imdb.com/'
    '?operationName=TitleReviewsRefine&variables={{"after":"{after}",'
    '"const":"{movie}","filter":{{}},"first":50,"locale":"zh-CN",'
    '"sort":{{"by":"HELPFULNESS_SCORE","order":"DESC"}}}}'
    '&extensions={{"persistedQuery":{{"sha256Hash":"89aff4cd7503e060ff1dd5aba91885d8bac0f7a21aa1e1f781848a786a5bdc19","version":1}}}}'
    ).format(movie=movie, after=endcur)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "content-type": "application/json"
    }
    res = requests.get(url, headers=headers)
    data = res.json()

    for item in data["data"]["title"]["reviews"]["edges"]:
        title = item["node"]["summary"]["originalText"]
        content = clean_text(item["node"]["text"]["originalText"]["plaidHtml"])
        rate = item["node"]["authorRating"]
        upvotes = item["node"]["helpfulness"]["upVotes"]
        downvotes = item["node"]["helpfulness"]["downVotes"]

        # print(title, content, rate, upvotes, downvotes)
        reviews.append(Review("", title, content, rate, upvotes, downvotes));


    if data["data"]["title"]["reviews"]["pageInfo"]["hasNextPage"]:
        endcur = data["data"]["title"]["reviews"]["pageInfo"]["endCursor"] 
    else:
        endcur = "END";
    # print(data)

def save_to_csv(file_name):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Movie", "Title", "Content", "Rate", "Upvotes", "Downvotes", "Polarity", "Subjectivity"])
        for review in reviews:
            writer.writerow([review.movie, review.title, review.content, review.rate, review.upvotes, review.downvotes, review.polarity, review.subjectivity  ])

if __name__ == '__main__':
    print("IMDB Review Fetcher\nAuthor: Qixiny<qixinynan@outlook.com>\n")
    movie_id = input("Enter movie ID (like tt10627720): ")
    file_name = input("Enter CSV file name to save (like reviews.csv): ")
    get_reviews_data(movie_id)
    save_to_csv(file_name)
    print(f"Reviews saved to {file_name}")