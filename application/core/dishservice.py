from application import db
from application.core.models import Dish, DishCategory, CartItem
from application.core import exceptions
from typing import List, Optional
from application.utils import files
import os
from config import Config


def get_all_categories(sort_by_number: bool = False) -> List[DishCategory]:
    if sort_by_number:
        return DishCategory.query.order_by(DishCategory.number.asc()).all()
    else:
        return DishCategory.query.all()


def get_parent_categories(sort_by_number: bool = False) -> List[DishCategory]:
    if sort_by_number:
        return DishCategory.query.filter(DishCategory.parent_id == None).order_by(DishCategory.name.asc()).all()
    else:
        return DishCategory.query.filter(DishCategory.parent_id == None).all()


def get_category_by_id(category_id) -> DishCategory:
    return DishCategory.query.get_or_404(category_id)


def update_category(category_id: int, name_ru: str, parent_id=0, image=None):
    if parent_id == 0:
        parent_id = None
    category = DishCategory.query.get_or_404(category_id)
    category.name = name_ru
    category.parent_id = parent_id
    if image and image.filename != '':
        if category.image_path:
            files.remove_file(category.image_path)
        file_path = os.path.join(Config.UPLOAD_DIRECTORY, image.filename)
        files.save_file(image, file_path)
        category.image_id = None
        category.image_path = file_path
    db.session.commit()
    return category


def create_category(name_ru: str, parent_id=0, image=None) -> DishCategory:
    if parent_id == 0:
        parent_id = None
    category = DishCategory(name=name_ru, parent_id=parent_id)
    if image and image.filename != '':
        file_path = os.path.join(Config.UPLOAD_DIRECTORY, image.filename)
        files.save_file(image, file_path, recreate=True)
        category.image_path = file_path
    db.session.add(category)
    db.session.commit()
    return category


def remove_category(category_id: int):
    db.session.delete(DishCategory.query.get_or_404(category_id))
    db.session.commit()


def create_dish(name, description, image, price, quantity, category_id, show_usd=False):
    check_quantity = ''
    if quantity != check_quantity:
        check_quantity = quantity
    elif quantity == check_quantity:
        check_quantity = 0

    dish = Dish(name=name, description=description,
                price=price, quantity=check_quantity, category_id=category_id, show_usd=show_usd)
    if type(image) is str and image != '':
        file_path = os.path.join(Config.UPLOAD_DIRECTORY, image)
        dish.image_path = file_path
    elif image and image.filename != '':
        file_path = os.path.join(Config.UPLOAD_DIRECTORY, image.filename)
        files.save_file(image, file_path, recreate=True)
        dish.image_path = file_path
    db.session.add(dish)
    db.session.commit()
    return dish


def update_dish(dish_id, name, description, image, price, category_id, delete_image, show_usd, quantity):
    dish = get_dish_by_id(dish_id)
    dish.name = name
    dish.description = description
    dish.price = price
    dish.show_usd = show_usd
    dish.category_id = category_id
    dish.quantity = quantity
    if (image and image.filename != '') and not delete_image:
        if dish.image_path:
            files.remove_file(dish.image_path)
        file_path = os.path.join(Config.UPLOAD_DIRECTORY, image.filename)
        files.save_file(image, file_path)
        dish.image_id = None
        dish.image_path = file_path
    if delete_image:
        if dish.image_path:
            files.remove_file(dish.image_path)
        dish.image_path = None
        dish.image_id = None
    db.session.commit()


def remove_dish(dish_id: int):
    db.session.delete(Dish.query.get_or_404(dish_id))
    cart_items = CartItem.query.filter(CartItem.dish_id == dish_id).all()
    for cart_item in cart_items:
        db.session.delete(cart_item)
    db.session.commit()


def toggle_hidden_dish(dish_id: int):
    dish = Dish.query.get_or_404(dish_id)
    dish.is_hidden = not dish.is_hidden
    db.session.commit()
    return dish.is_hidden


def set_dish_number(dish_id, number):
    dish = get_dish_by_id(dish_id)
    dish.number = number
    db.session.commit()


def set_category_number(category_id, number):
    category = get_category_by_id(category_id)
    category.number = number
    db.session.commit()


def get_dish_by_id(dish_id: int):
    return Dish.query.get_or_404(dish_id)


def get_category_by_name(name: str, language: str, parent_category: DishCategory = None) -> Optional[DishCategory]:
    if parent_category:
        return DishCategory.query.filter(DishCategory.name == name, DishCategory.parent_id == parent_category.id).first()
    return DishCategory.query.filter(DishCategory.name == name).first()


def get_dishes_by_category_name(name: str, language: str, sort_by_number: bool = False, include_hidden=False) -> list:
    category = DishCategory.query.filter(DishCategory.name == name).first()
    if category:
        query = category.dishes
        if not include_hidden:
            query = query.filter(Dish.is_hidden != True)
        if sort_by_number:
            query = query.order_by(Dish.number.asc())
        return query.all()
    else:
        raise exceptions.CategoryNotFoundError()


def get_dishes_from_category(category: DishCategory, sort_by_number: bool = False, include_hidden=False) -> List[Dish]:
    query = category.dishes
    if not include_hidden:
        query = query.filter(Dish.is_hidden != True)
    if sort_by_number:
        query = query.order_by(Dish.number.asc())
    return query.all()


def get_dish_by_name(name: str, language: str, category: DishCategory = None) -> Dish:
    if category:
        dish = Dish.query.filter(Dish.name.like(name + '%'), Dish.category_id == category.id).first()
    else:
        dish = Dish.query.filter(Dish.name.like(name + '%')).first()
    return dish


def set_dish_image_id(dish: Dish, image_id: str):
    dish.image_id = image_id
    db.session.commit()


def set_category_image_id(category: DishCategory, image_id: str):
    category.image_id = image_id
    db.session.commit()


def get_dish_and_count():
    dish_and_count = Dish.query.order_by(Dish.description.asc()).all()
    return dish_and_count
