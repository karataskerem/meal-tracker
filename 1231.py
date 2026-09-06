import requests


def get_foodx(name):
    resp = requests.get(("https://api.nal.usda.gov/fdc/v1/foods/search"), params ={"query": name,
        "dataType": "Foundation,SR Legacy",
        "api_key": "DHRgIZAz6E8mHDFVsL6FS2IN77MMv4SCliveAPWr"}).json()








        











