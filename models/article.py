from database.connection import get_db_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f"<Article {self.title}>"

    def get_magazine(self):
        """Return the magazine associated with this article."""
        from models.magazine import Magazine  
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (self.magazine_id,))
        result = cursor.fetchone()
        conn.close()
        return Magazine(result["id"], result["name"], result["category"])

    def get_author(self):
        """Return the author associated with this article."""
        from models.author import Author  
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (self.author_id,))
        result = cursor.fetchone()
        conn.close()
        return Author(result["id"], result["name"])
