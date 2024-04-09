from django.db import models

class AnimalNames(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)

class ImageUploadModel(models.Model):
    image = models.ImageField(upload_to='images/')

class DetectedObject(models.Model):
    image = models.ForeignKey(ImageUploadModel, on_delete=models.CASCADE)
    object_name = models.CharField(max_length=100)