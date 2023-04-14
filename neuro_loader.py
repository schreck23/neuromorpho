#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 10:46:18 2023

@author: wfschrec
"""

import json
import requests
import os

from pyhelpers.ops import is_downloadable
from pestuary.collections import add_content_to_collection, collection_create, collection_list_content
from pestuary.content import content_add

def process_json_file():

    data_file = open('neuromorpho.json')

    data = json.load(data_file)
    root = "/home/shrek/neuromorpho"

    for i in data['_embedded']['neuronResources']:
        collection_number = int(i['neuron_id'])
        
        collection_id = "neuromorpho-" + i['neuron_id']
        
        print("Creating collection with name: %S" % collection_id)
        collection_uuid = collection_create(collection_id, "Collection representing files around neuron_id: %i" % collection_number)
        neuron_name = i['neuron_name']
        tag = "swc"
        neuron_root = os.path.join(root, str(collection_number))
        os.makedirs(neuron_root, exist_ok=True)
         
        if(is_downloadable("https://neuromorpho.org/dableFiles/ascoli/CNG version/%s.CNG.%s" % (neuron_name, tag))):
            target = "https://neuromorpho.org/dableFiles/ascoli/CNG version/" + neuron_name + ".CNG." + tag
            result = requests.get(target, allow_redirects=False)
            neuron_file = os.path.join(neuron_root, '%s.CNG.%s' % (neuron_name, tag))
            with open(neuron_file, 'wb') as cng_target:
                cng_target.write(result.content) 
            
        if(is_downloadable("https://neuromorpho.org/dableFiles/ascoli/Source-Version/%s.%s" % (neuron_name, tag))):
            target = "https://neuromorpho.org/dableFiles/ascoli/Source-Version/" + neuron_name + "." + tag
            result = requests.get(target, allow_redirects=False)
            neuron_file = os.path.join(neuron_root, '%s.%s' % (neuron_name, tag))
            with open(neuron_file, 'wb') as source_target:
                source_target.write(result.content) 
                
        if(is_downloadable(i['png_url'])):
            result = requests.get(i['png_url'], allow_redirects=False)
            png_file = os.path.join(neuron_root, neuron_name + ".png")
            with open(png_file, 'wb') as png_target:
                png_target.write(result.content)

        if(is_downloadable(i['_links']['self']['href'])):
            result = requests.get(i['_links']['self']['href'], allow_redirects=False)
            href_file = os.path.join(neuron_root, neuron_name + ".self")
            with open(href_file, 'wb') as href_target:
                href_target.write(result.content)
            
        if(is_downloadable(i['_links']['measurements']['href'])):
            result = requests.get(i['_links']['measurements']['href'], allow_redirects=False)
            href_file = os.path.join(neuron_root, neuron_name + ".measure")
            with open(href_file, 'wb') as measure_target:
                measure_target.write(result.content)
            
        if(is_downloadable(i['_links']['persistence_vector']['href'])):
            result = requests.get(i['_links']['persistence_vector']['href'], allow_redirects=False)
            href_file = os.path.join(neuron_root, neuron_name + ".persist")
            with open(href_file, 'wb') as persist_target:
                persist_target.write(result.content)
            
        i['png_url'] = "new url for this png"
        i['_links']['self']['href'] = "new self link"
        i['_links']['measurements']['href'] = "new measurements link"
        i['_links']['persistence_vector']['href'] = "new persistence link"
        
        with open(os.path.join(neuron_root, "metadata.json"), "w") as outfile:
            json.dump(i, outfile)
    
process_json_file()