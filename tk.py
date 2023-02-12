from tkinter import *
from tkinter import Scrollbar
from bs4 import BeautifulSoup
from slugify import slugify
import requests
import html5lib
import webbrowser

flipkart_product_url = ''
amazon_product_url = ''

def Amazon(name):
    global amazon_product_url
    # print(f"----PRICE OF {name} AVAILABLE ON AMAZON------\n\n")
    name1 = slugify(name) 
    amazon_product_url = f"https://www.amazon.in/s?k={name1}&ref=pd_sl_119o56i2da_e"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    r = requests.get(url=amazon_product_url,headers=headers)
    htmlcontent = r.content
    soup = BeautifulSoup(htmlcontent,'html.parser')
    title = soup.title
    # print(title.string)
    try:
         x = soup.select(f'h2 > a[href*="{name1}"] > span')[0]
         product_name = x.string        
         y = soup.find("span",class_="a-price-whole")
         product_price = y.string
         z = soup.find("span",class_="a-icon-alt")
         # print(f"NAME    :   {product_name}")
         # print(f"PRICE   :   Rs {product_price}")
         # print(f'RATING  :   {z.get_text()}')
         return f"{product_name}\nPrice : {product_price}"

    except Exception as e:
        #  print (e)
         return f"https://www.amazon.in/s?k={name1}"
    

def Flipkart(name):
    global flipkart_product_url
    # print(f"----PRICE OF {name} AVAILABLE ON FLIPKART-----\n\n")
    name1 = slugify(name)
    flipkart_product_url = f"https://www.flipkart.com/search?q={name1}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    r = requests.get(url=flipkart_product_url)
    htmlcontent = r.content
    soup = BeautifulSoup(htmlcontent,'html.parser')
    title = soup.title
    # print(title.string)
    try:
         base_css = 'div[data-id] > div > a > div:nth-child(2)'
         summary_base_css = base_css+' > div:nth-child(1)[class*="col"]'
         product_name_css = summary_base_css+' > div:nth-child(1)'
         rating_css = summary_base_css+' > div:nth-child(2) > span > div'
         description_css = summary_base_css+' > div:nth-child(3)'
         price_css = base_css+' > div:nth-child(2)[class*="col"] > div > div > div'
         x = soup.select(f"{product_name_css}")[0]
         product_name = x.string       
         y = soup.select(f"{price_css}")[0]
         product_price = y.string
         z = soup.select(f"{description_css}")[0].getText()#.strip()
        #  print(f"NAME         :  {product_name}")
        #  print(f"PRICE        :  {product_price}")
        #  print(f"DISCRIPTION  :  {z}\n")
         return f"{product_name}\nPrice : {product_price}"

    except Exception as e:
        #  print(e)
         return f"https://www.flipkart.com/search?q={name1}"

def urls():
    global flipkart_product_url
    global amazon_product_url
    return f"{flipkart_product_url}\n\n\n{amazon_product_url}"

def open_url(event):
        global flipkart_product_url
        global amazon_product_url
        webbrowser.open_new(flipkart_product_url)
        webbrowser.open_new(amazon_product_url)

def search():
    box1.insert(1.0,"Loding...")
    box4.insert(1.0,"Loding...")
    box6.insert(1.0,"Loding...")


    # search_button.place_forget()


    box1.delete(1.0,"end")
    box4.delete(1.0,"end")
    box6.delete(1.0,"end")

    t1=Flipkart(product_name.get())
    box1.insert(1.0,t1)

    t4=Amazon(product_name.get())
    box4.insert(1.0,t4)

    t6 = urls()
    box6.insert(1.0,t6)


window = Tk()
window.wm_title("Prise comparison extinction")
window.minsize(1500,700)

lable_one =  Label(window, text="Enter Product Name :", font=("courier", 10))
lable_one.place(relx=0.2, rely=0.1, anchor="center")

product_name =  StringVar()
product_name_entry =  Entry(window, textvariable=product_name, width=50)
product_name_entry.place(relx=0.5, rely=0.1, anchor="center")

search_button =  Button(window, text="Search", width=12, command= search)
search_button.place(relx=0.5, rely=0.2, anchor="center")


l1 =  Label(window, text="flipkart", font=("courier", 20))
l4 =  Label(window, text="amazon", font=("courier", 20))
l6 =  Label(window, text="All urls", font=("courier", 20))
l8 =  Label(window, text="Loding.....", font=("courier", 30))

l1.place(relx=0.1, rely=0.3, anchor="center")
l4.place(relx=0.1, rely=0.6, anchor="center")
l6.place(relx=0.8, rely=0.6, anchor="center")

scrollbar = Scrollbar(window)
box1 =  Text(window, height=7, width=60, yscrollcommand=scrollbar.set)
box4 =  Text(window, height=7, width=60, yscrollcommand=scrollbar.set)


box1.place(relx=0.2, rely=0.4, anchor="center")
box4.place(relx=0.2, rely=0.7, anchor="center")

box6 =  Text(window, height=15, width=50, yscrollcommand=scrollbar.set, fg="blue", cursor="hand2")
box6.place(relx=0.8, rely=0.8, anchor="center")
box6.bind("<Button-1>", open_url)

window.mainloop()