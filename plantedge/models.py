'''
Object entity that stored in databases.
For Other Object, check plantedge/class
'''

from django.db import models
from django.forms import ModelForm
from django.contrib.postgres.fields import JSONField, ArrayField
from simple_history.models import HistoricalRecords

from plantedge.core.modelManager import AoiManager, ClientManager, AssetManager

class Client(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=15)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    objects = ClientManager()

    def __str__(self):
        return '{id} <{name}>'.format(**self.__dict__)

class Aoi(models.Model):
    '''
    Representation of 'Area of interest'.
    Each AOI belongs to one client.

    coordinates stored in following format: [[x1, y1], [x2, y2], [xn, yn]]
    '''
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client)
    client_aoi_id = models.CharField(max_length=50)
    status = models.CharField(max_length=15)
    name = models.CharField(max_length=50, blank=True)
    coordinates = ArrayField(
        ArrayField(models.FloatField(), size=2)
    )
    raw_coordinates = ArrayField(
        ArrayField(models.FloatField(), size=2)
    )
    description = JSONField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    objects = AoiManager()

    def __str__(self):
        return '{id} <{name}>'.format(**self.__dict__)

class Asset(models.Model):
    '''
    Represenation of raw or generated asset.
    Each asset belongs to one AOI.

    storage_url
        => Assets are stored in s3 bucket, hence download it from storage_url.

    note
        => Downloading and reading asset are expensive. Note used to store high level overall data and insight.
    '''
    id = models.AutoField(primary_key=True)
    aoi = models.ForeignKey(Aoi)
    type = models.CharField(max_length=20)
    date = models.DateTimeField()
    storage_url = models.CharField(max_length=200)
    planet_item_id = models.CharField(max_length=20)
    usability_score = models.FloatField(default=1.1)
    note = JSONField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    objects = AssetManager()

class Job(models.Model):
    '''
        Representation of job.
        Type of job might be :
            - downloading asset from planet
            - calculating indexes from raw asset
            - uploading asset to s3
            - etc

        params
            => A way to flexibly store parameters while job is queued
    '''
    id = models.AutoField(primary_key=True)
    aoi = models.ForeignKey(Aoi)
    type = models.CharField(max_length=15)
    status = models.CharField(max_length=15)
    params = JSONField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
