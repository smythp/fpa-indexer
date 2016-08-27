import sqlite3
import json
import elasticsearch


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


conn = sqlite3.connect('book.db')
conn.row_factory = dict_factory
cur = conn.cursor()

books = list(cur.execute('SELECT id, title, full_text FROM book;'))

es = elasticsearch.Elasticsearch()


for book in books:
    book_json = json.dumps(book)
    es.index(index='books',
             doc_type='book',
             id=book['id'],
             body=book_json)
