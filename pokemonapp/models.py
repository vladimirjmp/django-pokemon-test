from django.db import models

class Pokemon(models.Model):
  pokemon_id = models.IntegerField()
  name = models.CharField(max_length=20, unique=True)
  height = models.IntegerField()
  weight = models.IntegerField()

  def __str__(self):
    return self.name

class Evolution(models.Model):
  pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="evolution")
  evolves_to = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="evolves_to")

  def __str__(self):
    return str(self.pokemon) + ' > ' + str(self.evolves_to)

class Stat(models.Model):
  pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="stats")
  name = models.CharField(max_length=20)
  base_stat = models.IntegerField()

  def __str__(self):
    return str(self.pokemon) + ' - ' + self.name
