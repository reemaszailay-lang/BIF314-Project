#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install biopython requests pandas')


# In[2]:


from Bio import Entrez
from Bio import SeqIO
from io import StringIO
import requests

Entrez.email ="446005500@pnu.edu.sa"

acc_number = input("Enter Accession Number: ")

handle = Entrez.efetch(
    db="nucleotide",
    id=acc_number,
    rettype="fasta",
    retmode="text"
)

fasta_data = handle.read()
handle.close()

record = SeqIO.read(StringIO(fasta_data), "fasta")

description = record.description
sequence = str(record.seq)

parts = description.split()

if len(parts) >= 3:
    scientific_name = f"{parts[1]} {parts[2]}"
else:
    scientific_name = "Unknown"

print("Scientific Name:", scientific_name)
print("Sequence Length:", len(sequence), "bp")


# In[3]:


inat_url = f"https://api.inaturalist.org/v1/taxa?q={scientific_name}&per_page=1"

response = requests.get(inat_url).json()

results = response.get("results", [])

if results:

    taxon = results[0]

    common_name = taxon.get(
        "preferred_common_name",
        "Not Available"
    )

    print("Common Name:", common_name)

    if taxon.get("default_photo"):

        image_url = taxon["default_photo"]["medium_url"]

        print("Image URL:")
        print(image_url)

else:
    print("No data found")


# In[4]:


gbif_url = f"https://api.gbif.org/v1/species/match?name={scientific_name}"

gbif_data = requests.get(gbif_url).json()

species_key = gbif_data.get("speciesKey")

countries = []

if species_key:

    occ_url = (
        f"https://api.gbif.org/v1/occurrence/search"
        f"?speciesKey={species_key}&limit=50"
    )

    occ_data = requests.get(occ_url).json()

    for item in occ_data.get("results", []):

        country = item.get("country")

        if country and country not in countries:
            countries.append(country)

print("Distribution Countries:")

for country in countries[:10]:
    print("-", country)


# In[5]:


gc_count = sequence.count("G") + sequence.count("C")

gc_percent = (gc_count / len(sequence)) * 100

print("GC Content:", round(gc_percent, 2), "%")


# In[ ]:




