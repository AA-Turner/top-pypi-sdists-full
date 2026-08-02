#!/bin/bash
podman run -it -w /workspace --name dttlib --volume /opt/evr/projects:/workspace nvimdttlib /bin/bash
