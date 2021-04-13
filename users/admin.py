from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User,Profile,FriendRequest
class ProfileAdmin(admin.ModelAdmin):
    list_display=['user','slug','bio',]
admin.site.register(Profile,ProfileAdmin)
admin.site.register(FriendRequest)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):

    fieldsets = (
        (None, {'fields': ('phone','email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone','email','first_name','last_name', 'password1', 'password2'),
        }),
    )
    list_display = ('phone','email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('phone','email', 'first_name', 'last_name')
    ordering = ('email',)

