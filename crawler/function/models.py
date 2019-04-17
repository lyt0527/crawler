# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

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
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

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


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment_content = models.CharField(max_length=255, blank=True, null=True)
    otherside_address = models.CharField(max_length=255, blank=True, null=True)
    source = models.IntegerField(blank=True, null=True)
    sys_score = models.FloatField(blank=True, null=True)
    arti_score = models.FloatField(blank=True, null=True)
    catch_time = models.DateTimeField(blank=True, null=True)
    comment_time = models.DateTimeField(blank=True, null=True)
    is_scored = models.IntegerField()
    is_saved = models.IntegerField()
    is_sys = models.PositiveIntegerField()
    author_id = models.CharField(max_length=255, blank=True, null=True)
    author_nickname = models.CharField(max_length=255, blank=True, null=True)
    author_realname = models.CharField(max_length=255, blank=True, null=True)
    author_tel = models.CharField(max_length=255, blank=True, null=True)
    comment_score = models.CharField(max_length=255, blank=True, null=True)
    add_comments = models.CharField(max_length=255, blank=True, null=True)
    comment_stars = models.CharField(max_length=255, blank=True, null=True)
    comment_images = models.CharField(max_length=255, blank=True, null=True)
    comment_type = models.CharField(max_length=255, blank=True, null=True)
    info = models.ForeignKey('OthersideInfo', models.DO_NOTHING, blank=True, null=True)
    order_id = models.CharField(max_length=255, blank=True, null=True)
    order_number = models.CharField(max_length=255, blank=True, null=True)
    otherside_comment_id = models.CharField(max_length=255, blank=True, null=True)
    platform = models.CharField(max_length=255, blank=True, null=True)
    module = models.CharField(max_length=255, blank=True, null=True)
    code_name = models.CharField(max_length=255, blank=True, null=True)
    replys_count = models.IntegerField()
    type = models.IntegerField(blank=True, null=True)
    label_id = models.CharField(max_length=255, blank=True, null=True)
    label_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comments'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

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


class DjangoSite(models.Model):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


class LogTemp(models.Model):
    content = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_temp'


class News(models.Model):
    comment_id = models.IntegerField(blank=True, null=True)
    comment_time = models.DateTimeField(blank=True, null=True)
    alert_time = models.DateTimeField(blank=True, null=True)
    comment_content = models.CharField(max_length=255, blank=True, null=True)
    platform = models.CharField(max_length=255, blank=True, null=True)
    comment_star = models.CharField(max_length=255, blank=True, null=True)
    author_tel = models.CharField(max_length=255, blank=True, null=True)
    author_realname = models.CharField(max_length=255, blank=True, null=True)
    comment_score = models.CharField(max_length=255, blank=True, null=True)
    comment_type = models.CharField(max_length=255, blank=True, null=True)
    order_id = models.CharField(max_length=255, blank=True, null=True)
    order_number = models.CharField(max_length=255, blank=True, null=True)
    arti_score = models.FloatField(blank=True, null=True)
    is_read = models.IntegerField()
    is_ignored = models.PositiveIntegerField()
    otherside_address = models.CharField(max_length=255, blank=True, null=True)
    catch_time = models.DateTimeField(blank=True, null=True)
    author_nickname = models.CharField(max_length=255, blank=True, null=True)
    comment_images = models.CharField(max_length=255, blank=True, null=True)
    add_comments = models.CharField(max_length=255, blank=True, null=True)
    source = models.IntegerField(blank=True, null=True)
    author_id = models.CharField(max_length=255, blank=True, null=True)
    otherside_comment_id = models.CharField(max_length=255, blank=True, null=True)
    module = models.CharField(max_length=255, blank=True, null=True)
    sys_score = models.FloatField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    code_name = models.CharField(max_length=255, blank=True, null=True)
    label_id = models.CharField(max_length=255, blank=True, null=True)
    label_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news'


class OthersideInfo(models.Model):
    otherside_info_id = models.AutoField(primary_key=True)
    platform = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'otherside_info'


class OthersideModule(models.Model):
    otherside_module_id = models.AutoField(primary_key=True)
    info = models.ForeignKey(OthersideInfo, models.DO_NOTHING, blank=True, null=True)
    module = models.CharField(max_length=255, blank=True, null=True)
    code_name = models.CharField(max_length=255, blank=True, null=True)
    parent_id = models.PositiveIntegerField()
    comment_type = models.CharField(db_column='comment__type', max_length=255, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.

    class Meta:
        managed = False
        db_table = 'otherside_module'


class Reply(models.Model):
    reply_content = models.CharField(max_length=255, blank=True, null=True)
    reply_user = models.CharField(max_length=255, blank=True, null=True)
    reply_time = models.DateTimeField(blank=True, null=True)
    reply_count = models.IntegerField()
    comment_id = models.IntegerField(blank=True, null=True)
    author_realname = models.CharField(max_length=255, blank=True, null=True)
    author_tel = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reply'


class SysScore(models.Model):
    sys_score_time = models.DateTimeField(blank=True, null=True)
    precision_rate = models.CharField(max_length=255, blank=True, null=True)
    sum = models.CharField(max_length=255, blank=True, null=True)
    correct = models.CharField(max_length=255, blank=True, null=True)
    wrong = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sys_score'
