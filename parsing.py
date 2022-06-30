from urllib import response
from bs4 import BeautifulSoup as BS
import requests
import csv



HOST = 'https://www.kivano.kg/'


def get_html(url):
    response = requests.get(url)
    return(response.text)

def get_all_pages(html):
    soup = BS(html, 'lxml') 
    get_all_page = soup.find('div', class_ = 'pager-wrap').find('ul')
    last_page = get_all_page.find_all('li')[-1]
    all_pages = last_page.find('a').get('href').split('=')[-1]
    return int(all_pages)

def write_to_csv(data):
    with open('kivano_mobile.csv', 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter='/')
        writer.writerow((data['title'],
                         data['price'],
                         data['photo']))

def get_page_data(html):
    soup = BS(html, 'lxml')
    product_list = soup.find('div', class_ = 'list-view')
    products = product_list.find_all('div', class_ = 'item product_listbox oh')

    for product in products:
        try:
            photo = HOST + product.find('div', class_ = 'listbox_img pull-left').find('a').find('img').get('src')
            
        except:
            photo = ''
        try:
            title = product.find('div', class_ = 'listbox_title oh').find('a').text
            
        except:
            title = ''
        try:
            price = product.find('div', class_ = 'listbox_price text-center').text
            
        except:
            price = ''
        
        data = {'title': title, 'price': price, 'photo': photo}
        write_to_csv(data)
    



def main():
    mobile_url = 'https://www.kivano.kg/mobilnye-telefony'
    pages = '?page='
    total_pages = get_all_pages(get_html(mobile_url))

    for page in range(1, total_pages+1):
        url_with_page = mobile_url + pages + str(page)
        html = get_html(url_with_page)
        get_page_data(html)
main()