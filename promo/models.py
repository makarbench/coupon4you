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
    advertiser_name = models.CharField(max_length=50)
    advertiser_image = models.ImageField(upload_to='avertiserimages/', null=True, blank=True)
    advertiser_contact_manager_name = models.CharField(max_length=50)
    advertiser_contact_email = models.EmailField(max_length=254, null=True)
    advertiser_contact_phone = models.CharField(max_length=50, null=True)
    advertiser_country = models.CharField(max_length=50, null=True)



    def get_absolute_url(self):
        """
        Returns the url to access a particular owner instance.
        """
        return reverse('advertiser-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.advertiser_name)



class PromoCompany(models.Model):
    """
    Model representing a Project (not a specific server).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular advertiser")

    promo_company_name = models.CharField(max_length=100)
    advertiser = models.ForeignKey(Advertiser, on_delete=models.SET_NULL, null=True)
    # Foreign Key used because Project can only have one Owner, but Owner can have multiple project
    # Owner as a string rather than object because it hasn't been declared yet in the file.
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the PromotionsCompany")
    promo_company_valid_from = models.DateField(null=True, blank=True)
    promo_company_valid_to = models.DateField(null=True, blank=True)

    PromoCompany_STATUS = (
        ('on', 'Turn On'),
        ('off', 'Turn Off'),
    )

    status = models.CharField(max_length=3, choices=PromoCompany_STATUS, blank=True, default='on', help_text='PromoCompany Turn On')

    class Meta:
        ordering = ["status","promo_company_valid_from","promo_company_valid_to"]
        permissions = (
            ("can_mark_turn_status_PromoCompany", "Set Promo Company turn on/off status"),
            ("can_change_PromoCompany_name", "Change PromoCompany Name"),)

    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s %s' % (self.advertiser, self.promo_company_name,)

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
    promocode_url = models.CharField(max_length=500, null=True) # ссылка сайта рекламодателя
    promocode_cpa_url = models.CharField(max_length=500, null=True)  # партнерская ссылка
    promocode_decription = models.CharField(max_length=200, null=True)
    promocode_image = models.ImageField(upload_to='promocodeimages/', null=True, blank=True)
    advertiser = models.ForeignKey(Advertiser, on_delete=models.SET_NULL, null=True,blank=True)
    promo_company_name = models.ForeignKey(PromoCompany, on_delete=models.SET_NULL, null=True)
    promocode_valid_from = models.DateField(null=True, blank=True)
    promocode_valid_to = models.DateField(null=True, blank=True)


    Promocode_STATUS = (
        ('on', 'Turn On'),
        ('off', 'Turn Off'),
    )

    status = models.CharField(max_length=3, choices=Promocode_STATUS, blank=True, default='on', help_text='Promocode Turn On')

    class Meta:
        ordering = ["status","promocode_valid_from","promocode_valid_to"]
        permissions = (
            ("can_mark_turn_status_ promocode", "Set promocode turn on/off status"),
            ("can_change_promocode", "Change promocode"),)

    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s (%s) %s' % (self.advertiser,self.promocode_url, self.promocode_decription)

    def get_absolute_url(self):
        """
        Returns the url to access a particular server instance.
        """
        return reverse('promocode-detail', args=[str(self.id)])


class HotDealsAffiliateLink(models.Model):
    """
    Model representing a specific server (i.e. that can be part of project).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for promocode")
    affiliatelink_advertiser_url = models.CharField(max_length=500, null=True) #ссылка сайта рекламодателя
    affiliatelink_cpa_url = models.CharField(max_length=500, null=True) #то на что именно кликает пользователь
    affiliatelink_image = models.ImageField(upload_to='affiliatelinkimages/', null=True, blank=True)
    affiliatelink_decription = models.TextField(null=True)
    advertiser = models.ForeignKey(Advertiser, on_delete=models.SET_NULL, null=True,blank=True)
    affiliatelink_valid_from = models.DateField(null=True, blank=True)
    affiliatelink_valid_to = models.DateField(null=True, blank=True)


    affiliatelink_STATUS = (
        ('on', 'Turn On'),
        ('off', 'Turn Off'),
    )

    status = models.CharField(max_length=3, choices=affiliatelink_STATUS, blank=True, default='on', help_text='affiliatelink Turn On')

    class Meta:
        ordering = ["status","affiliatelink_valid_from","affiliatelink_valid_to"]
        permissions = (
            ("can_mark_turn_status_ affiliatelink", "Set affiliatelink turn on/off status"),
            ("can_change_affiliatelink", "Change affiliatelink"),)

    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s (%s) %s  %s' % (self.advertiser,self.affiliatelink_cpa_url, self.affiliatelink_advertiser_url , self.affiliatelink_decription)

    def get_absolute_url(self):
        """
        Returns the url to access a particular server instance.
        """
        return reverse('affiliatelink-detail', args=[str(self.id)])

