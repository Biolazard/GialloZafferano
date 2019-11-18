import requests
import urllib.request
from bs4 import BeautifulSoup
import re
import string
from string import digits
import json

#Prendere categoria ricetta
#Andare a vedere anche ricette su altri siti


def saveRecipe(linkRecipeToDownload):
    soup = downloadPage(linkRecipeToDownload)
    titleRecipe = findTitle(soup)
    Ingredients = findIngredients(soup)
    Description = findDescription(soup)
    recipe = {"titleRecipe": titleRecipe, "ingredients": Ingredients, "description": Description}
    createFileJson(recipe, titleRecipe)
 
def findTitle(soup):
    titleRecipe = ""
    for title in soup.find_all(attrs={'class' : 'gz-title-recipe gz-mBottom2x'}):
        titleRecipe = title.text
    return titleRecipe

def findIngredients(soup):
    allIngredients = []
    for tag in soup.find_all(attrs={'class' : 'gz-ingredient'}):
        link = tag.a.get('href')
        nameIngredient = tag.a.string
        contents = tag.span.contents[0]
        quantityProduct = re.sub(r"\s+", " ",  contents).strip()
        allIngredients.append([nameIngredient, quantityProduct])
    return allIngredients

def findDescription(soup):
    allDescription = ""
    for tag in soup.find_all(attrs={'class' : 'gz-content-recipe-step'}):
        removeNumbers = str.maketrans('', '', digits)
        description = tag.p.text.translate(removeNumbers)
        allDescription =  allDescription + description
    return allDescription
        
def createFileJson(recipes, name):
    with open(name + '.txt', 'w') as file:
     file.write(json.dumps(recipes, ensure_ascii=False))
    
def downloadPage(linkToDownload):
    response = requests.get(linkToDownload)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def downloadAllRecipesFromGialloZafferano():
    for pageNumber in range(1,countTotalPages() + 1):
        linkList = 'https://www.giallozafferano.it/ricette-cat/page' + str(pageNumber)
        response = requests.get(linkList)
        soup= BeautifulSoup(response.text, 'html.parser')
        
        for tag in soup.find_all(attrs={'class' : 'gz-title'}):
            link = tag.a.get('href')
            saveRecipe(link)
        for tag in soup.find_all(attrs={'class' : 'gz-breadcrumb'}):
            category = tag.a.get('href')
            print("hello")
            print(category)
        
        break
    
def countTotalPages():
    numberOfPages = 0
    linkList = 'https://www.giallozafferano.it/ricette-cat'
    response = requests.get(linkList)
    soup= BeautifulSoup(response.text, 'html.parser')
    for tag in soup.find_all(attrs={'class' : 'disabled total-pages'}):
        numberOfPages = int(tag.text)
    return numberOfPages
        
if __name__ == '__main__' :
    downloadAllRecipesFromGialloZafferano()

