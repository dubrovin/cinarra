import unittest
from webtest import TestApp
import server

test_app = TestApp(server.app)

class TestGet(unittest.TestCase):

    def test_found(self):
        # look up a word that should be in the dictionary
        title = 'bible'
        response = test_app.get('/books/%s' % title)

        # Response status should be HTTP 200 OK
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.status, '200 OK')

        book = {
            'author': 'unknown',
            'date_of_publication': '0001-11-22',
            'page_count': 600,
            'title': 'bible'
        }
        self.assertEqual(response.json['XBook-data'], book)

    def test_not_found(self):
        # look up a book not in the db
        # should return 404

        # need to tell WebTest to expect a status of 404
        # otherwise it will throw an exception
        response = test_app.get('/books/ghostbuster', status=404)
        self.assertEqual(response.status_int, 404)


class TestPostJSON(unittest.TestCase):

    def test_empty_title(self):
        json = dict()
        json['XBook-data'] = dict({
            'title': '',
            'author': 'anonymouse'
        })
        response = test_app.post_json('/books', json, status=400)
        self.assertEqual(response.status, '400 Bad Request')
        self.assertEqual(response.json['code'], 400)
        self.assertEqual(response.json['message'], 'Error! Empty book title.')

    def test_add(self):
        json = dict()
        json['XBook-data'] = dict({
            'title': 'hackers',
            'author': 'anonymouse'
        })
        response = test_app.post_json('/books', json)

        # Expect a new resource to be created
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.json['code'], 201)
        self.assertEqual(response.json['message'], 'Success! Book was created.')

        # to be really thorough, let's get the resource to ensure it was created
        response = test_app.get('/books/hackers')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.json['code'], 200)
        self.assertEqual(response.json['XBook-data']['title'], 'hackers')
        self.assertEqual(response.json['XBook-data']['author'], 'anonymouse')

    def test_already_in_db(self):
        # try to add a book that's already in the db
        json = dict()
        json['XBook-data'] = dict({
            'title': 'bible',
            'author': 'saint'
        })
        response = test_app.post_json('/books', json)
        # 302 indicating resource was found
        self.assertEqual(response.status, '302 Found')
        self.assertEqual(response.status_code, 302)

class TestPutJSON(unittest.TestCase):

    def test_update(self):
        # look up a word that should be in the db
        json = dict()
        json['XBook-data'] = dict({
            'title': 'bible',
            'author': 'anonymouse'
        })
        response = test_app.put_json('/books', json)

        # Response status should be HTTP 200 OK
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.status, '200 OK')


    def test_not_update(self):
        json = dict()
        json['XBook-data'] = dict({
            'title': 'ghostbuster',
            'author': 'anonymouse'
        })
        response = test_app.put_json('/books', json, status=404)
        self.assertEqual(response.status_int, 404)


class TestDelete(unittest.TestCase):

    def test_delete_ok(self):
        title = 'world and war'
        response = test_app.delete('/books/%s' % title)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.status, '200 OK')


    def test_not_found(self):
        title = 'ghostbuster'
        response = test_app.delete('/books/%s' % title, status=404)
        self.assertEqual(response.status_int, 404)
if __name__ == '__main__':
    unittest.main()