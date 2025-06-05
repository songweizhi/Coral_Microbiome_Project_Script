
rarefaction curve ([script and example input files](Rarefaction))
---

+ To get the rarefaction curve, get the input files ready, update the five lines at the bottom of `rarefaction.py` and run:

      python3 rarefaction.py

![figure](Rarefaction/output_folder/Coral_Water_Sediment_rarefaction.jpg)


community composition (Stacked_bar_plot) ([script and example input files](community_composition))
---

    python3 Stacked_bar_plot.py -m metadata.txt -otu OTU_Table.txt -otu_c OTU_Taxa.txt -w 12 -hr "sc,o,f" -mr "d" -o Coral_community_composition.pdf -sample interested_sample.txt

![figure](community_composition/Coral_community_composition.jpg)


NMDS ([script and example input files](NMDS))
---

+ To get the NMDS plot , get the input files ready, update the lines at the bottom of `NMDS.py` and run:

      python3 NMDS.py

![figure](NMDS/output_folder/NMDS_by_coral_family_nmds_genus_level.jpg)


pheatmapASV ([script and example input files](pheatmapASV))
---



