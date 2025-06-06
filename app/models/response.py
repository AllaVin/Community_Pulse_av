from app.models import db

class Response(db.Model):
    __tablename__ = 'responses'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    is_agree = db.Column(db.Boolean, nullable=False)  # True if agree, False if disagree
    text = db.Column(db.Text, nullable=False) # Response text must be provided
    question = db.relationship('Question', back_populates='responses', lazy=True)

    def __repr__(self):
        return f'Response text: {self.text}'