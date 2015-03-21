<link href="http://kevinburke.bitbucket.org/markdowncss/markdown.css" rel="stylesheet"></link>

# rsync_remote, a useful rsync backup script

This script uses a json config with various options controlling the process.

It contains source-destination pairs. Each of them is synced in a separate rsync call.

Let's start with an example config:

		{
			"command" : "rsync",
			"--log-file" : "/home/ugabuga/rsync.log",
			"options" : [
				"--rsh=/usr/bin/ssh -i /home/ugabuga/.ssh/boombox-rsync-key",
				"--verbose",
				"--progress",
				"--stats",
				"--compress",
				"--recursive",
				"--perms",
				"--times",
				"--links"
			],
			"remote_host" : "192.168.1.74",
			"mode" : "daemon",
			"direction" : ">",
			"mail" : false,
			"mail_profiles_dir" : "/home/ugabuga/.thunderbird/profiles.ini",
			"locations" :[
				{
					"src" : "/mnt/data/Projects",
					"dest" : "mon"
				}
			]
		}

And a rundown of the options:

* *command* - the only option at  the moment is `rsync`
* *--log-file* - self-explanatory
* *options* - a list of options to pass to rsync
	* in this example we specify ssh as the remote shell, using a key called boombox-rsync-key
* *direction* - either < or > determining the direction in which you want to move the files
* *mail* - whether to also backup mail
* *mail_profiles_dir* - where to look for the mail profile, e.g. `$HOME/.thunderbird`
* *remote_host* - the remote machine to transfer to/from
* *mode* - if `daemon` is specified, adds a double colon (::) between the hostname and path, so that the remote path is interpreted as an rsync daemon module. Otherwise the path is absolute.
* *locations* - a list of dictionaries, each containing `src` and `dest`
