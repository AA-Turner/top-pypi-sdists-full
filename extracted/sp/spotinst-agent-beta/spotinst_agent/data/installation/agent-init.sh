#!/bin/sh
set -e

readonly LOG_LEVEL_ERROR="ERROR"
readonly LOG_LEVEL_INFO="INFO"
readonly LOG_LEVEL_DEBUG="DEBUG"

lsb_dist=''
dist_version=''

command_exists() {
	command -v "$@" > /dev/null 2>&1
}

install() {
	user="$(id -un 2>/dev/null || true)"
	sh_c='sh -c'
	if [ "$user" != 'root' ]; then
		if command_exists sudo; then
			sh_c='sudo -E sh -c'
		elif command_exists su; then
			sh_c='su -c'
		else
			cat >&2 <<-'EOF'
			Error: this installer needs the ability to run commands as root.
			We are unable to find either "sudo" or "su" available to make this happen.
			EOF
			exit 1
		fi
	fi

#    log_info "Increasing file descriptor limit to 65535"
#    ulimit -n 65535
#    cat <<EOF >> /etc/security/limits.conf
#*       soft      nproc       65535
#*       hard      nproc       65535
#*       soft      nofile      65535
#*       hard      nofile      65535
#EOF
#
#	cat <<EOF >> /etc/sysctl.conf
#fs.file-max = 65536
#EOF

	# perform some very rudimentary platform detection
	if command_exists lsb_release; then
		os=`cat /etc/system-release | awk -F ' ' {'print $1'}`

		if [ "$os" = "CentOS" ]; then
			lsb_dist='centos'
		elif [ -r /etc/debian_version ]; then
          vrsn=`cat /etc/debian_version`

          if [ "$vrsn" = "jessie/sid" ]; then
            lsb_dist='ubuntu14'
          else
            lsb_dist='debian'
          fi
		fi
	fi
	if [ -z "$lsb_dist" ] && [ -r /etc/lsb-release ]; then
		lsb_dist="$(. /etc/lsb-release && echo "$DISTRIB_ID")"
	fi
	if [ -z "$lsb_dist" ] && [ -r /etc/debian_version ]; then
		vrsn=`cat /etc/debian_version`

		if [ "$vrsn" = "jessie/sid" ]; then
			lsb_dist='ubuntu14'
		else
			lsb_dist='debian'
		fi
	fi
	if [ -z "$lsb_dist" ] && [ -r /etc/fedora-release ]; then
		lsb_dist='fedora'
	fi
	if [ -z "$lsb_dist" ] && [ -r /etc/centos-release ]; then
		lsb_dist='centos'
	fi
	if [ -z "$lsb_dist" ] && [ -r /etc/redhat-release ]; then
		lsb_dist='redhat'
	fi
	if [ -z "$lsb_dist" ] && [ -r /etc/SuSE-release ]; then
		lsb_dist='suse'
	fi
	if [ -z "$lsb_dist" ] && [ -r /etc/system-release ]; then
		os=`cat /etc/system-release | awk -F ' ' {'print $1'}`

		if [ "$os" = "CentOS" ]; then
			lsb_dist='centos'
		else
			lsb_dist='amazon'
		fi
	fi
	if [ -z "$lsb_dist" ] && [ -r /etc/os-release ]; then
		lsb_dist="$(. /etc/os-release && echo "$ID")"
	fi

	lsb_dist="$(echo "$lsb_dist" | tr '[:upper:]' '[:lower:]')"

	# Special case redhatenterpriseserver
	if [ "${lsb_dist}" = "redhatenterpriseserver" ]; then
        	# Set it to redhat, it will be changed to centos below anyways
        	lsb_dist='redhat'
	fi

	# Run setup for each distro accordingly
	case "$lsb_dist" in
		amazon)
			log_info "Amazon Linux dist detected"
			log_info "Downloading init.d service file"
			curl -sL http://spotinst-public.s3.amazonaws.com/services/spotinst-agent/linux-initd/spotinst-agent -o /etc/init.d/spotinst-agent
			chmod +x /etc/init.d/spotinst-agent
			return
			;;

		ubuntu14)
			log_info "Old Ubuntu (initd) dist detected"
			log_info "Downloading init.d service file"
			curl -sL http://spotinst-public.s3.amazonaws.com/services/spotinst-agent/ubuntu-initd/spotinst-agent -o /etc/init.d/spotinst-agent
			chmod +x /etc/init.d/spotinst-agent
			return
			;;

		suse)
			log_info "SuSE dist detected"

			log_info "Downloading systemd service file"
			curl -sL http://spotinst-public.s3.amazonaws.com/services/spotinst-agent/spotinst-agent.service -o /etc/systemd/system/spotinst-agent.service
			log_info "done.."
			return
			;;

		ubuntu|debian)
			log_info "Ubuntu/Debian dist detected"
            log_info "Install dependencies"
            apt-get update
			apt-get install curl build-essential checkinstall libcap2-bin -y

			log_info "Adding capability +ep"
			setcap 'cap_net_bind_service=+ep' $SPOTINST_AGENT_PATH

			log_info "Downloading systemd service file"
			curl -sL http://spotinst-public.s3.amazonaws.com/services/spotinst-agent/spotinst-agent.service -o /lib/systemd/system/spotinst-agent.service

			return
			;;

		fedora|centos|redhat)
			log_info "Fedora/CentOS/RedHat dist detected"

			log_info "Adding capability +ep"
			setcap 'cap_net_bind_service=+ep' $SPOTINST_AGENT_PATH

			log_info "Downloading systemd service file"
			curl -sL http://spotinst-public.s3.amazonaws.com/services/spotinst-agent/spotinst-agent.service -o /lib/systemd/system/spotinst-agent.service

			return
			;;

		*)
			# intentionally mixed spaces and tabs here -- tabs are stripped by "<<-'EOF'", spaces are kept in the output
			cat >&2 <<-'EOF'

			  Either your platform is not easily detectable or is not supported by this
			  installer script.

			EOF
			exit 1
			;;
	esac
}

validate() {
    architecture=$(uname -m)
	case $architecture in
		# officially supported
		amd64|x86_64|aarch64)
			;;
		# not supported
		*)
			cat >&2 <<-EOF
			Error: $architecture is not a recognized platform.
			EOF
			exit 1
			;;
	esac
}

cleanup() {
    rm -rf /tmp/spotinst-agent*
    rm -rf /tmp/latest
}

start() {
	case "$lsb_dist" in
		amazon)
			log_info "Amazon Linux dist detected"
			/etc/init.d/spotinst-agent restart
			return
			;;

		ubuntu14)
			log_info "Old Ubuntu (initd) dist detected"
			/etc/init.d/spotinst-agent restart
			return
			;;

		suse)
			log_info "SuSE dist detected"
			/bin/systemctl daemon-reload
			/bin/systemctl restart spotinst-agent
			/bin/systemctl enable spotinst-agent
			return
			;;

		ubuntu|debian)
			log_info "Ubuntu/Debian dist detected"
			/bin/systemctl daemon-reload
			/bin/systemctl restart spotinst-agent
			/bin/systemctl enable spotinst-agent
			return
			;;

		fedora|centos|redhat)
			log_info "Fedora/CentOS/RedHat dist detected"
			/bin/systemctl daemon-reload
			/bin/systemctl restart spotinst-agent
			/bin/systemctl enable spotinst-agent
			return
			;;

		*)
			# intentionally mixed spaces and tabs here -- tabs are stripped by "<<-'EOF'", spaces are kept in the output
			cat >&2 <<-'EOF'

			  Either your platform is not easily detectable or is not supported by this
			  installer script.

			EOF
			exit 1
			;;
	esac
}

format_timestamp() {
  date +"%Y-%m-%d %H:%M:%S"
}

log_error() {
  log "$(format_timestamp)" "$LOG_LEVEL_ERROR" "$@"
}

log_info() {
  log "$(format_timestamp)" "$LOG_LEVEL_INFO" "$@"
}

log_debug() {
  log "$(format_timestamp)" "$LOG_LEVEL_DEBUG" "$@"
}

log() {
  local readonly timestamp="$1"
  shift
  local readonly log_level="$1"
  shift
  local readonly message="$@"
  echo -e "${timestamp} [${log_level}] ${message}"
}
log_info "Validating before install..."
validate

log_info "Installing..."
install

log_info "Cleaning up after install..."
cleanup

log_info "Starting spotinst-agent"
start

log_info "Successfully installed; DONE"