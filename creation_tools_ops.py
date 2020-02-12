# MB-Lab

# MB-Lab fork website : https://github.com/animate1978/MB-Lab

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
#
# Teto, for MB-Lab

import logging
import json
import os
import bpy
import numpy
#from . import algorithms
from. import numpy_ops

logger = logging.getLogger(__name__)

forbidden_directories = ["__pycache__", "data", "mb-lab_updater", "animations", "anthropometry",
    "bboxes", "expressions_comb", "expressions_morphs", "face_rig", "Hair_Data", "joints",
    "measures", "morphs", "Particle_Hair", "pgroups", "phenotypes", "poses", "presets",
    "textures", "transformations", "vertices", "vgroups", "hu_f_anthropometry",
    "hu_m_anthropometry", "anime_expressions", "human_expressions", "female_poses",
    "male_poses", "rest_poses"]

forbiden_names = ["human", "anime", "male", "female", "anthropometry", "bbox", "expressions",
    "exprs", "morphs", "hair", "joints", "offset", "measures", "extra", "polygs", "ptypes",
    "poses", "rest", "specialtype", "anyme", "style", "type", "base", "transf", "verts",
    "vgroups", "muscles"]

needed_directories = ["animations", "anthropometry", "bboxes", "expressions_comb",
    "expressions_morphs", "face_rig", "Hair_Data", "joints", "measures", "morphs",
    "Particle_Hair", "pgroups", "phenotypes", "poses", "presets", "textures", "transformations",
    "vertices", "vgroups"]

created_names = {} #The names created while making a new compatible model.
"""
The keys are (values are string):
body = the name of the body like "human"
body_short = the short name like "hu"
gender = the gender like "female"
gender_short = "f_"
...
"""

static_names = {
    "human": ["human", "hu"],
    "anime": ["anime", "an"],
    "male": ["male", "m_"],
    "female": ["female", "f_"],
    #"": [],
    }
#with complete name, short name.

static_genders = [("MA", "male", "All male characters"),
   ("FE", "female", "All female characters"),
   ("UN", "undefined", "CHaracter with no specific gender")]
#--------------------------------------

def get_forbidden_directories():
    return forbidden_directories

def is_forbidden_directory(dir):
    return dir.lower() in forbidden_directories

def get_forbidden_names():
    return forbiden_names

def is_forbidden_name(name):
    return name.lower() in forbiden_names

def get_static_names():
    return static_names

def get_created_names():
    return created_names

def get_created_name(key):
    return created_names.get(key, "")

def set_created_name(key, value):
    created_names[key] = value

def init_created_names():
    created_names = {}

def get_static_genders(key=None):
    if key == None:
        return static_genders
    value = None
    for index in range(len(static_genders)):
        if key in static_genders[index]:
            value = static_genders[index]
            return value[1]
    return ""
#--------------------------------------

def create_needed_directories(name=""):
    if name == None or name == "" or is_forbidden_name(name):
        logger.critical("!WARNING! Name doesn't exist or is forbidden.")
        return
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), name)
    if os.path.exists(path):
        logger.critical("!WARNING! Directory already exists.")
    for sub_dir in needed_directories:
        try:
            os.makedirs(os.path.join(path, sub_dir), True)
        except FileExistsError:
            logger.warning("Directory " + sub_dir + " already exists. Skipped.")