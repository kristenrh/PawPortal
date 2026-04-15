from django.db import models

class Animal(models.Model):
    animalname = models.CharField(max_length=100)
    animalid = models.AutoField(primary_key=True)
    #animalspecies = models.CharField(max_length=100, blank=True)
    animallocation = models.CharField(max_length=100, blank=True)
    lastwalk = models.DateTimeField(null=True, blank=True)
    animalage = models.IntegerField(null=True, blank=True)
    isadpted = models.BooleanField(default=False)


    class Meta:
        db_table = "animal"


    def __str__(self):
        return self.animalname
    
class person(models.Model):
    #firstname = models.CharField(max_length=100)
    #lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, blank=True)

    class Meta:
        db_table = "person"

    def __str__(self):
        return f"{self.firstname} {self.lastname}"