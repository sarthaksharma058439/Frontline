import pickle
import uuid

from django.shortcuts import render, redirect
from firebase import firebase

import firebase_admin
from firebase_admin import credentials, messaging
import datetime

config = {
    "apiKey":"AIzaSyCyEU1SBx8sUtQkQiWWYXCzOQ18tQ7LM24",
    "authDomain":"frontline-db.firebaseapp.com",
    "databaseURL":"https://frontline-db-default-rtdb.firebaseio.com/",
    "storageBucket":"frontline-db.appspot.com"
    }

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

def updateshorts(request):

    firebaseconn = firebase.FirebaseApplication(config["databaseURL"],None)
    result=firebaseconn.get('News','')
    
    def add_news(title, headline, summary, image_url,news_url):

        all_news_data = {}

        try:
            pickle_in = open("dict.pickle", "rb")
            pickledata = pickle.load(pickle_in)
            all_news_data = pickledata.get('all_news_data')
        except:
            pass

        if result == None:
            #post_id = len(result)
            all_news_data["0"] = [title,
                                           headline,
                                           summary,
                                           image_url,
                                           news_url]
            
        else:
            post_id = len(result)
            #new_post_id = -post_id - 1
            
            all_news_data[-post_id] = [title,
                                           headline,
                                           summary,
                                           image_url,
                                           news_url]

        

        print(all_news_data)

        pickle_out = open("dict.pickle", "wb")
        pickledata = {'all_news_data': all_news_data}
        pickle.dump(pickledata, pickle_out)
        pickle_out.close()



    if request.method == "POST":

        Title = request.POST.get("title")
        Headline = request.POST.get("headline")
        Summary = request.POST.get("summary")
        ImageUrl = request.POST.get("imageurl")
        NewsUrl = request.POST.get("newsurl")

        if 'post' in request.POST:

            add_news(Title, Headline, Summary, ImageUrl, NewsUrl)

            firebaseconn = firebase.FirebaseApplication(config["databaseURL"], None)

            all_news_data={}

            try:
                pickle_in = open("dict.pickle", "rb")
                pickledata = pickle.load(pickle_in)
                all_news_data = pickledata.get('all_news_data')
            except:
                pass

            for i in all_news_data:
                data = {"title": all_news_data[i][0],
                        "head": all_news_data[i][1],
                        "desc": all_news_data[i][2],
                        "imagelink": all_news_data[i][3],
                        "newslink": all_news_data[i][4]}

                result = firebaseconn.patch("/News/%s" % i, data)
                print(result)




            message = messaging.Message(
                android=messaging.AndroidConfig(
                    ttl=datetime.timedelta(seconds=1),
                    priority='normal',
                    notification=messaging.AndroidNotification(
                        title=Title,
                        body=Summary,
                        icon=ImageUrl
                    ),
                ),
                topic='notification',
            )

            response = messaging.send(message)
            # Response is a message ID string.
            print('Successfully sent message:', response)

            return render(request=request,
                          template_name='updateshorts.html')



    return render(request=request,
                  template_name='updateshorts.html')

def index(request):
    if request.method == "POST":
        if 'shorts' in request.POST:
            return redirect('updateshorts')

        elif 'news' in request.POST:
            return redirect('updatenews')
        else:
            return redirect('updateadvise')

    return render(request=request,
                  template_name='index.html')

def updatenews(request):

    if request.method == "POST":

        news_url = request.POST.get('newNewsUrl')
        firebaseconn = firebase.FirebaseApplication(config["databaseURL"], None)

        result = firebaseconn.get('NewsLinks', '')

        if result == None:
            try:
                newsurl = {"0": news_url}
                post = firebaseconn.patch("/NewsLinks/", newsurl)
            except:
                pass

        else:
            result = firebaseconn.get('NewsLinks', '')
            newsurl = {str(len(result)): news_url}
            post = firebaseconn.patch("/NewsLinks/", newsurl)

    return render(request=request,
                  template_name='updatenews.html')

def updateadvise(request):
    if request.method == "POST":
        webistename = request.POST.get('webistename')
        date = request.POST.get('date')
        companyname = request.POST.get('companyname')
        companycap = request.POST.get('companycap')
        targetprice = request.POST.get('targetprice')
        price = request.POST.get('price')

        firebaseconn = firebase.FirebaseApplication(config["databaseURL"], None)

        count = firebaseconn.get('Advise', '')

        data = {
            "webistename": webistename,
            "date": date,
            "companyname": companyname,
            "companycap": companycap,
            "targetprice": targetprice,
            "price": price
        }

        if count == None:
            try:
                post = firebaseconn.patch("/Advise/%s"%0, data)
            except:
                pass

        else:
            result = firebaseconn.get('Advise', '')
            finaldata = {str(-len(result)): data}
            post = firebaseconn.patch("Advise", finaldata)



    return render(request=request,template_name='updateadvise.html')