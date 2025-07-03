#!/bin/usr/env python

import logging
import time
import sys
from melodies_monet import driver 
import monetio as mio

# configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(config_file, species, model_type):
    # start time
    start_time = time.time()

    logging.info('Starting Script...')

    print(mio.__file__)

    an = driver.analysis()

    logging.info(f"Reading Control File: {config_file}")
    an.control = config_file
    an.read_control()

    logging.info('Opening Models!')
    an.open_models()
    if model_type == 'cesm_fv':
        ds = an.models['cesm_fv'].obj
    elif model_type == 'wrfchem':
        ds = an.models['wrfchem_v4.2'].obj
    else:
        logging.error(f"Unsupported model type: {model_type}")
        sys.exit(1)
   

    logging.info('Opening Observations!')
    an.open_obs()
    if species == 'tempo_l2_no2':
        ds_obs = an.obs['tempo_l2_no2'].obj
    elif species == 'tempo_l2_hcho':
        ds_obs = an.obs['tempo_l2_hcho'].obj
    else:
        logging.error(f"Unsupported species: {species}")
        sys.exit(1)

    logging.info('Pairing Data!')
    an.pair_data()

    logging.info('Saving Analysis!')
    an.save_analysis()

    logging.info('Reading Control File Again!')
    an.read_control()

    logging.info('Plotting Results!')
    an.plotting()

    # End time
    end_time = time.time()
    elapsed_time = end_time - start_time

    logging.info(f'Script Finished in {elapsed_time:.2f} Seconds!')

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python pair_tempo_model.py <config_file> <species> <model_type>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
