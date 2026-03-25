from django.db import models

class animal(models.Model):
    animalname = models.CharField(max_length=100)
    animalid = models.AutoField(primary_key=True)
    animalspecies = models.CharField(max_length=100, blank=True)
    animallocation = models.CharField(max_length=100, blank=True)
    lastfed = models.DateTimeField(null=True, blank=True)
    lastwalk = models.DateTimeField(null=True, blank=True)
    animalage = models.IntegerField(null=True, blank=True)
    behaviortype = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = "animal"


    def __str__(self):
        return f"{self.animalname} {self.animalspecies} {self.animallocation} {self.lastfed} {self.lastwalk} {self.animalage} {self.behaviortype}"
    
class person(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    personkey = models.AutoField(primary_key=True)

    class Meta:
        db_table = "person"

    def __str__(self):
        return f"{self.firstname} {self.lastname}"