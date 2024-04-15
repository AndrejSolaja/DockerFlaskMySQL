import requests

BASE_URL = 'http://localhost:5000'

def get_book_req(book_id):
    response = requests.get(f'{BASE_URL}/books/get/{book_id}')
    return response.json()

def get_all_books_req():
    response = requests.get(f'{BASE_URL}/books/all')
    return response.json()

def add_book_req():
    title = input('Enter title: ')
    category_id = input('Enter category ID: ')
    publisher_id = input('Enter publisher ID: ')
    author_ids = input('Enter author IDs (comma-separated): ').split(',')
    data = {
        'title': title,
        'category_id': category_id,
        'publisher_id': publisher_id,
        'author_ids': [int(author_id) for author_id in author_ids]
    }
    response = requests.post(f'{BASE_URL}/books/add', json=data)
    print(response.json())


def delete_book_req(book_id):
    response = requests.delete(f'{BASE_URL}/books/delete/{book_id}')
    print(response.json())

def print_book(book):
    print(f"Book ID: {book['bookID']}")
    print(f"Title: {book['title']}")
    print(f"Category ID: {book['categoryID']}")
    print(f"Publisher ID: {book['publisherID']}")
    print(f"Authors: {book['authors']}")


def main():
    while True:
        print("\nMenu:")
        print("1. Get Book")
        print("2. Add Book")
        print("3. Delete Book")
        print("4. Get All Books")
        print("5. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            book_id = input("Enter book ID: ")
            book = get_book_req(int(book_id))
            print_book(book)
        elif choice == '2':
            add_book_req()
        elif choice == '3':
            book_id = input("Enter book ID to delete: ")
            delete_book_req(int(book_id))
        elif choice == '4':
            books = get_all_books_req()
            for book in books:
                print_book(book)
                print("-" * 30) 
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
