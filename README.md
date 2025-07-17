This folder contains the necessary scripts for pairing model output with TEMPO NO2 and HCHO using MELODIES-MONET (https://github.com/NCAR/MELODIES-MONET). 
The purpose of creating these scripts was to be able to pair model output with TEMPO for longer periods of time. 

Note: The idea for these scripts are for them to be used with data on a structured grid (i.e., CAM-chem, regridded MUSICAv0) in order to pair with TEMPO NO2 and HCHO columns. 

For the tropospheric column calculation, in order to calculate the layer thickness (dz_m), temperature (T), surface pressure (PS), surface geopotential (PHIS), and hybrid levels at the interface (hyai, hybi) need to be provided. PHIS and T are used in the calculation of the hydrostatic height, and PS, hyai and hybi are used to calculate the pressure at the interface. If PHIS, hyai, and hybi are not included in the dataset, the dry pressure difference between levels (PDELDRY) can be used in the calculation of the layer thickness.

Contents:
    1. modify_yaml.py
    2. pair_tempo_model.py
    3. run_melodies_monet 

1. modify_yaml.py
    Used to generate YAML files for n number of days. This is based on a 'base' configuration YAML file located in the '~/pair_tempo/config' directory.
    In this python script, you are essentially making a copy of the 'base' configuration file with specific modifications to the date parameters, model and obs paths, and output directory path. 
    Note: This script can be used to modify other aspects of the YAML file to be used, it just needs to be added in. 

3. pair_tempo_model.py
    Runs all of the MELODIES-MONET commands for reading model and observational data, pairing, and plotting the data. 
    Note: If one does not want to run the an.plotting(), for example, you can simply comment out said line.

4. run_melodies_monet
    Script for running MELODIES-MONET and pairing the data for many days in a more quick way.
