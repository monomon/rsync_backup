#!/usr/bin/env python

"""
Remote backup script using rsync

Uses a json configuration containing pairs of src->dest in a list of dictionaries

TODO
* incremental backups - save a batch file?
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

def remote_backup(conf_path="conf_backup_test.json"):

    profileName = None

    # default command
    command = "rsync"
    config = None
    options = None

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

    if config["mode"] == "daemon":
        loc_string = "{}::{}"
    else:
        loc_string = "{}:{}"


    # call command for each item in the config
    for item in config["locations"]:

        if "direction" in config and config["direction"] == "<":
            src = loc_string.format(config["remote_host"], item["dest"])
            dest = item["src"]
        else:
            src = item["src"]
            dest = loc_string.format(config["remote_host"], item["dest"])

        if not os.access(src, os.R_OK):
            logger.error("source is not readable, skipping {}... ".format(src))
            continue

    # skip writeable check for remote.. maybe there's another check possible?
    #   if not os.access(item["dest"], os.W_OK):
    #       logger.error("destination {} is not writeable, skipping...".format(item["dest"]))
    #       continue

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
    # set config path
    if len(sys.argv) > 1:
        conf_path = sys.argv[1]
        remote_backup(conf_path)

