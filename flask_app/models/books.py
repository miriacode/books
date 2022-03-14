from flask_app.config.mysqlconnection import connectToMySQL

#Importación Circular
from flask_app.models import authors

class Book:
    def __init__(self, data):
        self.id = data['id']
        self.title = data ['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        #Linked Many to Many
        self.authors = []

    #READ (All)
    @classmethod
    def get_all_books(cls):
        query = 'SELECT * FROM books'
        result = connectToMySQL('books').query_db(query)
        books = []
        for b in result:
            book = cls(b)
            books.append(book)
        return books

    #CREATE
    @classmethod
    def create_book(cls, form):
        query = "INSERT INTO books (title, num_of_pages) VALUES (%(title)s,%(num_of_pages)s)"
        result = connectToMySQL('books').query_db(query, form)
        return result

    #READ (ONE)
    @classmethod
    def get_book_by_id(cls,data):
        #data = {'id': '1'}
        query = "SELECT * FROM books.books LEFT JOIN favorites ON books.id = favorites.book_id LEFT JOIN books.authors ON books.authors.id = favorites.author_id WHERE books.books.id = %(id)s;"
        result = connectToMySQL('books').query_db(query, data)


        # [
        #     {'1','Harry Potter','312','2022-03-09 14:50:58','2022-03-09 14:50:58'}
        # ]
        bk = result[0]
        book = cls(bk)
        #Until there all attributes have been stored, except liked books (favorite books)
        for author in result:
            #de la tabla resultante con el query
            #guardo esos datos en forma de book_data porque eso es lo q recibe la clase book

            #Always: Cut whats not needed here eg:title,num_of_pages)
            author_data = {
                "id":author['authors.id'],
                "name":author['name'],
                "created_at": author['authors.created_at'],
                "updated_at": author['authors.updated_at']
            }
            print(author_data)
            #Importación Circular
            author = authors.Author(author_data)
            #Now author has his/her favorite books, thanks to:
            book.authors.append(author)
            
        return book

    #CREATE
    @classmethod
    def create_new_fav_author(cls,data):
        query = "INSERT INTO favorites (author_id,book_id) VALUES (%(author_id)s, %(book_id)s)"
        result = connectToMySQL('books').query_db(query, data)
        return result
