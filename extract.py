from datetime import datetime
import requests
import time
start_date = "2016-08-25"
stop_date = "2019-04-27"
from bs4 import BeautifulSoup
start = datetime.strptime(start_date, "%Y-%m-%d")
stop = datetime.strptime(stop_date, "%Y-%m-%d")

from datetime import timedelta
main_url="https://www.dawn.com/newspaper/"
all_categories=["front-page/"]#,"national/","international/","business/"]# '"back-page/"'


def extract_headlines_link(soup_obj):
    
    #nsoup=soup_obj.findAll('div',{'class':'row'})
    #if len(nsoup)<2:
    #    nsoup=nsoup[0]
    #else:
    #    nsoup=nsoup[1]
    #nsoup=soup_obj.find('div',{'class':'row no-gutters'})
    all_classes=soup_obj.findAll('article',{'class':'story story--small'})
    all_classes=[soup_obj.find('article',{'class':'story story--large'})]+all_classes
    all_links=[]
    all_headlines=[]
    for x in all_classes:

        link_data=x.find("a")
        headline = link_data.text

        all_links.append(link_data.get("href"))
        all_headlines.append(headline)

    return all_headlines,all_links

while start < stop:
    start_string=str(start).split(" ")[0]
    for category in all_categories:        
        url_to_visit=main_url+category
        url_to_visit+=start_string
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        try:
            response=requests.request("GET",url_to_visit, headers=headers)
        except:
            f = open("error_urls.txt", "a+")
            f.write(url_to_visit)
            f.write("\n")
            f.close()
            time.sleep(2)
            print ("issue in url ignoring it")

        url_content=response.content
        while str(url_content).find("Request Aborted - Client Issue")!=-1:
            time.sleep(2)
            print ("requesting again")
            response = requests.request("GET", url_to_visit, headers=headers)

            url_content = response.content
        
        soup=BeautifulSoup(url_content,'html.parser')

        print (url_to_visit)
        print ("Extracted "+category+" for "+start_string)

        try:
            headlines,links=extract_headlines_link(soup)
            print ("total headlines and links are "+str(len(headlines))+"  "+str(len(links)))
            for i in range(0, len(headlines)):
                f1=open("categories_data.txt","a+")
                f1.write(category.replace("/","")+",")
                f1.write(url_to_visit+",")
                f1.write(start_string+",")
                f1.write(links[i]+",")
                f1.write(headlines[i].replace(","," ")+"\n")
                f1.close()

        except Exception as e:

            print ("______________")
            print (url_to_visit)

            print (e)
            f = open("temp.txt", 'w')
            f.write(str(url_content))
            f.close()

            f=open("problems_urls.txt","a+")
            f.write(url_to_visit)
            f.write("\n")
            f.close()


    start = start + timedelta(days=1)