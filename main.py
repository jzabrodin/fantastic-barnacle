# coding=utf-8
import requests
import pickle
import os
import bs4

class Warehouse():

    data = {}
    filename = os.path.join(os.getcwd(),"data.pkl")

    def getFile(self,attr="r"):

        if os.path.isfile(self.filename):
            return open(self.filename,attr)
        else:
            f = self.initFile()
            f.open(self.filename,"r")

    def initFile(self):
        f = open(self.filename, "w")
        f.close()
        return f

    def __init__(self):
        file = self.getFile("r")
        self.data = pickle.load(file)

    def save(self, object):

        file = self.getFile("w")
        pickle.dump(object , file)
        file.close()

class URLHelper:

    urlList = []

    def __init__(self):
        self.urlList =  [
            "https://ebanoe.it/2019/04/30/seeking-50-cyber-nerds/"
        ]

def main():

    warehouse = Warehouse()
    urlHelper = URLHelper()

    data = warehouse.data

    urls = urlHelper.urlList

    for url in urls:

        if data.get(url) is None:

            response = requests.get(url)
            data[url] = response.text

        else:
            print("{0} already in file".format(url))
            dataSoup = bs4.BeautifulSoup( data[url] , features="lxml" )

            list = dataSoup.select("li .comment")

            print "Длина списка {0}".format(len(list))

            for comment in list:

                commentSoup = bs4.BeautifulSoup(comment.text,features="lxml")
                like = commentSoup.select(".vortex-p-like-counter-comment")
                commentText = commentSoup.select("p")

                # print commentText[0].text
                try:
                    print "{0} количество лайков".format(like[0].text)
                except Exception as e:
                    print commentText[0].text
                    break
#
    warehouse.save(data)

main()

