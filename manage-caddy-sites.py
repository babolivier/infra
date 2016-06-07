#!/bin/python

from docker import Client
import os, sys, re

sites_dir = "/etc/infra.d/sites/"
image_base = "abiosoft/caddy:"

cli = Client(base_url='unix://var/run/docker.sock')

site_name = ""
config_file = ""
container_image = ""
out = {}

caddyImages = {}
caddyContainers = []

sites = os.listdir(sites_dir)

def stop_all():
    images = cli.images()

    for image in images:
        if "caddy:latest" in image["RepoTags"][0]:
            caddyImages["default"] = image["Id"]
        elif "caddy:php" in image["RepoTags"][0]:
            caddyImages["php"] = image["Id"]

    containers = cli.containers()

    for container in containers:
        if container["ImageID"] == caddyImages["default"] or container["ImageID"] == caddyImages["php"]:
            name = container["Names"][0][1:]
            # Let's manage the proxy with its own service
            if name != "proxy":
                print("Stopping", name)
                cli.stop(container=container.get("Id"), timeout=5)
                cli.remove_container(container=container.get("Id"))    


if sys.argv[1] == "--start":
    stop_all()

    for site in sites:
        test_buffer = re.search("(.+)\.caddyfile", site)
        if test_buffer:
            site_name = test_buffer.group(1)
            config_file = sites_dir + test_buffer.group(0)
            # This condition can be hard to understand as long as you don't realise that an 
            # Unix command's return code is 0 for a success and 1 for an error
            if os.system('grep "^startup php" ' + config_file + ' > /dev/null'):
                container_image = image_base + "latest"
            else:
                container_image = image_base + "php"
            print("Starting container for", site_name, "with image", container_image)
            out = cli.create_container(
                image=container_image, 
                name=site_name, 
                volumes=["/etc/Caddyfile"],
                host_config=cli.create_host_config(binds={
                    config_file: {
                        'bind': "/etc/Caddyfile",
                        'mode': 'ro',
                    }
                })
            )
            if out.get("Warnings") is None:
                cli.start(out.get("Id"))
                print("Container", out.get("Id"), "created and started.")

elif sys.argv[1] == "--stop":
    # Yup, dirty copy/paste from start-proxy. Should package it someday.
    stop_all()
