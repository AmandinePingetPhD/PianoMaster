"""Definition of models created."""

from django.db import models
from django.urls import reverse
from django.utils.timezone import now

# Models created

# PB d'authentif + pas de redirection
# Broken pipe ? Error ou pas
# BDD sqlite3 à créer
# import de données à faire avec csv
# pour admin favicon.ico not found

class PianoSheet(models.Model):
    """Table PianoSheet for partitions."""

    sheet_id = models.IntegerField(primary_key=True)
    title = models.TextField()
    author = models.TextField()
    level = models.IntegerField(default=0)
    kind = models.TextField()
    compteur = models.IntegerField(default=0)
    numsheet = models.IntegerField(default=1)

    class Meta:
        managed = True
        db_table = 'PianoSheet'

    def __str__(self):
        return "{0}".format(self.sheet_id, )

    def get_absolute_url(self):
        """Content details."""
        return reverse('recipe_detail', args=[str(self.sheet_id)])


class Musician(models.Model):
    """Table Cuisinier to store users' details."""

    user_id = models.AutoField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField(blank=True)
    date_visit = models.DateTimeField(default=now)
    email_address = models.TextField(blank=True)
    e_message = models.TextField(blank=True)
    sheet_id = models.IntegerField(blank=False, default='0')

    class Meta:
        managed = True
        db_table = 'Musician'

    def __str__(self):
        return "{0}".format(self.first_name, )


class Note(models.Model):
    """Table Note for suggestions's rating."""

    rating_id = models.AutoField(primary_key=True)
    rating = models.IntegerField(default='0')
    user_name = models.TextField(default='None')
    date_visit = models.DateTimeField(default=now)
    sheet_id = models.IntegerField(blank=False, default='0')

    class Meta:
        managed = True
        db_table = 'Note'

    def __str__(self):
        return "{0}".format(self.user_name, )


# Django models
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING,
                                     blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
