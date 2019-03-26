import pandas as pd
import xml.etree.ElementTree as ET
from urllib.request import urlopen


def extract_locations_from_URL(url="https://www.uniprot.org/uniprot/?query=*&format=xml"
                                   "&fil=organism:%22Homo%20sapiens%20(Human)%20[9606]%22%20AND%20reviewed:yes"):
    namespaces = {
        'd': 'http://uniprot.org/uniprot',
    }

    tree = ET.parse(urlopen(url))
    root = tree.getroot()
    locations_list = list()

    for protein in root.findall('d:entry', namespaces=namespaces):
        accession = protein.find('d:accession', namespaces=namespaces).text
        comments = protein.findall('d:comment[@type="subcellular location"]', namespaces=namespaces)

        for sub_cell_loc_comment in comments:
            subcellularLocations = sub_cell_loc_comment.findall('d:subcellularLocation', namespaces=namespaces)

            for subcellularLocation in subcellularLocations:
                location = subcellularLocation.find('d:location', namespaces=namespaces)
                location_text = location.text
                evidences = location.get('evidence')

                if evidences:
                    for evidence in evidences.split(' '):
                        current_evidence = protein.find('d:evidence[@key="{}"]'.format(evidence), namespaces=namespaces)
                        locations_list.append([accession, current_evidence.get('type'), location_text])
                else:
                    locations_list.append([accession, None, location_text])

    return pd.DataFrame(locations_list, columns=['accession', 'evidence', 'location']).drop_duplicates()
