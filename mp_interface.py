
#
# Interface to the Materials Project API
#

import requests

def get_url(m_id, key, feature='structure'):
   url = "https://legacy.materialsproject.org/rest/v2/tasks/{m_id}/{feature}?API_KEY={key}"
   url = url.format(m_id = m_id, key = key, feature=feature)

   print(url)

   return(url)

def get_json(url):
   response = requests.get(url).json()["response"][0]
   
   return(response)   

def print_summary(crystal, ibrav):
   print("Crystal System:", crystal)
   print("ibrav:", ibrav)

   return()
