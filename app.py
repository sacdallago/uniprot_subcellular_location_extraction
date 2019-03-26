import os
import re
import pandas as pd
from extractor import extract_locations_from_URL
from flask import Flask, request, abort

app = Flask(__name__)

# Check if cache file exists. If not, create it:
if os.path.isfile("cache"):
    print("Cache exists: loading...")
    cache = pd.read_csv("cache", sep="\t")
else:
    print("Cache doesn't exists: creating...")
    cache = extract_locations_from_URL()
    cache.to_csv("cache", sep='\t', index=False)

print("Cache loaded.")

UNIPROT_AC_REGEX = re.compile("[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}")

@app.route('/')
def get_location():
    query = request.args.get('q')

    if query:
        if UNIPROT_AC_REGEX.match(query):
            cache_results = cache[cache['accession'] == query]

            if cache_results.empty:
                results = extract_locations_from_URL("https://www.uniprot.org/uniprot/{}.xml".format(query))
                return results.to_json(orient="records")
            else:
                return cache_results.to_json(orient="records")
        else:
            abort(400)

    else:
        return cache.to_json(orient="records")
