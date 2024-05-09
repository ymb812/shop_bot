from django.db import models


class User(models.Model):
    class Meta:
        db_table = 'users'
        ordering = ['created_at']
        verbose_name = 'Пользователи'
        verbose_name_plural = verbose_name

    id = models.AutoField(primary_key=True, db_index=True)
    fio = models.CharField(max_length=64, null=True, blank=True)
    phone = models.CharField(max_length=64, null=True, blank=True)
    address = models.CharField(max_length=64, unique=True, null=True, blank=True)

    user_id = models.BigIntegerField(unique=True, null=True, blank=True)
    username = models.CharField(max_length=32, db_index=True, blank=True, null=True)
    status = models.CharField(max_length=32, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        display = self.username
        if not display:
            return f'{self.id}'
        return display


class Category(models.Model):
    class Meta:
        db_table = 'categories'
        ordering = ['id']
        verbose_name = 'Категории'
        verbose_name_plural = verbose_name

    id = models.AutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=32, null=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    class Meta:
        db_table = 'products'
        ordering = ['id']
        verbose_name = 'Товары'
        verbose_name_plural = verbose_name

    id = models.AutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=64)
    description = models.TextField()
    comment = models.TextField(null=True, default='', blank=True)
    price = models.IntegerField()
    media_content = models.CharField(max_length=256, null=True, blank=True)
    category = models.ForeignKey('Category', to_field='id', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class UserProduct(models.Model):
    class Meta:
        db_table = 'products_by_users'
        verbose_name = 'Корзины пользователей'
        verbose_name_plural = verbose_name

    id = models.AutoField(primary_key=True, db_index=True)
    product = models.ForeignKey('Product', to_field='id', on_delete=models.CASCADE)
    user = models.ForeignKey('User', to_field='user_id', on_delete=models.CASCADE)
    amount = models.IntegerField()
    order = models.ForeignKey('Order', to_field='id', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.product.name


class Order(models.Model):
    class Meta:
        db_table = 'orders'
        verbose_name = 'Заказы'
        verbose_name_plural = verbose_name

    id = models.UUIDField(primary_key=True, db_index=True)
    user = models.ForeignKey('User', to_field='user_id', on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    price = models.IntegerField()
    product_amount = models.IntegerField()
    address = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'


class Dispatcher(models.Model):
    class Meta:
        db_table = 'mailings'
        ordering = ['id']
        verbose_name = 'Рассылки'
        verbose_name_plural = verbose_name

    id = models.BigAutoField(primary_key=True)
    post = models.ForeignKey('Post', to_field='id', on_delete=models.CASCADE)
    send_at = models.DateTimeField()

    def __str__(self):
        return f'{self.id}'


class Post(models.Model):
    class Meta:
        db_table = 'static_content'
        ordering = ['id']
        verbose_name = 'Контент для рассылок'
        verbose_name_plural = verbose_name

    id = models.BigIntegerField(primary_key=True)
    text = models.TextField(blank=True, null=True)
    photo_file_id = models.CharField(max_length=256, blank=True, null=True)
    video_file_id = models.CharField(max_length=256, blank=True, null=True)
    video_note_id = models.CharField(max_length=256, blank=True, null=True)
    document_file_id = models.CharField(max_length=256, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'
