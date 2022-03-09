import requests
import json
import pickle
import pandas as pd

### https://api.thedogapi.com/v1/breeds/

####################
### PET DATABASE ###
####################

### DOG MODULE ###

# practice project using the dog breed API above to parse JSON data

class Dog:
    """Extract data about each dog breed from the API.
    Feed that data into class attributes."""
    pass

def getAllData(url):
    """Download API data for all breeds. Display readable JSON and return it."""
    json_data = requests.get(url).json()  # LIST
    return json_data

def jsonToPD(json_data):
    """Convert specified file from JSON dict to Pandas dataframe."""
    df = pd.DataFrame.from_dict(json_data)
    return df

def searchForBreed(data, breed):
    """Return whole dictionary from list where 'name' value contains
    breed string."""
    if type(breed) != str:
        raise Exception('Text input only.')
    if type(data) != list:
        raise Exception('Expected list data.')

    print(f'*** Search results for breed names containing {breed} ***')
    for breed_dict in data:  # for each dictionary in the list
        for k, v in breed_dict.items():  # iterate over keys and values
            if k == 'name' and breed in v:  # if the key is 'name' and breed stris within v str
                yield breed_dict

def displayResults(search_results):
    """Print results in readable, numbered format of any generator or list."""
    for i, d in enumerate(search_results, start=1):
        print(f'{i}: {d["name"]}')
        for k, v in d.items():
            if k != 'name':
                print(f'{k.upper()}: {v}')
        print()

def getBreedImage(data, breed, file_name):
    """Download image of specified dog breed. Doesn't work properly yet."""
    # image is a dictionary within the breed dictionary
    g = searchForBreed(data, breed)  # return generator
    for d in g:
        if d['name'] == breed:
            img = requests.get(d['image']['url'])
            jpg_name = f'{file_name}.jpg'
            with open(jpg_name, 'wb') as dog:
                dog.write(img.content)
            print('Download successful!')

def getRandomDogImages(how_many):
    """Download a specified number of images, automatically numbering
    the multiple image names."""
    # get a random json list of dicts for each dog
    dogs = []
    for i in range(how_many):
        # request json data using the search API
        rand_dog = requests.get('https://api.thedogapi.com/v1/images/search').json()
        dogs.append(rand_dog)

    images = []
    for d in dogs:
        img = requests.get(d[0]['url'])
        images.append(img)

    # write image links to new files:
    count = 1
    for i in images:
        file_name = 'dog' + str(count) + '.jpg'
        with open(file_name, 'wb') as dog:
            dog.write(i.content)
            count += 1

def inputMenu():
    print('Welcome to the Dog Database.')
    print('Loading in data from API...')
    # store whole JSON data in local variable during running of program
    # to avoid making multiple API calls
    masterData = getAllData('https://api.thedogapi.com/v1/breeds/')
    print('Data successfully loaded.\n')

    while True:
        select = int(input('1) Search breed\n2) Download image of a breed\n'
                           '3) Download random dog images\n4) Exit\nEnter selection: '))

        if select == 1:
            print('### search for a breed ###')
            while True:
                chosenBreed = input('Enter what you would like to search for: ')
                print('Searching...')
                results = searchForBreed(masterData, chosenBreed.title())
                displayResults(results)
                try:
                    another = int(input('1) Search another\n2) Back to main menu\n'
                                        'Enter selection: '))
                except ValueError:
                    print('Number input only.')
                else:
                    if another == 1:
                        continue
                    elif another == 2:
                        break

        elif select == 2:
            # need to return URL of image for specified dog breed
            # above function not quite working yet
            print('Work in progress!')
            continue

        elif select == 3:
            how_many = int(input('How many images? Max 10: '))
            if how_many > 10:
                raise Exception('Maximum image download is 10.')
            getRandomDogImages(how_many)
            print('Check your hard drive to see images!')

        elif select == 4:
            print('Goodbye.')
            break

inputMenu()

###########################

def searchBreedHeight(breed):
    """Also need to return the result."""
    query_params = {'q': breed}
    endpoint = "https://api.thedogapi.com/v1/breeds/search"
    a = requests.get(endpoint, params=query_params).json()
    name = ''
    height = ''
    for d in a:
        for k, v in d.items():
            if k == 'height':
                height = v
            elif k == 'name':
                name = v
    print(f'breed: {name}, height: {height}')

# https://docs.thedogapi.com/
# searchBreedHeight('Poodle')

