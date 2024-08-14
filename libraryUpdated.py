 # library
 # multiple books that you can choose from
 # name of book with prices
 #button buy now
 #image at top, label at middle, buy now at bottom
 # budget £15

import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image
from IPython.display import display
import ipywidgets as widgets
import io
import random

Lord_of_the_Rings = 7
Harry_potter = 6
Fallen_Kingdom = 5
budget = 15
cart = []

books = {"Lord of the Rings" : {'price' : 7, 'author' : 'John Ronald', 'year' : 1942 }, "Harry Potter" :  {'price' : 6, 'author' : 'J.K. Rowling', 'year' : 1997 }, "Fallen Kingdom" :  {'price' : 5, 'author' : 'Elizabeth May', 'year' : 2000 }}

book_widget = widgets.RadioButtons(
          options = list(books.keys()),
          description='book:',
          disabled=False
   )

details = widgets.Textarea(
    value = "",
    description = "details :",
    disabled = True,
    layout = widgets.Layout(width = "50%", height = "100px"),
)

def add_cart(b):
  selected_book = book_widget.value
  if selected_book not in cart:
    cart.append(selected_book)
    update_cart_display()
  else:
    print(selected_book,"already in cart")

def update_cart_display():
  if cart:
    cart_details = "\n".join([f"{book} - ${books[book]['price']}" for book in cart])
    cart_display.value = cart_details
  else:
    cart_display.value = "cart is empty"



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
     print("new balance is",budget)
  else:
     print("please enter a valid amount")


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


def update_details(change):
  selected_book = book_widget.value
  book_info = books[selected_book]
  details.value = f"author = {book_info['author']}\nYear = {book_info['year']}\nPrice = {book_info['price']}"

book_widget.observe(update_details, names = 'value')

def buy(b):
  global budget, cart
  selected_book = book_widget.value
  price = sum(books[book]['price'] for book in cart)
  if price <= budget:
    print(f"you have bought{' '.join(cart)}")
    budget -= price
    print("you have £",budget,"left")
    cart.clear()
    update_cart_display()
  else:
    print("you do not have any money")

buy_now = widgets.Button(
    button_style = "success",
    tooltip = "buy your books",
    description = 'buy now',
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

display(search_widget)
display(book_widget)
display(details)
display(deposit_widget)
display(deposit_button)
display(add_to_cart)
display(cart_display)
display(buy_now)
