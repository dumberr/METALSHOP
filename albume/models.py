from django.db import models

from django.contrib.postgres.fields import ArrayField

class Trupa(models.Model):
    id_trupa = models.AutoField(primary_key=True)

    nume_trupa = models.CharField(
        max_length=100,
        unique=True,
        error_messages={
            "unique": "Exista deja o trupa cu acest nume.",
            "blank": "Numele trupei este obligatoriu.",
            "max_length": "Numele trupei este prea lung."
        }
    )

    tara = models.CharField(
        max_length=60,
        null=True,
        blank=True
    )

    an_infiintare = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Anul infiintarii trupei, nu anul lansarii primului album."
    )

    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["nume_trupa"]
        verbose_name_plural = "Trupe"

        indexes = [
            models.Index(fields=["an_infiintare"], name="trupa_an_idx")
        ]

        constraints = [
            models.CheckConstraint(
                condition=models.Q(an_infiintare__gte=1900) |models.Q(an_infiintare__isnull=True),
                name="trupa_an_min_1900",
                violation_error_message="Anul infiintarii trebuie sa fie cel putin 1900."
            )
        ]

    def __str__(self):
        return self.nume_trupa



class CasaDiscuri(models.Model):
    id_casa = models.AutoField(primary_key=True)

    nume_label = models.CharField(
        max_length=100,
        unique=True,
        error_messages={
            "unique": "Exista deja o casa de discuri cu acest nume.",
            "blank": "Numele casei de discuri este obligatoriu.",
            "max_length": "Numele este prea lung."
        }
    )

    tara_sediu = models.CharField(
        max_length=60,
        null=True,
        blank=True,
        help_text="Tara in care se afla sediul principal."
    )

    website = models.URLField(
        null=True,
        blank=True,
        help_text="Adresa completa a site-ului, de exemplu https://example.com.",
        error_messages={
            "invalid": "Introduceti o adresa URL valida."
        }
    )

    class Meta:
        ordering = ["nume_label"]
        verbose_name_plural = "Case de discuri"

        indexes = [
            models.Index(fields=["tara_sediu"], name="casa_tara_idx")
        ]

    def __str__(self):
        return self.nume_label
    
    
    

class GenMuzical(models.Model):
    id_gen = models.AutoField(primary_key=True)

    nume_gen = models.CharField(
        max_length=80,
        unique=True,
        error_messages={
            "unique": "Exista deja un gen muzical cu acest nume.",
            "blank": "Numele genului muzical este obligatoriu.",
            "max_length": "Numele genului muzical este prea lung."
        }
    )

    descriere = models.TextField(
        null=True,
        blank=True,
        help_text="O scurta descriere a caracteristicilor genului muzical."
    )

    class Meta:
        verbose_name_plural = "Genuri muzicale"

    def __str__(self):
        return self.nume_gen
    

#albume


class Album(models.Model):
    id_album = models.AutoField(primary_key=True)

    nume_album = models.CharField(
        max_length=150,
        db_index=True,
        error_messages={
            "blank": "Numele albumului este obligatoriu.",
            "max_length": "Numele albumului este prea lung."
        }
    )

    an_lansare = models.PositiveIntegerField(
        help_text="Anul in care a fost lansat albumul."
    )

    pret = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        error_messages={
            "invalid": "Introduceti un pret valid.",
            "max_digits": "Pretul are prea multe cifre."
        }
    )

    stoc = models.PositiveIntegerField(default=0)

    data_adaug = models.DateTimeField(auto_now_add=True)

    taguri = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True
    )

    trupa = models.ForeignKey(
        Trupa,
        on_delete=models.PROTECT,
        related_name="albume"
    )

    casa_discuri = models.ForeignKey(
        CasaDiscuri,
        on_delete=models.PROTECT,
        related_name="albume"
    )

    genuri = models.ManyToManyField(
        GenMuzical,
        related_name="albume"
    )

    class Meta:
        ordering = ["nume_album"]
        verbose_name_plural = "Albume"

        indexes = [
            models.Index(fields=["pret"], name="album_pret_idx"),
            models.Index(fields=["an_lansare"], name="album_an_idx")
        ]

        constraints = [
            models.CheckConstraint(
                condition=models.Q(pret__gt=0),
                name="album_pret_pozitiv"
            ),
            models.CheckConstraint(
                condition=models.Q(an_lansare__gte=1900),
                name="album_an_min_1900"
            )
        ]

    def __str__(self):
        return self.nume_album
    

class Colectie(models.Model):
    class Sezon(models.TextChoices):
        PERMANENT = "permanent", "Permanent"
        PRIMAVARA = "primavara", "Primavara"
        VARA = "vara", "Vara"
        TOAMNA = "toamna", "Toamna"
        IARNA = "iarna", "Iarna"

    id_colectie = models.AutoField(primary_key=True)

    nume = models.CharField(
        max_length=100,
        unique=True,
        error_messages={
            "unique": "Exista deja o colectie cu acest nume.",
            "blank": "Numele colectiei este obligatoriu."
        }
    )

    descriere = models.TextField(null=True, blank=True)

    tematica = models.CharField(
        max_length=100,
        help_text="Tematica muzicala a colectiei, de exemplu albume clasice."
    )

    sezon = models.CharField(
        max_length=20,
        choices=Sezon.choices,
        default=Sezon.PERMANENT
    )

    procent_reducere = models.PositiveIntegerField(
        default=0,
        blank=True,
        help_text="Reducerea aplicata colectiei, intre 0 si 100."
    )

    culoare = models.CharField(
        max_length=7,
        default="#8B1E2D",
        help_text="Culoarea reprezentativa in format hexazecimal."
    )

    sigla = models.ImageField(
        upload_to="colectii/",
        null=True,
        blank=True
    )

    albume = models.ManyToManyField(
        Album,
        related_name="colectii"
    )

    class Meta:
        ordering = ["nume"]
        verbose_name_plural = "Colectii"

        constraints = [
            models.CheckConstraint(
                condition=models.Q(procent_reducere__gte=0) & models.Q(procent_reducere__lte=100),
                name="colectie_reducere_valida"
            )
        ]

    def __str__(self):
        return self.nume
    

class PiesaAlbum(models.Model):
    id_piesa = models.AutoField(primary_key=True)

    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name="piese"
    )

    nr_piesa = models.PositiveIntegerField(
        help_text="Pozitia piesei in album, incepand de la 1."
    )

    titlu_piesa = models.CharField(
        max_length=150,
        error_messages={
            "blank": "Titlul piesei este obligatoriu.",
            "max_length": "Titlul piesei este prea lung."
        }
    )

    durata_secunde = models.PositiveIntegerField(
        help_text="Durata piesei exprimata in secunde."
    )

    este_bonus = models.BooleanField(default=False)

    class Meta:
        ordering = ["album_id", "nr_piesa"]
        verbose_name_plural = "Piese album"

        constraints = [
            models.UniqueConstraint(
                fields=["album", "nr_piesa"],
                name="piesa_album_numar_unic"
            ),
            models.CheckConstraint(
                condition=models.Q(nr_piesa__gte=1),
                name="piesa_numar_pozitiv"
            ),
            models.CheckConstraint(
                condition=models.Q(durata_secunde__gt=0),
                name="piesa_durata_pozitiva"
            )
        ]

    def __str__(self):
        return f"{self.album} - {self.nr_piesa}. {self.titlu_piesa}"