# rsync_backup.py

Backup script using rsync that can sync to multiple local or remote locations.

Usage:

	python rsync_backup.py <config_file>

This script can be seen in action in [this article](http://monomon.me/protoblog/index.php/8-utils/1-setting-up-a-home-server-on-a-raspberry-pi) describing a complete setup with an rsync daemon on the server. Check [client configuration](http://monomon.me/protoblog/index.php/8-utils/2-setting-up-a-home-server-on-a-raspberry-pi-configuring-the-clients) in particular.

## configuration

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


## options

* *command* - the only option at  the moment is `rsync`
* *options* - a list of options to pass to rsync
	* in this example we specify ssh as the remote shell, using a key called boombox-rsync-key
	* `--log-file` - self-explanatory. Look here if things go wrong
	* add `--dry-run` to the options to test your configuration
	* for more rsync options check `man rsync`
* *direction* - either < or > determining the direction in which you want to move the files
* *mail* - whether to also backup mail
* *mail_profiles_dir* - where to look for the mail profile, e.g. `$HOME/.thunderbird`
* *remote_host* - the remote machine to transfer to/from. Omit this option for a local backup.
* *mode* - if `daemon` is specified, adds a double colon (::) between the hostname and path, so that the remote path is interpreted as an rsync daemon module. Otherwise the path is absolute.
* *locations* - a list of dictionaries, each containing `src` and `dest`

## how to use

It is easy to create per-machine config files.

You can use this script to backup to local and remote directories. By specifying `remote_host` in the configuration, you would get formatted paths like `remote_host::path` in daemon mode and `remote_host:path` in normal mode (or without mode).

You might want to run this script as a `cron` job. Check `man crontab` for more information.

## sky's the limit

How could this tool become better? Feedback and comments are welcome.