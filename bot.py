from PIL import Image
from io import BytesIO
import pytesseract as tess
import requests
import yaml
import praw

with open('config.yml') as data_file:
    CONFIG = yaml.load(data_file)


def main():
    reddit = praw.Reddit(client_id=CONFIG['id'],
                         client_secret=CONFIG['secret'],
                         user_agent="{}:0.1 (by /u/Tomus)".format(CONFIG['id']),
                         username=CONFIG['username'],
                         password=CONFIG['password'])

    subreddit = reddit.subreddit('all')
    for submission in subreddit.hot(limit=10):
        if submission.post_hint == 'image':
            print('Incoming OCR... (https://www.reddit.com{})'.format(submission.permalink))
            txt = read_img(submission.url)
            print('No text' if len(txt) == 0 else txt)
            print()


def read_img(url) -> str:
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    tess.pytesseract.tesseract_cmd = 'tesseract-bin/tesseract.exe'
    return tess.image_to_string(img)


if __name__ == '__main__':
    main()
