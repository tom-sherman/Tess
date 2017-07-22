from PIL import Image
from io import BytesIO
import pytesseract as tess
import requests
import yaml
import praw
import praw.models

with open('config.yml') as data_file:
    CONFIG = yaml.load(data_file)


def main():
    reddit = praw.Reddit(client_id=CONFIG['id'],
                         client_secret=CONFIG['secret'],
                         user_agent="{}:0.1 (by /u/Tomus)".format(CONFIG['id']),
                         username=CONFIG['username'],
                         password=CONFIG['password'])

    subreddit = reddit.subreddit('all')
    submission: praw.models.Submission
    for submission in subreddit.hot(limit=10):
        if submission.post_hint == 'image':
            print('Incoming OCR... (https://www.reddit.com{})'.format(submission.permalink))
            txt = read_img(submission.url)
            print('No text' if len(txt) == 0 else build_comment(txt))
            print()


def read_img(url) -> str:
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    tess.pytesseract.tesseract_cmd = 'tesseract-bin/tesseract.exe'
    return tess.image_to_string(img)


def build_comment(text) -> str:
    new_text = ''
    for line in text.split('\n'):
        new_text = new_text + '    {}\n'.format(line)

    return CONFIG['comment_template'].format(new_text)

if __name__ == '__main__':
    main()
