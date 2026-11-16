from django.contrib import admin

from .models import Trupa, CasaDiscuri, GenMuzical, Album, Colectie, PiesaAlbum

#2

from django.utils.html import format_html

#8
admin.site.site_header = "Administrare Metalshop"
admin.site.site_title = "Metalshop Admin"
admin.site.index_title = "Bine ai venit in panoul de administrare Metalshop"
admin.site.site_url = "/"

#10
import csv

from django.contrib import admin, messages
from django.http import HttpResponse


class TrupaAdmin(admin.ModelAdmin):
    list_display = ("nume_trupa", "tara", "an_infiintare", "activa")
    
    search_fields = ("nume_trupa", "tara")
    search_help_text = "Cautare dupa numele trupei sau dupa tara de origine."


class CasaDiscuriAdmin(admin.ModelAdmin):
    list_display = ("nume_label", "tara_sediu", "website")
    search_fields = ("nume_label", "tara_sediu")
    search_help_text = "Cautare dupa numele labelului sau dupa tara sediului."


class GenMuzicalAdmin(admin.ModelAdmin):
    list_display = ("nume_gen", "descriere")
    search_fields = ("nume_gen", "descriere")
    search_help_text = "Cautare dupa numele genului sau dupa descriere."


class AlbumAdmin(admin.ModelAdmin):
    #1 ordinea coloanelor; 
    list_display = (
        "nume_album",
        "trupa",
        "trupa__tara",
        "casa_discuri",
        "an_lansare",
        "pret_formatat",
        "stoc_formatat",
    )
    list_select_related = ("trupa", "casa_discuri")
    
    #2
    @admin.display(
        description="Pret",
        ordering="pret"
    )
    def pret_formatat(self, obj):
        return format_html(
            '<b style="color: #e0b04a;">{} lei</b>',
            obj.pret
        )

    #2
    @admin.display(
        description="Stoc",
        ordering="stoc"
    )
    def stoc_formatat(self, obj):
        if obj.stoc == 0:
            return format_html('<i style="color: #ff6b6b;">{}</i>', "epuizat")
        return format_html("<b>{}</b> buc.", obj.stoc)
    
    #3
    search_fields = ("nume_album", "trupa__nume_trupa")  
    search_help_text = "Cautare dupa numele albumului sau dupa numele trupei."
    
    #4 desc an
    list_per_page = 5  #6

    list_filter = ("genuri", "casa_discuri", "trupa")

    ordering = ("-an_lansare",)
    
    #10
    actions = ["export_csv_albume", "seteaza_stoc_zero"] 
    
    @admin.action(description="Exporta albumele selectate in format CSV")
    def export_csv_albume(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="albume.csv"'

        writer = csv.writer(response)
        writer.writerow(["Nume album", "Trupa", "Casa de discuri", "An lansare", "Pret", "Stoc"])

        for album in queryset:
            writer.writerow([
                album.nume_album,
                album.trupa,
                album.casa_discuri,
                album.an_lansare,
                album.pret,
                album.stoc
            ])
        return response

    #10
    @admin.action(description="Seteaza stocul la 0 pentru albumele selectate")
    def seteaza_stoc_zero(self, request, queryset):
        nr = queryset.update(stoc=0)
        messages.success(request, f"Stocul a fost setat la 0 pentru {nr} albume.")



class ColectieAdmin(admin.ModelAdmin):
    list_display = ("nume", "tematica", "sezon", "procent_reducere")
    search_fields = ("nume", "tematica")
    search_help_text = "Cautare dupa numele colectiei sau dupa tematica."
    
    #7
    fieldsets = (
        ("Date generale", {
            "fields": ("nume", "tematica", "sezon", "culoare", "albume")
        }),
        ("Date optionale", {
            "fields": ("descriere", "procent_reducere", "sigla"),
            "classes": ("collapse",),  #deschide/ascunde
        }),
    )
    


class PiesaAlbumAdmin(admin.ModelAdmin):
    list_display = ("titlu_piesa", "album", "nr_piesa", "durata_secunde", "este_bonus")
    search_fields = ("titlu_piesa", "album__nume_album")
    search_help_text = "Cautare dupa titlul piesei sau dupa numele albumului."  


admin.site.register(Trupa, TrupaAdmin)
admin.site.register(CasaDiscuri, CasaDiscuriAdmin)
admin.site.register(GenMuzical, GenMuzicalAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Colectie, ColectieAdmin)
admin.site.register(PiesaAlbum, PiesaAlbumAdmin)