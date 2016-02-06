#!/usr/bin/python

from docker import Client
import os
import pprint

caddyImages = {}
caddyContainers = []

cli = Client(base_url='unix://var/run/docker.sock')

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
        # We musn't link the proxy to itself
        if name != "proxy":
            caddyContainers.append(name)

link = ""

for name in caddyContainers:
    link = link + "--link " + name + ":" + name + " "

command = "/usr/bin/docker " + link + " run -p 80:80 -p 443:443 -v /root/.caddy:/root/.caddy -v /etc/infra.d/proxy.caddyfile:/etc/Caddyfile --name proxy abiosoft/caddy:latest"

os.system(command)
