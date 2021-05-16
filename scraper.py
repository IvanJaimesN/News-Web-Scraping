import requests
import lxml.html as html
import os        # Para crear las carpetas
import datetime  # Para asignar nombres con fechas

HOME_URL = 'https://www.larepublica.co/'

#XPATH_LINKS_TO_ARTICLE = '//h2/a/@href'
XPATH_LINKS_TO_ARTICLE = '//text-fill/a/@href'
#XPATH_TITLE = '//div[@class="mb-auto"]/h2/span/text()'
XPATH_TITLE = '//div[@class="mb-auto"]/text-fill/span/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')  # html de la noticia
            parsed = html.fromstring(notice) # html con permisos para trabajar

            # lectura de la noticia
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                title = title.replace(':', '')
                title = title[0:80]
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body =  parsed.xpath(XPATH_BODY)

            # Manejador contextual, permite si se llega a cerrar ele archivo de forma inesperada, mantiene todo seguro sin corromperse
                with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                    f.write(title)
                    f.write('\n \n')
                    f.write(summary)
                    f.write('\n \n')
                    for p in body:
                        f.write(p)
                        f.write('\n')
            except IndexError:
                return

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:    ## Para manejar los errores del servidor como por ejemplo el 404
        response = requests.get(HOME_URL) # se obtiene todo el documento HTML junto con las cabeceras

        if response.status_code == 200:
            home = response.content.decode('utf-8') # .decode transforma todos los caracteres especiales de tal modo que se pueda leer
            parsed = html.fromstring(home) # toma el contenido HTML y lo transforma en un documento especial para hacer scraper
            links_to_notices = parsed.xpath(XPATH_LINKS_TO_ARTICLE)
            #print(links_to_notices)

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):   # si no existe el directorio con el nombre today
                os.mkdir(today) # creación de la carpeta

            for link in links_to_notices:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()