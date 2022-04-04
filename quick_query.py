
import json
import requests

if __name__ == "__main__":

   data = {
      'criteria': {
         'elements':{'$in': ['Li', 'Na', 'K', 'Rb', 'Cs'], '$all': ['Cl']},
         'nelements': 2,
      }
      'properties': [
         'formula'
      ]
   }

   r = requests.post('https://materialsproject.org/rest/v2/query',
                      headers={'X-API-KEY':},
                      data={k: json.dumps(v) for k, v in data.items()})

   response_content = r.json()

