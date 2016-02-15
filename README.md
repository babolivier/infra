# Infrastructure

Oh, hey there, here's juste another repository with all the stuff I use to run and automate tasks on my server. Since I know at least some people will take bits of it, I thought it would be great to detail it somewhere. Here we go.

## The server

I was already done with the whole Caddy section right after this one when I realised that it would actually be cool for you to have a little description of the server. It's an OVH VPS ([first one here](https://www.ovh.com/fr/vps/vps-ssd.xml)) using Archlinux. I chose this distro because I really like to use it in my everyday life, but also because I like the concepts of rolling releases and quick releases of software updates (I was previously using Ubuntu Server, so I have something to compare with). I'm quite fed up of having to do a huge useless update once in a while, and to see all my software deprecated as I wait 2 years for an LTS. Also, I like to have all my software up to date, for compatibility and security reasons (and also because I don't really want to wait 6 months or more to play around with a new feature). So yeah, Archlinux was a great choice.

## Caddy (web server)

### Introduction

If you don't know this magnificent piece of software that is [Caddy](https://caddyserver.com/), I highly advise you to check it out. In a few words, it's an amazing web server which requires minimal configuration (to think I was using Apache before... hehe) and has HTTP2, Git and TLS (via Let's Encrypt) support. Yes, this means that, in three lines in my config file, I can have a fully working website with automated TLS and HTTP2, pulling now and then a specified Git repository. Isn't this awesome?

### How I use it

I prefer to run Caddy through Docker containers, using the image provided by [@abiosoft](https://hub.docker.com/r/abiosoft/caddy/), as I find this way cleaner than manually moving Caddy's binary and config files in `/usr/` and `/etc/` (and also because it's way funnier, yes). I currently use one container by website (yes, I know this is not really well optimised, I'll work on that later), with a reverse proxy acting as a gateway. Docker's `--link` arguments allows me to create a closed LAN between all my containers, so that only the proxy needs to publish ports (which are `:80` and `:443`).

So, if you followed me correctly up to this point, you understand why the sites' config files (placed in [`sites/`](https://github.com/babolivier/infra/tree/master/sites)) are set to listen on `:80` with no TLS, as it is the proxy who handles both TLS and redirecting request to the right containers (by the way, its config is in [`proxy.caddyfile`](https://github.com/babolivier/infra/blob/master/proxy.caddyfile)).

### Automation

All of this is automated thanks to two Python scripts I wrote, [`start-proxy.py`](https://github.com/babolivier/infra/blob/master/start-proxy.py) and [`manage-caddy-sites.py`](https://github.com/babolivier/infra/blob/master/manage-caddy-site.py) (this one requires a command-line argument, `--start` or `--stop`). The first one checks the running Docker containers using the Caddy image, and start the proxy with the correct `--link` arguments, while the second one lists websites from a JSON file ([`sites.json`](https://github.com/babolivier/infra/blob/master/sites.json)) and start a container for each of them if called with `--start`, or list all the containers running the Caddy image in order to stop and kill them. Both of them are ran by `systemd` services (yup, I know...). See how you can do quite a lot with only those two little, dirty-written, scripts.

My ultimate dream about this automation would be to create a web interface allowing me to add a website by just pasting its configuration and clicking a button. I don't care if something like this already exists, after all I'm only doing all of this because I find it fun and challenging. And I know there are chances I'll never get there.

## What's on here?

On the root of this repo, you'll find the README and LICENSE files (obviously), but also the Python scripts described above, among the proxy's config file and the JSON describing the different sites.

Within the `services` directory lie the `systemd` services used to launch everything at startup, and you'll find the sites' configs in the `sites` directory.

## Feedback and reusability

If you have any question or anything to report on what you see here, please let me know using a GitHub issue or sending me a mail at <infra@brendanabolivier.com>. Also, if you see something interesting around here, please feel free to use my work at your will. It's some side project I work on during my free time, and I'd be honoured if it could be useful to anyone. Everything here is released under a MIT license, so serve yourself! Also, if you want to interact with me about how you're using the work here, or anything else, feel free to contact me by the ways described above :-)

