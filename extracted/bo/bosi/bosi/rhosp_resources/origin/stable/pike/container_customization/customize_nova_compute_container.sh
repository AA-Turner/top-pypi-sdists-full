#!/bin/bash -eux
# Copyright 2018 Big Switch Networks, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

CONTAINER_BUILD_DIR='openstack_nova_compute_bigswitch'
BSN_NOVACOMPUTE_TAG='12.0.1'

# recreate workspace for container build
rm -rf ${CONTAINER_BUILD_DIR}
mkdir -p ${CONTAINER_BUILD_DIR}

# copy required packages to build dir
cp ivs-*.rpm ${CONTAINER_BUILD_DIR}/

# container tag_id used to deploy overcloud
UPSTREAM_TAG=`sudo openstack overcloud container image tag discover \
--image registry.access.redhat.com/rhosp12/openstack-base:latest \
--tag-from-label version-release`

# local registry address to push image
LOCAL_REGISTRY_ADDRESS=`sudo docker images | grep -v redhat.com | grep -o '^.*rhosp12' | sort -u`

cd ${CONTAINER_BUILD_DIR}

cat > Dockerfile <<EOF
FROM ${LOCAL_REGISTRY_ADDRESS}/openstack-nova-compute:${UPSTREAM_TAG}
MAINTAINER Big Switch Networks Inc.
LABEL name="rhosp12/openstack-nova-compute-bigswitch" vendor="Big Switch Networks Inc" version="11.0" release="1"
# switch to root and install a custom RPM, etc.
USER root
COPY ivs-*.rpm /tmp/

RUN rpm -ivh /tmp/*.rpm
# switch the container back to the default user (NOT)
# doing this has permission denied error during startup. skip it.
# USER horizon
EOF

sudo docker build ./ -t ${BSN_NOVACOMPUTE_TAG}
IMAGE_ID=`sudo docker images -q ${BSN_NOVACOMPUTE_TAG}`

# tag latest build image and push to local registry
sudo docker tag ${IMAGE_ID} ${LOCAL_REGISTRY_ADDRESS}/openstack-nova-compute-bigswitch:${BSN_NOVACOMPUTE_TAG}
sudo docker push ${LOCAL_REGISTRY_ADDRESS}/openstack-nova-compute-bigswitch:${BSN_NOVACOMPUTE_TAG}
