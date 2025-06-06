from app.models import db

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # --- Связь: одна категория — много вопросов ---
    questions = db.relationship('Question', back_populates='category', lazy=True)


    def __repr__(self):
        return f'Category: {self.name}'

#
# class Question(db.Model):
#     __tablename__ = 'questions'
#
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(255), nullable=False)
#     # --- Внешний ключ на категорию ---
#     category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
#
#     def __repr__(self):
#         return f'Category description: {self.text}'
#
