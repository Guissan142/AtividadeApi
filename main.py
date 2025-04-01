import requests
import os
from concurrent.futures import ThreadPoolExecutor

nomeFilme = input("Titulo do Filme em inglês: ") #Solicita o nome do filme ao usuário
anoFilme = input("Ano de Lançamento: ") #Solicita o ano do filme ao usuário

def requereReviews(anoFilme, nomeFilme):
    busca = f"https://api.themoviedb.org/3/search/movie?query={nomeFilme}&primary_release_year={anoFilme}" #URL de busca no TMDB
    cabecalho = { 
        "authorization": f"Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyYThlYzEzZDgwNGQwNjE1MTU0NmQwMjI3ZTliMGNlOSIsIm5iZiI6MTc0MzM4NDQ1MC41NzIsInN1YiI6IjY3ZTllZjgyNzAwYTZhOTRjNmU1NzAxMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VICAR9c8iRt-dXVmlzCqM28okiHrceFwRCYRXS5trC8",  # Substitua pelo seu token
        "accept": "application/json"
    } #Cabeçalho de busca no TMDB
    buscaFilme = requests.get(busca, headers=cabecalho) #Comando de busca do filme
    if buscaFilme.status_code == 200: #Checa se resultado é positivo
        filme = buscaFilme.json().get("results") #Retira as informações do JSON recebido anteriormente
        id = filme[0]["id"] #Recebe ID do filme para busca seguinte
        buscaReview = f"https://api.themoviedb.org/3/movie/{id}/reviews?language=pt-BR" #Busca as reviews baseado no filme que foi buscado anteriormente
        reviews = requests.get(buscaReview, headers=cabecalho) #Comando de busca para as reviews
        if reviews.status_code == 200: #Checa se resultado é positivo
            resultados = reviews.json().get("results", []) #Recebe os resultados do segundo JSON de busca
            texto = "" #Variável para alocação das reviews
            for i, review in enumerate(resultados[:3]):  # Limita às 3 primeiras resenhas
                conteudo = review.get("content") #Recebe o conteúdo da review
                texto += f"\nReview {i + 1} - \n{conteudo}" #Aloca na variável
            return texto #Retorna texto com as reviews
        else:
            return "Não foi possível obter review do TMDB." #Erro caso não seja possível obter as reviews
    else:
        return "Não foi possível encontrar o filme do TMDB." #Erro caso não seja possível obter o filme
def requereSinopse(anoFilme, nomeFilme): 
    chaveOmdb = "3ab81189" #Declaração da chave do OMDB
    requisicao = f"http://www.omdbapi.com/?apikey={chaveOmdb}&t={nomeFilme}&y={anoFilme}" #URL de busca no OMDB
    resposta = requests.get(requisicao) #Recebe o resultado da busca anterior

    if resposta.json().get("Plot") == "N/A": 
        return {"Não foi possível encontrar o filme solicitado"} #Retorna erro caso não seja encontrado os dados do filme
    else:
        sinopse = resposta.json().get("Plot") #Retira dados do JSON buscado
        return sinopse #retorna dados da sinopse

with ThreadPoolExecutor() as executaThread: #Executa as threads para fazer as solicitações em paralelo
    threadOMDB = executaThread.submit(requereSinopse, anoFilme, nomeFilme) #Thread que busca os dados do OMDB
    threadTMDB = executaThread.submit(requereReviews, anoFilme, nomeFilme) #Thread que busca os dados do TMDB
    resultadoSinopse = threadOMDB.result() #Recebe resultado sinopse
    resultadoReviews = threadTMDB.result() #Recebe resultado review

print("\nFilme:", nomeFilme) #Printa nome do filme
print("\nLançamento:", anoFilme) #Printa ano do filme
print("\nSinopse:", resultadoSinopse) #Printa Sinopses
print("\nReviews:",resultadoReviews) #Printa Reviews
