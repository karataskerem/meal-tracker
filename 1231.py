import requests


def list_food(name):
    resp = requests.get(("https://api.nal.usda.gov/fdc/v1/foods/search"), params ={"query": name,
        "dataType": "Foundation, SR Legacy",
        "api_key": "DHRgIZAz6E8mHDFVsL6FS2IN77MMv4SCliveAPWr"}).json()

    for i,e in zip(range(10), resp["foods"]):
        print(i, e["description"])

    usr_inp = int(input("Please pick the most suitable one: "))


    for e in resp["foods"][usr_inp]["foodNutrients"]:
        if e["nutrientId"] in (1003,1004,1005):
            if e["nutrientId"] == 1003:
                protein = e["value"]
                continue
            if e["nutrientId"] == 1004:
                fat = e["value"]
                continue
            if e["nutrientId"] == 1005:
                carb = e["value"]
    return (protein,carb,fat)




    



        
print(list_food("chicken breast"))

