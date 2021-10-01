from fastapi import FastAPI
from pydantic import BaseModel

import pymysql
import sentiment_analysis

from dotenv import load_dotenv   
load_dotenv()
import os

a=os.environ.get('host')
b=os.environ.get('user')
c=os.environ.get('password')	
d=os.environ.get('database')

mydb=pymysql.connect(host=a,user=b,password=c,database=d,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
mycursor=mydb.cursor()

app = FastAPI()


@app.get("/movie_list")
async def show_existing_movies():
    mycursor.execute("select distinct movie_name from movie_review.reviews;")
    result=mycursor.fetchall()
    res=[]
    for i in result:
        res.append(i["movie_name"])
    return res

@app.get("/show_reviews")
async def show_reviews_of_movie(movie_name):
    instruction="select user_review,sentiment from movie_review.reviews where movie_name=%s"
    data=(movie_name,)
    mycursor.execute(instruction,data)
    result=mycursor.fetchall()
    res={}
    for i in result:
        res[i["user_review"]]=i["sentiment"]
    return res

class review(BaseModel):
    name: str
    rev: str

@app.post("/send_review")
async def send_user_review(user_rev:review):
    review_sentiment=sentiment_analysis.predict([user_rev.rev])
    instruction="insert into movie_review.reviews (movie_name,user_review,sentiment) values (%s,%s,%s)"
    data=(user_rev.name,user_rev.rev,review_sentiment)
    mycursor.execute(instruction,data)
    mydb.commit()
    return "user review has been successfully registered in the database"
