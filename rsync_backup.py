#!/usr/bin/env python

"""
Backup script using rsync

Uses a json configuration containing pairs of src->dest in a list of dictionaries

Source and destination may be a location on a remote host or a local path.

Read conf_backup_example.json to get an idea of the configuration options.

"""

import logging
import subprocess
import os
import sys
import json
import re

__author__ = "Mois Moshev"
__email__ = "mois@monomon.me"

logging.basicConfig()
logger = logging.getLogger("backup")
logger.setLevel(logging.DEBUG)

def format_locations(src, dest, direction):

    # local locations - just switch on direction
    if direction == "<":
        return dest, src
    else:
        return src, dest

def format_remote_locations(src, dest, direction, host, mode):

    # FIXME: checks here could be a bit smarter
    if mode == "daemon":
        # rsync daemon module path with double colon
        loc_string = "{}::{}"
    else:
        # absolute path
        loc_string = "{}:{}"

    if direction == "<":
        return loc_string.format(host, dest), src
    else:
        return src, loc_string.format(host, dest)

def backup(conf_path):

    # default command
    command = "rsync"
    config = None
    options = None
    profileName = None

    # load config
    with open(conf_path, "r") as f:
        config = json.load(f)

    if "command" in config:
        command = config["command"]

    if "options" in config:
        options = config["options"]

    # check whether to archive mail
    if "mail" in config and config["mail"] == True:

        # try to obtain active mail profile
        with open(os.path.join(config["mail_profiles_dir"], "profiles.ini"), "r") as f:
           profileName = re.search('Path=(\w+)', f.read()).group(1)

        # add generated locations to config
        if profileName:
            logger.info("backing up email from {}".format(profileName))
            print("backing up mail from {}".format(os.path.join(config["mail_profiles_dir"], profileName + ".default")))
            config["locations"].append({
                "src" : os.path.join(config["mail_profiles_dir"], profileName + ".default"),
                "dest" : config["mail_dest"]
            })
    else:
        logger.info("skipping email")

    # call command for each item in the config
    for item in config["locations"]:

        if "remote_host" in config:
            src, dest = format_remote_locations(
                item["src"],
                item["dest"],
                config.get("direction", None),
                config["remote_host"],
                config.get("mode", None)
            )
        else:
            # local sync
            src, dest = format_locations(
                item["src"],
                item["dest"],
                config.get("direction", None)
            )

            # currently only perform these checks for local backups
            # FIXME: come up with better checks that would work for remote backups    
            if not os.access(src, os.R_OK):
                logger.error("source is not readable, skipping {}... ".format(src))
                continue

            if not os.access(dest, os.W_OK):
                logger.error("destination {} is not writeable, skipping...".format(dest))
                continue

        # make a big ol' array of stuff; mind slashes, as it makes a difference for the command's meaning
        cmd = [command] + \
            options + \
            [
                src,
                dest
            ]

        logger.debug("Calling {}".format(cmd))
        code = subprocess.call(cmd)

        if code == 0:
            logger.info("successfully transfered files")
        else:
            logger.error("transfer unsuccessful")

if __name__=="__main__":
    if len(sys.argv) > 1:
        backup(sys.argv[1])
    else:
        logger.error("Usage: {} <config_file>".format(sys.argv[0]))
        sys.exit()
