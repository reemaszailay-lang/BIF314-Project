import streamlit as st
from Bio import Entrez
from Bio import SeqIO
from io import StringIO
import requests

# Page Title
st.title("NCBI Biodiversity Tool")

# Your Email
Entrez.email = "446005500@pnu.edu.sa"

# User Input
acc_number = st.text_input("Enter Accession Number")

# Analyze Button
if st.button("Analyze"):

    if acc_number:

        try:

            # NCBI Data
            handle = Entrez.efetch(
                db="nucleotide",
                id=acc_number,
                rettype="fasta",
                retmode="text"
            )

            fasta_data = handle.read()
            handle.close()

            record = SeqIO.read(
                StringIO(fasta_data),
                "fasta"
            )

            description = record.description
            sequence = str(record.seq)

            parts = description.split()

            if len(parts) >= 3:
                scientific_name = f"{parts[1]} {parts[2]}"
            else:
                scientific_name = "Unknown"

            # Display Genomic Information
            st.subheader("Genomic Information")

            st.write(
                f"Scientific Name: {scientific_name}"
            )

            st.write(
                f"Sequence Length: {len(sequence)} bp"
            )

            # GC Content
            gc_count = (
                sequence.count("G")
                + sequence.count("C")
            )

            gc_percent = (
                gc_count / len(sequence)
            ) * 100

            st.write(
                f"GC Content: {gc_percent:.2f}%"
            )

            # iNaturalist
            inat_url = (
                f"https://api.inaturalist.org/v1/taxa"
                f"?q={scientific_name}&per_page=1"
            )

            response = requests.get(
                inat_url
            ).json()

            results = response.get(
                "results",
                []
            )

            if results:

                taxon = results[0]

                common_name = taxon.get(
                    "preferred_common_name",
                    "Not Available"
                )

                st.write(
                    f"Common Name: {common_name}"
                )

                if taxon.get(
                    "default_photo"
                ):

                    image_url = taxon[
                        "default_photo"
                    ]["medium_url"]

                    st.image(
                        image_url,
                        caption=scientific_name
                    )

            # GBIF
            gbif_url = (
                f"https://api.gbif.org/v1/species/match"
                f"?name={scientific_name}"
            )

            gbif_data = requests.get(
                gbif_url
            ).json()

            species_key = gbif_data.get(
                "speciesKey"
            )

            countries = []

            if species_key:

                occ_url = (
                    f"https://api.gbif.org/v1/occurrence/search"
                    f"?speciesKey={species_key}&limit=300"
                )

                occ_data = requests.get(
                    occ_url
                ).json()

                for item in occ_data.get(
                    "results",
                    []
                ):

                    country = item.get(
                        "country"
                    )

                    if (
                        country
                        and country not in countries
                    ):
                        countries.append(
                            country
                        )

            # Distribution Section
            st.subheader(
                "Distribution Countries"
            )

            if "Saudi Arabia" in countries:
                st.success(
                    "✅ Saudi Arabia Found"
                )
            else:
                st.warning(
                    "❌ Saudi Arabia not found in retrieved GBIF records"
                )

            st.write(
                f"Total Countries Found: {len(countries)}"
            )

            for country in countries[:40]:
                st.write(
                    f"• {country}"
                )

           

        except Exception as e:

            st.error(
                f"Error: {e}"
            )
