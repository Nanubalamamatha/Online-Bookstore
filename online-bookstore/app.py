from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import os

app = Flask(__name__)
app.secret_key = 'bookstore_secret_key'

# Load books from JSON
with open('books.json') as f:
    books = json.load(f)


# Home page - Display books
@app.route('/')
def index():
    return render_template('index.html', books=books)


# API to get books
@app.route('/api/books')
def get_books():
    return jsonify(books)


# Shopping cart - Initialize session if not exists
@app.route('/cart')
def view_cart():
    if 'cart' not in session:
        session['cart'] = []
    cart_items = session['cart']
    return render_template('cart.html', cart=cart_items)


# Add book to cart
@app.route('/add_to_cart/<int:book_id>', methods=['POST'])
def add_to_cart(book_id):
    if 'cart' not in session:
        session['cart'] = []
    for book in books:
        if book['id'] == book_id:
            session['cart'].append(book)
            session.modified = True
            break
    return redirect(url_for('index'))


# Remove book from cart
@app.route('/remove_from_cart/<int:book_id>', methods=['POST'])
def remove_from_cart(book_id):
    if 'cart' in session:
        session['cart'] = [book for book in session['cart'] if book['id'] != book_id]
        session.modified = True
    return redirect(url_for('view_cart'))


# Place order
@app.route('/place_order', methods=['POST'])
def place_order():
    if 'cart' in session and session['cart']:
        session.pop('cart', None)
        return render_template('order.html', message="Your order has been placed successfully!")
    return render_template('cart.html', cart=[], message="Your cart is empty!")


if __name__ == '__main__':
    app.run(debug=True)
