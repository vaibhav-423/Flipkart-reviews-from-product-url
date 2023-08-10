from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
import requests
import argparse

app = Flask(__name__)

@app.route("/", methods=['GET'])
@cross_origin()
def homepage():
    return render_template("index.html")

@app.route("/review", methods=['POST'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            flipkart_url = request.form['urlInput'].replace(" ", "")

            parsed_url = urlparse(flipkart_url)
            path_segments = parsed_url.path.split("/")
            product_name = path_segments[1]

            flipkartPage = requests.get(flipkart_url).text
            flipkart_html = bs(flipkartPage, "html.parser")
            commentboxes = flipkart_html.find_all('div', {'class': "col _2wzgFH"})

            reviews = []
            for commentbox in commentboxes:
                try:
                    name = commentbox.find('p', {'class': '_2sc7ZR _2V5EHH'}).text
                except Exception as e:
                    name = 'No Name'

                try:
                    rating = commentbox.find('div', {'class': '_3LWZlK _1BLPMq'}).text
                except Exception as e:
                    rating = 'No Rating'

                # try:
                #     commentHead = commentbox.find('p', {'class': '_2-N8zT'}).text
                # except Exception as e:
                #     commentHead = 'No Comment Heading'
                # "CommentHead": commentHead,

                try:
                    custComment = commentbox.find('div', {'class': 't-ZTKy'}).text
                except Exception as e:
                    custComment = 'No Comment'

                mydict = {"Product": product_name, "Name": name, "Rating": rating, 
                          "Comment": custComment}
             
                reviews.append(mydict)

            return render_template('result.html', reviews=reviews)
        except Exception as e:
            print(f"An error occurred: {e}")
            return 'Something went wrong.'
    else:
        return render_template('index.html')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app arguments")
    parser.add_argument("--host", default="127.0.0.1", help="Host IP address")
    parser.add_argument("--port", type=int, default=5000, help="Port number")
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=False)