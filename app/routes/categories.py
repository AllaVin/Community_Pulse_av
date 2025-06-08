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
    category = Category.query.get(id)
    if category is None:
        return jsonify({"warning": "No such category ID was found"}), 404
    return jsonify({"id": category.id, "name": category.name}), 200


@categories_bp.route("/<int:id>", methods=["PUT"])
def update_category(id):
    category = Category.query.get(id)
    if category is None:
        return jsonify({"warning": "No such category ID was found"}), 404

    data = request.get_json()
    new_name = data.get("name")
    if not new_name:
        return jsonify({"error": "Поле 'name' обязательно"}), 400

    category.name = new_name
    db.session.commit()
    return jsonify({"message": "Категория обновлена", "id": category.id, "name": category.name}), 200


@categories_bp.route("/<int:id>", methods=["DELETE"])
def delete_category(id):
    category = Category.query.get(id)
    if category is None:
        return jsonify({"error": "Категория с таким ID не найдена"}), 404

    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": f"Категория с ID {id} удалена"}), 200
