# app/routers/questions.py
from app.models.category import Category
from flask import Blueprint, request, jsonify
from app.models.question import Question
from app.models import db, question
from app.schemas.questions import MessageResponse, QuestionOut

questions_bp = Blueprint('questions', __name__, url_prefix='/questions')

# Questions related endpoints

@questions_bp.route("/", methods=["POST"])
def create_question():
    """Создание нового вопроса."""

    data = request.get_json()

    # Проверка на наличие текста вопроса и ID категории
    text = data.get("text")
    category_id = data.get("category_id")

    if not text or not category_id:
        return jsonify({"error": "Поле 'text' и 'category_id' обязательны"}), 400

    # Проверка существования категории
    from app.models.category import Category
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Категория с таким ID не найдена"}), 404

    # Создание нового вопроса
    question = Question(text=text, category_id=category_id)

    db.session.add(question)
    db.session.commit()

    return jsonify({
        "message": "Вопрос успешно создан",
        "id": question.id,
        "text": question.text,
        "category_id": question.category_id
    }), 201


@questions_bp.route('/', methods=['GET'])
def get_questions():
    """Получение списка всех вопросов из БД."""
    questions = Question.query.all()

    if questions:
        question_data = [QuestionOut(id=q.id, text=q.text, category_id=q.category_id) for q in questions]
        return jsonify(MessageResponse(message=question_data).model_dump()), 200
    else:
        return jsonify(MessageResponse(warning="No questions found").model_dump()), 200


@questions_bp.route('/<int:id>', methods=['GET'])
def get_question(id):
    """Получение деталей конкретного вопроса по его ID."""
    question = Question.query.get(id)
    if question is None:
        return jsonify({'warning': "Вопрос с таким ID не найден"}), 404
    return jsonify({'message': f"Вопрос: {question.text}"}), 200


@questions_bp.route('/<int:id>', methods=['PUT'])
def update_question(id):
    """Обновление конкретного вопроса по его ID."""
    question = Question.query.get(id)
    if question is None:
        return jsonify({'warning': "Вопрос с таким ID не найден"}), 404
    data = request.get_json()
    if 'text' in data:
        question.text = data['text']
        db.session.commit()
        return jsonify({'message': f"Вопрос обновлен: {question.text}"}), 200
    else:
        return jsonify({'warning': "Текст вопроса не предоставлен"}), 400


@questions_bp.route('/<int:id>', methods=['DELETE'])
def delete_question(id):
    """Удаление конкретного вопроса по его ID."""
    question = Question.query.get(id)
    if question is None:
        return jsonify({'warning': "Вопрос с таким ID не найден"}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': f"Вопрос с идентификатором {question.id} удален"}), 200


