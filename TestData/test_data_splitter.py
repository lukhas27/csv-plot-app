import os
import shutil

CURRENT_DATA_SET = 0

cur_dir = os.curdir
files = os.listdir(cur_dir)

csv_files = list()

for file in files:
    if file.endswith('.csv'):
        csv_files.append(file)

for file in csv_files:
    direction = file.split('_')[2].split('.')[0]
    target_folder = cur_dir + os.path.sep + direction
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    os.rename(file, cur_dir + os.path.sep + target_folder + os.path.sep + str(CURRENT_DATA_SET) + '_' + file)
