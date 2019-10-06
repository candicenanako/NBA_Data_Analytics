from bs4 import BeautifulSoup
import requests
import html.parser
import string
import salary

if __name__ == '__main__':
    # url to crawl data
    url='https://www.basketball-reference.com/players/'
    base='https://www.basketball-reference.com'
    list=[]
    for word in string.ascii_letters:
        list.append(word)
    list=list[0:26]
    people_count=0
    people_list = []

    for alphabet in list:
        response = requests.get(url+alphabet)

        # Check if link is valid
        if (response.status_code == 404):
            print(url+alphabet,'failure')
        else:
            print(url+alphabet,'success')

        # Store page content into variable
        src = response.content

        # Create beautifulsoup object
        soup = BeautifulSoup(src, 'html.parser')

        stats = soup.find("div", class_="overthrow table_container")
        if (stats == None):
            print("There are no stats available.")
        else:
            tbody=stats.tbody
            for t in tbody.children:
                if(t.find('a')!=-1):
                    nextUrl=base+t.find('a').get('href')
                    people_list.append(nextUrl)
                    # print(base+t.find('a').get('href'))
                    people_count+=1
    print(len(people_list))

    # for url in people_list:
    #     print(index)
    #     salary.getSalary(url)
    #     index+=1





