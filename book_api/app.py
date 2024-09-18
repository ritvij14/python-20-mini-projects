import bcrypt
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
http_auth = HTTPBasicAuth()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "publication_year": self.publication_year,
        }


def init_db():
    with app.app_context():
        db.create_all()
        if Book.query.count() == 0:
            sample_books = [
                Book(
                    title="The Great Gatsby",
                    author="F. Scott Fitzgerald",
                    publication_year=1925,
                ),
                Book(
                    title="To Kill a Mockingbird",
                    author="Harper Lee",
                    publication_year=1960,
                ),
                Book(title="1984", author="George Orwell", publication_year=1949),
            ]
            db.session.add_all(sample_books)
            db.session.commit()


authenticated_users = {
    "username": "admin",
    "password": bcrypt.hashpw("password".encode("utf-8"), bcrypt.gensalt()),
}


@http_auth.verify_password
def verify_user(username, password):
    if username == authenticated_users["username"]:
        return bcrypt.checkpw(password.encode("utf-8"), authenticated_users["password"])
    return False


@http_auth.error_handler
def auth_error():
    return jsonify({"error": "Access denied"}), 401


@app.route("/")
def hello():
    return "welcome to the book library API!"


@app.route("/login", methods=["POST"])
def login():
    if verify_user(request.authorization.username, request.authorization.password):
        return jsonify({"message": "login successful"}), 200
    return jsonify({"message": "login failed"}), 401


@app.route("/books", methods=["GET"])
def get_books():
    title = request.args.get("title", None, str)
    author = request.args.get("author", None, str)
    page = request.args.get("page", 1, int)
    per_page = request.args.get("per_page", 10, int)

    query = Book.query

    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))

    pagination = query.paginate(page=page, per_page=per_page)
    books = pagination.items
    if not books and page != 1:
        return jsonify({"error": "Page number out of range"}), 404

    return jsonify(
        {
            "books": [book.to_dict() for book in books],
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": page,
            "per_page": per_page,
        }
    )


@app.route("/books/<int:id>", methods=["GET"])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify(book.to_dict())


@http_auth.login_required
@app.route("/books", methods=["POST"])
def create_book():
    if not http_auth.current_user():
        return jsonify({"error": "Authentication required"}), 401

    try:
        data = request.json
        if not all(key in data for key in ("title", "author", "publication_year")):
            return jsonify({"error": "Missing required fields"}), 400

        new_book = Book(
            title=data["title"],
            author=data["author"],
            publication_year=data["publication_year"],
        )
        db.session.add(new_book)
        db.session.commit()
        return jsonify(new_book.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@http_auth.login_required
@app.route("/books/<int:id>", methods=["PUT"])
def update_book(id):
    if not http_auth.current_user():
        return jsonify({"error": "Authentication required"}), 401

    try:
        data = request.json
        book = Book.query.get_or_404(id)
        book.title = data["title"]
        book.author = data["author"]
        book.publication_year = data["publication_year"]
        db.session.commit()
        return jsonify(book.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@http_auth.login_required
@app.route("/books/<int:id>", methods=["DELETE"])
def delete_book(id):
    if not http_auth.current_user():
        return jsonify({"error": "Authentication required"}), 401

    try:
        book = Book.query.get_or_404(id)
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "book deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
