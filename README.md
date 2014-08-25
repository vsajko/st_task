st_task
=======
    
## Urls
    
### /summer/list/ 
    lista unsesenih feedova
    klikom na gumb na desnoj strani se mijenja status feeda

### /summer/add_channel/
    forma za dodavanje feeda

### /summer/rijec/
    JSON api
    parametri su 'rijec', 'feed_url' i 'unos_url'
    rijec je obavezan parametar

    jedinstven rezultat (jedna riječ i broj ponavljanja) se dobije za: 
    - 'rijec' - rezultat je jedna riječ i ukupan broj ponavljanja
    - ili za sve unešene parametre - rezultat je riječ i broj ponavljanja u navedenom feedu i unosu

    u svim drugim slučajevima riječ može pripadati većem broju feedova i/ili unosa
    - vraća se broj ponavljanja po feedu/unosu i ukupan broj ponavljanja

### /summer/toplist/
    top-lista riječi
    može se filtrirati po feedu uz pomoć select forme

## Manage Commands

### fetch 
        Dohvaća unešene akivne feedove i puni bazu sa riječima.
        Moguće je procesirati sve formate feedova koje Feedparser procesira. 
        Dohvat i procesiranje feedova iz initial_data traje cca 10min.
        Kasnije se dohvaćaju samo novo dodani unosi.

        Riječi se uzimaju iz title-a i contenta ili summary-a
        (ovisno o tome koji je duži content ili summary)
        Imena stvarnih polja se razlikuju. Koristim Feedparser termine.
        Fetch prima parametre od kojih ni jedan nije obavezan.
        - wordlen je minimalna dužina riječi (više od dva slova je default)
        - link url feeda koji želimo dodati, a koji nije unešen u bazu
        - forcefetch procesira feed bez obzira na etag i last-modified headere


### initial_data
        unosi neke feedove u bazu da bi se izbjeglo neefikasno punjenje preko forme
        (south ne radi sa sqlite-om odnosno sqlite ne podržava promjene foreign keyeva
         u kreiranim tablicama :( )
     

## Requirements
    nije sve nužno za rad aplikacije
    - feedparser za čitanje i procesiranje feedova
    - beautifoulsoup za extrahiranje texta
    

 
