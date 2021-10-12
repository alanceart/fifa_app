import streamlit as stm
import pandas as pd # our main data management package
import matplotlib.pyplot as plt # our main display package
import numpy as np # used for managing NaNs
import seaborn as sns
import scipy.stats as st
import matplotlib as mpl
mpl.style.use('seaborn')
import requests
from bs4 import BeautifulSoup
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import math

#Infos scraping

alexandre = "https://proclubshead.com/22/club/pc-69685/player/Lanceou/form-league/"
rachel = "https://proclubshead.com/22/club/pc-69685/player/RachelLaFleur/form-league/"
pierre = "https://proclubshead.com/22/club/pc-69685/player/Sandishh/form-league/"
#jose = "https://proclubshead.com/22/club/ps5-12599/player/sofiane02100/form-league/"
paul = "https://proclubshead.com/22/club/pc-69685/player/SensualBoromir/form-league/"
baptiste = "https://proclubshead.com/22/club/pc-69685/player/eirneken47/form-league/"
romain = "https://proclubshead.com/22/club/pc-69685/player/FCPortoFR76/form-league/"

club = "https://proclubshead.com/22/club/pc-69685/"
match_club = "https://proclubshead.com/22/club/pc-69685/matches-league/"

#comptes = [rachel,alexandre,pierre]
#header = ["Rachel","Alexandre","Pierre"]
header_but = ["Buts Alexandre", "Buts Rachel", "Buts Pierre", "Buts Baptiste", "Buts Romain","Buts Paul"]
header_pd = ["Pd Alexandre", "Pd Rachel", "Pd Pierre", "Pd Baptiste", "Pd Romain", "Pd Paul"]
comptes = [alexandre,rachel,pierre,baptiste,romain,paul]
header = ["Alexandre","Rachel","Pierre","Baptiste","Romain","Paul"]


nb_match_joues = stm.slider('Nombre de matchs', 5, 10, 10, 1)


#Récupération note joueurs
liste_note = []
j=0
for i in comptes :
    r = requests.get(i)
    c = r.content
    soup = BeautifulSoup(c,)
    note_joueur = []
    compteur = 1
    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        if compteur <= nb_match_joues:
            val = row.findAll('td')[1].text
            note_joueur.insert(0,val)
        compteur = compteur + 1
    liste_note.append(note_joueur)
    j=j+1

liste_note = np.asarray(liste_note)
liste_note[liste_note == '--'] = '-1'

long = liste_note.shape[1]
match = []
for i in range(1,long+1):
    val = "M" + str(i)
    match.append(val)

df_note=pd.DataFrame(liste_note, columns=match) 
df_note.index = header
df_note = df_note.T
df_note = df_note.apply(pd.to_numeric)
df_note[df_note == -1] = None

liste_but = []
liste_pd = []
j=0
for i in comptes :
    r = requests.get(i)
    c = r.content
    soup = BeautifulSoup(c,)
    but_joueur = []
    pd_joueur = []
    compteur = 1
    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        if compteur <= nb_match_joues:
            val_but = row.findAll('td')[3].text
            but_joueur.insert(0,val_but)
            val_pd = row.findAll('td')[6].text
            pd_joueur.insert(0,val_pd)
        compteur = compteur + 1
    liste_but.append(but_joueur)
    liste_pd.append(pd_joueur)
    j=j+1

liste_but = np.asarray(liste_but)
liste_but[liste_but == '--'] = '-1'
liste_pd = np.asarray(liste_pd)
liste_pd[liste_pd == '--'] = '-1'

df_but=pd.DataFrame(liste_but, columns=match) 
df_but.index = header
df_but = df_but.T
df_but = df_but.apply(pd.to_numeric)
df_but[df_but == -1] = None

df_pd=pd.DataFrame(liste_pd, columns=match) 
df_pd.index = header
df_pd = df_pd.T
df_pd = df_pd.apply(pd.to_numeric)
df_pd[df_pd == -1] = None

#Récupérations résultats WIN/DEFAITE
r = requests.get(match_club)
c = r.content
soup = BeautifulSoup(c,)
res_equipe = []
main_content = soup.find_all('li', attrs = {'class': ['badge list-inline-item match-result me-1 px-0 text-light bg-result-win','badge list-inline-item match-result me-1 px-0 text-light bg-result-draw','badge list-inline-item match-result me-1 px-0 text-light bg-result-loss']})
for item in main_content:
    res_equipe.append(item.text)
val = nb_match_joues * -1
res_equipe = res_equipe[val:]    

#Recupération résultats score
r = requests.get(match_club)
c = r.content
soup = BeautifulSoup(c,)
score_equipe = []
main_content = soup.find_all('div', attrs = {'class': ['col-auto font-tabular-nums px-3 py-2 text-light bg-result-win','col-auto font-tabular-nums px-3 py-2 text-light bg-result-draw','col-auto font-tabular-nums px-3 py-2 text-light bg-result-loss']})
for item in main_content:
    score_equipe.insert(0,item.text)
val = nb_match_joues * -1
score_equipe = score_equipe[val:]

#Plot

fig = plt.figure()
plt.plot(df_note.index,df_note["Rachel"],linestyle='-', marker='.', markersize = 10, label="Rachel", color="pink")
plt.plot(df_note.index,df_note["Alexandre"],linestyle='-', marker='.', markersize = 10, label="Alexandre")
plt.plot(df_note.index,df_note["Pierre"],linestyle='-', marker='.', markersize = 10, label="Pierre")
plt.plot(df_note.index,df_note["Baptiste"],linestyle='-', marker='.', markersize = 10, label="Baptiste")
plt.plot(df_note.index,df_note["Romain"],linestyle='-', marker='.', markersize = 10, label="Romain")
plt.plot(df_note.index,df_note["Paul"],linestyle='-', marker='.', markersize = 10, label="Paul")

but = mpimg.imread('./Logo/but.png')
but = OffsetImage(but, zoom=0.015)
pd = mpimg.imread('./Logo/pd.png')
pd = OffsetImage(pd, zoom=0.015)


for i in range(1,nb_match_joues+1):
    nb = i-1
    val = res_equipe[nb]
    x1 = i - 1.45
    x2 = i - 0.55
    if val == "W":
         plt.axvspan(x1,x2,facecolor='green',alpha=0.3)
    if val == "D":
         plt.axvspan(x1,x2,facecolor='grey',alpha=0.3)
    if val == "L":
         plt.axvspan(x1,x2,facecolor='red',alpha=0.3)

for i in range(1,nb_match_joues+1):
        plt.text(i-1,10.5,score_equipe[i-1], color='black', bbox={'color':'white', 'edgecolor':'black','alpha':0.5,'pad':3}, ha='center', va='center')

axes = plt.gca()
axes.set_ylim([df_note.min().min()-1,10.9])   
axes.set_xlim(-0.5,nb_match_joues+nb_match_joues/7) 


nb_joueurs = len(header)

for i in range(1,nb_joueurs+1):
    note_temp = df_note[header[i-1]]
    but_temp = df_but[header[i-1]]
    pd_temp = df_pd[header[i-1]]
    for j in range(1,nb_match_joues+1):
        if not(math.isnan(note_temp[j-1])):
            note_match_j = note_temp[j-1]
            but_match_j = int(but_temp[j-1])
            pd_match_j = int(pd_temp[j-1])
            total = but_match_j + pd_match_j       
            if(total == 1):
                val_dep = j-1
            if(total == 2):
                val_dep = j-1-((nb_match_joues+1)/100)
            if(total == 3):
                val_dep = j-1-2*((nb_match_joues+1)/100)
            if(total == 4):
                val_dep = j-3*((nb_match_joues+1)/100)
            if(total == 5):
                val_dep = j-4*((nb_match_joues+1)/100)         
            if(total == 6):
                val_dep = j-5*((nb_match_joues+1)/100)
            if(total == 7):
                val_dep = j-6*((nb_match_joues+1)/100)
                
            compteur = 0
            for j in range(0,but_match_j):
                ab = AnnotationBbox(but,(val_dep+compteur, note_match_j+0.02*(10-(df_note.min().min()-1))),frameon=False)
                axes.add_artist(ab)
                compteur = compteur + 2*((nb_match_joues+1)/100)
            for j in range(0,pd_match_j):
                ab = AnnotationBbox(pd,(val_dep+compteur, note_match_j+0.02*(10-(df_note.min().min()-1))),frameon=False)
                axes.add_artist(ab)
                compteur = compteur + 2*((nb_match_joues+1)/100)

plt.grid(axis='x')
plt.legend()
plt.legend(loc=0, frameon=False,fontsize ='small')

stm.pyplot(fig)