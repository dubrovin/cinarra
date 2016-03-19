from sqlite3 import connect as conn

class DataBase(object):
    SETUP_TABLE = '''
    CREATE TABLE books(
            title varchar(255) PRIMARY KEY,
            author varchar(255),
            page_count int,
            date_of_publication DATE
        );
    INSERT INTO books
        VALUES ('bible', 'unknown', '600', '0001-11-22'),
                ('world and war', 'dostoevsky', '2000', '1801-11-22');
    '''
    INSERT_TEMPLATE = '''
        INSERT INTO books (title, author, page_count, date_of_publication)
        VALUES(?, ?, ?, ?);
    '''

    EXISTS_TEMPALTE = '''
            SELECT title FROM books
            WHERE title=?
            LIMIT 1;
    '''

    SELECT_TEMPLATE = '''
        SELECT title, author, page_count, date_of_publication FROM books
        WHERE title=?
    '''

    UPDATE_TEMPLATE = '''
        UPDATE books
        SET author=?, page_count=?, date_of_publication=?
        WHERE title='{title}'
    '''

    DELETE_TEMPLATE = '''
        DELETE FROM books
        WHERE title=?
    '''

    def __init__(self, db_name=':memory:'):
        self.connect = conn(db_name)
        self.connect.executescript(self.SETUP_TABLE)

    def exists(self, title):
        result = self.connect.execute(self.EXISTS_TEMPALTE, (title, ))
        return result.fetchone()

    def append(self, book):
        self.connect.execute(self.INSERT_TEMPLATE, book)

    def update(self, title, book):
        self.connect.execute(
            self.UPDATE_TEMPLATE.format(title=title), book[1:]
        )

    def select(self, title):
        result = self.connect.execute(self.SELECT_TEMPLATE, (title, ))
        return result.fetchone()

    def remove(self, title):
        self.connect.execute(self.DELETE_TEMPLATE, (title, ))

    @staticmethod
    def prepare_data(book):
        return (
            book['title'],
            book.get('author', ''),
            book.get('page_count', 0),
            book.get('date_of_publication', '')
        )