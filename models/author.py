from database.connection import get_db_connection

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Author {self.name}>"

    def articles(self):
        """Return a list of articles associated with this author."""
        from models.article import Article  
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        articles_data = cursor.fetchall()
        conn.close()
        return [Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"]) for article in articles_data]

    def magazines(self):
        """Return a list of magazines associated with this author."""
        from models.magazine import Magazine 
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT magazines.* FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        ''', (self.id,))
        magazines_data = cursor.fetchall()
        conn.close()
        return [Magazine(magazine["id"], magazine["name"], magazine["category"]) for magazine in magazines_data]
