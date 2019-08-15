# -*- coding: utf-8 -*-

###
# Graphs
###
import json
import math
from os import path, makedirs
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from consts import SUBJECTS, NAMES

FIRST_LEVEL_FOLDER = u'графіки'


def check_folders(*args):
    if not path.exists(path.join(*args)):
        makedirs(path.join(*args))


def compose_file_name(folders, name):
    names_list = folders[:]
    names_list.append(name)
    return path.join(*names_list)


def trim_extra_text(text):
    extras = (u' область', u' район')
    for e in extras:
        text = text.replace(e, '')
    return text


fig, ax = plt.subplots()


def plot_mean_by_regions(data, units_names, subj, title, file_name, reg_name=None):
    unit_marks = [(unit_name, data[unit_name][subj]) for unit_name in units_names if not math.isnan(data[unit_name][subj]) and unit_name != reg_name]
    unit_marks.sort(key=lambda x: x[1])
    if not unit_marks:
        return
    y_data, x_data = zip(*unit_marks)
    y_data = [trim_extra_text(i) for i in y_data]
    
    ax.barh(y_data, x_data)
    ax.set_title(title)

    fig.subplots_adjust(left=0.25, right=0.95, bottom=0.1, top=0.9)
    fig.savefig(file_name, dpi=200)
    plt.cla()  # we clean active axis in the current figure to reuse the fig


# read data from a json file
with open('/vagrant/ZNO/results.json') as f:
    data = json.load(f)

check_folders(FIRST_LEVEL_FOLDER)

regions = set(data.keys()).difference(SUBJECTS)
for subj in SUBJECTS:
    file_name = path.join(FIRST_LEVEL_FOLDER, '%s.png' % subj)
    # mean values for each study subject among regions
    plot_mean_by_regions(data, regions, subj, u'Середній бал з %s по областях' % NAMES[subj], file_name)
    for reg_name in regions:
        district_names = set(data[reg_name].keys()).difference(SUBJECTS)
        FOLDERS_BY_REGION = [FIRST_LEVEL_FOLDER, u'по областях', reg_name]
        check_folders(*FOLDERS_BY_REGION)
        file_name = compose_file_name(FOLDERS_BY_REGION, u'%s-%s.png' % (subj, reg_name))
        # mean values for each study subject among districts in every region
        plot_mean_by_regions(data[reg_name], district_names, subj,
            u'Середній бал з %s по районах, %s' % (NAMES[subj], reg_name),
            file_name,
            reg_name
        )
        for distr_name in district_names:
            if distr_name == reg_name:
                continue
            cities = set(data[reg_name][distr_name].keys()).difference(SUBJECTS)
            FOLDERS_BY_DISTRICT = FOLDERS_BY_REGION[:]
            FOLDERS_BY_DISTRICT.extend([u'по районах', distr_name])
            check_folders(*FOLDERS_BY_DISTRICT)
            file_name = compose_file_name(FOLDERS_BY_DISTRICT, u'%s-%s.png' % (subj, distr_name))
            # mean values for each study subject among ciries for every district
            plot_mean_by_regions(data[reg_name][distr_name], cities, subj,
                u'Середній бал з %s по містах, %s, %s' % (NAMES[subj], reg_name, distr_name),
                file_name
            )
