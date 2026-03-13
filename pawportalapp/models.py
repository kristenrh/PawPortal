from django.db import models

class animal(models.Model):
    animalname = models.CharField(max_length=100)
    animalid = models.AutoField(primary_key=True)

    class Meta:
        db_table = "animal"


    def __str__(self):
        return self.animalname