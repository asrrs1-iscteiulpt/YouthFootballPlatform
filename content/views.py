from django.http import HttpResponse
from django.shortcuts import render
from TwitterSearch import *
import time
import requests
import os
from TwitterAPI import TwitterAPI
import itertools
from GoogleNews import GoogleNews               # Noticias google
from newspaper import Article                   # Noticias google
import pandas as pd 
from bs4 import BeautifulSoup
import pymongo                                              # PARA INSERIR DOCUMENTOS NO MONGO
from pymongo import MongoClient                             # PARA INSERIR DOCUMENTOS NO MONGO
import json                                                 # PARA TRANSFORMAR A STRING DO TWITTER EM JSON/BSON
from datetime import datetime
from time import time
import re
import string
from django import forms
from urllib import parse
import matplotlib
import matplotlib.pyplot as plt                             # PARA FAZER GRÁFICOS
from matplotlib.pyplot import figure                        # PARA FAZER GRÁFICOS
import mpld3                                                # PARA FAZER GRÁFICOS
import base64                                               # PARA FAZER GRÁFICOS - MOSTRA A IMAGEM NO BROWSER (HTML)
from pylab import rcParams
import urllib.request                                       # PARA GRAVAR IMAGEM DO JOGADOR PROCURADO NO ZEROZERO
from requests.models import PreparedRequest                 # ADICIONA QUERY PARAMETERS AO URL

from importlib import import_module
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
import urllib3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import random
import csv

matplotlib.use('Agg')

s = requests.Session()

driver = webdriver.Chrome("/Applications/chromedriver")
driver.get("https://www.zerozero.pt/")
WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]'))).click()

EPOCA_PT= {
    '16_17': '96',
    'oca=16_17': '96',
    '17_18': '97',
    'oca=17_18': '97',
    '18_19': '98',
    'oca=18_19': '98',
#    '19_20': '99'
}

ASSOCIACAO_EPOCA_PT= {
    'af_algarve': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=224&seasonId=', '&af=af_algarve': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=224&seasonId=',
    'af_angra': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=216&seasonId=', '&af=af_angra': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=216&seasonId=',
    'af_aveiro': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=217&seasonId=', '&af=af_aveiro': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=217&seasonId=', 
    'af_beja': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=218&seasonId=', '&af=af_beja': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=218&seasonId=', 
    'af_braga': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=219&seasonId=', '&af=af_braga': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=219&seasonId=', 
    'af_braganca': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=220&seasonId=', '&af=af_braganca': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=220&seasonId=', 
    'af_castelo_branco': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=221&seasonId=', '&af=af_castelo_branco': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=221&seasonId=', 
    'af_coimbra': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=222&seasonId=', '&af=af_coimbra': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=222&seasonId=', 
    'af_evora': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=223&seasonId=', '&af=af_evora': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=223&seasonId=', 
    'af_guarda': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=226&seasonId=', '&af=af_guarda': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=226&seasonId=', 
    'af_horta': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=227&seasonId=', '&af=af_horta': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=227&seasonId=', 
    'af_leiria': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=228&seasonId=', '&af=af_leiria': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=228&seasonId=', 
    'af_lisboa': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=229&seasonId=', '&af=af_lisboa': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=229&seasonId=', 
    'af_madeira': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=225&seasonId=', '&af=af_madeira': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=225&seasonId=', 
    'af_ponta_delgada': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=230&seasonId=', '&af=af_ponta_delgada': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=230&seasonId=', 
    'af_portalegre': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=231&seasonId=', '&af=af_portalegre': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=231&seasonId=', 
    'af_porto': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=232&seasonId=', '&af=af_porto': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=232&seasonId=', 
    'af_santarem': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=233&seasonId=', '&af=af_santarem': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=233&seasonId=', 
    'af_setubal': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=234&seasonId=', '&af=af_setubal': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=234&seasonId=', 
    'af_viana_castelo': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=235&seasonId=', '&af=af_viana_castelo': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=235&seasonId=', 
    'af_vila_real': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=236&seasonId=', '&af=af_vila_real': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=236&seasonId=', 
    'af_viseu': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=237&seasonId=', '&af=af_viseu': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=237&seasonId=', 
}

ASSOCIACAO_PT= {
    'af_algarve': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=224&seasonId=98', '?af=af_algarve': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=224&seasonId=98',
    'af_angra': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=216&seasonId=98', '?af=af_angra': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=216&seasonId=98',
    'af_aveiro': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=217&seasonId=98', '?af=af_aveiro': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=217&seasonId=98', 
    'af_beja': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=218&seasonId=98', '?af=af_beja': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=218&seasonId=98',
    'af_braga': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=219&seasonId=98', '?af=af_braga': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=219&seasonId=98',
    'af_braganca': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=220&seasonId=98', '?af=af_braganca': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=220&seasonId=98',
    'af_castelo_branco': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=221&seasonId=98', '?af=af_castelo_branco': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=221&seasonId=98', 
    'af_coimbra': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=222&seasonId=98', '?af=af_coimbra': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=222&seasonId=98',
    'af_evora': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=223&seasonId=98', '?af=af_evora': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=223&seasonId=98',
    'af_guarda': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=226&seasonId=98', '?af=af_guarda': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=226&seasonId=98', 
    'af_horta': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=227&seasonId=98', '?af=af_horta': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=227&seasonId=98',
    'af_leiria': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=228&seasonId=98', '?af=af_leiria': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=228&seasonId=98',
    'af_lisboa': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=229&seasonId=98', '?af=af_lisboa': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=229&seasonId=98',
    'af_madeira': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=225&seasonId=98', '?af=af_madeira': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=225&seasonId=98',
    'af_ponta_delgada': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=230&seasonId=98', '?af=af_ponta_delgada': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=230&seasonId=98', 
    'af_portalegre': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=231&seasonId=98', '?af=af_portalegre': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=231&seasonId=98', 
    'af_porto': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=232&seasonId=98', '?af=af_porto': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=232&seasonId=98', 
    'af_santarem': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=233&seasonId=98', '?af=af_santarem': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=233&seasonId=98', 
    'af_setubal': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=234&seasonId=98', '?af=af_setubal': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=234&seasonId=98', 
    'af_viana_castelo': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=235&seasonId=98', '?af=af_viana_castelo': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=235&seasonId=98', 
    'af_vila_real': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=236&seasonId=98', '?af=af_vila_real': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=236&seasonId=98', 
    'af_viseu': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=237&seasonId=98', '?af=af_viseu': 'https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=237&seasonId=98', 
}

ASSOCIACAO_EXTENSO= {
    'comp_fpf': 'Competições FPF',
    'af_algarve': 'AF Algarve',
    'af_angra': 'AF Angra', 
    'af_aveiro': 'AF Aveiro', 
    'af_beja': 'AF Beja', 
    'af_braga': 'AF Braga', 
    'af_braganca': 'AF Bragança', 
    'af_castelo_branco': 'AF Castelo Branco', 
    'af_coimbra': 'AF Coimbra', 
    'af_evora': 'AF Évora', 
    'af_guarda': 'AF Guarda', 
    'af_horta': 'AF Horta', 
    'af_leiria': 'AF Leiria', 
    'af_lisboa': 'AF Lisboa', 
    'af_madeira': 'AF Madeira', 
    'af_ponta_delgada': 'AF Ponta Delgada', 
    'af_portalegre': 'AF Portalegre', 
    'af_porto': 'AF Porto', 
    'af_santarem': 'AF Santarém', 
    'af_setubal': 'AF Setúbal', 
    'af_viana_castelo': 'AF Viana do Castelo', 
    'af_vila_real': 'AF Vila Real', 
    'af_viseu': 'AF Viseu', 
}

ESPECIALISTAS_TWITTER= {
    'AndreRouiller': '@AndreRouiller'

}

def homepage(request):
    print('Página: Home')
    print('Requisito funcional: Obter highlights')
    start_time = time()
    
    data = 'O mundo das camadas jovens de futebol em Portugal'

    req = requests.get('https://www.ojogo.pt/futebol/formacao.html')

    if req.status_code == 200:
        print('Requisição bem sucedida!')
        content = req.content

    soup = BeautifulSoup(content, 'html.parser')
    news_soup = soup.find_all('article', {'class':['t-g1-l1-m1', 't-g1-l1-m2']})

    noticia1 = str(news_soup[0])
    noticia2 = str(news_soup[1])
    noticia3 = str(news_soup[2])

    noticia1 = re.search('<h2>(.*)</a></h2>', noticia1).group(1)
    noticia1 = re.search('">(.*)', noticia1).group(1)   
    noticia2 = re.search('<h2>(.*)</a></h2>', noticia2).group(1)
    noticia2 = re.search('">(.*)', noticia2).group(1)   
    noticia3 = re.search('<h2>(.*)</a></h2>', noticia3).group(1)    
    noticia3 = re.search('">(.*)', noticia3).group(1)   
    
    end_time = time()
    print('Tempo para carregar a página: %s segundos' %(round(end_time-start_time, 3)))
    return render(request, 'home.html', {'data':data, 'noticia1':noticia1, 'noticia2':noticia2, 'noticia3':noticia3})       

def statoptions(request):
    print('Página: Estatísticas')
    print('Requisito funcional: Consultar estatísticas')
    start_time = time()
    header = '<b><a style="color: #006699">Estatísticas</a></b><hr>'
    data = '<table style="width: 100%; text-align: center;"><tr><td><form action="/statistics"><input style="background-color: #006699;width: 100%;font-size:14px;" type="submit" value="Estatísticas externas" /></form></td><td><form action="/yfpstats"><input style="background-color: #012b41; width: 100%;font-size:14px;" type="submit" value="Estatísticas internas" /></form></td></tr></table>'
    end_time = time()
    print('Tempo para carregar a página: %s segundos' %(round(end_time-start_time, 3)))    
    return render(request, 'home.html', {'header':header, 'data':data})    

def yfpstats(request):
    print('Página: Estatísticas internas')
    print('Requisito funcional: Consultar estatísticas internas')
    start_time = time()
    header = '<b><a style="color: #006699">Estatísticas internas</a></b><hr>'
    search = '<form><input type="text" name="search" placeholder="Pesquisa.." required><br><input type="submit" value="Pesquisar"></form><br>'
    search_query = request.GET.get('search')
    data = ''

    legenda_jogos = ['V', 'E', 'D']
    resultado_jogos = [0,0,0]

    header_left = ''
    data_left = ''
    data_games = ''
    titulo_jogos = ''
    titulo_info = ''
    jogos = 0
    golos = 0
    vitorias = 0
    empates = 0
    derrotas = 0
    min_jogo = 0
    golos_p_jogo = 0
    minutos = 0
    outra_info = ''
    graphic_games = ''
    erro = False

    if search_query != None: #pesquisa na bd
        try:
            client = MongoClient('mongodb://localhost:27017/')                      # PARA INSERIR DOCUMENTOS NO MONGO
            db = client['db']                                                       # PARA INSERIR DOCUMENTOS NO MONGO
            collection = db['players'] 
            count = 0
            try:
                for x in client['db']['players'].find({ 'nome': re.compile(search_query, re.IGNORECASE) }):
                    count += 1
                    data_left = '<b>Nome: </b> %s<br><b>Nome completo: </b>%s<br><b>Nacionalidade: </b>%s<br><b>Nascimento: </b>%s<br><b>Clube: </b>%s<br><b>Posição: </b>%s<br>' %(str(x['nome']), str(x['nome_completo']), str(x['nacionalidade']), str(x['nascimento']), str(x['clube']), str(x['posicao']))
                    resultado_jogos = [int(x['vitorias']), int(x['empates']), int(x['derrotas'])]
                    break
                if count == 0:
                    header_left = ''
                    data = f'<b><a style="color: #006699">{count}</a> resultado(s) correspondente(s) ao jogador <a style="color: #006699">{search_query}</a>.</b><br><br>'
                else:
                    data = ''
                    header_left = '<div style="background-color:#006699;font-size:12px;height: 35px;padding-left: 10px;color: white;padding-top: 20px;"><b>%s</b></div>' %(str(x['nome']))
                    titulo_jogos = '<div style="background-color:#ececec;height: 35px;padding-left: 10px;padding-top: 20px;"><b>Jogos disputados</b></div>'

                    rcParams['figure.figsize'] = 3, 3
                    fig,ax = plt.subplots()
                    plt.bar(legenda_jogos,resultado_jogos)
                    ax.legend(['Jogos'])
                    fig.savefig('plot.png')
                    data_uri1 = base64.b64encode(open('plot.png', 'rb').read()).decode('utf-8')
                    graphic_games = '<img src="data:image/png;base64,{0}">'.format(data_uri1)

                    data_games = '<div style="background-color: gray;padding: 10px;color: white;font-size: 15px;"><b>Vitórias:</b> %s<br><hr><b>Empates:</b> %s<br><hr><b>Derrotas:</b> %s</div><br>' %(str(x['vitorias']), str(x['empates']), str(x['derrotas']))

                    titulo_info = '<div style="background-color:#ececec;height: 35px;padding-left: 10px;padding-top: 20px;"><b>Estatísticas da época</b></div>'

                    outra_info = '<style>table {text-align: center;width:100%;} th{border-bottom: 1px solid #ddd;}</style>'
                    outra_info = outra_info + '<div><table><thead><tr><th>Jogos</th><th>Golos</th><th>Minutos p/ jogo</th><th>Golos p/ jogo</th><th>Total minutos jogados</th></tr></thead><tbody><tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr></tbody></table></div>' %(str(x['jogos']), str(x['golos']), str(x['minutos_por_jogo']), str(x['golos_por_jogo']), str(x['total_minutos']))
            except:
                print('Erro na conexão à base de dados ou jogador não encontrado.')
            data = f'<b><a style="color: #006699">{count}</a> resultado(s) correspondente(s) ao jogador <a style="color: #006699">{search_query}</a>.</b><br><br>'
        except:
            data = f'<b><a style="color: #006699">{count}</a> resultado(s) correspondente(s) ao jogador <a style="color: #006699">{search_query}</a>.</b><br><br>'
            header_left = ''
            print('Erro')

    end_time = time()
    print('Tempo para carregar a página: %s segundos' %(round(end_time-start_time, 3)))    
    return render(request, 'home.html', {'header':header, 'search':search, 'data':data, 'header_left':header_left, 'data_left':data_left, 'graphic_games': graphic_games, 'data_games':data_games,'titulo_jogos':titulo_jogos,'titulo_info':titulo_info, 'outra_info':outra_info})  

def statistics(request):
    print('Página: Estatísticas externas')
    print('Requisito funcional: Consultar estatísticas externas')
    start_time = time()

    header = '<b><a style="color: #006699">Estatísticas externas</a></b><hr><br>'

    search = '<form><input type="text" name="search" placeholder="Pesquisa.." required><br><input type="submit" value="Pesquisar"></form><br>'
    search_query = request.GET.get('search')

    legenda_jogos = ['V', 'E', 'D']
    resultado_jogos = [0,0,0]

    data = ''
    header_left = ''
    data_left = ''
    data_games = ''
    titulo_jogos = ''
    titulo_info = ''
    jogos = 0
    golos = 0
    vitorias = 0
    empates = 0
    derrotas = 0
    min_jogo = 0
    golos_p_jogo = 0
    minutos = 0
    outra_info = ''
    graphic_games = ''
    erro = False

    if search_query is not None: 
        start_time_dados_iniciais = time()
        driver.get(f"https://www.zerozero.pt/search_player.php?op=all&search_string={search_query}&fem=0&ida=1&mod=1&ord=i&peq=1&sta=0&op=all")
        try: 
            table = driver.find_element_by_class_name("zztable")
            table_code = table.get_attribute('innerHTML')
            try:
                imagem_url = "http://zerozero.pt%s" %(re.search('src="(.*?)"', table_code).group(1))
                urllib.request.urlretrieve(imagem_url, "jogador.jpg")
                data_uri = base64.b64encode(open('jogador.jpg', 'rb').read()).decode('utf-8')
                info_imagem_str = '<img src="data:image/png;base64,{0}">'.format(data_uri)
            except:
                info_imagem_str = ''

            info_nome = re.search('style="text-decoration:none;">(.*)</a>', table_code).group(1)
            info_nome_completo = re.search('<span class="small_faded">(.*)</span>', table_code).group(1)
            info_nacionalidade = re.search('<div class="text">(.*?)</div>', table_code).group(1)
            try:
                info_nascimento = re.search('Nascimento</td><td style="text-align:left;">(.*)</td></tr><tr><td class="label">Clube', table_code).group(1)
            except:
                info_nascimento = ''
            try:
                info_clube = re.search('Clube</td><td style="text-align:left;">(.*)</td></tr><tr><td', table_code).group(1)
                info_clube = re.search('<div class="text">(.*)</div></div>', info_clube).group(1)
            except:
                info_clube = ''

            info_posicao = re.search('Posição</td><td style="text-align:left;">(.*)</td>', table_code).group(1)
            player_information = '%s<br><b>Nome:</b> %s<br><b>Nome completo:</b> %s<br><b>Nacionalidade:</b> %s<br><b>Nascimento:</b> %s<br><b>Clube:</b> %s<br><b>Posição:</b> %s<br>' %(info_imagem_str, info_nome, info_nome_completo, info_nacionalidade, info_nascimento, info_clube, info_posicao)
            data = 'Encontrou o jogador.'
        except:
            player_information = '<i>Nenhum jogador corresponde à pesquisa "%s".</i>' %(search_query)
            data = '<i>Nenhum jogador corresponde à pesquisa "%s".</i><br>' %(search_query)
            erro = True

        end_time_dados_iniciais = time()
        print('Tempo para carregar os dados iniciais do jogador: %s segundos' %(round(end_time_dados_iniciais-start_time_dados_iniciais, 3))) 
        if erro == False:
            try:
                player_number = re.search('<div><a href="/player.php(.*)&amp;epoca_id=0&amp;search=1" style="text-decoration:none;">', table_code).group(1)
            except:
                player_number = 0

            # Outros dados
            try:
                data = ''
                

                start_time_estatisticas = time()
                driver.get(f"https://www.zerozero.pt/player_results.php{player_number}")
                # Imprimir tempo
                wait = WebDriverWait(driver, 10)
                jogos = ''
                golos = ''
                resultado_jogos = []
                # -------------------- Época 18/19 --------------------
                try:   
                    driver.execute_script("window.scrollBy(0, 500)", "")
                    element_epoca = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="epoca_id_chosen"]')))
                    # Start Imprimir tempo
                    element_epoca[1].click()
                    # Imprimir tempo
                    try:
                        element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="epoca_id_chosen"]/div/ul/li[3]')))
                        # Start Imprimir tempo
                        element.click()
                        # Imprimir tempo
                        try:
                            jogos = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="team_filters"]/div[1]/div[1]/div[1]/div[1]'))).get_attribute('innerHTML')
                        except:
                            jogos = 0
                        if int(jogos) > 0:
                            try:
                                golos = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="team_filters"]/div[1]/div[1]/div[2]/div[1]'))).get_attribute('innerHTML')  
                            except:
                                golos = 0
                            try:
                                vitorias = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="facts"]/div/div[1]/div[1]/div[2]/span[1]'))).get_attribute('innerHTML')  
                                vitorias = [int(s) for s in vitorias.split() if s.isdigit()]
                                vitorias = vitorias[0]
                                resultado_jogos.append(vitorias)
                            except:
                                vitorias = '-'
                                resultado_jogos.append(0)
                            try:
                                empates = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="facts"]/div/div[1]/div[1]/div[2]/span[2]'))).get_attribute('innerHTML')  
                                empates = [int(s) for s in empates.split() if s.isdigit()]
                                empates = empates[0]
                                resultado_jogos.append(empates)
                            except:
                                empates = '-'
                                resultado_jogos.append(0)
                            try:
                                derrotas = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="facts"]/div/div[1]/div[1]/div[2]/span[3]'))).get_attribute('innerHTML')  
                                derrotas = [int(s) for s in derrotas.split() if s.isdigit()]
                                derrotas = derrotas[0]
                                resultado_jogos.append(derrotas)
                            except:
                                derrotas = '-'
                                resultado_jogos.append(0)
                            try:
                                minutos = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="facts"]/div/div[1]/div[3]/div/div'))).get_attribute('innerHTML')
                            except:
                                minutos = '-'
                        else:
                            raise Exception
                    except:
                        jogos = 0
                        golos = 0
                        resultado_jogos = [0,0,0]
                except:
                    jogos = 0
                    golos = 0   
                    resultado_jogos = [0,0,0]           
                    print('Erro na procura dos elementos')
            except:
                player_information = '<i>Nenhum jogador corresponde à pesquisa "%s".</i>' %(search_query)
                search_query = ''
                header_left = ''
                search = '<form><input type="text" name="search" placeholder="Pesquisa.."><br><input style="border: 1px solid #999999;background-color: #cccccc;color: #666666;" type="submit" value="Submit" disabled></form><br>'                
                print('Erro na driver')
                print('Erro provável: excesso de acessos ao zerozero.')
            
            end_time_estatisticas = time()
            print('Tempo para carregar dados estatísticos do jogador: %s segundos' %(round(end_time_estatisticas-start_time_estatisticas, 3))) 

            start_time_graph = time()

            try:
                golos_p_jogo = '{:.1f}'.format(int(golos)/int(jogos))
            except:
                golos_p_jogo = 0
            try:
                minutos = [int(s) for s in minutos.split() if s.isdigit()]
                minutos = minutos[0]
            except:
                minutos = 0
            try:
                min_jogo = round(minutos/int(jogos)) 
            except:
                min_jogo = 0

            
            rcParams['figure.figsize'] = 3, 3
            fig,ax = plt.subplots()
            plt.bar(legenda_jogos,resultado_jogos)
            ax.legend(['Jogos'])
            fig.savefig('plot.png')

            header = '<b><a style="color: #006699">Estatísticas</a></b><hr><br>'

            data_uri1 = base64.b64encode(open('plot.png', 'rb').read()).decode('utf-8')
            end_time_graph = time()
            print('Tempo para a criação do gráfico: %s segundos' %(round(end_time_graph-start_time_graph, 3))) 

            if search_query is not None:
                header_left = '<div style="background-color:#006699;font-size:12px;height: 35px;padding-left: 10px;color: white;padding-top: 20px;"><b>%s</b></div>' %(search_query.title())
                data_left = player_information

                graphic_games = '<img src="data:image/png;base64,{0}">'.format(data_uri1)
                data_games = '<div style="background-color: gray;padding: 10px;color: white;font-size: 15px;"><b>Vitórias:</b> %s<br><hr><b>Empates:</b> %s<br><hr><b>Derrotas:</b> %s</div><br>' %(vitorias, empates, derrotas)
                outra_info = '<style>table {border-collapse: collapse;text-align: center;width:100%;font-size:14px}th, td {padding: 8px;border-bottom: 1px solid #ddd;} tr:hover{background-color:#f5f5f5;}</style>'
                outra_info = outra_info + '<div><table><thead><tr><th>Jogos</th><th>Golos</th><th>Minutos p/ jogo</th><th>Golos p/ jogo</th><th>Total minutos jogados</th></tr></thead><tbody><tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr></tbody></table></div>' %(jogos, golos, min_jogo, golos_p_jogo, minutos)

            else:
                header_left = ''
                data_left = ''
                graphic_games = ''
                outra_info = ''
                data_games =''

            titulo_jogos = '<div style="background-color:#ececec;height: 35px;padding-left: 10px;padding-top: 20px;"><b>Jogos disputados</b></div>'
            titulo_info = '<div style="background-color:#ececec;height: 35px;padding-left: 10px;padding-top: 20px;"><b>Estatísticas da época</b></div>'

    end_time = time()
    print('Tempo para carregar a página: %s segundos' %(round(end_time-start_time, 3)))

    return render(request, 'home.html', {'header':header, 'search':search, 'data':data, 'header_left':header_left, 'data_left':data_left, 'graphic_games': graphic_games, 'data_games':data_games,'titulo_jogos':titulo_jogos,'titulo_info':titulo_info, 'outra_info':outra_info})


def classoptions(request):
    print('Página: Classificação')
    print('Requisito funcional: Consultar classificação')
    start_time = time()
    header = '<b><a style="color: #006699">Classificação</a></b><hr>'
    data = '<table style="width: 100%; text-align: center;"><tr><td><form action="/classification"><input style="background-color: #006699;width: 100%;font-size:14px;" type="submit" value="Época atual" /></form></td><td><form action="/archive"><input style="background-color: #012b41; width: 100%;font-size:14px;" type="submit" value="Épocas anteriores" /></form></td></tr></table>'
    end_time = time()
    print('Tempo para carregar a página: %s segundos' %(round(end_time-start_time, 3)))    
    return render(request, 'home.html', {'header':header, 'data':data})      

def classification(request):
    print('Página: Classificação época atual')
    print('Requisito funcional: Consultar classificação época atual')
    start_time = time()

    str_1 = request.GET.get('af')
    str_2 = request.GET.get('campeonato')
    str_3 = request.GET.get('competicao')
    str_4 = request.GET.get('div')
    str_af = str(str_1)
    str_campeonato = str(str_2)
    str_competicao = str(str_3)  
    str_div = str(str_4)

    search = """ 
    <form>
    <select id="af" name="af">
    <option value="comp_fpf">Competições FPF</option>
    <option value="af_algarve">AF Algarve</option><option value="af_angra">AF Angra</option>
    <option value="af_aveiro">AF Aveiro</option><option value="af_beja">AF Beja</option>
    <option value="af_braga">AF Braga</option><option value="af_braganca">AF Bragança</option>
    <option value="af_castelo_branco">AF Castelo Branco</option><option value="af_coimbra">AF Coimbra</option>   
    <option value="af_evora">AF Évora</option><option value="af_guarda">AF Guarda</option>   
    <option value="af_horta">AF Horta</option><option value="af_leiria">AF Leiria</option>       
    <option value="af_lisboa">AF Lisboa</option><option value="af_madeira">AF Madeira</option> 
    <option value="af_ponta_delgada">AF Ponta Delgada</option><option value="af_portalegre">AF Portalegre</option>   
    <option value="af_porto">AF Porto</option><option value="af_santarem">AF Santarém</option>       
    <option value="af_setubal">AF Setúbal</option><option value="af_viana_castelo">AF Viana do Castelo</option>     
    <option value="af_vila_real">AF Vila Real</option><option value="af_viseu">AF Viseu</option>           
    </select>
    <select id="campeonato" name="campeonato">
    <option value="juniores">Juniores (Juniores A)</option>
    <option value="juvenis">Juvenis (Juniores B)</option>
    <option value="iniciados">Iniciados (Juniores C)</option>
    <option value="infantis">Infantis (Juniores D)</option>
    <option value="benjamins">Benjamins (Juniores E)</option>
    <option value="traquinas">Traquinas (Juniores F)</option>
    <option value="petizes">Petizes (Juniores G)</option>
    </select> 
    <br>
    <input type="submit" value="Seguinte">
    </form>
    <br>
    """

    if str_1 == 'comp_fpf':
        if str_2 == 'juniores':
            header = '<b><a style="color: #006699">Classificação:</a></b> %s > %s<hr><br>' %(ASSOCIACAO_EXTENSO[str_af], str_campeonato)
            search = """
                <form>
                <select id="div" name="div">
                <option value="divisao1">1ª divisão</option>
                <option value="divisao2">2ª divisão</option>
                </select> 
                <br>
                <input type="submit" value="Seguinte">
                <input type="button" value="Voltar" onclick="history.back()">
                </form>
            """
            subsearch = ''
            data = ''
            return render(request, 'home.html', {'header':header, 'search':search, 'subsearch':subsearch, 'data':data})
        elif str_2 == 'juvenis':
            header = '<b><a style="color: #006699">Classificação:</a></b> %s > %s<hr><br>' %(ASSOCIACAO_EXTENSO[str_af], str_campeonato)
            search = 'TABELA DISTO AQUI https://resultados.fpf.pt/Competition/Details?competitionId=17017&seasonId=98'
            subsearch = ''
            data = ''
        elif str_2 == 'iniciados':
            header = '<b><a style="color: #006699">Classificação:</a></b> %s > %s<hr><br>' %(ASSOCIACAO_EXTENSO[str_af], str_campeonato)
            search = 'TABELA DISTO AQUI https://resultados.fpf.pt/Competition/Details?competitionId=17022&seasonId=98'
            subsearch = ''
            data = ''
        else:
            header = '<b><a style="color: #006699">Classificação:</a></b> %s > %s<hr><br>' %(ASSOCIACAO_EXTENSO[str_af], str_campeonato)
            search = ''
            subsearch = 'Não existem dados ou não existe campeonato de <b>%s</b> nas competições da FPF.<br><br><input type="button" value="Voltar" onclick="history.back()">'%(str_campeonato)
            data = ''
            return render(request, 'home.html', {'header':header, 'search':search, 'subsearch':subsearch, 'data':data})
        
    if str_4 is not None:           # Competições FPF
        if str_4 == 'divisao1':
            header = '<b><a style="color: #006699">Classificação:</a></b> Competições FPF > Júniores A > 1ª Divisão<hr><br>'
            search = 'TABELA DA 1A DIVISAO AQUI https://resultados.fpf.pt/Competition/Details?competitionId=14820&seasonId=98'
            subsearch = ''
            data = ''
        if str_4 == 'divisao2': 
            header = '<b><a style="color: #006699">Classificação:</a></b> Competições FPF > Júniores A > 2ª Divisão<hr><br>'
            search = 'TABELA DA 2A DIVISAO AQUI https://resultados.fpf.pt/Competition/Details?competitionId=17016&seasonId=98'
            subsearch = ''
            data = ''

    if str_1 is not None:
        header = '<b><a style="color: #006699">Classificação:</a></b> %s > %s<hr><br>' %(ASSOCIACAO_EXTENSO[str_af], str_campeonato)
        search = ''
        data = ''
    else:
        header = '<b><a style="color: #006699">Classificação</a></b><hr><br>'
        data = '' 

    search_query = str_af+'-'+str_campeonato

    last_url = str(request.META.get('HTTP_REFERER'))
  
    req = requests.get('https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=224&seasonId=99')
	
    if str_af != 'None' and str_af != 'comp_fpf':
        req = requests.get(ASSOCIACAO_PT[str_1])  
    elif str_3 is not None:
        req = requests.get(ASSOCIACAO_PT[last_url.split("&", 1)[0][40:]])

    if req.status_code == 200:
        print('Requisição bem sucedida!')
        content = req.content

    soup = BeautifulSoup(content, 'html.parser')
    div_table = soup.find_all(name='div', attrs={'class':'list-links'})

    count = 0

    str_form = """ <form>
    <select id="competicao" name="competicao"> """

    str_form_fim = """
    </select> 
    <br>
    <input type="submit" value="Seguinte"><input type="button" value="Voltar" onclick="history.back()"></form>
    """

    for x in div_table:
        if count == 0 or 'SENIOR' in str(x):
            pass
        elif 'FUTSAL' in str(x) or 'FEMININO' in str(x) or 'Futsal' in str(x) or 'Feminino' in str(x) or 'FEM' in str(x):
            pass
        elif count == 1:
            if str_campeonato == 'juniores':
                for y in str(x).splitlines()[1:-1]:
                    if 'Taça' in y or 'TACA' in y or 'taca' in y or 'TAÇA' in y or 'taça' in y or 'Cup' in y:
                        pass
                    else:
                        str_form+=str('<option>%s</option>') %(y)
        elif count == 2:
            if str_campeonato == 'juvenis':
                for y in str(x).splitlines()[1:-1]:
                    if 'Taça' in y or 'TACA' in y or 'taca' in y or 'TAÇA' in y or 'taça' in y or 'Cup' in y:
                        pass
                    else:
                        str_form+=str('<option>%s</option>') %(y)
        elif count == 3:
            if str_campeonato == 'iniciados':
                for y in str(x).splitlines()[1:-1]:
                    if 'Taça' in y or 'TACA' in y or 'taca' in y or 'TAÇA' in y or 'taça' in y or 'Cup' in y:
                        pass
                    else:
                        str_form+=str('<option>%s</option>') %(y)  
        elif count == 4:
            if str_campeonato == 'infantis':
                for y in str(x).splitlines()[1:-1]:
                    if 'Taça' in y or 'TACA' in y or 'taca' in y or 'TAÇA' in y or 'taça' in y or 'Cup' in y:
                        pass
                    else:
                        str_form+=str('<option>%s</option>') %(y) 
        elif count == 5:
            if str_campeonato == 'benjamins':
                for y in str(x).splitlines()[1:-1]:
                    if 'Taça' in y or 'TACA' in y or 'taca' in y or 'TAÇA' in y or 'taça' in y or 'Cup' in y:
                        pass
                    else:
                        str_form+=str('<option>%s</option>') %(y) 
        elif count == 6:
            if str_campeonato == 'traquinas':
                for y in str(x).splitlines()[1:-1]:
                    if 'Taça' in y or 'TACA' in y or 'taca' in y or 'TAÇA' in y or 'taça' in y or 'Cup' in y:
                        pass
                    else:
                        str_form+=str('<option>%s</option>') %(y)
                # data = x   
        elif count == 7:
            if str_campeonato == 'petizes':
                for y in str(x).splitlines()[1:-1]:
                    if 'Taça' in y or 'TACA' in y or 'taca' in y or 'TAÇA' in y or 'taça' in y or 'Cup' in y:
                        pass
                    else:
                        str_form+=str('<option>%s</option>') %(y)
        count=count+1

    subsearch = str_form + str_form_fim

    if '<option' not in subsearch:
        subsearch = 'Não existem dados ou não existe campeonato de <b>%s</b> na %s.<br><br><input type="button" value="Voltar" onclick="history.back()">'%(str_campeonato, str_af)

    if (str_3 is not None) or (str_4 is not None) or (str_1 == 'comp_fpf' and str_2 == 'juvenis') or (str_1 == 'comp_fpf' and str_2 == 'iniciados'):
        header = '<b><a style="color: #006699">Classificação:</a></b> %s<hr><br>' %(str_competicao)
        search = ''
        subsearch = ''
        str_url = ''
        if str_3 is not None:
            for x in div_table:
                for y in str(x).splitlines()[1:-1]:
                    if str_3 in y and 'Futsal' not in y and 'FUTSAL' not in y:
                        str_url = y.split('" ', 1)[0][9:]
                        # Adicionei esta linha \/ porque não fazia scraping certo na AF Madeira por exemplo
                        str_url = str_url.replace('amp;', '')
            url_comp = 'https://resultados.fpf.pt%s' %(str_url) 

        if str_4 == 'divisao1':
            header = '<b><a style="color: #006699">Classificação:</a></b> Competições FPF > Júniores > 1ª Divisão<hr><br>'
            url_comp = 'https://resultados.fpf.pt/Competition/Details?competitionId=17007&seasonId=98'
        if str_4 == 'divisao2':
            header = '<b><a style="color: #006699">Classificação:</a></b> Competições FPF > Júniores > 2ª Divisão<hr><br>'
            url_comp = 'https://resultados.fpf.pt/Competition/Details?competitionId=17016&seasonId=98'
        if str_1 == 'comp_fpf' and str_2 == 'juvenis':
            header = '<b><a style="color: #006699">Classificação:</a></b> Competições FPF > Juvenis<hr><br>'
            url_comp = 'https://resultados.fpf.pt/Competition/Details?competitionId=17017&seasonId=98'
        if str_1 == 'comp_fpf' and str_2 == 'iniciados':
            header = '<b><a style="color: #006699">Classificação:</a></b> Competições FPF > Iniciados<hr><br>'
            url_comp = 'https://resultados.fpf.pt/Competition/Details?competitionId=17022&seasonId=98'
        
        req = requests.get(url_comp)
        if req.status_code == 200:
            print('Requisição bem sucedida!')
            content = req.content

        soup = BeautifulSoup(content, 'html.parser')

        classification_table = soup.find_all(name='div', attrs={'class':'game classification no-gutters'})
        equipas = []
        for linha in classification_table:
            str_equipas = linha.contents[3]
            equipas.append(str_equipas)
    
        jogos = []
        for linha in classification_table:
            str_jogos = linha.contents[5]
            jogos.append(str_jogos)

        posicoes = []
        for linha in classification_table:
            str_posicoes = linha.contents[1]
            str_posicoes = str(str_posicoes).replace('<div class="col-md-1 col-sm-1 col-xs-1 text-left no-padding"><span>', '')
            str_posicoes = str(str_posicoes).replace('</span></div>', '')
            posicoes.append(str_posicoes) 

        vitorias = []
        for linha in classification_table:
            str_vitorias = linha.contents[7]
            vitorias.append(str_vitorias)        
    
        empates = []
        for linha in classification_table:
            str_empates = linha.contents[9]
            empates.append(str_empates)  

        derrotas = []
        for linha in classification_table:
            str_derrotas = linha.contents[11]
            derrotas.append(str_derrotas)  

        golos_marcados = []
        for linha in classification_table:
            str_golos_marcados = linha.contents[13]
            golos_marcados.append(str_golos_marcados)  

        golos_sofridos = []
        for linha in classification_table:
            str_golos_sofridos = linha.contents[15]
            golos_sofridos.append(str_golos_sofridos)  

        pontuacao = []
        for linha in classification_table:
            str_pontuacao = linha.contents[17]
            pontuacao.append(str_pontuacao)                  

        try:
            a = {'Equipas': equipas}
            classif_table_final = pd.DataFrame(data=a)
            classif_table_final['Equipas'] = classif_table_final['Equipas'].str.join(', ')  
            classif_table_final.insert(0, 'POS', posicoes)
            classif_table_final.insert(2, 'JGS', jogos)   
            classif_table_final['JGS'] = classif_table_final['JGS'].str.join(', ')     
            classif_table_final.insert(3, 'V', vitorias)
            classif_table_final['V'] = classif_table_final['V'].str.join(', ') 
            classif_table_final.insert(4, 'E', empates)
            classif_table_final['E'] = classif_table_final['E'].str.join(', ') 
            classif_table_final.insert(5, 'D', derrotas)   
            classif_table_final['D'] = classif_table_final['D'].str.join(', ')  
            classif_table_final.insert(6, 'GM', golos_marcados)  
            classif_table_final['GM'] = classif_table_final['GM'].str.join(', ')   
            classif_table_final.insert(7, 'GS', golos_sofridos) 
            classif_table_final['GS'] = classif_table_final['GS'].str.join(', ') 
            classif_table_final.insert(8, 'PTS', pontuacao)  
            classif_table_final['PTS'] = classif_table_final['PTS'].str.join(', ')
        except:
            data = 'Não existem dados para esta competição ou a competição que selecionou é uma Taça.'   
        

        if str_4 is not None:
            data = '<style>table {border-collapse: collapse;width:100%;font-size:11px}th, td {padding: 8px;text-align: left;border-bottom: 1px solid #ddd;} tr:hover{background-color:#f5f5f5;}</style><table><tr><td style="border-style: none;" colspan="9"><a style="color: #006699"><b>Outra fase</b></a></td><tr style="background-color: #006699;color:white;height:30px;"><td><b>POS</b></td><td><b>Equipas</b></td><td><b>JGS</b></td><td><b>V</b></td><td><b>E</b></td><td><b>D</b></td><td><b>GM</b></td><td><b>GS</b></td><td><b>PTS</b></td></tr>' #+ '<br>'
        else:
            data = '<style>table {border-collapse: collapse;width:100%;font-size:11px}th, td {padding: 8px;text-align: left;border-bottom: 1px solid #ddd;} tr:hover{background-color:#f5f5f5;}</style><table><tr><td style="border-style: none;" colspan="9"><a style="color: #006699"><b>&#9917; FASE FINAL</b></a></td><tr style="background-color: #006699;color:white;height:30px;"><td><b>POS</b></td><td><b>Equipas</b></td><td><b>JGS</b></td><td><b>V</b></td><td><b>E</b></td><td><b>D</b></td><td><b>GM</b></td><td><b>GS</b></td><td><b>PTS</b></td></tr>' #+ '<br>'
  
        for linha in classif_table_final.index:
            if classif_table_final['POS'][linha] == '1' and linha != 0:
                data = data + '<tr><td style="border-style: none; height: 50px;" colspan="9"></td></tr><tr><td style="border-style: none;" colspan="9"><a style="color: #006699"><b>Outra fase</b></a></td></tr><tr style="background-color: #006699;color:white;height:30px;"><td><b>POS</b></td><td><b>Equipas</b></td><td><b>JGS</b></td><td><b>V</b></td><td><b>E</b></td><td><b>D</b></td><td><b>GM</b></td><td><b>GS</b></td><td><b>PTS</b></td></tr><tr><td>' + classif_table_final['POS'][linha] + '</td><td>' + classif_table_final['Equipas'][linha] + '</td><td>' + classif_table_final['JGS'][linha] + '</td><td>' + classif_table_final['V'][linha] + '</td><td>' + classif_table_final['E'][linha] + '</td><td>' + classif_table_final['D'][linha] + '</td><td>' + classif_table_final['GM'][linha] + '</td><td>' + classif_table_final['GS'][linha] + '</td><td>' + classif_table_final['PTS'][linha] + '</td></tr>'
            else:
                data = data + '<tr><td>' + classif_table_final['POS'][linha] + '</td><td>' + classif_table_final['Equipas'][linha] + '</td><td>' + classif_table_final['JGS'][linha] + '</td><td>' + classif_table_final['V'][linha] + '</td><td>' + classif_table_final['E'][linha] + '</td><td>' + classif_table_final['D'][linha] + '</td><td>' + classif_table_final['GM'][linha] + '</td><td>' + classif_table_final['GS'][linha] + '</td><td>' + classif_table_final['PTS'][linha] + '</td></tr>'
         
        try:
            classif_table_final.set_index('POS', inplace=True)
            classif_table_final = classif_table_final.rename_axis(None)
        except:
            data = 'Não existem dados para esta competição ou a competição que selecionou é uma Taça.'

        data = data + '</table>' + '<br><input type="button" value="Voltar" onclick="history.back()">' 

        if str_4 is not None: 
            data = data.replace("Outra fase", '<a style="color: #006699">&#9917; FASE FINAL</a>', 3)
            data = data.replace('<a style="color: #006699">&#9917; FASE FINAL</a>', "Outra fase", 2)

    if str_1 is None:
        subsearch = ''
    
    if div_table == []:
        search = ''
        subsearch = ''
        data = 'Não existem dados ou não existe campeonato de <b>%s</b> na %s.<br><br><input type="button" value="Voltar" onclick="history.back()">'%(str_campeonato, str_af)
    
    end_time = time()
    print('Tempo para carregar a página: %s segundos' %(round(end_time-start_time, 3)))
    return render(request, 'home.html', {'header':header, 'search':search, 'subsearch':subsearch, 'data':data})






def matches(request):
    print('Página: Jornadas')
    print('Requisito funcional: Consultar jornadas')
    start_time = time()
    str_1 = request.GET.get('af')
    str_2 = request.GET.get('campeonato')
    str_3 = request.GET.get('competicao')
    str_4 = request.GET.get('div')
    str_5 = request.GET.get('jornada')
    str_af = str(str_1)
    str_campeonato = str(str_2)
    str_competicao = str(str_3)  
    str_div = str(str_4)

    search = """ 
    <form>
    <select id="af" name="af">
    <option value="comp_fpf">Competições FPF</option>
    <option value="af_algarve">AF Algarve</option><option value="af_angra">AF Angra</option>
    <option value="af_aveiro">AF Aveiro</option><option value="af_beja">AF Beja</option>
    <option value="af_braga">AF Braga</option><option value="af_braganca">AF Bragança</option>
    <option value="af_castelo_branco">AF Castelo Branco</option><option value="af_coimbra">AF Coimbra</option>   
    <option value="af_evora">AF Évora</option><option value="af_guarda">AF Guarda</option>   
    <option value="af_horta">AF Horta</option><option value="af_leiria">AF Leiria</option>       
    <option value="af_lisboa">AF Lisboa</option><option value="af_madeira">AF Madeira</option> 
    <option value="af_ponta_delgada">AF Ponta Delgada</option><option value="af_portalegre">AF Portalegre</option>   
    <option value="af_porto">AF Porto</option><option value="af_santarem">AF Santarém</option>       
    <option value="af_setubal">AF Setúbal</option><option value="af_viana_castelo">AF Viana do Castelo</option>     
    <option value="af_vila_real">AF Vila Real</option><option value="af_viseu">AF Viseu</option>           
    </select>
    <select id="campeonato" name="campeonato">
    <option value="juniores">Juniores (Juniores A)</option>
    <option value="juvenis">Juvenis (Juniores B)</option>
    <option value="iniciados">Iniciados (Juniores C)</option>
    <option value="infantis">Infantis (Juniores D)</option>
    <option value="benjamins">Benjamins (Juniores E)</option>
    <option value="traquinas">Traquinas (Juniores F)</option>
    <option value="petizes">Petizes (Juniores G)</option>
    </select> 
    <br>
    <input type="submit" value="Seguinte">
    </form>
    <br>
    """

    if str_1 == 'comp_fpf':
        if str_2 == 'juniores':
            header = '<b><a style="color: #006699">Jornadas:</a></b> %s > %s<hr><br>' %(ASSOCIACAO_EXTENSO[str_af], str_campeonato)
            search = """
                <form>
                <select id="div" name="div">
                <option value="divisao1">1ª divisão</option>
                <option value="divisao2">2ª divisão</option>
                </select>
                <select id="jornada" name="jornada">
                <option value="1">Jornada 1</option><option value="2">Jornada 2</option><option value="3">Jornada 3</option>
                <option value="4">Jornada 4</option><option value="5">Jornada 5</option><option value="6">Jornada 6</option>
                <option value="7">Jornada 7</option><option value="8">Jornada 8</option><option value="9">Jornada 9</option>
                <option value="10">Jornada 10</option><option value="11">Jornada 11</option><option value="12">Jornada 12</option>
                <option value="13">Jornada 13</option><option value="14">Jornada 14</option><option value="15">Jornada 15</option>
                <option value="16">Jornada 16</option><option value="17">Jornada 17</option><option value="18">Jornada 18</option>
                <option value="19">Jornada 19</option><option value="20">Jornada 20</option><option value="21">Jornada 21</option>
                <option value="22">Jornada 22</option><option value="23">Jornada 23</option><option value="24">Jornada 24</option>
                <option value="25">Jornada 25</option><option value="26">Jornada 26</option><option value="27">Jornada 27</option>
                <option value="28">Jornada 28</option><option value="29">Jornada 29</option><option value="30">Jornada 30</option>
                </select> 
                <br>
                <input type="submit" value="Seguinte">
                <input type="button" value="Voltar" onclick="history.back()">
                </form>
            """
            subsearch = ''
            data = ''
            return render(request, 'home.html', {'header':header, 'search':search, 'subsearch':subsearch, 'data':data})
        elif str_2 == 'juvenis':
            header = '<b><a style="color: #006699">Jornadas:</a></b> %s > %s<hr><br>' %(ASSOCIACAO_EXTENSO[str_af], str_campeonato)
            search = """
                <form>
                <select id="div" name="div">
                <option value="juvenis">Juvenis</option>
                </select>
                <select id="jornada" name="jornada">
                <option value="1">Jornada 1</option><option value="2">Jornada 2</option><option value="3">Jornada 3</option>
                <option value="4">Jornada 4</option><option value="5">Jornada 5</option><option value="6">Jornada 6</option>
                <option value="7">Jornada 7</option><option value="8">Jornada 8</option><option value="9">Jornada 9</option>
                <option value="10">Jornada 10</option><option value="11">Jornada 11</option><option value="12">Jornada 12</option>
                <option value="13">Jornada 13</option><option value="14">Jornada 14</option><option value="15">Jornada 15</option>
                <option value="16">Jornada 16</option><option value="17">Jornada 17</option><option value="18">Jornada 18</option>
                <option value="19">Jornada 19</option><option value="20">Jornada 20</option><option value="21">Jornada 21</option>
                <option value="22">Jornada 22</option><option value="23">Jornada 23</option><option value="24">Jornada 24</option>
                <option value="25">Jornada 25</option><option value="26">Jornada 26</option><option value="27">Jornada 27</option>
                <option value="28">Jornada 28</option><option value="29">Jornada 29</option><option value="30">Jornada 30</option>
                </select> 
                <br>
                <input type="submit" value="Seguinte">
                <input type="button" value="Voltar" onclick="history.back()">
                </form>
            """
            subsearch = ''
            data = ''
            return render(request, 'home.html', {'header':header, 'search':search, 'subsearch':subsearch, 'data':data})
        elif str_2 == 'iniciados':
            header = '<b><a style="color: #006699">Jornadas:</a></b> %s > %s<hr><br>' %(ASSOCIACAO_EXTENSO[str_af], str_campeonato)
            search = """
                <form>
                <select id="div" name="div">
                <option value="iniciados">Iniciados</option>
                </select>
                <select id="jornada" name="jornada">
                <option value="1">Jornada 1</option><option value="2">Jornada 2</option><option value="3">Jornada 3</option>
                <option value="4">Jornada 4</option><option value="5">Jornada 5</option><option value="6">Jornada 6</option>
                <option value="7">Jornada 7</option><option value="8">Jornada 8</option><option value="9">Jornada 9</option>
                <option value="10">Jornada 10</option><option value="11">Jornada 11</option><option value="12">Jornada 12</option>
                <option value="13">Jornada 13</option><option value="14">Jornada 14</option><option value="15">Jornada 15</option>
                <option value="16">Jornada 16</option><option value="17">Jornada 17</option><option value="18">Jornada 18</option>
                <option value="19">Jornada 19</option><option value="20">Jornada 20</option><option value="21">Jornada 21</option>
                <option value="22">Jornada 22</option><option value="23">Jornada 23</option><option value="24">Jornada 24</option>
                <option value="25">Jornada 25</option><option value="26">Jornada 26</option><option value="27">Jornada 27</option>
                <option value="28">Jornada 28</option><option value="29">Jornada 29</option><option value="30">Jornada 30</option>
                </select> 
                <br>
                <input type="submit" value="Seguinte">
                <input type="button" value="Voltar" onclick="history.back()">
                </form>
            """
            subsearch = ''
            data = ''
            return render(request, 'home.html', {'header':header, 'search':search, 'subsearch':subsearch, 'data':data})
        else:
            header = '<b><a style="color: #006699">Jornadas:</a></b> %s > %s<hr><br>' %(ASSOCIACAO_EXTENSO[str_af], str_campeonato)
            search = ''
            subsearch = 'Não existem dados ou não existe campeonato de <b>%s</b> nas competições da FPF.<br><br><input type="button" value="Voltar" onclick="history.back()">'%(str_campeonato)
            data = ''
            return render(request, 'home.html', {'header':header, 'search':search, 'subsearch':subsearch, 'data':data})
        
   
    if str_4 is not None:           
        if str_4 == 'divisao1':
            header = '<b><a style="color: #006699">Jornadas:</a></b> Competições FPF > Júniores A > 1ª Divisão<hr><br>'
            search = 'TABELA DA 1A DIVISAO AQUI https://resultados.fpf.pt/Competition/Details?competitionId=14820&seasonId=98'
            subsearch = ''
            data = ''
        if str_4 == 'divisao2': 
            header = '<b><a style="color: #006699">Jornadas:</a></b> Competições FPF > Júniores A > 2ª Divisão<hr><br>'
            search = 'TABELA DA 2A DIVISAO AQUI https://resultados.fpf.pt/Competition/Details?competitionId=17016&seasonId=98'
            subsearch = ''
            data = ''
    
    if str_1 is not None:
        header = '<b><a style="color: #006699">Jornadas:</a></b> %s > %s<hr><br>' %(ASSOCIACAO_EXTENSO[str_af], str_campeonato)
        search = ''
        data = ''
    else:
        header = '<b><a style="color: #006699">Jornadas</a></b><hr><br>'
        data = '' 

    
    search_query = str_af+'-'+str_campeonato


    last_url = str(request.META.get('HTTP_REFERER'))
    req = requests.get('https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=224&seasonId=99')

    if str_af != 'None' and str_af != 'comp_fpf':
        teste_url = ASSOCIACAO_PT[str_1]
        req = requests.get(teste_url)          
    elif str_3 is not None:
        teste_url = ASSOCIACAO_PT[last_url.split("&", 1)[0][33:]]
        req = requests.get(teste_url)        

    if req.status_code == 200:
        print('Requisição bem sucedida!')
        content = req.content

    soup = BeautifulSoup(content, 'html.parser')
    div_table = soup.find_all(name='div', attrs={'class':'list-links'})
    count = 0

    str_form = """ <form>
    <select id="competicao" name="competicao"> """

    str_form_fim = """
    </select> 
    <select id="jornada" name="jornada">
    <option value="1">Jornada 1</option><option value="2">Jornada 2</option><option value="3">Jornada 3</option>
    <option value="4">Jornada 4</option><option value="5">Jornada 5</option><option value="6">Jornada 6</option>
    <option value="7">Jornada 7</option><option value="8">Jornada 8</option><option value="9">Jornada 9</option>
    <option value="10">Jornada 10</option><option value="11">Jornada 11</option><option value="12">Jornada 12</option>
    <option value="13">Jornada 13</option><option value="14">Jornada 14</option><option value="15">Jornada 15</option>
    <option value="16">Jornada 16</option><option value="17">Jornada 17</option><option value="18">Jornada 18</option>
    <option value="19">Jornada 19</option><option value="20">Jornada 20</option><option value="21">Jornada 21</option>
    <option value="22">Jornada 22</option><option value="23">Jornada 23</option><option value="24">Jornada 24</option>
    <option value="25">Jornada 25</option><option value="26">Jornada 26</option><option value="27">Jornada 27</option>
    <option value="28">Jornada 28</option><option value="29">Jornada 29</option><option value="30">Jornada 30</option>
    </select>
    <br>
    <input type="submit" value="Seguinte"><input type="button" value="Voltar" onclick="history.back()"></form>
    """

    for x in div_table:
        if count == 0 or 'SENIOR' in str(x):
            pass
        elif 'FUTSAL' in str(x) or 'FEMININO' in str(x) or 'Futsal' in str(x) or 'Feminino' in str(x) or 'FEM' in str(x):
            pass
        elif count == 1:
            if str_campeonato == 'juniores':
                for y in str(x).splitlines()[1:-1]:
                    if 'Taça' in y or 'Taca' in y or 'taca' in y or 'taça' in y or 'Cup' in y:
                        pass
                    else:
                        str_form+=str('<option>%s</option>') %(y)
        elif count == 2:
            if str_campeonato == 'juvenis':
                for y in str(x).splitlines()[1:-1]:
                    str_form+=str('<option>%s</option>') %(y)
        elif count == 3:
            if str_campeonato == 'iniciados':
                for y in str(x).splitlines()[1:-1]:
                    str_form+=str('<option>%s</option>') %(y)
        elif count == 4:
            if str_campeonato == 'infantis':
                for y in str(x).splitlines()[1:-1]:
                    str_form+=str('<option>%s</option>') %(y)
        elif count == 5:
            if str_campeonato == 'benjamins':
                for y in str(x).splitlines()[1:-1]:
                    str_form+=str('<option>%s</option>') %(y)
        elif count == 6:
            if str_campeonato == 'traquinas':
                for y in str(x).splitlines()[1:-1]:
                    str_form+=str('<option>%s</option>') %(y)
        elif count == 7:
            if str_campeonato == 'petizes':
                for y in str(x).splitlines()[1:-1]:
                    str_form+=str('<option>%s</option>') %(y)
        count=count+1

    subsearch = ''
    if str_1 is not None:
        subsearch = str_form + str_form_fim

    if (str_3 is not None) or (str_4 is not None):
        header = '<b><a style="color: #006699">Jornada %s:</a></b>  %s<hr><br>' %((str(str_5)), str_competicao)
        search = ''
        subsearch = ''
        str_url = ''
        if str_3 is not None:
            for x in div_table:
                for y in str(x).splitlines()[1:-1]:
                    if str_3 in y and 'Futsal' not in y and 'FUTSAL' not in y:
                        str_url = y.split('" ', 1)[0][9:]

                        str_url = str_url.replace('amp;', '')

            url_comp = 'https://resultados.fpf.pt%s' %(str_url) 

        if str_4 == 'divisao1':
            header = '<b><a style="color: #006699">Jornada %s:</a></b> Competições FPF > Júniores > 1ª Divisão<hr><br>' %(str(str_5))
            url_comp = 'https://resultados.fpf.pt/Competition/Details?competitionId=17007&seasonId=98'
        if str_4 == 'divisao2':
            header = '<b><a style="color: #006699">Jornada %s:</a></b> Competições FPF > Júniores > 2ª Divisão<hr><br>' %(str(str_5))
            url_comp = 'https://resultados.fpf.pt/Competition/Details?competitionId=17016&seasonId=98'
        if str_4 == 'juvenis':
            header = '<b><a style="color: #006699">Jornada %s:</a></b> Competições FPF > Juvenis<hr><br>' %(str(str_5))
            url_comp = 'https://resultados.fpf.pt/Competition/Details?competitionId=17017&seasonId=98'
        if str_4 == 'iniciados':
            header = '<b><a style="color: #006699">Jornada %s:</a></b> Competições FPF > Iniciados<hr><br>' %(str(str_5))
            url_comp = 'https://resultados.fpf.pt/Competition/Details?competitionId=17022&seasonId=98'
        
        req = requests.get(url_comp)
        if req.status_code == 200:
            print('Requisição bem sucedida!')
            content = req.content

        soup = BeautifulSoup(content, 'html.parser')

        jornadas = soup.find_all(name='div', attrs={'class':'row game-nav-days no-gutters'})
        jornadas_num = soup.find_all(name='a', attrs={'class':['text-center past', 'text-center current']})

        data = ''
        if (str_3 is not None) or (str_4 is not None) or (str_2 == 'juvenis') or (str_2 == 'iniciados'):
            data = '<style>table {border-style: none;border-collapse: collapse;width:100%;font-size:11px}td {border-style: none;padding: 8px;text-align: center;border-bottom: 1px solid #ddd;} tr:hover{background-color:#f5f5f5;} th{border-style: none;background-color:#006699;color: white; padding: 8px;text-align: center;}</style>'
            for x in jornadas_num:
                if str_5 in x:
                    url = re.search('href="(.*)">', str(x)).group(1)
                    url_completo = 'https://resultados.fpf.pt/%s' % url

                    req = requests.get(url_completo)
                    soup = BeautifulSoup(req.content, 'html.parser')
                    jornada = soup.find_all(name='div', attrs={'id':'matches'})

                    for linha in jornada:
                        data_jogo = re.findall('<span class="game-schedule">(.*?)</span>', str(linha), re.DOTALL)
                        equipa_casa = re.findall('text-left">(.*?)</div>', str(linha), re.DOTALL) 
                        resultado = re.findall('<span>(.*?)</span>', str(linha), re.DOTALL) 
                        if len(equipa_casa) != len(resultado):
                            resultado = re.findall('text-center">(.*?)</span>', str(linha), re.DOTALL) 
                        equipa_fora = re.findall('text-right">(.*?)</div>', str(linha), re.DOTALL) 
                        localizacao = re.findall('none;">(.*?)</small>', str(linha), re.DOTALL) 

                        a = {'Resultado': resultado}
                        jornadas_tabela = pd.DataFrame(data=a)
                        jornadas_tabela = jornadas_tabela.rename_axis(None)
                        jornadas_tabela['Resultado'] = jornadas_tabela['Resultado'].str.replace('\r\n', '')
                        jornadas_tabela['Resultado'] = jornadas_tabela['Resultado'].str.replace(' ', '')
                        jornadas_tabela['Resultado'] = jornadas_tabela['Resultado'].str.replace('\n<span>', '')
                        jornadas_tabela['Resultado'] = jornadas_tabela['Resultado'].str.replace('\n<spanclass="game-schedule">', '')
                        jornadas_tabela['Resultado'] = jornadas_tabela['Resultado'].str.replace('<br/>', ' - ')
                        jornadas_tabela.insert(0, 'Data', data_jogo)
                        jornadas_tabela['Data'] = jornadas_tabela['Data'].str.replace('\r\n', '')
                        jornadas_tabela['Data'] = jornadas_tabela['Data'].str.replace(' ', '')
                        jornadas_tabela['Data'] = jornadas_tabela['Data'].str.replace('<br/>', ' - ')
                        jornadas_tabela.insert(1, 'Casa', equipa_casa)
                        jornadas_tabela.insert(3, 'Fora', equipa_fora) 
                        jornadas_tabela.insert(4, 'Localização', localizacao) 

                        data = data + jornadas_tabela.to_html(index=False) + '<br><br>' 
                else:
                    pass
            if '</table>' not in data:
                data = data + 'Não existe a jornada %s nesta competição.<br><br>' %(str(str_5))
            data = data + '<input type="button" value="Voltar" onclick="history.back()">'             
    end_time = time()
    print('Tempo para carregar a página: %s segundos' %(round(end_time-start_time, 3)))

    return render(request, 'home.html', {'header':header, 'search':search, 'subsearch':subsearch, 'data':data})

def options(request):
    print('Página: Jogadores')
    print('Requisito funcional: Consultar informação de jogadores')
    start_time = time()
    header = '<b><a style="color: #006699">Jogadores</a></b><hr>'
    data = '<table style="width: 100%; text-align: center;"><tr><td><form action="/players"><input style="background-color: #006699;width: 100%;font-size:14px;" type="submit" value="Jogadores externos" /></form></td><td><form action="/yfpplayers"><input style="background-color: #012b41; width: 100%;font-size:14px;" type="submit" value="Jogadores internos" /></form></td></tr></table>'
    end_time = time()
    print('Tempo para carregar a página: %s segundos' %(round(end_time-start_time, 3)))    
    return render(request, 'home.html', {'header':header, 'data':data}) 

def yfpplayers(request):
    print('Página: Jogadores internos')
    print('Requisito funcional: Consultar jogadores internos')
    start_time = time()
    header = '<b><a style="color: #006699">Jogadores internos</a></b><hr>'
    search = '<form><input type="text" name="search" placeholder="Pesquisa.." required><br><input type="submit" value="Pesquisar"></form>'
    search_query = request.GET.get('search')
    data = ''
    insert_player = '<form action="/insert_player"><input style="background-color: #006699" type="submit" value="Inserir novo jogador interno" /></form>'

    if search_query != None: #pesquisa na bd
        try:
            client = MongoClient('mongodb://localhost:27017/')                      # PARA INSERIR DOCUMENTOS NO MONGO
            db = client['db']                                                       # PARA INSERIR DOCUMENTOS NO MONGO
            collection = db['players']
            count = 0
            try:
                for x in client['db']['players'].find({ 'nome': re.compile(search_query, re.IGNORECASE) }):
                    count += 1
                    data = data + '<b>Nome: <a style="color: #006699">%s</a></b><br><b>Nome completo: </b>%s<br><b>Nacionalidade: </b>%s<br><b>Nascimento: </b>%s<br><b>Clube: </b>%s<br><b>Posição: </b>%s<br><b>Jogos: </b>%s<br><b>Vitórias: </b>%s<br><b>Empates: </b>%s<br><b>Derrotas: </b>%s<br><b>Golos: </b>%s<br><b>Média de minutos por jogo: </b>%s<br><b>Média de golos por jogo: </b>%s<br><b>Total minutos jogados: </b>%s<br><b>Hora do registo: </b>%s<br><b>Autor do registo: </b>%s<br>' %(str(x['nome']), str(x['nome_completo']), str(x['nacionalidade']), str(x['nascimento']), str(x['clube']), str(x['posicao']), str(x['jogos']), str(x['vitorias']), str(x['empates']), str(x['derrotas']), str(x['golos']), str(x['minutos_por_jogo']), str(x['golos_por_jogo']), str(x['total_minutos']), str(x['data_doc']), str(x['autor'])) + '<hr>'
            except:
                print('Erro na conexão à base de dados ou jogador não encontrado.')
            data = f'<b><a style="color: #006699">{count}</a> resultado(s) correspondente(s) ao jogador <a style="color: #006699">{search_query}</a>.</b><br><br>' + data
        except:
            data = f'<b><a style="color: #006699">{count}</a> resultado(s) correspondente(s) ao jogador <a style="color: #006699">{search_query}</a>.</b><br><br>' + data
            print('Erro')

    end_time = time()
    print('Tempo para carregar a página: %s segundos' %(round(end_time-start_time, 3)))    
    return render(request, 'home.html', {'header':header, 'search':search, 'data':data, 'insert_player':insert_player})

def players(request):
    print('Página: Jogadores externos')
    print('Requisito funcional: Consultar jogadores externos')
    start_time = time()
    header = '<b><a style="color: #006699">Jogadores externos</a></b><hr><br>'
    search = '<form><input type="text" name="search" placeholder="Pesquisa.." required><br><input type="submit" value="Pesquisar"></form><br>'
    search_query = request.GET.get('search')

    player_header = ''
    player_information = ''
    data_header = ''
    player_image = ''
    news_header = ''
    news = ''
    specialist_header = ''
    specialist = ''
    specialist_name = ''
    data = ''

    if search_query != None:
        start_time_extracao = time()
        
        driver.get(f"https://www.zerozero.pt/search_player.php?op=all&search_string={search_query}&fem=0&ida=1&mod=1&ord=i&peq=1&sta=0&op=all")

        try: 
            table = driver.find_element_by_class_name("zztable")
            table_code = table.get_attribute('innerHTML')
            try:
                imagem_url = "http://zerozero.pt%s" %(re.search('src="(.*?)"', table_code).group(1))
                urllib.request.urlretrieve(imagem_url, "jogador.jpg")
                data_uri = base64.b64encode(open('jogador.jpg', 'rb').read()).decode('utf-8')
                info_imagem_str = '<img src="data:image/png;base64,{0}">'.format(data_uri)
            except:
                info_imagem_str = ''

            info_nome = re.search('style="text-decoration:none;">(.*)</a>', table_code).group(1)
            info_nome_completo = re.search('<span class="small_faded">(.*)</span>', table_code).group(1)
            info_nacionalidade = re.search('<div class="text">(.*?)</div>', table_code).group(1)
            try:
                info_nascimento = re.search('Nascimento</td><td style="text-align:left;">(.*)</td></tr><tr><td class="label">Clube', table_code).group(1)
            except:
                info_nascimento = ''
            try:
                info_clube = re.search('Clube</td><td style="text-align:left;">(.*)</td></tr><tr><td', table_code).group(1)
                info_clube = re.search('<div class="text">(.*)</div></div>', info_clube).group(1)
            except:
                info_clube = ''

            info_posicao = re.search('Posição</td><td style="text-align:left;">(.*)</td>', table_code).group(1)
            player_information = '%s<br><b>Nome:</b> %s<br><b>Nome completo:</b> %s<br><b>Nacionalidade:</b> %s<br><b>Nascimento:</b> %s<br><b>Clube:</b> %s<br><b>Posição:</b> %s' %(info_imagem_str, info_nome, info_nome_completo, info_nacionalidade, info_nascimento, info_clube, info_posicao)
        except:
            player_information = '<i>Nenhum jogador corresponde à pesquisa "%s".</i>' %(search_query)
            data = ''

        #driver.close()
        end_time_extracao = time()
        print('Tempo para carregar a informação do jogador: %s segundos' %(round(end_time_extracao-start_time_extracao, 3)))  

    if search_query != None and player_information != '':
        print('Requisito funcional: Consultar informação do Twitter')
        start_time_twitter = time()
        try:
            tso = TwitterSearchOrder() # create a TwitterSearchOrder object
            tso.set_keywords([search_query, '-filter:retweets']) # let's define all words we would like to have a look for
            tso.set_language('pt') # we want to see PT tweets only
            tso.set_include_entities(False) # and don't give us all those entity information

            ts = TwitterSearch(
                consumer_key = 'MFpmoi9o2v1t3AfiVvq3FLfx0',
                consumer_secret = 'qzcwYGhWADg4Ki6f3h9Ah439Y6yqSIlwyCJ9XpztXehWRHPmnG',
                access_token = '1231903899487023104-v85tu1G7AK1KA4ewbqXd237c1Gb73K',
                access_token_secret = 'i3LeVRf8gF8AZKZaf0FibkbRPr9TndbWc159694zj6nf7'
            )

            count = 0
            for tweet in ts.search_tweets_iterable(tso):
                if count < 3:
                    tweet_str = '<b style="background-color: #ececec; color: #006699">@%s</b> <a style="font-size: 10px">(%s)</a><br>%s<hr>' % ( tweet['user']['screen_name'], tweet['created_at'], tweet['text'] )
                    tweet_link = tweet['text'].split()[-1]
                    data = data + tweet_str                    
                    if tweet_link[0:5] == 'https':
                        data = data.rsplit(' ', 1)[0]
                        data = data + '<form action="%s" target="_blank"><input type="submit" value="Ver tweet completo" /></form><hr>' % ( tweet_link)
                    count = count + 1 
                else:
                    break

        except TwitterSearchException as e: # take care of all those ugly errors if there are some
            print(e)    
        end_time_twitter = time()
        print('Tempo para carregar a informação do Twitter: %s segundos' %(round(end_time_twitter-start_time_twitter, 3)))   
    
    start_time_specialist = time()
    if player_information != '':
        player_header = '<table style="width:100%"><tr><td style="background-color:#006699;height: 50px;padding-left: 10px;color:white;"><b>' + search_query.title() + '</b>&nbsp;<a href="/statistics?search=%s" style="text-decoration: none; color: black"><b>&nbsp; &rarr; Ver estatísticas</b></a></td></tr></table><br>' %(search_query)
        data_header = '<table style="width:100%"><tr><td><br></td></tr><tr><td style="background-color: #006699; width: 5px"></td><td style="background-color:#ececec;height: 50px;padding-left: 10px;"><b>Últimos tweets relacionados</b></td></tr></table><br>'
        news_header = '<table style="width:100%"><tr><td><br></td></tr><tr><td style="background-color: #006699; width: 5px"></td><td style="background-color:#ececec;height: 50px;padding-left: 10px;"><b>Últimas notícias relacionadas</b></td></tr></table><br>'
        if data == '' or data is None:
            data = '<i>Não há tweets relacionados com o jogador.</i>'
        news = ''
        specialist_header = '<table style="width:100%"><tr><td><br></td></tr><tr><td style="background-color: #006699; width: 5px"></td><td style="background-color:#ececec;height: 50px;padding-left: 10px;"><b>O que dizem os especialistas</b></td></tr></table><br>'
        specialist = ''
        specialist_name = ''
        # Comentário especialista
        try:
            tso = TwitterSearchOrder() # create a TwitterSearchOrder object
            tso.set_keywords(['#YouthFootballPlatform', search_query, '#Especialista']) # let's define all words we would like to have a look for
            tso.set_language('pt') # we want to see German tweets only
            tso.set_include_entities(False) # and don't give us all those entity information
            ts = TwitterSearch(
                consumer_key = 'MFpmoi9o2v1t3AfiVvq3FLfx0',
                consumer_secret = 'qzcwYGhWADg4Ki6f3h9Ah439Y6yqSIlwyCJ9XpztXehWRHPmnG',
                access_token = '1231903899487023104-v85tu1G7AK1KA4ewbqXd237c1Gb73K',
                access_token_secret = 'i3LeVRf8gF8AZKZaf0FibkbRPr9TndbWc159694zj6nf7'
            )

            count_criticas = 0
            for tweet in ts.search_tweets_iterable(tso):
                for x in ESPECIALISTAS_TWITTER:
                    if x == tweet['user']['screen_name'] and count_criticas == 0:
                        count_criticas = 1
                        specialist = '&rarr; ' + tweet['text']
                        specialist_name = '@' + tweet['user']['screen_name']
                        tweet_link = tweet['text'].split()[-1]
                        if tweet_link[0:5] == 'https':
                            specialist = specialist.rsplit(' ', 1)[0]
                            specialist = specialist + '<form action="%s" target="_blank"><input type="submit" value="Ver tweet completo" /></form>' % ( tweet_link)

        except TwitterSearchException as e: # take care of all those ugly errors if there are some
            print(e)

        end_time_specialist = time()
        print('Tempo para carregar comentário do especialista: %s segundos' %(round(end_time_specialist-start_time_specialist, 3))) 

        print('Requisito funcional: Consultar informação do Google News')
        start_time_google = time()

        googlenews = GoogleNews(lang='pt')
        googlenews.search('"' + search_query + '"')
        result=googlenews.result()
        df=pd.DataFrame(result)
        for x in df.index[0:2]:
            news_title = df['title'][x]            
            news_date = df['date'][x]
            news_journal = df['media'][x]
            news_link = df['link'][x]
            news = news + '<b><a href="' + news_link + '" target="_blank" style="text-decoration: none; color: #302f2f">' + news_title + '</a></b><br><a style="color: #006699"><b>' + news_date + '</b></a> ' + news_journal + '<br>'
        end_time_google = time()
        print('Tempo para carregar a informação do Google News: %s segundos' %(round(end_time_google-start_time_google, 3))) 

        if specialist == '':
            specialist = '<i>Não há comentários dos especialistas a este jogador.</i>'

    if search_query is None:
        player_information = ''

    end_time = time()
    print('Tempo para carregar a página: %s segundos' %(round(end_time-start_time, 3)))
    return render(request, 'results.html', {'header':header, 'search':search, 'data':data, 'player_header':player_header, 'player_image':player_image, 'player_information':player_information, 'data_header':data_header, 'news_header':news_header, 'news':news, 'specialist_header':specialist_header, 'specialist':specialist, 'specialist_name':specialist_name})  


def insert_player(request):
    print('Página: Inserir jogador')
    start_time = time()

    header = '<b><a style="color: #006699">Inserir jogador</a></b><hr>'
    sub_header = '<i>Para inserir um jogador na base de dados da <b>Youth Football Platform</b>, necessita de um utilizador.</i>'

    data = ''
    nome = ''
    nome_completo = ''
    nacionalidade = ''
    nascimento = ''
    clube = ''
    posicao = ''
    jogos = ''
    vitorias = ''
    empates = ''
    derrotas = ''
    golos = ''
    minutos_por_jogo = ''
    golos_por_jogo = ''
    total_minutos = ''
    autor = ''
    login = False

    try:
        nome = request.GET.get('nome')
        nome_completo = request.GET.get('nome_completo')
        nacionalidade = request.GET.get('nacionalidade')
        nascimento = request.GET.get('nascimento')
        clube = request.GET.get('clube')
        posicao = request.GET.get('posicao')
        jogos = request.GET.get('jogos')
        vitorias = request.GET.get('vitorias')
        empates = request.GET.get('empates')
        derrotas = request.GET.get('derrotas')
        golos = request.GET.get('golos')
        total_minutos = request.GET.get('total_minutos')
        minutos_por_jogo = round(int(total_minutos)/int(jogos))
        golos_por_jogo = '{:.1f}'.format(int(golos)/int(jogos))
        autor = request.GET.get('autor')
    except:
        nome = None

    try:
        client = MongoClient('mongodb://localhost:27017/')                      # PARA INSERIR DOCUMENTOS NO MONGO
        db = client['db']                                                       # PARA INSERIR DOCUMENTOS NO MONGO
        collection = db['players']                                              # PARA INSERIR DOCUMENTOS NO MONGO   
        users = db['users']

        form = """
            <style>
            form {
            /* Apenas para centralizar o form na página */
                margin: 0 auto;
                width: 400px;
            /* Para ver as bordas do formulário */
                padding: 1em;
                border-radius: 1em;
            }
            form div + div {
                margin-top: 1em;
            }
            label {
            /*Para ter certeza que todas as labels tem o mesmo tamanho e estão propriamente alinhadas */
                display: inline-block;
                width: 400px;
                text-align: left;
            }
            input, textarea {
            /* Para certificar-se que todos os campos de texto têm as mesmas configurações de fonte. Por padrão, textareas ter uma fonte monospace*/
                font: 1em sans-serif;
                

            /* Para dar o mesmo tamanho a todos os campo de texto */
                width: 300px;
                -moz-box-sizing: border-box;
                box-sizing: border-box;

            /* Para harmonizar o look & feel das bordas nos campos de texto*/
                border: 1px solid #999;
            }
            input:focus, textarea:focus {
            /* Dar um pouco de destaque nos elementos ativos */
                border-color: #000;
            }
            textarea {
            /* Para alinhar corretamente os campos de texto de várias linhas com sua label*/
                vertical-align: top;

            /* Para dar espaço suficiente para digitar algum texto */
                height: 5em;

            /* Para permitir aos usuários redimensionarem qualquer textarea verticalmente. Ele não funciona em todos os browsers */
                resize: vertical;
            }
            </style>

            <form>
            <div>
                <label for="username"><b>Username:</b></label><br>
                <input type="name" name="username" placeholder="Username..." required/>
            </div>
            <div>
                <label for="password"><b>Password:</b></label><br>
                <input type="password" name="password" placeholder="Password..." required/>
            </div>
            <div class="button">
                <input type="submit" style="background-color: #006699" value="Login">
            </div>
            </form>
            <form action="/signup">
				<input type="submit" style="font-size: 15px;background-color: #012b41;color: rgb(255, 255, 255);border-style: none;padding: 10px 10px 10px 10px;" value="Registar">
			</form>
            """
        try:
            username = str(request.GET.get('username'))
            password = str(request.GET.get('password'))
        except:
            username = 'erro'
            password = 'erro'

        if users.count_documents({ 'user': username, 'password': password }, limit = 1) != 0:
            login = True
            print('Login efetuado com sucesso!')
            print('Requisito funcional: Fazer login')
        else:
            login = False
            if username != 'None':
                data = '<i style="color: red">Login incorreto.</i>'
            else:
                data = ''


        if login == True:
            sub_header = ''
            form = """
            <style>
            form {
            /* Apenas para centralizar o form na página */
                margin: 0 auto;
                width: 400px;
            /* Para ver as bordas do formulário */
                padding: 1em;
                border-radius: 1em;
            }
            form div + div {
                margin-top: 1em;
            }
            label {
            /*Para ter certeza que todas as labels tem o mesmo tamanho e estão propriamente alinhadas */
                display: inline-block;
                width: 400px;
                text-align: left;
            }
            input, textarea {
            /* Para certificar-se que todos os campos de texto têm as mesmas configurações de fonte. Por padrão, textareas ter uma fonte monospace*/
                font: 1em sans-serif;
                

            /* Para dar o mesmo tamanho a todos os campo de texto */
                width: 300px;
                -moz-box-sizing: border-box;
                box-sizing: border-box;

            /* Para harmonizar o look & feel das bordas nos campos de texto*/
                border: 1px solid #999;
            }
            input:focus, textarea:focus {
            /* Dar um pouco de destaque nos elementos ativos */
                border-color: #000;
            }
            textarea {
            /* Para alinhar corretamente os campos de texto de várias linhas com sua label*/
                vertical-align: top;

            /* Para dar espaço suficiente para digitar algum texto */
                height: 5em;

            /* Para permitir aos usuários redimensionarem qualquer textarea verticalmente. Ele não funciona em todos os browsers */
                resize: vertical;
            }
            </style>

            <form>
            <div>
                <label for="autor"><b>Autor do registo:</b></label><br>
                <input type="name" name="autor" value="%s" disabled/>
            </div>
            <div>
                <label for="nome"><b>Nome do jogador:</b></label><br>
                <input type="name" name="nome" placeholder="Inserir nome..." required/>
            </div>
            <div>
                <label for="nome_completo"><b>Nome do jogador completo:</b></label><br>
                <input type="name" name="nome_completo" placeholder="Inserir nome completo..." required/>
            </div>
            <div>
                <label for="nacionalidade"><b>Nacionalidade:</b></label><br>
                <input type="name" name="nacionalidade" placeholder="Inserir nacionalidade..." required/>
            </div>
            <div>
                <label for="nascimento"><b>Nascimento:</b></label><br>
                <input type="date" name="nascimento" required/>
            </div>
            <div>
                <label for="clube"><b>Clube:</b></label><br>
                <input type="name" name="clube" required/>
            </div>
            <div>
                <label for="posicao"><b>Posição:</b></label><br>
                <input type="radio" id="gr" name="posicao" value="Guarda-redes" required>
                <label for="gr">Guarda-redes</label><br>
                <input type="radio" id="def" name="posicao" value="Defesa">
                <label for="def">Defesa</label><br>
                <input type="radio" id="med" name="posicao" value="Médio">
                <label for="med">Médio</label>    
                <input type="radio" id="ava" name="posicao" value="Avançado">
                <label for="ava">Avançado</label>    
            </div>
            <div>
                <label for="jogos"><b>Jogos:</b></label><br>
                <input type="number" name="jogos" min="0" max="200" required/>
            </div>
            <div>
                <label for="vitorias"><b>Vitórias:</b></label><br>
                <input type="number" name="vitorias" min="0" max="200" required/>
            </div>
            <div>
                <label for="empates"><b>Empates:</b></label><br>
                <input type="number" name="empates" min="0" max="200" required/>
            </div>
            <div>
                <label for="derrotas"><b>Derrotas:</b></label><br>
                <input type="number" name="derrotas" min="0" max="200" required/>
            </div>
            <div>
                <label for="golos"><b>Golos:</b></label><br>
                <input type="number" name="golos" min="0" max="1000" required/>
            </div>
            <div>
                <label for="total_minutos"><b>Total de minutos jogados:</b></label><br>
                <input type="number" name="total_minutos" min="0" max="24000" required/>
            </div>
            <div class="button">
                <input type="submit" value="Inserir jogador">
            </div>
            <input type="hidden" name="username" value="%s" />
            <input type="hidden" name="password" value="%s" />
            </form>
            """ %(username, username, password)


        doc = []
        if nome != None:
            form = ''
            try:

                now = datetime.now()
                data_doc = now.strftime("%d/%m/%Y - %H:%M:%S")

                doc.append('{ "nome": "%s", "nome_completo": "%s", "nacionalidade": "%s", "nascimento": "%s", "clube": "%s", "posicao": "%s", "jogos": "%s", "vitorias": "%s", "empates": "%s", "derrotas": "%s", "golos": "%s", "minutos_por_jogo": "%s", "golos_por_jogo": "%s", "total_minutos": "%s", "autor": "%s", "data_doc": "%s"}' %(nome, nome_completo, nacionalidade, nascimento, clube, posicao, jogos, vitorias, empates, derrotas, golos, minutos_por_jogo, golos_por_jogo, total_minutos, username, data_doc))
                    
                top5 = itertools.islice(doc, 1)
                doc = ', '.join(top5)

                doc_json = json.loads(doc)
                x = collection.insert_one(doc_json)  

                print('Jogador inserido com sucesso.')
                print('Requisito funcional: Inserir jogadores na base de dados')
            except:
                data = 'Não funcionou.'
    except:
        data = '<a style="color: red">Erro na conexão à base de dados.</a>'

    if nome_completo != None and nome_completo != '' and nome_completo != 'None':
        header = f'<b><a style="color: #006699">Inserir jogador: {str(nome)}</a></b><hr>'
        sub_header = '<a style="color: limegreen"><i>Jogador inserido com sucesso!</i></a><br><br>'
        form = f'<b>Nome: </b>{nome}<br><b>Nome completo: </b>{nome_completo}<br><b>Nacionalidade: </b>{nacionalidade}<br><b>Nascimento: </b>{nascimento}<br><b>Clube: </b>{clube}<br><b>Posição: </b>{posicao}<br><b>Jogos: </b>{jogos}<br><b>Vitórias: </b>{vitorias}<br><b>Empates: </b>{empates}<br><b>Derrotas: </b>{derrotas}<br><b>Golos: </b>{golos}<br><b>Média de minutos por jogo: </b>{minutos_por_jogo}<br><b>Média de golos por jogo: </b>{golos_por_jogo}<br><b>Total minutos jogados: </b>{total_minutos}<br><b>Hora do registo: </b>{data_doc}<br><b>Autor do registo: </b>{username}<br>'
        data = '<br><form><input type="hidden" name="username" value="%s" /><input type="hidden" name="password" value="%s" /><input type="submit" value="Inserir novo jogador" onclick="/insert_player"></form>' %(username, password)
    end_time = time()
    print('Tempo para carregar a página: %s segundos' %(round(end_time-start_time, 3)))    
    return render(request, 'home.html', {'header':header, 'sub_header':sub_header, 'form':form, 'data':data})

def signup(request):
    print('Página: Registar')
    print('Requisito funcional: Registar na plataforma')
    start_time = time()
    header = '<b><a style="color: #006699">Registar</a></b><hr>'

    try:
        user = request.GET.get('user')
        password = request.GET.get('password')
        tipo_utilizador = request.GET.get('tipo_utilizador')
        nome = request.GET.get('nome')
        email = request.GET.get('email')
        data_nascimento = request.GET.get('data_nascimento')
        genero = request.GET.get('genero')
    except:
        nome = None

    data = """
            <style>
            form {
            /* Apenas para centralizar o form na página */
                margin: 0 auto;
                width: 400px;
            /* Para ver as bordas do formulário */
                padding: 1em;
                border-radius: 1em;
            }
            form div + div {
                margin-top: 1em;
            }
            label {
            /*Para ter certeza que todas as labels tem o mesmo tamanho e estão propriamente alinhadas */
                display: inline-block;
                width: 400px;
                text-align: left;
            }
            input, textarea {
            /* Para certificar-se que todos os campos de texto têm as mesmas configurações de fonte. Por padrão, textareas ter uma fonte monospace*/
                font: 1em sans-serif;
                

            /* Para dar o mesmo tamanho a todos os campo de texto */
                width: 300px;
                -moz-box-sizing: border-box;
                box-sizing: border-box;

            /* Para harmonizar o look & feel das bordas nos campos de texto*/
                border: 1px solid #999;
            }
            input:focus, textarea:focus {
            /* Dar um pouco de destaque nos elementos ativos */
                border-color: #000;
            }
            textarea {
            /* Para alinhar corretamente os campos de texto de várias linhas com sua label*/
                vertical-align: top;

            /* Para dar espaço suficiente para digitar algum texto */
                height: 5em;

            /* Para permitir aos usuários redimensionarem qualquer textarea verticalmente. Ele não funciona em todos os browsers */
                resize: vertical;
            }
            </style>

            <form>
            <div>
                <label for="user"><b>Username:</b></label><br>
                <input type="name" name="user" placeholder="Inserir user..." required/>
            </div>
            <div>
                <label for="password"><b>Password:</b></label><br>
                <input type="name" name="password" placeholder="Inserir password..." required/>
            </div>
            <div>
                <label for="tipo_utilizador"><b>Tipo de utilizador:</b></label><br>
                <select id="tipo_utilizador" name="tipo_utilizador">
                    <option value="dirigente">Dirigente</option>
                    <option value="atleta">Atleta</option>
                    <option value="olheiro">Olheiro</option>
                    <option value="adepto">Adepto</option>
                </select>
            </div>
            <div>
                <label for="nome"><b>Nome:</b></label><br>
                <input type="name" name="nome" placeholder="Inserir nome..." required/>
            </div>
            <div>
                <label for="email"><b>E-mail:</b></label><br>
                <input type="email" name="email" required/>
            </div>
            <div>
                <label for="data_nascimento"><b>Data de nascimento:</b></label><br>
                <input type="date" name="data_nascimento" required/>
            </div>
            <div>
                <label for="genero"><b>Género:</b></label><br>
                
                <label for="masc">Masculino <input type="radio" id="masc" name="genero" value="Masculino" required></label><br>
                
                <label for="fem">Feminino <input type="radio" id="fem" name="genero" value="Feminino"></label><br>
            </div>
            <div class="button">
                <input type="submit" value="Registar">
            </div>
            </form>
    """
    if user != None:
        try:
            client = MongoClient('mongodb://localhost:27017/')                     
            db = client['db']                                                                   
            users = db['users']
            if users.count_documents({ 'user': user }, limit = 1) != 0 or users.count_documents({ 'email': email }, limit = 1) != 0: 
                nome = None
                data = '<a style="color: red">Erro! O username ou o e-mail que indicou já estão a ser utilizados na plataforma.</a>' + data
        except:   
            nome = None
            data = '<a style="color: red">Erro na conexão à base de dados!</a>'
    doc = []
    if nome != None:
        try:
            doc.append('{ "user": "%s", "password": "%s", "tipo_utilizador": "%s", "nome": "%s", "email": "%s", "data_nascimento": "%s", "genero": "%s"}' %(user, password, tipo_utilizador, nome, email, data_nascimento, genero))

            top5 = itertools.islice(doc, 1)
            doc = ', '.join(top5)

            doc_json = json.loads(doc)
            x = users.insert_one(doc_json) 

            data = '<a style="color: limegreen"><i>Utilizador registado com sucesso.</i></a> Bem-vind@ à comunidade, <b>%s</b>!<br><form action="/insert_player"><input type="submit" style="font-size: 15px;background-color: #012b41;color: rgb(255, 255, 255);border-style: none;padding: 10px 10px 10px 10px;" value="Inserir jogador"></form>' %(user)
            print('Utilizador registado com sucesso!')
        except:
            pass

    end_time = time()
    print('Tempo para carregar a página: %s segundos' %(round(end_time-start_time, 3)))    
    return render(request, 'home.html', {'header':header, 'data':data})  


def contacts(request):
    print('Página: Contactos')
    start_time = time()

    header = '<b><a style="color: #006699">Contactos</a></b><hr><br>'
    data = 'Se tiver sugestões ou dúvidas sobre a plataforma, não hesite em nos deixar uma mensagem.'
    form = """
    <style>
    form {
    /* Apenas para centralizar o form na página */
        margin: 0 auto;
        width: 400px;
    /* Para ver as bordas do formulário */
        padding: 1em;
        border-radius: 1em;
    }
    form div + div {
        margin-top: 1em;
    }
    label {
    /*Para ter certeza que todas as labels tem o mesmo tamanho e estão propriamente alinhadas */
        display: inline-block;
        width: 90px;
        text-align: left;
    }
    input, textarea {
    /* Para certificar-se que todos os campos de texto têm as mesmas configurações de fonte. Por padrão, textareas ter uma fonte monospace*/
        font: 1em sans-serif;
        

    /* Para dar o mesmo tamanho a todos os campo de texto */
        width: 300px;
        -moz-box-sizing: border-box;
        box-sizing: border-box;

    /* Para harmonizar o look & feel das bordas nos campos de texto*/
        border: 1px solid #999;
    }
    input:focus, textarea:focus {
    /* Dar um pouco de destaque nos elementos ativos */
        border-color: #000;
    }
    textarea {
    /* Para alinhar corretamente os campos de texto de várias linhas com sua label*/
        vertical-align: top;

    /* Para dar espaço suficiente para digitar algum texto */
        height: 5em;

    /* Para permitir aos usuários redimensionarem qualquer textarea verticalmente. Ele não funciona em todos os browsers */
        resize: vertical;
    }
    </style>

    <form action="mailto:andrerouiller1995@gmail.com" method="post">
    <div>
        <label for="name"><b>Nome:</b></label><br>
        <input type="name" id="name" />
    </div>
    <div>
        <label for="mail"><b>E-mail:</b></label><br>
        <input type="email" id="mail" />
    </div>
    <div>
        <label for="msg"><b>Mensagem:</b></label><br>
        <textarea id="msg"></textarea>
    </div>
    <div class="button">
        <input type="submit" value="Enviar mensagem">
    </div>
    </form>
    """

    end_time = time()
    print('Tempo para carregar a página: %s segundos' %(round(end_time-start_time, 3)))
    return render(request, 'contacts.html', {'header':header, 'data':data, 'form':form})  


def archive(request):
    print('Página: Épocas anteriores')
    start_time = time()

    str_1 = request.GET.get('af')
    str_2 = request.GET.get('campeonato')
    str_3 = request.GET.get('competicao')
    str_4 = request.GET.get('epoca')
    str_5 = request.GET.get('div')
    str_af = str(str_1)
    str_campeonato = str(str_2)
    str_competicao = str(str_3)  
    str_epoca = str(str_4)
    str_div = str(str_5)
    search = """ 
    <form>
    <select id="epoca" name="epoca">
    <option value="16_17">2016/2017</option><option value="17_18">2017/2018</option>
    <option value="18_19">2018/2019</option>       
    </select>
    <select id="af" name="af">
    <option value="comp_fpf">Competições FPF</option>
    <option value="af_algarve">AF Algarve</option><option value="af_angra">AF Angra</option>
    <option value="af_aveiro">AF Aveiro</option><option value="af_beja">AF Beja</option>
    <option value="af_braga">AF Braga</option><option value="af_braganca">AF Bragança</option>
    <option value="af_castelo_branco">AF Castelo Branco</option><option value="af_coimbra">AF Coimbra</option>   
    <option value="af_evora">AF Évora</option><option value="af_guarda">AF Guarda</option>   
    <option value="af_horta">AF Horta</option><option value="af_leiria">AF Leiria</option>       
    <option value="af_lisboa">AF Lisboa</option><option value="af_madeira">AF Madeira</option> 
    <option value="af_ponta_delgada">AF Ponta Delgada</option><option value="af_portalegre">AF Portalegre</option>   
    <option value="af_porto">AF Porto</option><option value="af_santarem">AF Santarém</option>       
    <option value="af_setubal">AF Setúbal</option><option value="af_viana_castelo">AF Viana do Castelo</option>     
    <option value="af_vila_real">AF Vila Real</option><option value="af_viseu">AF Viseu</option>           
    </select>
    <select id="campeonato" name="campeonato">
    <option value="juniores">Juniores (Juniores A)</option>
    <option value="juvenis">Juvenis (Juniores B)</option>
    <option value="iniciados">Iniciados (Juniores C)</option>
    <option value="infantis">Infantis (Juniores D)</option>
    <option value="benjamins">Benjamins (Juniores E)</option>
    <option value="traquinas">Traquinas (Juniores F)</option>
    <option value="petizes">Petizes (Juniores G)</option>
    </select> 
    <br>
    <input type="submit" value="Seguinte">
    </form>
    <br>
    """
    
    if str_1 == 'comp_fpf':
        if (str_2 == 'juniores') and (str_4 == '16_17'):
            header = '<b><a style="color: #006699">Classificação:</a></b> %s > %s<hr><br>' %(ASSOCIACAO_EXTENSO[str_af], str_campeonato)
            search = """
                <form>
                <select id="div" name="div">
                <option value="divisao1_16_17">1ª divisão</option>
                <option value="divisao2_16_17">2ª divisão</option>
                </select> 
                <br>
                <input type="submit" value="Seguinte">
                <input type="button" value="Voltar" onclick="history.back()">
                </form>
            """
            subsearch = ''
            data = ''
            return render(request, 'home.html', {'header':header, 'search':search, 'subsearch':subsearch, 'data':data})
        if (str_2 == 'juniores') and (str_4 == '17_18'):
            header = '<b><a style="color: #006699">Classificação:</a></b> %s > %s<hr><br>' %(ASSOCIACAO_EXTENSO[str_af], str_campeonato)
            search = """
                <form>
                <select id="div" name="div">
                <option value="divisao1_17_18">1ª divisão</option>
                <option value="divisao2_17_18">2ª divisão</option>
                </select> 
                <br>
                <input type="submit" value="Seguinte">
                <input type="button" value="Voltar" onclick="history.back()">
                </form>
            """
            subsearch = ''
            data = ''
            return render(request, 'home.html', {'header':header, 'search':search, 'subsearch':subsearch, 'data':data})
        if (str_2 == 'juniores') and (str_4 == '18_19'):
            header = '<b><a style="color: #006699">Classificação:</a></b> %s > %s<hr><br>' %(ASSOCIACAO_EXTENSO[str_af], str_campeonato)
            search = """
                <form>
                <select id="div" name="div">
                <option value="divisao1_18_19">1ª divisão</option>
                <option value="divisao2_18_19">2ª divisão</option>
                </select> 
                <br>
                <input type="submit" value="Seguinte">
                <input type="button" value="Voltar" onclick="history.back()">
                </form>
            """
            subsearch = ''
            data = ''
            return render(request, 'home.html', {'header':header, 'search':search, 'subsearch':subsearch, 'data':data})

    if str_5 is not None:           # Competições FPF
        if str_5 == 'divisao1':
            header = '<b><a style="color: #006699">Classificação:</a></b> Competições FPF > Júniores A > 1ª Divisão<hr><br>'
            search = 'TABELA DA 1A DIVISAO AQUI https://resultados.fpf.pt/Competition/Details?competitionId=14820&seasonId=98'
            subsearch = ''
            data = ''
        if str_5 == 'divisao2': 
            header = '<b><a style="color: #006699">Classificação:</a></b> Competições FPF > Júniores A > 2ª Divisão<hr><br>'
            search = 'TABELA DA 2A DIVISAO AQUI https://resultados.fpf.pt/Competition/Details?competitionId=17016&seasonId=98'
            subsearch = ''
            data = ''

    if str_1 is not None:
        header = '<b><a style="color: #006699">Classificação:</a></b> %s<hr><br>' %(ASSOCIACAO_EXTENSO[str_af])
        search = ''
        data = ''
    else:
        header = '<b><a style="color: #006699">Classificação épocas anteriores</a></b><hr><br>'
        data = ''

    last_url = str(request.META.get('HTTP_REFERER'))
    req = requests.get('https://resultados.fpf.pt/Competition/GetCompetitionsByAssociation?associationId=224&seasonId=99')

    if str_af != 'None' and str_af != 'comp_fpf':
        req = requests.get(ASSOCIACAO_EPOCA_PT[str_1]+EPOCA_PT[str_epoca])
    elif str_3 is not None:
        req = requests.get(ASSOCIACAO_EPOCA_PT[last_url.split("&campeonato", 1)[0][45:]]+EPOCA_PT[last_url.split("&", 1)[0][36:]])

    if req.status_code == 200:
        print('Requisição bem sucedida!')
        content = req.content

    soup = BeautifulSoup(content, 'html.parser')
    div_table = soup.find_all(name='div', attrs={'class':'list-links'})

    count = 0

    str_form = """ <form>
    <select id="competicao" name="competicao"> """

    str_form_fim = """
    </select> 
    <br>
    <input type="submit" value="Seguinte"><input type="button" value="Voltar" onclick="history.back()"></form>
    """

    for x in div_table:
        if 'JOGO PART FUTEBOL SETE' in str(x):
            count = -1
        elif count == 0 or 'SENIOR' in str(x) or 'Desconhecida' in str(x) or 'SENIORES' in str(x) or 'JOGO PART FUTEBOL SETE' in str(x):
            pass
        elif 'FUTSAL' in str(x) or 'FEMININO' in str(x) or 'Futsal' in str(x) or 'Feminino' in str(x) or 'FEM' in str(x):
            pass
        elif count == 1:
            if str_campeonato == 'juniores':
                for y in str(x).splitlines()[1:-1]:
                    if 'Taça' in y or 'TACA' in y or 'taca' in y or 'TAÇA' in y or 'taça' in y or 'Cup' in y:
                        pass
                    else:
                        str_form+=str('<option>%s</option>') %(y)
        elif count == 2:
            if str_campeonato == 'juvenis':
                for y in str(x).splitlines()[1:-1]:
                    if 'Taça' in y or 'TACA' in y or 'taca' in y or 'TAÇA' in y or 'taça' in y or 'Cup' in y:
                        pass
                    else:
                        str_form+=str('<option>%s</option>') %(y)
        elif count == 3:
            if str_campeonato == 'iniciados':
                for y in str(x).splitlines()[1:-1]:
                    if 'Taça' in y or 'TACA' in y or 'taca' in y or 'TAÇA' in y or 'taça' in y or 'Cup' in y:
                        pass
                    else:
                        str_form+=str('<option>%s</option>') %(y)
        elif count == 4:
            if str_campeonato == 'infantis':
                for y in str(x).splitlines()[1:-1]:
                    if 'Taça' in y or 'TACA' in y or 'taca' in y or 'TAÇA' in y or 'taça' in y or 'Cup' in y:
                        pass
                    else:
                        str_form+=str('<option>%s</option>') %(y)
        elif count == 5:
            if str_campeonato == 'benjamins':
                for y in str(x).splitlines()[1:-1]:
                    if 'Taça' in y or 'TACA' in y or 'taca' in y or 'TAÇA' in y or 'taça' in y or 'Cup' in y:
                        pass
                    else:
                        str_form+=str('<option>%s</option>') %(y)
        elif count == 6:
            if str_campeonato == 'traquinas':
                for y in str(x).splitlines()[1:-1]:
                    if 'Taça' in y or 'TACA' in y or 'taca' in y or 'TAÇA' in y or 'taça' in y or 'Cup' in y:
                        pass
                    else:
                        str_form+=str('<option>%s</option>') %(y)
        elif count == 7:
            if str_campeonato == 'petizes':
                for y in str(x).splitlines()[1:-1]:
                    if 'Taça' in y or 'TACA' in y or 'taca' in y or 'TAÇA' in y or 'taça' in y or 'Cup' in y:
                        pass
                    else:
                        str_form+=str('<option>%s</option>') %(y)
        count=count+1
    
    subsearch = str_form + str_form_fim

    if '<option' not in subsearch:
        subsearch = 'Não existem dados ou não existe campeonato de <b>%s</b> na %s.<br><br><input type="button" value="Voltar" onclick="history.back()">'%(str_campeonato, str_af)


    if str_1 == 'comp_fpf':
        subsearch = ''

    if (str_3 is not None) or (str_5 is not None) or (str_1 == 'comp_fpf' and str_2 == 'juvenis') or (str_1 == 'comp_fpf' and str_2 == 'iniciados'):
        header = '<b><a style="color: #006699">Classificação:</a></b> %s<hr><br>' %(str_competicao)
        search = ''
        subsearch = ''
        str_url = ''
        if str_3 is not None:
            for x in div_table:
                for y in str(x).splitlines()[1:-1]:
                    if str_3 in y and 'Futsal' not in y and 'FUTSAL' not in y:
                        str_url = y.split('" ', 1)[0][9:]
            url_comp = 'https://resultados.fpf.pt%s' %(str_url) 
        if str_5 == 'divisao1_16_17':
            header = '<b><a style="color: #006699">Classificação:</a></b> Competições FPF > Júniores > 1ª Divisão 2016/17<hr><br>'
            url_comp = 'https://resultados.fpf.pt/Competition/Details?competitionId=17007&seasonId=96'
        if str_5 == 'divisao2_16_17':
            header = '<b><a style="color: #006699">Classificação:</a></b> Competições FPF > Júniores > 2ª Divisão 2016/17<hr><br>'
            url_comp = 'https://resultados.fpf.pt/Competition/Details?competitionId=17016&seasonId=96'
        if str_5 == 'divisao1_17_18':
            header = '<b><a style="color: #006699">Classificação:</a></b> Competições FPF > Júniores > 1ª Divisão 2017/18<hr><br>'
            url_comp = 'https://resultados.fpf.pt/Competition/Details?competitionId=17007&seasonId=97'
        if str_5 == 'divisao2_17_18':
            header = '<b><a style="color: #006699">Classificação:</a></b> Competições FPF > Júniores > 2ª Divisão 2017/18<hr><br>'
            url_comp = 'https://resultados.fpf.pt/Competition/Details?competitionId=17016&seasonId=97'
        if str_5 == 'divisao1_18_19':
            header = '<b><a style="color: #006699">Classificação:</a></b> Competições FPF > Júniores > 1ª Divisão 2018/19<hr><br>'
            url_comp = 'https://resultados.fpf.pt/Competition/Details?competitionId=17007&seasonId=98'
        if str_5 == 'divisao2_18_19':
            header = '<b><a style="color: #006699">Classificação:</a></b> Competições FPF > Júniores > 2ª Divisão 2018/19<hr><br>'
            url_comp = 'https://resultados.fpf.pt/Competition/Details?competitionId=17016&seasonId=98'                        
        if str_1 == 'comp_fpf' and str_2 == 'juvenis':
            header = '<b><a style="color: #006699">Classificação:</a></b> Competições FPF > Juvenis<hr><br>'
            url_comp = 'https://resultados.fpf.pt/Competition/Details?competitionId=17017&seasonId=98'
        if str_1 == 'comp_fpf' and str_2 == 'iniciados':
            header = '<b><a style="color: #006699">Classificação:</a></b> Competições FPF > Iniciados<hr><br>'
            url_comp = 'https://resultados.fpf.pt/Competition/Details?competitionId=17022&seasonId=98'

        req = requests.get(url_comp)

        if req.status_code == 200:
            print('Requisição bem sucedida!')
            content = req.content

        soup = BeautifulSoup(content, 'html.parser')

        classification_table = soup.find_all(name='div', attrs={'class':'game classification no-gutters'})
        equipas = []
        jogos = []
        posicoes = []
        vitorias = []
        empates = []
        derrotas = []
        golos_marcados = []
        golos_sofridos = []
        pontuacao = []
        for linha in classification_table:
            str_equipas = linha.contents[3]
            equipas.append(str_equipas)
            str_jogos = linha.contents[5]
            jogos.append(str_jogos)
            str_posicoes = linha.contents[1]
            str_posicoes = str(str_posicoes).replace('<div class="col-md-1 col-sm-1 col-xs-1 text-left no-padding"><span>', '')
            str_posicoes = str(str_posicoes).replace('</span></div>', '')
            posicoes.append(str_posicoes) 
            str_vitorias = linha.contents[7]
            vitorias.append(str_vitorias)        
            str_empates = linha.contents[9]
            empates.append(str_empates)  
            str_derrotas = linha.contents[11]
            derrotas.append(str_derrotas)  
            str_golos_marcados = linha.contents[13]
            golos_marcados.append(str_golos_marcados)  
            str_golos_sofridos = linha.contents[15]
            golos_sofridos.append(str_golos_sofridos)  
            str_pontuacao = linha.contents[17]
            pontuacao.append(str_pontuacao)                  

        try:
            a = {'Equipas': equipas}
            classif_table_final = pd.DataFrame(data=a)
            classif_table_final['Equipas'] = classif_table_final['Equipas'].str.join(', ')  
            classif_table_final.insert(0, 'POS', posicoes)
            classif_table_final.insert(2, 'JGS', jogos)   
            classif_table_final['JGS'] = classif_table_final['JGS'].str.join(', ')     
            classif_table_final.insert(3, 'V', vitorias)
            classif_table_final['V'] = classif_table_final['V'].str.join(', ') 
            classif_table_final.insert(4, 'E', empates)
            classif_table_final['E'] = classif_table_final['E'].str.join(', ') 
            classif_table_final.insert(5, 'D', derrotas)   
            classif_table_final['D'] = classif_table_final['D'].str.join(', ')  
            classif_table_final.insert(6, 'GM', golos_marcados)  
            classif_table_final['GM'] = classif_table_final['GM'].str.join(', ')   
            classif_table_final.insert(7, 'GS', golos_sofridos) 
            classif_table_final['GS'] = classif_table_final['GS'].str.join(', ') 
            classif_table_final.insert(8, 'PTS', pontuacao)  
            classif_table_final['PTS'] = classif_table_final['PTS'].str.join(', ')    
        except:
            data = 'Não existem dados para esta competição ou a competição que selecionou é uma Taça.'  
        
        if str_5 is not None: 
            data = '<style>table {border-collapse: collapse;width:100%;font-size:11px}th, td {padding: 8px;text-align: left;border-bottom: 1px solid #ddd;} tr:hover{background-color:#f5f5f5;}</style><table><tr><td style="border-style: none;" colspan="9"><a style="color: #006699"><b>Outra fase</b></a></td><tr style="background-color: #006699;color:white;height:30px;"><td><b>POS</b></td><td><b>Equipas</b></td><td><b>JGS</b></td><td><b>V</b></td><td><b>E</b></td><td><b>D</b></td><td><b>GM</b></td><td><b>GS</b></td><td><b>PTS</b></td></tr>' #+ '<br>'
        else:
            data = '<style>table {border-collapse: collapse;width:100%;font-size:11px}th, td {padding: 8px;text-align: left;border-bottom: 1px solid #ddd;} tr:hover{background-color:#f5f5f5;}</style><table><tr><td style="border-style: none;" colspan="9"><a style="color: #006699"><b>&#9917; FASE FINAL</b></a></td><tr style="background-color: #006699;color:white;height:30px;"><td><b>POS</b></td><td><b>Equipas</b></td><td><b>JGS</b></td><td><b>V</b></td><td><b>E</b></td><td><b>D</b></td><td><b>GM</b></td><td><b>GS</b></td><td><b>PTS</b></td></tr>' #+ '<br>'
  
        for linha in classif_table_final.index:
            if classif_table_final['POS'][linha] == '1' and linha != 0:
                data = data + '<tr><td style="border-style: none; height: 50px;" colspan="9"></td></tr><tr><td style="border-style: none;" colspan="9"><a style="color: #006699"><b>Outra fase</b></a></td></tr><tr style="background-color: #006699;color:white;height:30px;"><td><b>POS</b></td><td><b>Equipas</b></td><td><b>JGS</b></td><td><b>V</b></td><td><b>E</b></td><td><b>D</b></td><td><b>GM</b></td><td><b>GS</b></td><td><b>PTS</b></td></tr><tr><td>' + classif_table_final['POS'][linha] + '</td><td>' + classif_table_final['Equipas'][linha] + '</td><td>' + classif_table_final['JGS'][linha] + '</td><td>' + classif_table_final['V'][linha] + '</td><td>' + classif_table_final['E'][linha] + '</td><td>' + classif_table_final['D'][linha] + '</td><td>' + classif_table_final['GM'][linha] + '</td><td>' + classif_table_final['GS'][linha] + '</td><td>' + classif_table_final['PTS'][linha] + '</td></tr>'
            else:
                data = data + '<tr><td>' + classif_table_final['POS'][linha] + '</td><td>' + classif_table_final['Equipas'][linha] + '</td><td>' + classif_table_final['JGS'][linha] + '</td><td>' + classif_table_final['V'][linha] + '</td><td>' + classif_table_final['E'][linha] + '</td><td>' + classif_table_final['D'][linha] + '</td><td>' + classif_table_final['GM'][linha] + '</td><td>' + classif_table_final['GS'][linha] + '</td><td>' + classif_table_final['PTS'][linha] + '</td></tr>'
  
        try:
            classif_table_final.set_index('POS', inplace=True)
            classif_table_final = classif_table_final.rename_axis(None)
        except:
            data = 'Não existem dados para esta competição ou a competição que selecionou é uma Taça.'


        data = data + '</table>' + '<br><input type="button" value="Voltar" onclick="history.back()">' 

        if str_5 is not None: 
            data = data.replace("Outra fase", '<a style="color: #006699">&#9917; FASE FINAL</a>', 3)
            data = data.replace('<a style="color: #006699">&#9917; FASE FINAL</a>', "Outra fase", 2)

    if str_1 is None:
        subsearch = ''
    
    if div_table == []:
        search = ''
        subsearch = ''
        data = 'Não existem dados ou não existe campeonato de <b>%s</b> na <b>%s</b>.<br><br><input type="button" value="Voltar" onclick="history.back()">'%(str_campeonato, ASSOCIACAO_EXTENSO[str_af])
    


    end_time = time()
    print('Tempo para carregar a página: %s segundos' %(round(end_time-start_time, 3)))
    return render(request, 'home.html', {'header':header, 'subsearch':subsearch, 'search':search, 'data':data})
