from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f'<Magazine {self.name}>'

    def articles(self):
        """Return a list of articles associated with this magazine."""
        from models.article import Article  
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE magazine_id = ?', (self.id,))
        articles_data = cursor.fetchall()
        conn.close()
        return [Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"]) for article in articles_data]

    def contributors(self):
        """Return a list of authors who have contributed to this magazine."""
        from models.author import Author 
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        ''', (self.id,))
        authors_data = cursor.fetchall()
        conn.close()
        return [Author(author["id"], author["name"]) for author in authors_data]

    def article_titles(self):
        """Return the titles of all articles for this magazine."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT title FROM articles WHERE magazine_id = ?', (self.id,))
        titles = cursor.fetchall()
        conn.close()
        return [title["title"] for title in titles] if titles else None

    def contributing_authors(self):
        """Return authors who have written more than 2 articles for this magazine."""
        from models.author import Author  
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING COUNT(articles.id) > 2
        ''', (self.id,))
        authors_data = cursor.fetchall()
        conn.close()
        return [Author(author["id"], author["name"]) for author in authors_data] if authors_data else None
