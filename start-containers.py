#!/bin/python

from docker import Client
import os
import json

json_file = "/etc/infra.d/sites.json"
data = open(json_file)
sites = json.load(data)

cli = Client(base_url='unix://var/run/docker.sock')

site_name = ""
config_file = ""
container_image = ""
out = {}

for site in sites:
    site_name = site["name"]
    config_file = "/etc/infra.d/sites/" +  site["name"] + ".caddyfile"
    container_image = "abiosoft/caddy:" + site["image"]
    print("Working on site", site_name)
    if os.path.exists(config_file):
        print("Starting container for", site_name)
        out = cli.create_container(
            image=container_image, 
            name=site_name, 
            volumes=["/etc/Caddyfile"],
            host_config=cli.create_host_config(binds={
                config_file: {
                    'bind': '/etc/Caddyfile',
                    'mode': 'ro',
                }
            })
        )
        if out.get("Warnings") is None:
            cli.start(out.get("Id"))
            print("Container", out.get("Id"), "created and started.")
    else:
        print("File", config_file,"doesn't exist.")

