from django.db import models
from django.utils.encoding import smart_bytes
from shortuuid.django_fields import ShortUUIDField    #package to creat customizable ids of you wish
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

STATUS_CHOICE = (
    ("Processing", "Processing"),
    ("Shipping", "Shipping"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("Draft", "Draft"),
    ("Disable", "Disable"),
    ("rejected", "rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

RATING = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),

)

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)  # If instance.user.id = 42 and filename = 'profile_pic.jpg', the function will return: user_42/profile_pic.jpg'

# Create your models here.
class Category(models.Model):
    cid = ShortUUIDField(unique=True, length = 10, max_length=30, prefix = "cat", alphabet = "abcdefgh12345")  #cat575e9969795t69
    title = models.CharField( max_length=100, default="Toys")   #title Heading
    image = models.ImageField( upload_to='category', default="category.jpg")  #thumbnail of image

    class Meta:
        verbose_name_plural = "Categories"  #categorys ==> Categories  in table

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))  # This is the fuction we have creted in order to return image
    
    def __str__(self):
        return self.title
    
class tags(models.Model):   # tagmanager
    pass
    
class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length = 10, max_length=30, prefix = "ven", alphabet = "abcdefgh12345")  #cat575e9969795t69
    title = models.CharField( max_length=100, default="Rohan")   #title Heading
    image = models.ImageField( upload_to=user_directory_path, default="assets/images/pushpa_img.jpeg")  #thumbnail of image
    # description = models.TextField(null= True, blank= True, default="Amazing Vendor")
    description = RichTextUploadingField(null= True, blank= True, default="Amazing Vendor")

    cover_image = models.ImageField( upload_to=user_directory_path, default="assets/images/background-pattern.jpg")  #thumbnail of image

    address = models.CharField(max_length=100, default="Pune Pimpri")
    contact = models.CharField(max_length=100, default="(91)+987654321")
    chat_resp_time = models.CharField(max_length=100, default="100")
    shipping_on_time = models.CharField(max_length=100, default="100")
    authentic_rating = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="100")
    warranty_period = models.CharField(max_length=100, default="100")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField( auto_now_add=True, null=True, blank = True)
    class Meta:
        verbose_name_plural = "Vendors"  #categorys ==> Categories  in table

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))  # This is the fuction we have creted in order to return image
    
    def __str__(self):
        return self.title
    
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length = 10, max_length=30, alphabet = "abcdefgh12345")  #cat575e9969795t69

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name='product')


    title = models.CharField( max_length=100, default="Fresh Cookies")   #title Heading
    image = models.ImageField( upload_to=user_directory_path, default="product.jpg")  #thumbnail of image
    # description = models.TextField(null= True, blank= True, default="This is product")
    description = RichTextUploadingField(null= True, blank= True, default="This is product")


    price = models.DecimalField(max_digits=9999999999999, decimal_places=2, default="1.99")
    old_price = models.DecimalField(max_digits=9999999999999, decimal_places=2, default="2.99")

    specification = RichTextUploadingField(null=True, blank=True)
    # specification = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=100, default="Organic",null = True, blank=True)
    life = models.CharField(max_length=100, default="100",null = True, blank=True)
    mfg = models.DateTimeField(auto_now_add=False, null = True, blank=True)
    stock = models.DecimalField(max_digits=10000000, decimal_places=0,  null=True, blank=True)
    #tags = models.ForeignKey(tags, on_delete=models.SET_NULL, null=True)
    tags = TaggableManager(blank=True)

    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    vid = ShortUUIDField(unique=True, length = 4, max_length=20, prefix="sku", alphabet = "1234567890")  #cat575e9969795t69

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null = True, blank=True)

    
    class Meta:
        verbose_name_plural = "Product"  #categorys ==> Categories  in table

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))  # This is the fuction we have creted in order to return image
    
    def __str__(self):
        return self.title
    
    #for Discount
    def get_percentage(self):
        #formula
        #(10 / 25) * 100  new price / old price

        new_price = ((self.old_price - self.price)/self.old_price) * 100
        return new_price
    
# fro multiple Images
class ProductImages(models.Model):
    images = models.ImageField(upload_to = "product-images", default="product.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null = True, related_name="p_images")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"  #categorys ==> Categories  in table

############################################# Cart Order, OrderItem #####################################


class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9999999999999, decimal_places=2, default="1.99")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=10, default="Processing")

    class Meta:
        verbose_name_plural = "Cart Order"  #categorys ==> Categories  in table


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    images = models.CharField(max_length=200)
    qty = models.IntegerField(max_length=200, default=0)
    price = models.DecimalField(max_digits=9999999999999, decimal_places=2, default="1.99")
    total = models.DecimalField(max_digits=9999999999999, decimal_places=2, default="1.99")

    class Meta:
        verbose_name_plural = "Cart Order Items"  #categorys ==> Categories  in table
    
    def order_image(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))  # This is the fuction we have creted in order to return image
    
    
    ############################################### Product  Review, wishlist, address ####################################


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="review")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING , default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"  #categorys ==> Categories  in table

    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    
class wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "wish list"  #categorys ==> Categories  in table

    def __str__(self):
        return self.product.title
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null = True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"  #categorys ==> Categories  in table







    




   

