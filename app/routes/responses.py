# app/routers/response.py
from flask import Blueprint, request, jsonify
from app.models import db
from app.models.question import Statistic, Question
from app.models.response import Response

responses_bp = Blueprint('responses', __name__, url_prefix='/responses')

@responses_bp.route('/', methods=['GET'])
def get_responses():
    statistics = Statistic.query.all()
    results = [
        {
            "question_id": stat.question_id,
            "agree_count": stat.agree_count,
            "disagree_count": stat.disagree_count
        }
        for stat in statistics
    ]
    return jsonify(results), 200@responses_bp.route('/', methods=['POST'])
def add_response():
    data = request.get_json()
    if not data or 'question_id' not in data or 'is_agree' not in data:
        return jsonify({'message': "Некорректные данные"}), 400

    text = data.get('text', '')
    if not text:
        return jsonify({'message': "Поле 'text' обязательно"}), 400

    question = Question.query.get(data['question_id'])
    if not question:
        return jsonify({'message': "Вопрос не найден"}), 404

    response = Response(
        question_id=question.id,
        is_agree=data['is_agree'],
        text=text
    )
    db.session.add(response)

    statistic = Statistic.query.filter_by(question_id=question.id).first()
    if not statistic:
        statistic = Statistic(question_id=question.id, agree_count=0, disagree_count=0)
        db.session.add(statistic)
    if data['is_agree']:
        statistic.agree_count += 1
    else:
        statistic.disagree_count += 1
    db.session.commit()
    return jsonify({'message': f"Ответ на вопрос {question.id} добавлен"}), 201