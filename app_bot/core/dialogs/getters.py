from aiogram.enums import ContentType
from core.database.models import User, Category, Product, UserProduct, Order, Post
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from settings import settings


async def get_welcome_msg(dialog_manager: DialogManager, **kwargs):
    welcome_post = await Post.get(id=settings.welcome_post_id)

    return {
        'caption': welcome_post.text,
        'photo': MediaAttachment(ContentType.PHOTO, url=welcome_post.photo_file_id)
    }


async def get_categories(dialog_manager: DialogManager, **kwargs) -> dict[str, list[Category]]:
    return {
        'categories': await Category.all()
    }


async def get_products_by_category(dialog_manager: DialogManager, **kwargs) -> dict[str, list[Product]]:
    current_page = await dialog_manager.find('product_scroll').get_page()
    category_id = dialog_manager.dialog_data['category_id']


    products = await Product.filter(category_id=category_id).all()
    if not products:
        raise ValueError
    current_product = products[current_page]

    # product data for page
    product_data = await get_product_info_data(product=current_product)

    # data for CallbackHandler
    if products:
        dialog_manager.dialog_data['pages'] = len(products)
    dialog_manager.dialog_data['category_id'] = category_id
    dialog_manager.dialog_data['current_product_id'] = current_product.id

    return {
        'pages': len(products),
        'current_page': current_page + 1,
        'media_content': product_data['media_content'],
        'name': current_product.name,
        'description': current_product.description,
        'price': current_product.price,
    }


async def get_product_info_data(product: Product):
    if not product:
        raise ValueError

    media_content = None
    if product.media_content:
        media_content = MediaAttachment(ContentType.PHOTO, url=product.media_content)


    return {
        'media_content': media_content,
        'name': product.name,
    }
