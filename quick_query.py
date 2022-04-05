#
# Allows query of the Materials Project Database by Atomic Species
# Searches for all variable atoms combined with specific family atom (loops over family)
# Returns a csv will all compatible materials (point group to distinguish between ==
# formula)
#

import os
import json
import requests
import pandas as pd


def makeQuery(apikey, variable, fixed):
"""
Make a Query to the API
Return result of query, for additional properties add to the list properties
within the data dictionary
"""

   data = {
      'criteria': {
         'elements':{'$in': variable, '$all': fixed},
         'nelements': 2,
      },
      'properties': [
         'pretty_formula',
         'material_id',
         'spacegroup'
      ]
   }

   r = requests.post('https://materialsproject.org/rest/v2/query',
                      headers={'X-API-KEY': apikey},
                      data={k: json.dumps(v) for k, v in data.items()})

   return(r)

def getIdsFromQuery(r):
"""
Seperate out all the properties in the request
"""
   ids = []

   for result in r.json()["response"]:

      tag = result["pretty_formula"] + "_" + result["spacegroup"]["symbol"].replace('/','|')
      i   = result["material_id"]
      ids.append( { "Material ID" : i, 
                    "Formula"     : result["pretty_formula"], 
                    "Point Group" : result["spacegroup"]["symbol"],
                    "Path"        : tag
                   } )

   return(ids)

if __name__ == "__main__":

   key = 

   scan = ['Li', 'Na', 'K', 'Rb', 'Cs']
   family = ['O']

   try:
      df = pd.read_csv("materials_project.csv")

   except:
      d = {'Material ID':[], 'Formula':[], 'Point Group': [], 'Path': []} 
      df = pd.DataFrame(data=d)

   matIds = []

   for f in family:   
      compounds = makeQuery(key, scan, [f])
      matIds = matIds + getIdsFromQuery(compounds)

   for matId in matIds:

      df.loc[df.shape[0]] = matId

   df.to_csv("materials_project.csv", index=False)
