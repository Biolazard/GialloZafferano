import requests
import urllib.request
from bs4 import BeautifulSoup
import re
import string
from string import digits
import json
from ModelRecipe import ModelRecipe
import os
import base64

debug = False

def saveRecipe(linkRecipeToDownload):
    soup = downloadPage(linkRecipeToDownload)
    title = findTitle(soup)
    ingredients = findIngredients(soup)
    description = findDescription(soup)
    category = findCategory(soup)
    imageBase64 = findImage(soup)

    modelRecipe = ModelRecipe()
    modelRecipe.title = title
    modelRecipe.ingredients = ingredients
    modelRecipe.description = description
    modelRecipe.category = category
    modelRecipe.imageBase64 = imageBase64

    createFileJson(modelRecipe.toDictionary(), modelRecipe.title)

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

def findCategory(soup):
    for tag in soup.find_all(attrs={'class' : 'gz-breadcrumb'}):
        category = tag.li.a.string
        return category

def findImage(soup):

    # Find the first picture tag
    pictures = soup.find('picture', attrs={'class': 'gz-featured-image'})

    # Fallback: find a div with class `gz-featured-image-video gz-type-photo`
    if pictures is None:
        pictures = soup.find('div', attrs={'class': 'gz-featured-image-video gz-type-photo'})

    imageSource = pictures.find('img')

    # Most of the times the url is in the `data-src` attribute
    imageURL = imageSource.get('data-src')

    # Fallback: if not found in `data-src` look for the `src` attr
    # Most likely, recipes which have the `src` attr
    # instead of the `data-src` one
    # are the older ones.
    # As a matter of fact, those are the ones enclosed
    # in <div> tags instead of <picture> tags (supported only on html5 and onward)
    if imageURL is None:
        imageURL = imageSource.get('src')

    imageToBase64 = str(base64.b64encode(requests.get(imageURL).content))
    imageToBase64 = imageToBase64[2:len(imageToBase64) - 1]
    return imageToBase64

def createFileJson(recipes, name):
    compact_name = name.replace(" ", "_").lower()
    folderRecipes = "Recipes"
    if not os.path.exists(folderRecipes):
        os.makedirs(folderRecipes)
    with open(folderRecipes + '/' + compact_name + '.json', 'w') as file:
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
            if debug :
                break

        if debug :
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
