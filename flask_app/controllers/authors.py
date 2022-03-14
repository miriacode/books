from flask import Flask, render_template, request, redirect

from flask_app import app
from flask_app.models.authors import Author
from flask_app.models.books import Book


@app.route('/authors')
def authors_index():
    authors = Author.get_all_authors()
    return render_template("authors.html", authors=authors)

@app.route('/authors/add',methods =['POST'])
def authors_add():
    Author.create_author(request.form)
    return redirect('/authors')

@app.route('/books')
def books_index():
    books = Book.get_all_books()
    return render_template("books.html", books=books)

@app.route('/books/add',methods =['POST'])
def books_add():
    Book.create_book(request.form)
    return redirect('/books')


@app.route('/authors/<int:id>')
def author_show(id):
    data = {
        "id": id
    }
    author = Author.get_author_by_id(data)
    books = Book.get_all_books()
    return render_template("author_show.html", author=author, books=books)

@app.route('/authors/add_favorite', methods=['POST'])
def author_add_fav_book():
    data = {
        "author_id" : request.form['author_id'],
        "book_id" : request.form['book_id']
    }
    Author.create_new_fav_book(data)
    return '<script>document.location.href = document.referrer</script>'


@app.route('/books/<int:id>')
def book_show(id):
    data = {
        "id": id
    }
    book= Book.get_book_by_id(data)
    authors = Author.get_all_authors()
    print(authors)
    return render_template("book_show.html",book=book,authors=authors)


@app.route('/books/add_favorite', methods=['POST'])
def book_add_fav_author():
    data = {
        "author_id" : request.form['author_id'],
        "book_id" : request.form['book_id']
    }
    Book.create_new_fav_author(data)
    return '<script>document.location.href = document.referrer</script>'
