#!/usr/bin/env python

from ruamel.yaml import YAML    # offers full format preservation
from datetime import datetime, timedelta

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)

#-- USER MODIFICATIONS

# specify species and model type
species = 'no2'     # 'no2' or 'hcho'
model_type = 'cesm_fv'   # 'cesm_fv' or 'wrf' are the only tested options for now
default_config_file = f"/glade/u/home/nmariscal/melodies-monet/yaml/control_tempo_l2_{species}_{model_type}.yaml"

# specify date parameters
start_date = datetime(2024, 7, 1)   # first day to process
num_days = 5                       # number of days to process (consecutive)

# paths to paired output directory (should be the same for all files)
# !!! needs to be created before running this script !!!
output_dir_pathname = '/glade/derecho/scratch/nmariscal/tempo_files/cesm-fv/202407/'

# path to TEMPO data
obs_path = '/glade/campaign/acom/acom-da/sma/TEMPO_HCHO_V03'

# path to model data
model_path = '/glade/derecho/scratch/gaubert/tempo/merge'
model_file = 'f.e22.FCnudged.ne0CONUSne30x8_ne0CONUSne30x8_mt12.musica_cams_mosaic.003.cam.h1'

# needs to be created before running this script
save_filepath = '/glade/u/home/nmariscal/melodies-monet/yaml/tests'

#-- END USER MODIFICATIONS

#-- load original configuration file
with open(default_config_file, 'r') as file:
    # config = yaml.safe_load(file)
    config = yaml.load(file)

#-- generate configuration files for each day
for day_offset in range(num_days):
    current_date = start_date + timedelta(days=day_offset)
    prev_date = current_date - timedelta(days=1)
    next_date = current_date + timedelta(days=1)    # get datetime object first 

    # deep copy to preserve original structure of yaml
    # new_config = copy.deepcopy(config)
    new_config = config

    # format dates for different requirements in yaml
    ymd_current_format = current_date.strftime('%Y%m%d')    # YYYYMMDD
    iso_current_format = current_date.strftime('%Y-%m-%d')  # YYYY-MM-DD
    iso_prev_format = prev_date.strftime('%Y-%m-%d')
    iso_next_format = next_date.strftime('%Y-%m-%d')       

    # update 'analysis' section
    new_config['analysis']['start_time'] = iso_current_format
    new_config['analysis']['end_time'] = iso_next_format
    new_config['analysis']['save']['paired']['prefix'] = ymd_current_format
    new_config['analysis']['output_dir'] = output_dir_pathname  
    new_config['analysis']['output_dir_read'] = output_dir_pathname

    # update 'obs' section
    if species == 'no2':
        tempo_l2_key = 'tempo_l2_no2'
        tempo_l2_obs_name = 'TEMPO_NO2_L2_V03'
    elif species == 'hcho': 
        tempo_l2_key = 'tempo_l2_hcho'
        tempo_l2_obs_name = 'TEMPO_HCHO_L2_V03'
    else:
        raise ValueError("Species must be either 'no2' or 'hcho'.")
    new_config['obs'][tempo_l2_key]['filename'] = f"{obs_path}/{tempo_l2_obs_name}_{ymd_current_format}*_S*"

    # update 'model' section
    new_config['model'][model_type]['files'] = \
        f'{model_path}/{model_file}.{iso_prev_format}-*.nc', \
        f'{model_path}/{model_file}.{iso_current_format}-*.nc'
     
    #-- save new configuration file
    save_filename = f"{save_filepath}/control_{tempo_l2_key}_{model_type}_{ymd_current_format}.yaml"
    with open(save_filename, 'w') as file:
        yaml.dump(new_config, file,
                #   default_flow_style=False,
                #   sort_keys=False,   # preserves original key order
                #   allow_unicode=True
                  )

print(f"Configuration files generated for {num_days} days starting from {start_date}!")
