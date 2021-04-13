from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.conf import settings
from autoslug import AutoSlugField
# Create your models here.

class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, phone,email,first_name,last_name, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,phone=phone,first_name=first_name,last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone,email,first_name,last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone,email,first_name,last_name, password, **extra_fields)

    def create_superuser(self, phone,email,first_name,last_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)


        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone,email,first_name,last_name,password, **extra_fields)



class User(AbstractUser):
    """User model."""

    phone		    = models.CharField(_('phone'),max_length=10,unique=True,default=None)
    email 			= models.EmailField(_('email address'), unique=True)
    username 		= None
    first_name		= models.CharField(_('First Name'),max_length=60,default=None)
    last_name		= models.CharField(_('Last Name'),max_length=60,default=None)
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email','first_name','last_name',]

    objects = UserManager()

 
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.png', upload_to='profile_pics')
	slug = AutoSlugField(populate_from='user')
	bio = models.CharField(max_length=255, blank=True)
	friends = models.ManyToManyField("Profile", blank=True)

	def __str__(self):
		return str(self.user.first_name)

	def get_absolute_url(self):
		return "/users/{}".format(self.slug)

def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except:
            pass

post_save.connect(post_save_user_model_receiver, sender=User)

class FriendRequest(models.Model):
	to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
	from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "From {}, to {}".format(self.from_user.first_name, self.to_user.first_name)
