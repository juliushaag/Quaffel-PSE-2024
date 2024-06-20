from django.db import models

# Create your models here.

class AdminAccount(models.Model):
    
  identifier = models.CharField(max_length=50, primary_key=True)

  def __str__(self):
    return self.identifier
