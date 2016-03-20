# cinarra
Test task

Need to implement http server without frontend, only backend. You can implement your own server or use libraris like Flask or Tornado except Django. Server should store information about books such as:

Title (unique)
Author
Page count
Date of publication
Title is unique field.

As a data storage you need to implement simple in-memory db.
Server should able to use next requests:

1. POST request. Send data to server. Data sending in request header in field "XBook-data" in JSON format. If book doesn't exist and saving passed correctly, should be returned success code and success message. If book with such title already exist, server should return error code and error message. All returned message should be in JSON format.

2. PUT request. Send data update to server. Data sending in request header in field "XBook-data" in JSON format. If book doesn't exist server should return error code and error message. If book exist server should update information about this book and return success code and success message. All returned message should be in JSON format.

3. GET request. Get data from server. If book not exist server should return error code and error message. If book exist server should return success code and information about this book. All returned message should be in JSON format.

4. DELETE request. Removing data from server. If book doesn't exist server should return error code and error message. If book exist server should delete information about this book and return success code and success message. All returned message should be in JSON format.

Server should provide CLI interface. This interface should contain the same commands as in http requests + statistic information with data about book count in DB and time of last added, deleted and updated book. CLI command should be entered in plain text format, for example:
get stats
get book “war and peace”
delete book “war and peace”
And etc. Information should be returned in plain text format to. To provide access to CLI you can use Telnet utility.

Server should be covered by unit and functional tests and be tested with load tests.
For testing server we will use CURL and Telnet utility. Server should be able to run on Ubuntu OS 14.04.

Links:

HTTP error codes description: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

Ubuntu CURl: http://askubuntu.com/questions/299870/http-post-and-get-using-curl-in-linux

JSON: http://www.json.org/

# To get started:
0)setup python 3.4.3

1) clone repo

2) pip install -r requirments.txt

3) from folder app run server.py, after that we can use curl

4) tests.py run from folder app

# cURL examples
POST: curl -H "Content-Type: application/json" -X POST -d '{"XBook-data":{"title":"xyz","author":"xyz"}}' http://localhost:8080/books

PUT: curl -H "Content-Type: application/json" -X PUT -d '{"XBook-data":{"title":"xyz","author":"xyz"}}' http://localhost:8080/books

GET: curl -H "Content-Type: application/json" -X GET http://localhost:8080/books/bible

DELETE: curl -H "Content-Type: application/json" -X DELETE http://localhost:8080/books/bible

# Apache benchmark examples
To get 100000 GET requests
ab -n 100000 -c 5  http://127.0.0.1:8080/books/bible > ab_get_test_100k.txt

To get 100000 PUT requests(put.txt placed in folder test)
ab -n 100000 -u put.txt -T application/json http://127.0.0.1:8080/books > ab_put_test_100k.txt

JMeter file(HTTP Request.jmx) placed into /test/reports 
Data for JMeter(data.csv) app placed into folder test
