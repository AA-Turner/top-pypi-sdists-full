#!/bin/bash -eux

# Make sure only root can run this script
if [ "$(id -u)" != "0" ]; then
   echo -e "Please run as root"
   exit 1
fi

CERTS_DIR=`podman inspect neutron_api | jq ".[0].GraphDriver.Data.UpperDir" | tr -d '"'`

echo "deleting certs from "$CERTS_DIR
rm -rf $CERTS_DIR/var/lib/neutron/host_certs/*.pem
rm -rf $CERTS_DIR/var/lib/neutron/ca_certs/*.pem
rm -rf $CERTS_DIR/var/lib/neutron/combined/*.pem

podman stop neutron_api
echo "Stopped neutron_api container. Sleep for 10 secs before starting again.."
sleep 10
podman start neutron_api
