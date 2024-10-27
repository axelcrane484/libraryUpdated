 # library
 # multiple books that you can choose from
 # name of book with prices
 #button buy now
 #image at top, label at middle, buy now at bottom
 # budget £15
!pip install pymongo
from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image
from IPython.display import display, clear_output
import ipywidgets as widgets
import io
import random
import re

client=MongoClient('mongodb+srv://root:root@library.6rypl.mongodb.net/?retryWrites=true&w=majority&appName=library')
db = client['library']
user_collection = db['login_details']


users = {}
Lord_of_the_Rings = 7
Harry_potter = 6
Fallen_Kingdom = 5
budget = 15
admin = False
cart = []

books = {
    'Lord of the Rings': {'price': 7, 'author': 'J.R.R. Tolkien', 'year': 1954, 'wiki': 'https://en.wikipedia.org/wiki/The_Lord_of_the_Rings'},
    'Harry Potter': {'price': 6, 'author': 'J.K. Rowling', 'year': 1997, 'wiki': 'https://en.wikipedia.org/wiki/Harry_Potter'},
    'Fallen Kingdom': {'price': 5, 'author': 'James Smith', 'year': 2010, 'wiki': 'https://en.wikipedia.org/wiki/Fallen_Kingdom'},
    'The Hobbit': {'price': 8, 'author': 'J.R.R. Tolkien', 'year': 1937, 'wiki': 'https://en.wikipedia.org/wiki/The_Hobbit'},
    'Game of Thrones': {'price': 9, 'author': 'George R.R. Martin', 'year': 1996, 'wiki': 'https://en.wikipedia.org/wiki/A_Game_of_Thrones'},
    '1984': {'price': 4, 'author': 'George Orwell', 'year': 1949, 'wiki': 'https://en.wikipedia.org/wiki/Nineteen_Eighty-Four'},
    'To Kill a Mockingbird': {'price': 6, 'author': 'Harper Lee', 'year': 1960, 'wiki': 'https://en.wikipedia.org/wiki/To_Kill_a_Mockingbird'},
    'The Great Gatsby': {'price': 5, 'author': 'F. Scott Fitzgerald', 'year': 1925, 'wiki': 'https://en.wikipedia.org/wiki/The_Great_Gatsby'},
    'Moby Dick': {'price': 7, 'author': 'Herman Melville', 'year': 1851, 'wiki': 'https://en.wikipedia.org/wiki/Moby-Dick'},
    'War and Peace': {'price': 10, 'author': 'Leo Tolstoy', 'year': 1869, 'wiki': 'https://en.wikipedia.org/wiki/War_and_Peace'},
    'Pride and Prejudice': {'price': 6, 'author': 'Jane Austen', 'year': 1813, 'wiki': 'https://en.wikipedia.org/wiki/Pride_and_Prejudice'},
    'The Catcher in the Rye': {'price': 5, 'author': 'J.D. Salinger', 'year': 1951, 'wiki': 'https://en.wikipedia.org/wiki/The_Catcher_in_the_Rye'},
    'The Chronicles of Narnia': {'price': 7, 'author': 'C.S. Lewis', 'year': 1950, 'wiki': 'https://en.wikipedia.org/wiki/The_Chronicles_of_Narnia'},
    'Animal Farm': {'price': 4, 'author': 'George Orwell', 'year': 1945, 'wiki': 'https://en.wikipedia.org/wiki/Animal_Farm'},
    'Brave New World': {'price': 6, 'author': 'Aldous Huxley', 'year': 1932, 'wiki': 'https://en.wikipedia.org/wiki/Brave_New_World'},
    'The Lord of the Flies': {'price': 5, 'author': 'William Golding', 'year': 1954, 'wiki': 'https://en.wikipedia.org/wiki/Lord_of_the_Flies'},
    'Jane Eyre': {'price': 7, 'author': 'Charlotte Brontë', 'year': 1847, 'wiki': 'https://en.wikipedia.org/wiki/Jane_Eyre'},
    'Wuthering Heights': {'price': 6, 'author': 'Emily Brontë', 'year': 1847, 'wiki': 'https://en.wikipedia.org/wiki/Wuthering_Heights'},
    'Hamlet': {'price': 4, 'author': 'William Shakespeare', 'year': 1600, 'wiki': 'https://en.wikipedia.org/wiki/Hamlet'},
    'Macbeth': {'price': 4, 'author': 'William Shakespeare', 'year': 1606, 'wiki': 'https://en.wikipedia.org/wiki/Macbeth'}
}


def update_feedback(message, success = True):
  if success:
    feedback.value = f'<span style="color: green;">{message}</span>'
  else:
    feedback.value = f'<span style="color: red;">{message}</span>'

username_register = widgets.Text(description = "email")
password_register = widgets.Password(description = "password")
comfirm_password_register = widgets.Password(description = "Comfirm Password")
register_button = widgets.Button(description = "register", button_style = "success", disabled = False)

username_login = widgets.Text(description = "username")
password_login = widgets.Password(description = "password")
login_button = widgets.Button(description = "login", button_style = "primary")

logout_button = widgets.Button(description = "logout", button_style = "warning")



def register_user(b):
  global username, password, new_users, admin
  username = username_register.value
  password = password_register.value
  comfirm_password = comfirm_password_register.value
  regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
  isEmailValid = re.fullmatch(regex, username)
  if username in users:
    update_feedback(f"details have already been used, try another account", success=False)
  elif not username or not password:
    update_feedback(f"you have not filled in anything", success = False)
  elif len(password) < 8 or containsUpperCase(password) == False or comfirm_password != password or isEmailValid == None:
    if len(password) < 8:
      update_feedback(f"password is to short must be atleast 8 characters")
    if containsUpperCase(password) == False:
      update_feedback(f"password needs atleast one capital")
    if comfirm_password != password:
      update_feedback(f"you have not re-written your password correctly")
    if isEmailValid == None:
      update_feedback(f"your email is invalid please try again")
  else:
    users[username] = password
    new_user = {"username": username , "password": password, "admin" : admin}
    user_collection.insert_one(new_user)
    update_feedback(f"user has now created an account")


def containsUpperCase(str):

  res = False
  for ele in str:

      # checking for uppercase character and flagging
      if ele.isupper():
          res = True
  return res


register_button.on_click(register_user)

def login_user(b):
  global current_user
  username = username_login.value
  password = password_login.value

  users = user_collection.find_one({"username": username, "password": password})

  if users:
    update_feedback(f"you have successfully logged in as",users)
    current_user = username
    after_login()
  else:
    update_feedback(f"invalid login please try again")


login_button.on_click(login_user)

def after_login():
  clear_output()
  display(tabs)

def logout_user(b):
  global current_user
  username = username_login.value
  password = password_login.value
  if username in users:
    clear_output()
    display(auth_tabs)
  else:
    update_feedback(f"account is not logged in")

logout_button.on_click(logout_user)

current_user_text = widgets.Text(description = "username")

current_user_delete_button = widgets.Button(description = "delete current user", button_style = "warning", disabled = False)

def delete_current_user (b):
  global current_user
  user_to_delete = current_user_text.value
  if current_user_delete_button:
    delete_dict = {"username" : current_user_text.value}
    user_collection.delete_one(delete_dict)
    update_feedback(f"user has been deleted")
    print("hello")
  else:
    update_feedback(f"user has not been found please try again")

current_user_delete_button.on_click(delete_current_user)

make_user_admin_button = widgets.Button(description = "make admin", button_style = "success", disabled = False)

def make_user_admin(b):
  admin_user= current_user_text.value
  make_admin = user_collection.find_one({"username" : admin_user})
  user_collection.update_one({"username": admin_user}, {"$set": {"admin": True}})
  update_feedback(f"user is now admin")
  

make_user_admin_button.on_click(make_user_admin)

book_widget = widgets.RadioButtons(
          options = list(books.keys()),
          description='book:',
          disabled=False,
          layout=widgets.Layout(width = 'auto', margin = '0 0 20px 0')
   )

details2 = widgets.HTML(
    value='',
    layout=widgets.Layout(width = 'auto', height = '150px', margon = '0 0 20px 0', border = '1px solid black',  padding = '10px' )

)



details = widgets.HTML(
    value = "",
    layout = widgets.Layout(width = "auto", height = "170px", border = '1px solid black'),
)

def update_details(change):
  selected_book = book_widget.value
  book_info = books[selected_book]
  details.value = f"""
  <h3><a href = "{book_info['wiki']}"target = "_blank">{selected_book}</a></h3>
  <p><strong>Author:</strong> {book_info['author']}</p>
  <p><strong>Year:</strong>{book_info['year']}</p>
  <p><strong>Price:</strong>{book_info['price']}</p>"""

book_widget.observe(update_details, names = 'value')



def add_cart(b):
  selected_book = book_widget.value
  if selected_book not in cart:
    cart.append(selected_book)
    update_cart_display()
    update_feedback(f"{selected_book} has been added to the cart")
  else:
    update_feedback(f"{selected_book} is already in cart", success=False)


def update_cart_display():
  if cart:
    cart_details = "\n".join([f"{book} - ${books[book]['price']}" for book in cart])
    cart_display.value = cart_details
  else:
    cart_display.value = "cart is empty"

def clear_cart(b):
  if cart:
    cart.clear()
    update_cart_display()
  else:
    print("nothing is inside cart")


clear_cart_button = widgets.Button(
    button_style = "warning",
    tooltip = "clear your cart",
    description = "clear cart",
    disabled = False,
)

clear_cart_button.on_click(clear_cart)

cart_display = widgets.Textarea(
    value = "cart is empty",
    description = "cart",
    disabled = False,
    layout = widgets.Layout(width = "50%", height = "100px"),
)

add_to_cart = widgets.Button(
    button_style = "success",
    tooltip = "Add your book to cart",
    description = "add to cart",
    disabled = False,
)

buy_cart = widgets.Button(
    button_style = "success",
    tooltip = "buy the books inside your cart",
    description = "buy cart",
    disabled = False,
)

add_to_cart.observe(add_cart, names = "value")

add_to_cart.on_click(add_cart)

def deposit_money(b):
  global budget
  deposit_value = deposit_widget.value
  if deposit_value > 0 or deposit_value < 500:
     budget = budget + deposit_value
     update_feedback(f"money has been deposited",budget)
  else:
     update_feedback(f"enter a valid amount",success = False)


deposit_button = widgets.Button(
    button_style = "info",
    tooltip = "deposit more money into your budget",
    description = "deposit money",
    disabled = False,
)

deposit_widget = widgets.BoundedFloatText(
    min = 1,
    max = 500,
    description = "deposit amount",
    disabled = False,
)

deposit_button.on_click(deposit_money)


def buy(b):
  global budget, cart
  selected_book = book_widget.value
  price = sum(books[book]['price'] for book in cart)
  if price <= budget:
    print(f"you have bought{' '.join(cart)}")
    budget -= price
    update_feedback(f"you have £",budget,"left")
    cart.clear()
    update_cart_display()
  else:
    update_feedback(f"you dont have enough balance",success=False)

buy_now = widgets.Button(
    button_style = "success",
    tooltip = "buy your books",
    description = 'buy cart',
    disabled = False,
)

buy_now.on_click(buy)

def search(b):
  search_query = search_widget.value.lower()
  matching_books = [book for book in books if search_query in book.lower()]
  if matching_books:
    book_widget.options = matching_books
  else:
    book_widget.options = ["no found books"]



search_widget = widgets.Text(
    description = 'search book:',
    disabled = False,

  )

search_widget.on_submit(search)

feedback = widgets.HTML(value='', placeholder='Feedback will be shown here', layout=widgets.Layout(width='auto', margin='0 0 15px 0'))
feedback = widgets.HTML()


home_Tab = widgets.VBox([
    book_widget,
    details,
    add_to_cart,
    feedback
])

cart_Tab = widgets.VBox([
    cart_display,
    clear_cart_button,
    buy_now,
    feedback

])

search_Tab = widgets.VBox([
    search_widget,
    book_widget,
    feedback

])

logout_Tab = widgets.VBox([
    logout_button,
    feedback
])
admin_Tab = widgets.VBox([
    current_user_text,
    current_user_delete_button,
    make_user_admin_button,
    feedback
])

tabs = widgets.Tab([
    home_Tab,
    cart_Tab,
    search_Tab,
    logout_Tab,
    admin_Tab
])

register_tab = widgets.VBox([
    widgets.HTML('<h2>Register</h2>'),
    username_register,
    password_register,
    comfirm_password_register,
    register_button,
    feedback

])

Login_tab = widgets.VBox([
    widgets.HTML('<h2>Login</h2>'),
    username_login,
    password_login,
    login_button,
    feedback

])

auth_tabs = widgets.Tab([register_tab, Login_tab])
auth_tabs.set_title(0,"register")
auth_tabs.set_title(1,"login")

tabs.set_title(0,"Home")
tabs.set_title(1,"Cart")
tabs.set_title(2,"Search")
tabs.set_title(3,"logout")
tabs.set_title(4, "Admin")

display(auth_tabs)





