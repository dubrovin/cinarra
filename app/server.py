from bottle import Bottle, run, get, post, put, delete, request, response, redirect
from data_base import DataBase
app = Bottle()
db = DataBase()
err_404 = {
    'code': 404,
    'status': '404 Not Found',
    'message': 'Error! Book not found.'
}

err_400 = {
    'code': 400,
    'status': '400 Bad Request',
    'message': 'Error! Empty book title.'
}

@app.post('/books')
def create_book():
    # import ipdb; ipdb.set_trace()
    book = request.json['XBook-data']
    result = err_400
    if book.get('title', ''):
        if db.exists(book['title']) is None:
            db.append(db.prepare_data(book))
            result = {
                'code': 201,
                'status': '201 Created',
                'message': 'Success! Book was created.'
            }
        else:
            result = {
                'code': 302,
                'status': '302 Found',
                'message': 'Error! Book already in db.'
            }
            response.status = result['status']
            redirect('/books/%s' % book['title'])
    response.status = result['status']
    return result

@app.put('/books')
def update_book():
    book = request.json['XBook-data']
    result = err_400
    if book.get('title', ''):
        if db.exists(book['title']):
            db.update(book['title'], db.prepare_data(book))
            result = {
                'code': 200,
                'status': '200 OK',
                'message': 'Success! Book was updated.'
            }
        else:
            result = err_404
    response.status = result['status']
    return result

@app.get('/books/:title')
def get_book(title=''):
    result = err_400
    if title:
        if db.exists(title):
            book_in_db = db.select(title)
            result = {
                'code': 200,
                'status': '200 OK',
                'message': 'Success! Book was found.',
                'XBook-data': {
                    'title': book_in_db[0],
                    'author': book_in_db[1],
                    'page_count': book_in_db[2],
                    'date_of_publication': book_in_db[3],
                }
            }
        else:
            result = err_404
    response.status = result['status']
    return result

@app.delete('/books/:title')
def delete_book(title=''):
    result = err_400
    if title:
        if db.exists(title):
            db.remove(title)
            result = {
                'code': 200,
                'status': '200 OK',
                'message': 'Success! Book was deleted.'
            }
        else:
            result = err_404
    response.status = result['status']
    return result
if __name__ == '__main__':
    run(app, host='localhost', port=8080, reloader=True)


# POST
# curl -H "Content-Type: application/json" -X POST -d '{"XBook-data":{"title":"xyz","author":"xyz"}}' http://localhost:8080/books

# PUT
# curl -H "Content-Type: application/json" -X PUT -d '{"XBook-data":{"title":"xyz","author":"xyz"}}' http://localhost:8080/books

# GET
# curl -H "Content-Type: application/json" -X GET http://localhost:8080/books/bible

# DELETE
# curl -H "Content-Type: application/json" -X DELETE -d '{"XBook-data":{"title":"xyz","author":"xyz"}}' http://localhost:8011/books

# curl 'http://localhost:8080/books/title' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36' --compressed