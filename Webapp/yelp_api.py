import json
import requests

def get_photos(bus_id):
    client_id = "RadFTkw0aERI-H5eYBQvHw"
    api_key = "nUfx8O-TF1h1Qm_qA-gYA1AT5KO-vdRvyNsiJFOFELDO-ovFz3MSL36oJNK41-CEkBocBEy8tHDOdInA1n-5KbFPvIkYZ_mapHHpCt9r0xrQeYDeE6i0xFzzt06IXnYx"
    headers = {'Authorization': 'Bearer %s' % api_key}
    url='https://api.yelp.com/v3/businesses/'
    req=requests.get(url+bus_id, headers=headers)
    return json.loads(req.text)["photos"]

bus_id = 'QXAEGFB4oINsVuTFxEYKFQ'
print(get_photos(bus_id))
