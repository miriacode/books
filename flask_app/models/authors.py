from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.books import Book

class Author:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        #Link Many to Many
        self.books = []
    
    #READ (ALL)
    @classmethod
    def get_all_authors(cls):
        query = "SELECT * FROM authors"
        results = connectToMySQL('books').query_db(query)
        authors = []

        for a in results:
            author = cls(a)
            authors.append(author)
        return authors

    #CREATE
    @classmethod
    def create_author(cls, form):
        query = "INSERT INTO authors (name) VALUES (%(name)s)"
        result = connectToMySQL('books').query_db(query, form)
        return result

    #READ (One)
    @classmethod
    def get_author_by_id(cls,data):
        #data = {"id": "1"}
        query = "SELECT * FROM books.authors LEFT JOIN favorites ON authors.id = favorites.author_id LEFT JOIN books.books ON books.books.id = favorites.book_id WHERE books.authors.id = %(id)s;"
        result = connectToMySQL('books').query_db(query, data)


        # [
        #     {'1','J.K.Rowling','2022-03-09 14:50:58','2022-03-09 14:50:58'}
        # ]
        auth = result[0]
        author = cls(auth)
        #Until there all attributes have been stored, except liked books (favorite books)

        for book in result:
            #de la tabla resultante con el query
            #guardo esos datos en forma de book_data porque eso es lo q recibe la clase book

            #Always: Cut whats not needed here eg:title,num_of_pages)
            book_data = {
                "id":book['books.id'],
                "title":book['title'],
                "num_of_pages":book['num_of_pages'],
                "created_at": book['books.created_at'],
                "updated_at": book['books.updated_at']
            }
            print(book_data)
            book = Book(book_data)
            #Now author has his/her favorite books, thanks to:
            author.books.append(book)

        return author


    #CREATE
    @classmethod
    def create_new_fav_book(cls,data):
        query = "INSERT INTO favorites (author_id,book_id) VALUES (%(author_id)s, %(book_id)s)"
        result = connectToMySQL('books').query_db(query, data)
        return result

    

   

    #READ
    # @classmethod
    # def get_ninjas_by_dojo_id(cls, data):
    #     query = "SELECT * FROM ninjas WHERE dojo_id = %(dojo_id)s"
    #     results = connectToMySQL('books').query_db(query,data)
    #     ninjas =[]
    #     print(results)
    #     for n in results:
    #         #Lo obligo a que sea instancia de ninjas, ahora tenemos un ninj relleno en todos los campos, pero con un self.dojo= None
    #         ninj = cls(n)
    #         data = {
    #             "id": ninj.dojo_id
    #         }
    #         returnedDojo = Book.get_dojo_by_id(data)
    #         ninj.dojo = returnedDojo
    #         #Ya esta listo y se inserta a la lista
    #         ninjas.append(cls(n))
        
    #     return ninjas
    