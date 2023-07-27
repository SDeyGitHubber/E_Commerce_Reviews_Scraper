from flask import Flask,request,render_template
from flask_cors import CORS,cross_origin
import requests,logging
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uo
from pymongo.mongo_client import MongoClient

app=Flask(__name__)

@app.route('/',methods=['GET'])
def homepage():
    return render_template('base.html')

@app.route('/review',methods=['GET','POST'])
def review():
    if(request.method=='POST'):
        try:
            search_string=request.form['content'].replace(' ','')
            flipkart_url='https://www.flipkart.com/search?q='+search_string
            ureq=uo(flipkart_url)
            flipkart_page=ureq.read()
            ureq.close()
            flipkart_html=bs(flipkart_page,'html.parser')
            bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
            del bigboxes[0:3]
            box = bigboxes[0]
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
            prodRes = requests.get(productLink)
            prodRes.encoding='utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            print(prod_html)
            commentboxes = prod_html.find_all('div', {'class': "_16PBlm"})

            # filename = search_string + ".csv"
            # fw = open(filename, "w")
            # headers = "Product, Customer Name, Rating, Heading, Comment \n"
            # fw.write(headers)
            review = []
            for commentbox in commentboxes:
                try:
                    #name.encode(encoding='utf-8')
                    name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text

                except:
                    name = 'No Name'

                try:
                    #rating.encode(encoding='utf-8')
                    rating = commentbox.div.div.div.div.text

                except:
                    rating = 'No Rating'

                try:
                    #commentHead.encode(encoding='utf-8')
                    commentHead = commentbox.div.div.div.p.text

                except:
                    commentHead = 'No Comment Heading'
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    #custComment.encode(encoding='utf-8')
                    custComment = comtag[0].div.text
                except Exception as e:
                    print("Exception while creating dictionary: ",e)

                mydict = {"Product": search_string, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}
                review.append(mydict)
            # client = MongoClient("mongodb+srv://shouvikdey21:shouvikdey21@cluster0.cieh90v.mongodb.net/?retryWrites=true&w=majority")
            # db = client['review_scrap']
            # review_col = db['review_scrap_data']
            # review_col.insert_many(review)
            return render_template('result.html', reviews=review[0:(len(review)-1)])
        except Exception as e:
            print('The Exception message is: ',e)
            logging.exception(e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
	#app.run(debug=True)