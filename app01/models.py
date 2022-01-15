# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models



class PatentApplicantDetail(models.Model):
    old_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    nation_code = models.IntegerField(blank=True, null=True)
    province = models.SmallIntegerField(blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    county = models.CharField(max_length=30, blank=True, null=True)
    category = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patent_applicant_detail'




class PatentConstGroupSet(models.Model):
    old_id = models.IntegerField(blank=True, null=True)
    group = models.IntegerField(blank=True, null=True)
    sort_index = models.SmallIntegerField(blank=True, null=True)
    stored_value = models.CharField(max_length=50, blank=True, null=True)
    display_name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    const_desc = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patent_const_group_set'




class PatentCategory(models.Model):
    old_id = models.IntegerField(blank=True, null=True)
    system = models.SmallIntegerField(blank=True, null=True)
    first_class = models.CharField(max_length=4, blank=True, null=True)
    second_class = models.CharField(max_length=4, blank=True, null=True)
    third_class = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    note = models.CharField(max_length=200, blank=True, null=True)
    version = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patent_category'


class PatentPatent(models.Model):
    old_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    wi_post3_code = models.CharField(max_length=2, blank=True, null=True)
    pr_doc_num = models.CharField(max_length=10, blank=True, null=True)
    pr_kind = models.CharField(max_length=2, blank=True, null=True)
    pr_date = models.DateTimeField(blank=True, null=True)
    ar_doc_num = models.CharField(max_length=15, blank=True, null=True)
    ar_date = models.DateTimeField(blank=True, null=True)
    loc = models.SmallIntegerField(blank=True, null=True)
    agency_code = models.CharField(max_length=10, blank=True, null=True)
    agency_name = models.CharField(max_length=30, blank=True, null=True)
    agent = models.CharField(max_length=15, blank=True, null=True)
    legal_status = models.CharField(max_length=2, blank=True, null=True)
    r_applicant_details = models.CharField(max_length=200, blank=True, null=True)
    pr_doc_num_full = models.CharField(max_length=14, blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    add_date = models.DateTimeField(blank=True, null=True)
    change_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patent_patent'


class PatentLocTip(models.Model):
    first_class = models.CharField(max_length=3)
    second_class = models.CharField(max_length=3)
    chinese_display = models.CharField(max_length=255)
    english_display = models.CharField(max_length=255)
    class_type = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patent_loc_tip'

class Map(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'map'








