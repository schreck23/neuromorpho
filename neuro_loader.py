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

def store_get_cid(file_name):
    
    url = "https://edge.estuary.tech/api/v1/content/add"

    payload={}
    files=[
      ('data',('filename',open(file_name,'rb'),'application/zip'))
    ]
    headers = {
      'Authorization': 'Bearer [API KEY]'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    output = json.loads(response.content.decode('utf-8'))
    
    return output['contents'][0]['cid']

def process_json_file():

    data_file = open('neuromorpho.json')

    data = json.load(data_file)
    root = "/Users/wfschrec/Downloads/neuromorpho"
    
    for i in data['_embedded']['neuronResources']:
        collection_number = int(i['neuron_id'])
                
        neuron_name = i['neuron_name']
        tag = "swc"
        neuron_root = os.path.join(root, str(collection_number))
        os.makedirs(neuron_root, exist_ok=True)

        base_edge_url = "https://edge.estuary.tech/ipfs/"
         
        print("Storing neuro sample with ID: %i" % collection_number)
        
        if(is_downloadable("https://neuromorpho.org/dableFiles/ascoli/CNG version/%s.CNG.%s" % (neuron_name, tag))):
            target = "https://neuromorpho.org/dableFiles/ascoli/CNG version/" + neuron_name + ".CNG." + tag
            result = requests.get(target, allow_redirects=False)
            neuron_file = os.path.join(neuron_root, '%s.CNG.%s' % (neuron_name, tag))
            with open(neuron_file, 'wb') as cng_target:
                cng_target.write(result.content) 
            cid = store_get_cid(neuron_file)
            print(neuron_file + " -> " + base_edge_url + cid)
            
        if(is_downloadable("https://neuromorpho.org/dableFiles/ascoli/Source-Version/%s.%s" % (neuron_name, tag))):
            target = "https://neuromorpho.org/dableFiles/ascoli/Source-Version/" + neuron_name + "." + tag
            result = requests.get(target, allow_redirects=False)
            neuron_file = os.path.join(neuron_root, '%s.%s' % (neuron_name, tag))
            with open(neuron_file, 'wb') as source_target:
                source_target.write(result.content)
            cid = store_get_cid(neuron_file)
            print(neuron_file + " -> " + base_edge_url + cid)
            
        if(is_downloadable(i['png_url'])):
            result = requests.get(i['png_url'], allow_redirects=False)
            png_file = os.path.join(neuron_root, neuron_name + ".png")
            with open(png_file, 'wb') as png_target:
                png_target.write(result.content)
            cid = store_get_cid(png_file)
            png_url = base_edge_url + cid
            print(png_file + " -> " + base_edge_url + cid)

        if(is_downloadable(i['_links']['self']['href'])):
            result = requests.get(i['_links']['self']['href'], allow_redirects=False)
            self_file = os.path.join(neuron_root, neuron_name + ".self")
            with open(self_file, 'wb') as self_target:
                self_target.write(result.content)
            cid = store_get_cid(self_file)
            self_url = base_edge_url + cid
            print(self_file + " -> " + base_edge_url + cid)
            
        if(is_downloadable(i['_links']['measurements']['href'])):
            result = requests.get(i['_links']['measurements']['href'], allow_redirects=False)
            meas_file = os.path.join(neuron_root, neuron_name + ".measure")
            with open(meas_file, 'wb') as measure_target:
                measure_target.write(result.content)
            cid = store_get_cid(meas_file)
            meas_url = base_edge_url + cid
            print(meas_file + " -> " + base_edge_url + cid)
            
        if(is_downloadable(i['_links']['persistence_vector']['href'])):
            result = requests.get(i['_links']['persistence_vector']['href'], allow_redirects=False)
            persist_file = os.path.join(neuron_root, neuron_name + ".persist")
            with open(persist_file, 'wb') as persist_target:
                persist_target.write(result.content)
            cid = store_get_cid(persist_file)
            persist_url = base_edge_url + cid
            print(persist_file + " -> " + base_edge_url + cid)
            
        i['png_url'] = png_url
        i['_links']['self']['href'] = self_url
        i['_links']['measurements']['href'] = meas_url
        i['_links']['persistence_vector']['href'] = persist_url
        
        with open(os.path.join(neuron_root, "metadata.json"), "w") as outfile:
            json.dump(i, outfile)
        
        cid = store_get_cid(os.path.join(neuron_root, "metadata.json"))
        print("Sample Metadata -> " + base_edge_url + cid)
        
process_json_file()