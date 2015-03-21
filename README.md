<link href="http://kevinburke.bitbucket.org/markdowncss/markdown.css" rel="stylesheet"></link>

# rsync_backup

Usage:

	python rsync_backup.py <config_file>

This script uses a json config with various options controlling the process.

It contains source-destination pairs. Each of them is synced in a separate rsync call.

Let's start with the example config:

	{
		"command" : "rsync",
		"options" : [
			"--rsh=/usr/bin/ssh -i /home/birdman/.ssh/mybox-homeserver-rsync",
			"--log-file=/home/birdman/rsync.log",
			"--port=54777",
			"--recursive",
			"--verbose",
			"--progress",
			"--stats",
			"--perms",
			"--times",
			"--compress",
			"--cvs-exclude",
			"--exclude=\".*.swp\"",
			"--links"
		], 
		"remote_host" : "raspi_server",
		"direction" : ">",
		"mail" : false,
		"mail_profiles_dir" : "/home/birdman/.thunderbird",
		"mail_dest" : "bird/userdata/",
		"mode" : "daemon",
		"locations" :[
			{
				"src" : "/mnt/data/projects",
				"dest" : "bird/projects"
			}, {
				"src" : "~/.bashrc",
				"dest" : "bird/dotfiles/"
			}, {
				"src" : "~/.tmux.conf",
				"dest" : "bird/dotfiles/"
			}, {
				"src" : "/mnt/data/music",
				"dest" : "music"
			}
		]
	}


And a rundown of the options:

* *command* - the only option at  the moment is `rsync`
* *options* - a list of options to pass to rsync
	* in this example we specify ssh as the remote shell, using a key called boombox-rsync-key
	* *--log-file* - self-explanatory. Look here if things go wrong
* *direction* - either < or > determining the direction in which you want to move the files
* *mail* - whether to also backup mail
* *mail_profiles_dir* - where to look for the mail profile, e.g. `$HOME/.thunderbird`
* *remote_host* - the remote machine to transfer to/from. Omit this option for a local backup.
* *mode* - if `daemon` is specified, adds a double colon (::) between the hostname and path, so that the remote path is interpreted as an rsync daemon module. Otherwise the path is absolute.
* *locations* - a list of dictionaries, each containing `src` and `dest`
