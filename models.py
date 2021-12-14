from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import bcrypt

db = SQLAlchemy()


# ======= DB Models =========
# User
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(20), unique=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), unique=True)  # Generated
    token = db.Column(db.String(40), unique=True)
    password = db.Column(db.Text)
    is_admin = db.Column(db.Boolean)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    @property
    def email(self):
        return f"{self.first_name}.{self.last_name}@tudublin.ie"

    @property
    def name(self):
        return f"{self.user_name} {self.first_name} {self.last_name}"

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.name

    @property
    def as_dict(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "created": self.created.isoformat() if self.created else None,
            "updated": self.updated.isoformat() if self.updated else None
        }

    @property
    def as_dict_short(self):
        return {
            "username": self.user_name,
            "email": self.email,
            "is_admin": self.is_admin
        }

    @staticmethod
    def create_password_hash(plaintext_password):
        if not plaintext_password:
            return None
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(b'plaintext_password', salt)

    def password_is_verified(self, entered_password):
        # entered_password = str(entered_password).encode("utf-8")
        # encoded_pw = str(self.password).encode("utf-8")
        dbpassword = self.password
        return bcrypt.checkpw(entered_password, dbpassword)

    # ======= User Login/Register =========
    # def usrLogin(self, usrname, pw):
    #     dbusername = User.query.filter_by(user_name=usrname).one_or_none()
    #     dbpassword = User.query.filter_by(password=pw).one_or_none()
    #
    #     if dbusername and dbpassword:
    #         print("the user is in the db and can login")
    #         return True
    #     else:
    #         print("Cant find User")
    #         return False

    def all_user(self):
        users = User.query(User).all()
        return users

    # ======= END User Login/Register =========


# Category
class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)
    hashtag = db.Column(db.String(20))
    description = db.Column(db.Text)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __str__(self):
        return f"{self.name} (#{self.hashtag})"

    @property
    def category_name(self):
        return self.name


# Post
class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    title = db.Column(db.String(50))
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    content = db.Column(db.Text)
    owner = db.relationship(User, backref=db.backref("owner_assoc"))
    category = db.relationship(Category, backref=db.backref("category_assoc"))

    def __str__(self):
        return f"{self.title}"

# ======= END DB Models =========
