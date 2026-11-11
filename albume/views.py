from django.http import HttpResponse, request

from datetime import datetime

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.shortcuts import render

from django.contrib import messages


# 4
class Accesare:
    id_urmator = 1

    def __init__(self, ip_client, url, parametri=None):
        self.id = Accesare.id_urmator
        Accesare.id_urmator += 1

        self.ip_client = ip_client
        self.url = url
        self.parametri = parametri if parametri is not None else {}
        self.data = datetime.now()
        
    def lista_parametri(self):
        lista = []

        for nume in self.parametri:
            
            valori = self.parametri.getlist(nume)
            
            for valoare in valori:
                
                if valoare == "":
                    valoare = None
                    
                    
                lista.append((nume, valoare))

        return lista
    
    #6
    def string_url(self):
        return self.url
        
    def pagina(self):
        return "/" + self.url.split("/", 3)[3].split("?")[0]
    

    #7
    def calculeaza_data(self, format="{zi_saptamana}, {zi} {luna} {an}", mod=""):
        zile = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]

        luni = ["Ianuarie", "Februarie", "Martie", "Aprilie", "Mai", "Iunie",
                "Iulie", "August", "Septembrie", "Octombrie", "Noiembrie", "Decembrie"]

        #10
        data_format = format.format(
            zi_saptamana=zile[self.data.weekday()],
            zi=self.data.day,
            luna=luni[self.data.month - 1],
            an=self.data.year
        )
        
        just_data = f"{self.data.day} {luni[self.data.month - 1]} {self.data.year}"
        ora = f"{self.data.hour:02d}:{self.data.minute:02d}:{self.data.second:02d}"
        
        if mod == "zi":
            out = just_data
        elif mod == "timp":
            out = ora
        else:
            out = f"{data_format}, {ora}"
            
        # html in template
        return out
    #9
    
    def __str__(self):
        return (
            f"id: {self.id}\n"
            f"ip_client: {self.ip_client}\n"
            f"string_url: {self.string_url()}\n"
            f"pagina: {self.pagina()}\n"
            f"calculeaza_data: {self.calculeaza_data(mod='text')}\n"
            f"lista_parametri: {self.lista_parametri()}"
        )
    

lista_accesari = []

def index(request):
    accesare = Accesare(
        #request.META.get("REMOTE_ADDR"),
        #8
        request.ip_client,
        request.build_absolute_uri(),
        request.GET
    )
    
    lista_accesari.append(accesare)
    
    print(accesare)

    

    #return HttpResponse("Metalshop este un magazin online specializat in comercializarea albumelor muzicale din genul metal si subgenurile acestuia.")

    # render template index.html care extinde baza.html 
    return render(request, "albume/index.html")

def info(request):
    
    accesare = Accesare(
        #request.META.get("REMOTE_ADDR"),
        request.ip_client,
        request.build_absolute_uri(),
        request.GET
    )
    
    lista_accesari.append(accesare)
    
    print(accesare)
    
    mod = request.GET.get("data", "")
    
    print(mod)
    
    out = accesare.calculeaza_data(mod=mod)
    

    
    #print(accesare.data.strftime("%A, %d %B %Y"))
    
    
    #now = datetime.now()
    
    #zile = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]

    #luni = ["Ianuarie", "Februarie", "Martie", "Aprilie", "Mai", "Iunie",   
    #    "Iulie", "August", "Septembrie", "Octombrie", "Noiembrie", "Decembrie"]
    
    #data_fix = f"{zile[now.weekday()]}, {now.day} {luni[now.month - 1]} {now.year}"

    #ora_fix = f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}"
    
    
    
    
    #data_fix = accesare.calculeaza_data()

    #ora_fix = f"{accesare.data.hour:02d}:{accesare.data.minute:02d}:{accesare.data.second:02d}"
    
    # Trimitem rezultatul către template.
    return render(request, "albume/info.html", {
        "out": out
    })

#lab2

def log(request):
    
    accesare = Accesare(
        request.ip_client,
        request.build_absolute_uri(),
        request.GET
    )

    lista_accesari.append(accesare)
    print(accesare)
    
    ultimele = request.GET.get("ultimele")

    accesari = lista_accesari
    eroare = ""

    if ultimele is not None:
        if not ultimele.isdigit():
            eroare = "Eroare: parametrul ultimele trebuie sa fie un numar intreg."
            accesari = []
        else:
            n = int(ultimele)

            if n == 0:
                accesari = []
            elif n > len(lista_accesari):
                
                eroare = f"Exista doar {len(lista_accesari)} accesari fata de {n} accesari cerute"
            else:
                accesari = lista_accesari[-n:]      
    
        #1.2
    afis_nr = request.GET.get("accesari") == "nr"
    
    nr_accesari = len(lista_accesari)
    
    iduri = request.GET.getlist("iduri")

    dubluri = request.GET.get("dubluri", "false") == "true"


    if iduri:
        accesari_selectate = []
        iduri_vazute = []


        for grup in iduri:
            for id_text in grup.split(","):

                if id_text.isdigit():
                    id_cautat = int(id_text)

                
                    if not dubluri and id_cautat in iduri_vazute:
                        continue

                
                    for a in accesari:
                        if a.id == id_cautat:
                            accesari_selectate.append(a)
                            iduri_vazute.append(id_cautat)
                            break

        accesari = accesari_selectate    
        
        #1.3
    afis_detalii = request.GET.get("accesari") == "detalii"

    nume_parametri = []

    for nume in request.GET:
        for valoare in request.GET.getlist(nume):
            nume_parametri.append(nume)

    nr_parametri = len(nume_parametri)
    
    
    #1.4
    tabel = request.GET.get("tabel")

    proprietati = ["id", "ip_client", "url", "parametri", "data"]

    coloane = []
    randuri = []
    afis_tabel = False

    if tabel is not None:
        if tabel == "tot":
            
            coloane = proprietati
        else:
            
            coloane = tabel.split(",")

        
        if all(col in proprietati for col in coloane):
            afis_tabel = True

            for accesare in accesari:
                
                date_accesare = {
                    "id": accesare.id,
                    "ip_client": accesare.ip_client,
                    "url": accesare.url,
                    "parametri": accesare.parametri,
                    "data": accesare.data
                }

                rand = []

                
                for col in coloane:
                    rand.append(date_accesare[col])

                randuri.append(rand)
        else:
            eroare = "Eroare: tabelul contine proprietati inexistente."                                           

    #nr de accesari
    numarari_pagini = {}

    for a in lista_accesari:
        pagina = a.pagina()

        if pagina in numarari_pagini:
            numarari_pagini[pagina] += 1
        else:
            numarari_pagini[pagina] = 1

    #listele min si max
    pagina_max = ""
    pagina_min = ""
    max_accesari = 0
    min_accesari = len(lista_accesari) + 1

    for pagina, nr in numarari_pagini.items():
        if nr > max_accesari:
            max_accesari = nr
            pagina_max = pagina

        if nr < min_accesari:
            min_accesari = nr
            pagina_min = pagina

    
    return render(request, "albume/log.html", 
{
    "accesari": accesari,
    "eroare": eroare,
    "afis_nr": afis_nr,
    "nr_accesari": nr_accesari,

    #3
    "afis_detalii": afis_detalii,
    "nume_parametri": nume_parametri,
    "nr_parametri": nr_parametri,
    
    #4
    "afis_tabel": afis_tabel,
    "coloane": coloane,
    "randuri": randuri,
    
    #5
    "pagina_max": pagina_max,
    "max_accesari": max_accesari,
    "pagina_min": pagina_min,
    "min_accesari": min_accesari
    })
    
def istoric(request):
    accesare = Accesare(
        request.ip_client,
        request.build_absolute_uri(),
        request.GET
    )


    lista_accesari.append(accesare)
    print(accesare)

    return render(request, "albume/istoric.html")


def despre(request):
    accesare = Accesare(
        request.ip_client,
        request.build_absolute_uri(),
        request.GET
    )

    lista_accesari.append(accesare)
    print(accesare)

    return render(request, "albume/despre.html")
    
def detalii_accesare(request, id):
    # Memorăm și vizita paginii de detalii.
    accesare_noua = Accesare(
        request.ip_client,
        request.build_absolute_uri(),
        request.GET
    )

    lista_accesari.append(accesare_noua)
    print(accesare_noua)

    # caut accesarea
    accesare_cautata = None

    for a in lista_accesari:
        if a.id == int(id):
            accesare_cautata = a
            break

    # send to template
    return render(request, "albume/accesare.html", {
        "accesare": accesare_cautata,
        "id": id
    })
    
def in_lucru(request):
    accesare = Accesare(
        request.ip_client,
        request.build_absolute_uri(),
        request.GET
    )

    lista_accesari.append(accesare)
    
    messages.error(request, "error.")

    return render(request, "albume/in_lucru.html")


