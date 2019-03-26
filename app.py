import re
from extractor import extract_locations_from_URL
from flask import Flask, request, abort
from flask_cors import cross_origin

app = Flask(__name__)

UNIPROT_AC_REGEX = re.compile("[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}")


@app.route('/')
@cross_origin()
def get_location():
    query = request.args.get('q')

    if query:
        if UNIPROT_AC_REGEX.match(query):
            results = extract_locations_from_URL("https://www.uniprot.org/uniprot/{}.xml".format(query))
            return results.to_json(orient="records")
        else:
            abort(400)

    else:
        abort(404)


if __name__ == '__main__':
    app.run()
