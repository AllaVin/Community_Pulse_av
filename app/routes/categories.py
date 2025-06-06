from flask import Blueprint, jsonify, request

from app.models import db
from app.models.category import Category

categories_bp = Blueprint("categories", __name__, url_prefix="/categories")

@categories_bp.route("/", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify([{"id": c.id, "name": c.name} for c in categories])

@categories_bp.route("/", methods=["POST"])
def create_category():
    data = request.get_json()

    # Проверка наличия поля name
    name = data.get("name")
    if not name:
        return jsonify({"error": "Поле 'name' обязательно"}), 400

    # Создание и сохранение категории
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()

    return jsonify({"message": "Категория успешно создана", "id": category.id}), 201


@categories_bp.route('/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.get_or_404(id)
    return jsonify({"id": category.id, "name": category.name})

@categories_bp.route('/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": f"Категория {id} удалена"}), 200
