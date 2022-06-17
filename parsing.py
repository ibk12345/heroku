import requests
from bs4 import BeautifulSoup
import lxml

URL='https://www.kivano.kg/'
prod_id=1

def get_html(url):
    html=requests.get(url).text
    return html

def get_soup(html):
    soup=BeautifulSoup(html,"lxml")
    return soup

def get_category_list(soup):
    category_list=soup.find("div", class_="leftmenu").find_all("div", class_="leftmenu-item")
    return category_list

def get_category(category_list):
    cat_list=[]
    subcat_list=[]
    for i in range(0,len(category_list)-1):
        category=category_list[i].find('div', class_='leftmenu-title').text
        slug=category_list[i].find('div', class_='leftmenu-title').find ('a').get('href')
        cat_list.append({'category':category, 'slug':slug})
        subcategory_list=category_list[i].find_all('div', class_='box')
        for sub in subcategory_list:
            subcategory=sub.find_all('div', class_='secondli')
            for s in subcategory:
                subcat=s.find('a').text
                subcat_slug=s.find('a').get('href')
                subcat_list.append({'category':subcat, 'slug':subcat_slug, 'parent':(i+1)})
    return cat_list, subcat_list    

def get_product_list(soup):
    product_list=soup.find("div", class_="list-view").find_all("div", class_="item")
    return product_list

product=[]
images=[]
def get_product(product_list, prod_id, id):
    for prod in product_list:
        try:
            title=prod.find('div', class_='listbox_title').text
        except:
            title=''
        try:
            desc=prod.find('div', class_='product_text').text
            desc=desc.split('\n\n')[2].strip().replace('\r\n', ' ').replace('\t', '').replace('\xa0', '')
        except:
            desc=''
        try:
            price=prod.find('div', class_='listbox_price').find('strong').text.replace('\n', '').replace('сом', '').strip()
        except:
            price=0

        image='https://www.kivano.kg'+prod.find('div', class_='listbox_img').find('img').get('src')
        product.append({'title': title.replace('\n', ''), 'desc':desc, 'price':int(price), 'category_id':id+1})
        images.append({'image':image, 'product_id':prod_id})
        prod_id+=1
    return images, product





def get_categories(url):
    html=get_html(url)
    soup=get_soup(html)
    category_list=get_category_list(soup)
    return get_category(category_list)

def get_product_image(url_, prod_id, all_categories):
    cat_len=len(all_categories[0])
    for i in all_categories:
        for id in range(len(i)):
            url=url_[:-1]+i[id]['slug']
            html=get_html(url)
            soup=get_soup(html)
            product_list=get_product_list(soup)
            if i[id].get('parent',0):
                cat_id=id+cat_len            
            else:
                cat_id=id
            prod_image=get_product(product_list, prod_id, cat_id)
            prod_id+=len(product_list)
    return prod_image


all_categories=get_categories(URL)
prod_image=get_product_image(URL,prod_id, all_categories)
print(all_categories)
print(prod_image)