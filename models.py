from app import db


class Shortcut(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input = db.Column(db.String(127))
    output = db.Column(db.String(1920))

    def __repr__(self):
        return f"<User {self.input}>"

    def get_username(self):
        return self.username


db.create_all()
