#!/bin/bash
usage() { echo -e "Usage:\n   $0 "\
"[-l <string>] [-u <string>] [-p <string>]\n"\
"   -l  Target url to capture screenshot from\n"\
"   -u  username for login (if required)\n"\
"   -p  password for login (if required)" 1>&2; exit 1; }

while getopts "l:u:p:" o; do
    case "${o}" in
        l)
            url=${OPTARG}
            ;;
        p)
            p=${OPTARG}
            ;;
        u)
            u=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${url}" ] || [ -z "${u}" ] || [ -z "${p}" ]; then
	echo -e "Missing args!\n"
    usage
fi

docker run -v `pwd`:/captured -ti docker.io/erezhorev/captscreenshot \
  --url=$url\
  --out=/captured/screenshot.png \
  --user=$u --password=$p \
  --chown=$UID