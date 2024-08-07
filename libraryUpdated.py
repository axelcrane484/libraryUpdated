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

def deposit_money(b):
  global budget
  deposit_value = deposit_widget.value
  if deposit_value > 0 or deposit_value < 500:
     budget = budget + deposit_value
     print("new balance is",budget)
  else:
     print("please enter a valid amount")


deposit_button = widgets.Button(
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
  global budget
  selected_book = book_widget.value
  price = books[selected_book]['price']
  if price <= budget:
    print("you have bought", selected_book)
    budget -= price
    print("you have £",budget,"left")
  else:
    print("you do not have any money")

buy_now = widgets.Button(
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
display(buy_now)