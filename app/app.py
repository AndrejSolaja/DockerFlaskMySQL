from flask import Flask, jsonify, request, render_template
import mysql.connector
import requests

app = Flask(__name__)

BASE_URL = 'http://localhost:5000'

config = {
        'user': 'root',
        'password': 'root',
        'host': 'mydb',
        'port': '3306',
        'database': 'library'
    }

db = mysql.connector.connect(**config)
cursor = db.cursor(dictionary=True)


@app.route('/books/all', methods=['GET'])
def get_all_books():
    # Retrieve all books from the database
    query = """
        SELECT b.bookID, b.title, b.categoryID, b.publisherID, GROUP_CONCAT(a.name) AS authors
        FROM Books b
        JOIN BookAuthor ba ON b.bookID = ba.bookID
        JOIN Authors a ON ba.authorID = a.authorID
        GROUP BY b.bookID
    """
    cursor.execute(query)
    books = cursor.fetchall()
    return jsonify(books)

@app.route('/books/add', methods=['POST'])
def add_book():
    # Parse request data
    data = request.get_json()
    title = data['title']
    category_id = data['category_id']
    publisher_id = data['publisher_id']
    author_ids = data.get('author_ids', [])  # Optional: List of author IDs

    # Add book to the database
    query = "INSERT INTO Books (title, categoryID, publisherID) VALUES (%s, %s, %s)"
    cursor.execute(query, (title, category_id, publisher_id))
    db.commit()

    # Get the ID of the newly added book
    book_id = cursor.lastrowid

    # Add book author relations to the database
    for author_id in author_ids:
        # Check if the author exists
        cursor.execute("SELECT * FROM Authors WHERE authorID = %s", (author_id,))
        author = cursor.fetchone()
        if not author:
            return jsonify({'message': f'Author with ID {author_id} not found'}), 404

        # Add book author relation to the database
        query = "INSERT INTO BookAuthor (bookID, authorID) VALUES (%s, %s)"
        cursor.execute(query, (book_id, author_id))
        db.commit()

    return jsonify({'message': 'Book added successfully'})


@app.route('/books/delete/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    # Check if the book exists
    cursor.execute("SELECT * FROM Books WHERE bookID = %s", (book_id,))
    book = cursor.fetchone()
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    # Delete book from the database
    query = "DELETE FROM Books WHERE bookID = %s"
    cursor.execute(query, (book_id,))
    db.commit()
    return jsonify({'message': 'Book deleted successfully'})


@app.route('/books/get/<int:book_id>', methods=['GET'])
def get_book(book_id):
    # Retrieve book information from the database
    query = """
        SELECT b.bookID, b.title, b.categoryID, b.publisherID, a.name AS author_name
        FROM Books b
        JOIN BookAuthor ba ON b.bookID = ba.bookID
        JOIN Authors a ON ba.authorID = a.authorID
        WHERE b.bookID = %s
    """
    cursor.execute(query, (book_id,))
    books = cursor.fetchall()
    if books:
        book_info = {
            'bookID': books[0]['bookID'],
            'title': books[0]['title'],
            'categoryID': books[0]['categoryID'],
            'publisherID': books[0]['publisherID'],
            'authors': [book['author_name'] for book in books]
        }
        return jsonify(book_info)
    else:
        return jsonify({'message': 'Book not found'}), 404



@app.route('/')
def index():
    return "Server works"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)