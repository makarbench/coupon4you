from django.db import models
import uuid
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

# Create your models here.
class Advertiser(models.Model):
    """
    Model representing an author.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular advertiser")
    Advertiser_Name = models.CharField(max_length=50)
    Advertiser_Contact_Manager_Name = models.CharField(max_length=50)
    Advertiser_Contact_Email = models.CharField(max_length=50, null=True)
    Advertiser_Contact_Phone = models.CharField(max_length=50, null=True)
    Advertiser_Country = models.CharField(max_length=50, null=True)



    def get_absolute_url(self):
        """
        Returns the url to access a particular owner instance.
        """
        return reverse('advertiser-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.Advertiser_Name)



class PromoCompany(models.Model):
    """
    Model representing a Project (not a specific server).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular advertiser")

    PromoCompanyName = models.CharField(max_length=100)
    Advertiser = models.ForeignKey(Advertiser, on_delete=models.SET_NULL, null=True)
    # Foreign Key used because Project can only have one Owner, but Owner can have multiple project
    # Owner as a string rather than object because it hasn't been declared yet in the file.
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the PromotionsCompany")
    PromoCompany_valid_from = models.DateField(null=True, blank=True)
    PromoCompany_valid_to = models.DateField(null=True, blank=True)

    PromoCompany_STATUS = (
        ('on', 'Turn On'),
        ('off', 'Turn Off'),
    )

    status = models.CharField(max_length=3, choices=PromoCompany_STATUS, blank=True, default='on', help_text='PromoCompany Turn On')

    class Meta:
        ordering = ["status","PromoCompany_valid_from","PromoCompany_valid_to"]
        permissions = (
            ("can_mark_turn_status_PromoCompany", "Set Promo Company turn on/off status"),
            ("can_change_PromoCompany_name", "Change PromoCompany Name"),)

    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s %s' % (self.Advertiser, self.PromoCompanyName,)

    def get_absolute_url(self):
        """
        Returns the url to access a particular server instance.
        """
        return reverse('promocompany-detail', args=[str(self.id)])


class Promocode(models.Model):
    """
    Model representing a specific server (i.e. that can be part of project).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for promocode")
    promocode_entity = models.CharField(max_length=20, null=True)
    promocode_url = models.CharField(max_length=500, null=True)
    promocode_decription = models.CharField(max_length=200, null=True)
    Advertiser = models.ForeignKey(Advertiser, on_delete=models.SET_NULL, null=True)
    PromoCompany = models.ForeignKey(PromoCompany, on_delete=models.SET_NULL, null=True)
    Promocode_valid_from = models.DateField(null=True, blank=True)
    Promocode_valid_to = models.DateField(null=True, blank=True)


    Promocode_STATUS = (
        ('on', 'Turn On'),
        ('off', 'Turn Off'),
    )

    status = models.CharField(max_length=3, choices=Promocode_STATUS, blank=True, default='on', help_text='Promocode Turn On')

    class Meta:
        ordering = ["status","Promocode_valid_from","Promocode_valid_to"]
        permissions = (
            ("can_mark_turn_status_ promocode", "Set promocode turn on/off status"),
            ("can_change_promocode", "Change promocode"),)

    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s (%s) %s' % (self.Advertiser,self.promocode_url, self.promocode_decription)

    def get_absolute_url(self):
        """
        Returns the url to access a particular server instance.
        """
        return reverse('promocode-detail', args=[str(self.id)])




