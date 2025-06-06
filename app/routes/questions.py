# app/routers/questions.py
from flask import Blueprint, request, jsonify
from app.models.question import Question
from app.models import db

questions_bp = Blueprint('questions', __name__, url_prefix='/questions')

@questions_bp.route('/', methods=['GET'])
def get_questions():
    """Получение списка всех вопросов."""
    return "Список всех вопросов"

# @questions_bp.route('/', methods=['POST'])
# def create_question():
#     """Создание нового вопроса."""
#     return "Вопрос создан"


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






@questions_bp.route('/<int:id>', methods=['GET'])
def get_question(id):
    """Получение деталей конкретного вопроса по его ID."""
    return f"Детали вопроса {id}"

@questions_bp.route('/<int:id>', methods=['DELETE'])
def delete_question(id):
    """Удаление конкретного вопроса по его ID."""
    return f"Вопрос {id} удален"