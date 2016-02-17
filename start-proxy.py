#!/usr/bin/python

from docker import Client
import os
import pprint

config_file = "/etc/infra.d/proxy.caddyfile"

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

links={}
for name in caddyContainers:
    links[name] = name

# Creating the specific HostConfig for the proxy
host_config = cli.create_host_config(links=links, binds={
    config_file: {
        'bind': '/etc/Caddyfile',
        'mode': 'ro'
    },
    "/root/.caddy": {
        'bind': '/root/.caddy',
        'mode': 'rw'
    }
}, port_bindings={
    80: 80,
    443: 443
})

container = cli.create_container(
    image="abiosoft/caddy:latest",
    name="proxy",
    host_config=host_config
)

if container.get("Warnings") is None:
    cli.start(container.get("Id"))
    print("Proxy successfully started with id", container.get("Id"))


#command = "/usr/bin/docker run " + link + " -p 80:80 -p 443:443 -v /root/.caddy:/root/.caddy -v /etc/infra.d/proxy.caddyfile:/etc/Caddyfile --name proxy abiosoft/caddy:latest"

#os.system(command)
