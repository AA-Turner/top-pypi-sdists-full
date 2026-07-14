#!/usr/bin/env python

#
# Generated Sun Jul 12 18:06:51 2026 by generateDS.py version 2.44.3.
# Python 3.10.12 (main, Jun 22 2026, 18:55:27) [GCC 11.4.0]
#
# Command line options:
#   ('-q', '')
#   ('-f', '')
#   ('-o', 'pyone/bindings/supbind.py')
#   ('-s', 'pyone/bindings/__init__.py')
#   ('--super', 'supbind')
#   ('--external-encoding', 'utf-8')
#   ('--silence', '')
#
# Command line arguments:
#   ../../../share/doc/xsd/index.xsd
#
# Command line:
#   /home/one/init-build-jenkins.HKHdhA/one/src/oca/python/bin/generateDS -q -f -o "pyone/bindings/supbind.py" -s "pyone/bindings/__init__.py" --super="supbind" --external-encoding="utf-8" --silence ../../../share/doc/xsd/index.xsd
#
# Current working directory (os.getcwd()):
#   python
#

import os
import sys
from pyone.util import TemplatedType
from lxml import etree as etree_

from . import supbind as supermod

def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        parser = etree_.ETCompatXMLParser()
    try:
        if isinstance(infile, os.PathLike):
            infile = os.path.join(infile)
    except AttributeError:
        pass
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc

def parsexmlstring_(instring, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    element = etree_.fromstring(instring, parser=parser, **kwargs)
    return element

#
# Globals
#

ExternalEncoding = 'utf-8'
SaveElementTreeNode = True

#
# Data representation classes
#


class HISTORY_RECORDSSub(TemplatedType, supermod.HISTORY_RECORDS):
    def __init__(self, HISTORY=None, **kwargs_):
        super(HISTORY_RECORDSSub, self).__init__(HISTORY,  **kwargs_)
supermod.HISTORY_RECORDS.subclass = HISTORY_RECORDSSub
# end class HISTORY_RECORDSSub


class HISTORYSub(TemplatedType, supermod.HISTORY):
    def __init__(self, OID=None, SEQ=None, HOSTNAME=None, HID=None, CID=None, STIME=None, ETIME=None, VM_MAD=None, TM_MAD=None, DS_ID=None, PLAN_ID=None, ACTION_ID=None, PSTIME=None, PETIME=None, RSTIME=None, RETIME=None, ESTIME=None, EETIME=None, ACTION=None, UID=None, GID=None, REQUEST_ID=None, VM=None, **kwargs_):
        super(HISTORYSub, self).__init__(OID, SEQ, HOSTNAME, HID, CID, STIME, ETIME, VM_MAD, TM_MAD, DS_ID, PLAN_ID, ACTION_ID, PSTIME, PETIME, RSTIME, RETIME, ESTIME, EETIME, ACTION, UID, GID, REQUEST_ID, VM,  **kwargs_)
supermod.HISTORY.subclass = HISTORYSub
# end class HISTORYSub


class LOCKSub(TemplatedType, supermod.LOCK):
    def __init__(self, LOCKED=None, OWNER=None, TIME=None, REQ_ID=None, **kwargs_):
        super(LOCKSub, self).__init__(LOCKED, OWNER, TIME, REQ_ID,  **kwargs_)
supermod.LOCK.subclass = LOCKSub
# end class LOCKSub


class PERMISSIONSSub(TemplatedType, supermod.PERMISSIONS):
    def __init__(self, OWNER_U=None, OWNER_M=None, OWNER_A=None, GROUP_U=None, GROUP_M=None, GROUP_A=None, OTHER_U=None, OTHER_M=None, OTHER_A=None, **kwargs_):
        super(PERMISSIONSSub, self).__init__(OWNER_U, OWNER_M, OWNER_A, GROUP_U, GROUP_M, GROUP_A, OTHER_U, OTHER_M, OTHER_A,  **kwargs_)
supermod.PERMISSIONS.subclass = PERMISSIONSSub
# end class PERMISSIONSSub


class IDSSub(TemplatedType, supermod.IDS):
    def __init__(self, ID=None, **kwargs_):
        super(IDSSub, self).__init__(ID,  **kwargs_)
supermod.IDS.subclass = IDSSub
# end class IDSSub


class SCHED_ACTIONSub(TemplatedType, supermod.SCHED_ACTION):
    def __init__(self, ID=None, PARENT_ID=None, TYPE=None, ACTION=None, ARGS=None, TIME=None, REPEAT=None, DAYS=None, END_TYPE=None, END_VALUE=None, DONE=None, MESSAGE=None, WARNING=None, **kwargs_):
        super(SCHED_ACTIONSub, self).__init__(ID, PARENT_ID, TYPE, ACTION, ARGS, TIME, REPEAT, DAYS, END_TYPE, END_VALUE, DONE, MESSAGE, WARNING,  **kwargs_)
supermod.SCHED_ACTION.subclass = SCHED_ACTIONSub
# end class SCHED_ACTIONSub


class DATASTORE_QUOTASub(TemplatedType, supermod.DATASTORE_QUOTA):
    def __init__(self, DATASTORE=None, **kwargs_):
        super(DATASTORE_QUOTASub, self).__init__(DATASTORE,  **kwargs_)
supermod.DATASTORE_QUOTA.subclass = DATASTORE_QUOTASub
# end class DATASTORE_QUOTASub


class NETWORK_QUOTASub(TemplatedType, supermod.NETWORK_QUOTA):
    def __init__(self, NETWORK=None, **kwargs_):
        super(NETWORK_QUOTASub, self).__init__(NETWORK,  **kwargs_)
supermod.NETWORK_QUOTA.subclass = NETWORK_QUOTASub
# end class NETWORK_QUOTASub


class VM_QUOTASub(TemplatedType, supermod.VM_QUOTA):
    def __init__(self, VM=None, **kwargs_):
        super(VM_QUOTASub, self).__init__(VM,  **kwargs_)
supermod.VM_QUOTA.subclass = VM_QUOTASub
# end class VM_QUOTASub


class IMAGE_QUOTASub(TemplatedType, supermod.IMAGE_QUOTA):
    def __init__(self, IMAGE=None, **kwargs_):
        super(IMAGE_QUOTASub, self).__init__(IMAGE,  **kwargs_)
supermod.IMAGE_QUOTA.subclass = IMAGE_QUOTASub
# end class IMAGE_QUOTASub


class VMSub(TemplatedType, supermod.VM):
    def __init__(self, ID=None, UID=None, GID=None, UNAME=None, GNAME=None, NAME=None, PERMISSIONS=None, LAST_POLL=None, STATE=None, LCM_STATE=None, PREV_STATE=None, PREV_LCM_STATE=None, RESCHED=None, STIME=None, ETIME=None, DEPLOY_ID=None, LOCK=None, MONITORING=None, SCHED_ACTIONS=None, TEMPLATE=None, USER_TEMPLATE=None, HISTORY_RECORDS=None, SNAPSHOTS=None, BACKUPS=None, **kwargs_):
        super(VMSub, self).__init__(ID, UID, GID, UNAME, GNAME, NAME, PERMISSIONS, LAST_POLL, STATE, LCM_STATE, PREV_STATE, PREV_LCM_STATE, RESCHED, STIME, ETIME, DEPLOY_ID, LOCK, MONITORING, SCHED_ACTIONS, TEMPLATE, USER_TEMPLATE, HISTORY_RECORDS, SNAPSHOTS, BACKUPS,  **kwargs_)
supermod.VM.subclass = VMSub
# end class VMSub


class ACL_POOLSub(TemplatedType, supermod.ACL_POOL):
    def __init__(self, ACL=None, **kwargs_):
        super(ACL_POOLSub, self).__init__(ACL,  **kwargs_)
supermod.ACL_POOL.subclass = ACL_POOLSub
# end class ACL_POOLSub


class CALL_INFOSub(TemplatedType, supermod.CALL_INFO):
    def __init__(self, RESULT=None, PARAMETERS=None, EXTRA=None, **kwargs_):
        super(CALL_INFOSub, self).__init__(RESULT, PARAMETERS, EXTRA,  **kwargs_)
supermod.CALL_INFO.subclass = CALL_INFOSub
# end class CALL_INFOSub


class BACKUPJOB_POOLSub(TemplatedType, supermod.BACKUPJOB_POOL):
    def __init__(self, BACKUPJOB=None, **kwargs_):
        super(BACKUPJOB_POOLSub, self).__init__(BACKUPJOB,  **kwargs_)
supermod.BACKUPJOB_POOL.subclass = BACKUPJOB_POOLSub
# end class BACKUPJOB_POOLSub


class BACKUPJOBSub(TemplatedType, supermod.BACKUPJOB):
    def __init__(self, ID=None, UID=None, GID=None, UNAME=None, GNAME=None, NAME=None, LOCK=None, PERMISSIONS=None, PRIORITY=None, LAST_BACKUP_TIME=None, LAST_BACKUP_DURATION=None, SCHED_ACTIONS=None, UPDATED_VMS=None, OUTDATED_VMS=None, BACKING_UP_VMS=None, ERROR_VMS=None, TEMPLATE=None, **kwargs_):
        super(BACKUPJOBSub, self).__init__(ID, UID, GID, UNAME, GNAME, NAME, LOCK, PERMISSIONS, PRIORITY, LAST_BACKUP_TIME, LAST_BACKUP_DURATION, SCHED_ACTIONS, UPDATED_VMS, OUTDATED_VMS, BACKING_UP_VMS, ERROR_VMS, TEMPLATE,  **kwargs_)
supermod.BACKUPJOB.subclass = BACKUPJOBSub
# end class BACKUPJOBSub


class CLUSTER_POOLSub(TemplatedType, supermod.CLUSTER_POOL):
    def __init__(self, CLUSTER=None, **kwargs_):
        super(CLUSTER_POOLSub, self).__init__(CLUSTER,  **kwargs_)
supermod.CLUSTER_POOL.subclass = CLUSTER_POOLSub
# end class CLUSTER_POOLSub


class CLUSTERSub(TemplatedType, supermod.CLUSTER):
    def __init__(self, ID=None, NAME=None, HOSTS=None, DATASTORES=None, VNETS=None, TEMPLATE=None, PLAN=None, **kwargs_):
        super(CLUSTERSub, self).__init__(ID, NAME, HOSTS, DATASTORES, VNETS, TEMPLATE, PLAN,  **kwargs_)
supermod.CLUSTER.subclass = CLUSTERSub
# end class CLUSTERSub


class DATASTORE_POOLSub(TemplatedType, supermod.DATASTORE_POOL):
    def __init__(self, DATASTORE=None, **kwargs_):
        super(DATASTORE_POOLSub, self).__init__(DATASTORE,  **kwargs_)
supermod.DATASTORE_POOL.subclass = DATASTORE_POOLSub
# end class DATASTORE_POOLSub


class DATASTORESub(TemplatedType, supermod.DATASTORE):
    def __init__(self, ID=None, UID=None, GID=None, UNAME=None, GNAME=None, NAME=None, PERMISSIONS=None, DS_MAD=None, TM_MAD=None, BASE_PATH=None, TYPE=None, DISK_TYPE=None, STATE=None, CLUSTERS=None, TOTAL_MB=None, FREE_MB=None, USED_MB=None, IMAGES=None, TEMPLATE=None, **kwargs_):
        super(DATASTORESub, self).__init__(ID, UID, GID, UNAME, GNAME, NAME, PERMISSIONS, DS_MAD, TM_MAD, BASE_PATH, TYPE, DISK_TYPE, STATE, CLUSTERS, TOTAL_MB, FREE_MB, USED_MB, IMAGES, TEMPLATE,  **kwargs_)
supermod.DATASTORE.subclass = DATASTORESub
# end class DATASTORESub


class DOCUMENT_POOLSub(TemplatedType, supermod.DOCUMENT_POOL):
    def __init__(self, DOCUMENT=None, **kwargs_):
        super(DOCUMENT_POOLSub, self).__init__(DOCUMENT,  **kwargs_)
supermod.DOCUMENT_POOL.subclass = DOCUMENT_POOLSub
# end class DOCUMENT_POOLSub


class DOCUMENTSub(TemplatedType, supermod.DOCUMENT):
    def __init__(self, ID=None, UID=None, GID=None, UNAME=None, GNAME=None, NAME=None, TYPE=None, PERMISSIONS=None, LOCK=None, TEMPLATE=None, **kwargs_):
        super(DOCUMENTSub, self).__init__(ID, UID, GID, UNAME, GNAME, NAME, TYPE, PERMISSIONS, LOCK, TEMPLATE,  **kwargs_)
supermod.DOCUMENT.subclass = DOCUMENTSub
# end class DOCUMENTSub


class GROUP_POOLSub(TemplatedType, supermod.GROUP_POOL):
    def __init__(self, GROUP=None, QUOTAS=None, VLAN_RULES=None, DEFAULT_GROUP_QUOTAS=None, **kwargs_):
        super(GROUP_POOLSub, self).__init__(GROUP, QUOTAS, VLAN_RULES, DEFAULT_GROUP_QUOTAS,  **kwargs_)
supermod.GROUP_POOL.subclass = GROUP_POOLSub
# end class GROUP_POOLSub


class GROUPSub(TemplatedType, supermod.GROUP):
    def __init__(self, ID=None, NAME=None, TEMPLATE=None, USERS=None, ADMINS=None, DATASTORE_QUOTA=None, NETWORK_QUOTA=None, VM_QUOTA=None, IMAGE_QUOTA=None, VLAN_RULES=None, DEFAULT_GROUP_QUOTAS=None, **kwargs_):
        super(GROUPSub, self).__init__(ID, NAME, TEMPLATE, USERS, ADMINS, DATASTORE_QUOTA, NETWORK_QUOTA, VM_QUOTA, IMAGE_QUOTA, VLAN_RULES, DEFAULT_GROUP_QUOTAS,  **kwargs_)
supermod.GROUP.subclass = GROUPSub
# end class GROUPSub


class HOOK_MESSAGESub(TemplatedType, supermod.HOOK_MESSAGE):
    def __init__(self, HOOK_TYPE=None, CALL=None, CALL_INFO=None, **kwargs_):
        super(HOOK_MESSAGESub, self).__init__(HOOK_TYPE, CALL, CALL_INFO,  **kwargs_)
supermod.HOOK_MESSAGE.subclass = HOOK_MESSAGESub
# end class HOOK_MESSAGESub


class HOOK_POOLSub(TemplatedType, supermod.HOOK_POOL):
    def __init__(self, HOOK=None, **kwargs_):
        super(HOOK_POOLSub, self).__init__(HOOK,  **kwargs_)
supermod.HOOK_POOL.subclass = HOOK_POOLSub
# end class HOOK_POOLSub


class HOOKSub(TemplatedType, supermod.HOOK):
    def __init__(self, ID=None, NAME=None, TYPE=None, LOCK=None, TEMPLATE=None, HOOKLOG=None, **kwargs_):
        super(HOOKSub, self).__init__(ID, NAME, TYPE, LOCK, TEMPLATE, HOOKLOG,  **kwargs_)
supermod.HOOK.subclass = HOOKSub
# end class HOOKSub


class HOST_POOLSub(TemplatedType, supermod.HOST_POOL):
    def __init__(self, HOST=None, **kwargs_):
        super(HOST_POOLSub, self).__init__(HOST,  **kwargs_)
supermod.HOST_POOL.subclass = HOST_POOLSub
# end class HOST_POOLSub


class HOSTSub(TemplatedType, supermod.HOST):
    def __init__(self, ID=None, NAME=None, STATE=None, PREV_STATE=None, IM_MAD=None, VM_MAD=None, CLUSTER_ID=None, CLUSTER=None, HOST_SHARE=None, VMS=None, TEMPLATE=None, MONITORING=None, **kwargs_):
        super(HOSTSub, self).__init__(ID, NAME, STATE, PREV_STATE, IM_MAD, VM_MAD, CLUSTER_ID, CLUSTER, HOST_SHARE, VMS, TEMPLATE, MONITORING,  **kwargs_)
supermod.HOST.subclass = HOSTSub
# end class HOSTSub


class IMAGE_POOLSub(TemplatedType, supermod.IMAGE_POOL):
    def __init__(self, IMAGE=None, **kwargs_):
        super(IMAGE_POOLSub, self).__init__(IMAGE,  **kwargs_)
supermod.IMAGE_POOL.subclass = IMAGE_POOLSub
# end class IMAGE_POOLSub


class IMAGESub(TemplatedType, supermod.IMAGE):
    def __init__(self, ID=None, UID=None, GID=None, UNAME=None, GNAME=None, NAME=None, LOCK=None, PERMISSIONS=None, TYPE=None, DISK_TYPE=None, PERSISTENT=None, REGTIME=None, MODTIME=None, SOURCE=None, PATH=None, FORMAT=None, FS=None, SIZE=None, STATE=None, PREV_STATE=None, RUNNING_VMS=None, CLONING_OPS=None, CLONING_ID=None, TARGET_SNAPSHOT=None, DATASTORE_ID=None, DATASTORE=None, VMS=None, CLONES=None, APP_CLONES=None, TEMPLATE=None, SNAPSHOTS=None, BACKUP_INCREMENTS=None, BACKUP_DISK_IDS=None, **kwargs_):
        super(IMAGESub, self).__init__(ID, UID, GID, UNAME, GNAME, NAME, LOCK, PERMISSIONS, TYPE, DISK_TYPE, PERSISTENT, REGTIME, MODTIME, SOURCE, PATH, FORMAT, FS, SIZE, STATE, PREV_STATE, RUNNING_VMS, CLONING_OPS, CLONING_ID, TARGET_SNAPSHOT, DATASTORE_ID, DATASTORE, VMS, CLONES, APP_CLONES, TEMPLATE, SNAPSHOTS, BACKUP_INCREMENTS, BACKUP_DISK_IDS,  **kwargs_)
supermod.IMAGE.subclass = IMAGESub
# end class IMAGESub


class MARKETPLACEAPP_POOLSub(TemplatedType, supermod.MARKETPLACEAPP_POOL):
    def __init__(self, MARKETPLACEAPP=None, **kwargs_):
        super(MARKETPLACEAPP_POOLSub, self).__init__(MARKETPLACEAPP,  **kwargs_)
supermod.MARKETPLACEAPP_POOL.subclass = MARKETPLACEAPP_POOLSub
# end class MARKETPLACEAPP_POOLSub


class MARKETPLACEAPPSub(TemplatedType, supermod.MARKETPLACEAPP):
    def __init__(self, ID=None, UID=None, GID=None, UNAME=None, GNAME=None, LOCK=None, REGTIME=None, NAME=None, ZONE_ID=None, ORIGIN_ID=None, SOURCE=None, MD5=None, SIZE=None, DESCRIPTION=None, VERSION=None, FORMAT=None, APPTEMPLATE64=None, MARKETPLACE_ID=None, MARKETPLACE=None, STATE=None, TYPE=None, PERMISSIONS=None, TEMPLATE=None, **kwargs_):
        super(MARKETPLACEAPPSub, self).__init__(ID, UID, GID, UNAME, GNAME, LOCK, REGTIME, NAME, ZONE_ID, ORIGIN_ID, SOURCE, MD5, SIZE, DESCRIPTION, VERSION, FORMAT, APPTEMPLATE64, MARKETPLACE_ID, MARKETPLACE, STATE, TYPE, PERMISSIONS, TEMPLATE,  **kwargs_)
supermod.MARKETPLACEAPP.subclass = MARKETPLACEAPPSub
# end class MARKETPLACEAPPSub


class MARKETPLACE_POOLSub(TemplatedType, supermod.MARKETPLACE_POOL):
    def __init__(self, MARKETPLACE=None, **kwargs_):
        super(MARKETPLACE_POOLSub, self).__init__(MARKETPLACE,  **kwargs_)
supermod.MARKETPLACE_POOL.subclass = MARKETPLACE_POOLSub
# end class MARKETPLACE_POOLSub


class MARKETPLACESub(TemplatedType, supermod.MARKETPLACE):
    def __init__(self, ID=None, UID=None, GID=None, UNAME=None, GNAME=None, NAME=None, STATE=None, MARKET_MAD=None, ZONE_ID=None, TOTAL_MB=None, FREE_MB=None, USED_MB=None, MARKETPLACEAPPS=None, PERMISSIONS=None, TEMPLATE=None, **kwargs_):
        super(MARKETPLACESub, self).__init__(ID, UID, GID, UNAME, GNAME, NAME, STATE, MARKET_MAD, ZONE_ID, TOTAL_MB, FREE_MB, USED_MB, MARKETPLACEAPPS, PERMISSIONS, TEMPLATE,  **kwargs_)
supermod.MARKETPLACE.subclass = MARKETPLACESub
# end class MARKETPLACESub


class MONITORING_DATASub(TemplatedType, supermod.MONITORING_DATA):
    def __init__(self, MONITORING=None, **kwargs_):
        super(MONITORING_DATASub, self).__init__(MONITORING,  **kwargs_)
supermod.MONITORING_DATA.subclass = MONITORING_DATASub
# end class MONITORING_DATASub


class OPENNEBULA_CONFIGURATIONSub(TemplatedType, supermod.OPENNEBULA_CONFIGURATION):
    def __init__(self, ACTION_TIMEOUT=None, API_LIST_ORDER=None, AUTH_MAD=None, AUTH_MAD_CONF=None, CLUSTER_ENCRYPTED_ATTR=None, COLD_MIGRATE_MODE=None, CONTEXT_ALLOW_ETH_UPDATES=None, CONTEXT_RESTRICTED_DIRS=None, CONTEXT_SAFE_DIRS=None, DATASTORE_CAPACITY_CHECK=None, DATASTORE_ENCRYPTED_ATTR=None, DATASTORE_LOCATION=None, DATASTORE_MAD=None, DB=None, DEFAULT_AUTH=None, DEFAULT_COST=None, DEFAULT_DEVICE_PREFIX=None, DEFAULT_IMAGE_PERSISTENT=None, DEFAULT_IMAGE_PERSISTENT_NEW=None, DEFAULT_IMAGE_TYPE=None, DEFAULT_UMASK=None, DEFAULT_VDC_CLUSTER_DATASTORE_ACL=None, DEFAULT_VDC_CLUSTER_HOST_ACL=None, DEFAULT_VDC_CLUSTER_NET_ACL=None, DEFAULT_VDC_DATASTORE_ACL=None, DEFAULT_VDC_HOST_ACL=None, DEFAULT_VDC_VNET_ACL=None, DOCUMENT_ENCRYPTED_ATTR=None, DRS_INTERVAL=None, DS_MAD_CONF=None, DS_MONITOR_VM_DISK=None, ENABLE_OTHER_PERMISSIONS=None, FEDERATION=None, GROUP_RESTRICTED_ATTR=None, GRPC_LISTEN_ADDRESS=None, GRPC_PORT=None, HM_MAD=None, HOOK_LOG_CONF=None, HOST_ENCRYPTED_ATTR=None, IMAGE_ENCRYPTED_ATTR=None, IMAGE_RESTRICTED_ATTR=None, IM_MAD=None, INHERIT_DATASTORE_ATTR=None, INHERIT_IMAGE_ATTR=None, INHERIT_VNET_ATTR=None, IPAM_MAD=None, KEEPALIVE_MAX_CONN=None, KEEPALIVE_TIMEOUT=None, LISTEN_ADDRESS=None, LIVE_RESCHEDS=None, LOG=None, LOG_CALL_FORMAT=None, LOG_RESULT_LENGTH=None, MAC_GLOBAL_SPACE=None, MAC_PREFIX=None, MANAGER_TIMER=None, MARKET_MAD=None, MARKET_MAD_CONF=None, MAX_ACTIONS_PER_CLUSTER=None, MAX_ACTIONS_PER_HOST=None, MAX_BACKUPS=None, MAX_BACKUPS_HOST=None, MAX_CONN=None, MAX_CONN_BACKLOG=None, MESSAGE_SIZE=None, MONITORING_INTERVAL_DATASTORE=None, MONITORING_INTERVAL_HOST=None, MONITORING_INTERVAL_MARKET=None, MONITORING_INTERVAL_VM=None, NETWORK_SIZE=None, ONE_KEY=None, PCI_PASSTHROUGH_BUS=None, PORT=None, RAFT=None, RPC_LOG=None, SCHED_MAD=None, SCHED_MAX_WND_LENGTH=None, SCHED_MAX_WND_TIME=None, SCHED_RETRY_TIME=None, SCRIPTS_REMOTE_DIR=None, SESSION_EXPIRATION_TIME=None, SHOWBACK_ONLY_RUNNING=None, TIMEOUT=None, TM_MAD=None, TM_MAD_CONF=None, USER_ENCRYPTED_ATTR=None, USER_RESTRICTED_ATTR=None, VLAN_IDS=None, VM_ADMIN_OPERATIONS=None, VM_ENCRYPTED_ATTR=None, VM_MAD=None, VM_MANAGE_OPERATIONS=None, VM_RESTRICTED_ATTR=None, VM_SNAPSHOT_FACTOR=None, VM_SUBMIT_ON_HOLD=None, VM_USE_OPERATIONS=None, VNC_PORTS=None, VNET_ENCRYPTED_ATTR=None, VNET_RESTRICTED_ATTR=None, VN_MAD_CONF=None, VXLAN_IDS=None, **kwargs_):
        super(OPENNEBULA_CONFIGURATIONSub, self).__init__(ACTION_TIMEOUT, API_LIST_ORDER, AUTH_MAD, AUTH_MAD_CONF, CLUSTER_ENCRYPTED_ATTR, COLD_MIGRATE_MODE, CONTEXT_ALLOW_ETH_UPDATES, CONTEXT_RESTRICTED_DIRS, CONTEXT_SAFE_DIRS, DATASTORE_CAPACITY_CHECK, DATASTORE_ENCRYPTED_ATTR, DATASTORE_LOCATION, DATASTORE_MAD, DB, DEFAULT_AUTH, DEFAULT_COST, DEFAULT_DEVICE_PREFIX, DEFAULT_IMAGE_PERSISTENT, DEFAULT_IMAGE_PERSISTENT_NEW, DEFAULT_IMAGE_TYPE, DEFAULT_UMASK, DEFAULT_VDC_CLUSTER_DATASTORE_ACL, DEFAULT_VDC_CLUSTER_HOST_ACL, DEFAULT_VDC_CLUSTER_NET_ACL, DEFAULT_VDC_DATASTORE_ACL, DEFAULT_VDC_HOST_ACL, DEFAULT_VDC_VNET_ACL, DOCUMENT_ENCRYPTED_ATTR, DRS_INTERVAL, DS_MAD_CONF, DS_MONITOR_VM_DISK, ENABLE_OTHER_PERMISSIONS, FEDERATION, GROUP_RESTRICTED_ATTR, GRPC_LISTEN_ADDRESS, GRPC_PORT, HM_MAD, HOOK_LOG_CONF, HOST_ENCRYPTED_ATTR, IMAGE_ENCRYPTED_ATTR, IMAGE_RESTRICTED_ATTR, IM_MAD, INHERIT_DATASTORE_ATTR, INHERIT_IMAGE_ATTR, INHERIT_VNET_ATTR, IPAM_MAD, KEEPALIVE_MAX_CONN, KEEPALIVE_TIMEOUT, LISTEN_ADDRESS, LIVE_RESCHEDS, LOG, LOG_CALL_FORMAT, LOG_RESULT_LENGTH, MAC_GLOBAL_SPACE, MAC_PREFIX, MANAGER_TIMER, MARKET_MAD, MARKET_MAD_CONF, MAX_ACTIONS_PER_CLUSTER, MAX_ACTIONS_PER_HOST, MAX_BACKUPS, MAX_BACKUPS_HOST, MAX_CONN, MAX_CONN_BACKLOG, MESSAGE_SIZE, MONITORING_INTERVAL_DATASTORE, MONITORING_INTERVAL_HOST, MONITORING_INTERVAL_MARKET, MONITORING_INTERVAL_VM, NETWORK_SIZE, ONE_KEY, PCI_PASSTHROUGH_BUS, PORT, RAFT, RPC_LOG, SCHED_MAD, SCHED_MAX_WND_LENGTH, SCHED_MAX_WND_TIME, SCHED_RETRY_TIME, SCRIPTS_REMOTE_DIR, SESSION_EXPIRATION_TIME, SHOWBACK_ONLY_RUNNING, TIMEOUT, TM_MAD, TM_MAD_CONF, USER_ENCRYPTED_ATTR, USER_RESTRICTED_ATTR, VLAN_IDS, VM_ADMIN_OPERATIONS, VM_ENCRYPTED_ATTR, VM_MAD, VM_MANAGE_OPERATIONS, VM_RESTRICTED_ATTR, VM_SNAPSHOT_FACTOR, VM_SUBMIT_ON_HOLD, VM_USE_OPERATIONS, VNC_PORTS, VNET_ENCRYPTED_ATTR, VNET_RESTRICTED_ATTR, VN_MAD_CONF, VXLAN_IDS,  **kwargs_)
supermod.OPENNEBULA_CONFIGURATION.subclass = OPENNEBULA_CONFIGURATIONSub
# end class OPENNEBULA_CONFIGURATIONSub


class RAFTSub(TemplatedType, supermod.RAFT):
    def __init__(self, SERVER_ID=None, STATE=None, TERM=None, VOTEDFOR=None, COMMIT=None, LOG_INDEX=None, LOG_TERM=None, FEDLOG_INDEX=None, **kwargs_):
        super(RAFTSub, self).__init__(SERVER_ID, STATE, TERM, VOTEDFOR, COMMIT, LOG_INDEX, LOG_TERM, FEDLOG_INDEX,  **kwargs_)
supermod.RAFT.subclass = RAFTSub
# end class RAFTSub


class SECURITY_GROUP_POOLSub(TemplatedType, supermod.SECURITY_GROUP_POOL):
    def __init__(self, SECURITY_GROUP=None, **kwargs_):
        super(SECURITY_GROUP_POOLSub, self).__init__(SECURITY_GROUP,  **kwargs_)
supermod.SECURITY_GROUP_POOL.subclass = SECURITY_GROUP_POOLSub
# end class SECURITY_GROUP_POOLSub


class SECURITY_GROUPSub(TemplatedType, supermod.SECURITY_GROUP):
    def __init__(self, ID=None, UID=None, GID=None, UNAME=None, GNAME=None, NAME=None, PERMISSIONS=None, UPDATED_VMS=None, OUTDATED_VMS=None, UPDATING_VMS=None, ERROR_VMS=None, TEMPLATE=None, **kwargs_):
        super(SECURITY_GROUPSub, self).__init__(ID, UID, GID, UNAME, GNAME, NAME, PERMISSIONS, UPDATED_VMS, OUTDATED_VMS, UPDATING_VMS, ERROR_VMS, TEMPLATE,  **kwargs_)
supermod.SECURITY_GROUP.subclass = SECURITY_GROUPSub
# end class SECURITY_GROUPSub


class SHOWBACK_RECORDSSub(TemplatedType, supermod.SHOWBACK_RECORDS):
    def __init__(self, SHOWBACK=None, **kwargs_):
        super(SHOWBACK_RECORDSSub, self).__init__(SHOWBACK,  **kwargs_)
supermod.SHOWBACK_RECORDS.subclass = SHOWBACK_RECORDSSub
# end class SHOWBACK_RECORDSSub


class USER_POOLSub(TemplatedType, supermod.USER_POOL):
    def __init__(self, USER=None, QUOTAS=None, DEFAULT_USER_QUOTAS=None, **kwargs_):
        super(USER_POOLSub, self).__init__(USER, QUOTAS, DEFAULT_USER_QUOTAS,  **kwargs_)
supermod.USER_POOL.subclass = USER_POOLSub
# end class USER_POOLSub


class USERSub(TemplatedType, supermod.USER):
    def __init__(self, ID=None, GID=None, GROUPS=None, GNAME=None, NAME=None, PASSWORD=None, AUTH_DRIVER=None, ENABLED=None, LOGIN_TOKEN=None, TEMPLATE=None, DATASTORE_QUOTA=None, NETWORK_QUOTA=None, VM_QUOTA=None, IMAGE_QUOTA=None, DEFAULT_USER_QUOTAS=None, **kwargs_):
        super(USERSub, self).__init__(ID, GID, GROUPS, GNAME, NAME, PASSWORD, AUTH_DRIVER, ENABLED, LOGIN_TOKEN, TEMPLATE, DATASTORE_QUOTA, NETWORK_QUOTA, VM_QUOTA, IMAGE_QUOTA, DEFAULT_USER_QUOTAS,  **kwargs_)
supermod.USER.subclass = USERSub
# end class USERSub


class VDC_POOLSub(TemplatedType, supermod.VDC_POOL):
    def __init__(self, VDC=None, **kwargs_):
        super(VDC_POOLSub, self).__init__(VDC,  **kwargs_)
supermod.VDC_POOL.subclass = VDC_POOLSub
# end class VDC_POOLSub


class VDCSub(TemplatedType, supermod.VDC):
    def __init__(self, ID=None, NAME=None, GROUPS=None, CLUSTERS=None, HOSTS=None, DATASTORES=None, VNETS=None, TEMPLATE=None, **kwargs_):
        super(VDCSub, self).__init__(ID, NAME, GROUPS, CLUSTERS, HOSTS, DATASTORES, VNETS, TEMPLATE,  **kwargs_)
supermod.VDC.subclass = VDCSub
# end class VDCSub


class VM_GROUP_POOLSub(TemplatedType, supermod.VM_GROUP_POOL):
    def __init__(self, VM_GROUP=None, **kwargs_):
        super(VM_GROUP_POOLSub, self).__init__(VM_GROUP,  **kwargs_)
supermod.VM_GROUP_POOL.subclass = VM_GROUP_POOLSub
# end class VM_GROUP_POOLSub


class VM_GROUPSub(TemplatedType, supermod.VM_GROUP):
    def __init__(self, ID=None, UID=None, GID=None, UNAME=None, GNAME=None, NAME=None, PERMISSIONS=None, LOCK=None, ROLES=None, TEMPLATE=None, **kwargs_):
        super(VM_GROUPSub, self).__init__(ID, UID, GID, UNAME, GNAME, NAME, PERMISSIONS, LOCK, ROLES, TEMPLATE,  **kwargs_)
supermod.VM_GROUP.subclass = VM_GROUPSub
# end class VM_GROUPSub


class VM_POOLSub(TemplatedType, supermod.VM_POOL):
    def __init__(self, VM=None, **kwargs_):
        super(VM_POOLSub, self).__init__(VM,  **kwargs_)
supermod.VM_POOL.subclass = VM_POOLSub
# end class VM_POOLSub


class VMTEMPLATE_POOLSub(TemplatedType, supermod.VMTEMPLATE_POOL):
    def __init__(self, VMTEMPLATE=None, **kwargs_):
        super(VMTEMPLATE_POOLSub, self).__init__(VMTEMPLATE,  **kwargs_)
supermod.VMTEMPLATE_POOL.subclass = VMTEMPLATE_POOLSub
# end class VMTEMPLATE_POOLSub


class VMTEMPLATESub(TemplatedType, supermod.VMTEMPLATE):
    def __init__(self, ID=None, UID=None, GID=None, UNAME=None, GNAME=None, NAME=None, LOCK=None, PERMISSIONS=None, REGTIME=None, TEMPLATE=None, **kwargs_):
        super(VMTEMPLATESub, self).__init__(ID, UID, GID, UNAME, GNAME, NAME, LOCK, PERMISSIONS, REGTIME, TEMPLATE,  **kwargs_)
supermod.VMTEMPLATE.subclass = VMTEMPLATESub
# end class VMTEMPLATESub


class VNET_POOLSub(TemplatedType, supermod.VNET_POOL):
    def __init__(self, VNET=None, **kwargs_):
        super(VNET_POOLSub, self).__init__(VNET,  **kwargs_)
supermod.VNET_POOL.subclass = VNET_POOLSub
# end class VNET_POOLSub


class VNETSub(TemplatedType, supermod.VNET):
    def __init__(self, ID=None, UID=None, GID=None, UNAME=None, GNAME=None, NAME=None, LOCK=None, PERMISSIONS=None, CLUSTERS=None, BRIDGE=None, BRIDGE_TYPE=None, STATE=None, PREV_STATE=None, PARENT_NETWORK_ID=None, TEMPLATE_ID=None, VN_MAD=None, PHYDEV=None, VLAN_ID=None, OUTER_VLAN_ID=None, VLAN_ID_AUTOMATIC=None, OUTER_VLAN_ID_AUTOMATIC=None, USED_LEASES=None, VROUTERS=None, UPDATED_VMS=None, OUTDATED_VMS=None, UPDATING_VMS=None, ERROR_VMS=None, TEMPLATE=None, AR_POOL=None, **kwargs_):
        super(VNETSub, self).__init__(ID, UID, GID, UNAME, GNAME, NAME, LOCK, PERMISSIONS, CLUSTERS, BRIDGE, BRIDGE_TYPE, STATE, PREV_STATE, PARENT_NETWORK_ID, TEMPLATE_ID, VN_MAD, PHYDEV, VLAN_ID, OUTER_VLAN_ID, VLAN_ID_AUTOMATIC, OUTER_VLAN_ID_AUTOMATIC, USED_LEASES, VROUTERS, UPDATED_VMS, OUTDATED_VMS, UPDATING_VMS, ERROR_VMS, TEMPLATE, AR_POOL,  **kwargs_)
supermod.VNET.subclass = VNETSub
# end class VNETSub


class VNTEMPLATE_POOLSub(TemplatedType, supermod.VNTEMPLATE_POOL):
    def __init__(self, VNTEMPLATE=None, **kwargs_):
        super(VNTEMPLATE_POOLSub, self).__init__(VNTEMPLATE,  **kwargs_)
supermod.VNTEMPLATE_POOL.subclass = VNTEMPLATE_POOLSub
# end class VNTEMPLATE_POOLSub


class VNTEMPLATESub(TemplatedType, supermod.VNTEMPLATE):
    def __init__(self, ID=None, UID=None, GID=None, UNAME=None, GNAME=None, NAME=None, LOCK=None, PERMISSIONS=None, REGTIME=None, TEMPLATE=None, **kwargs_):
        super(VNTEMPLATESub, self).__init__(ID, UID, GID, UNAME, GNAME, NAME, LOCK, PERMISSIONS, REGTIME, TEMPLATE,  **kwargs_)
supermod.VNTEMPLATE.subclass = VNTEMPLATESub
# end class VNTEMPLATESub


class VROUTER_POOLSub(TemplatedType, supermod.VROUTER_POOL):
    def __init__(self, VROUTER=None, **kwargs_):
        super(VROUTER_POOLSub, self).__init__(VROUTER,  **kwargs_)
supermod.VROUTER_POOL.subclass = VROUTER_POOLSub
# end class VROUTER_POOLSub


class VROUTERSub(TemplatedType, supermod.VROUTER):
    def __init__(self, ID=None, UID=None, GID=None, UNAME=None, GNAME=None, NAME=None, PERMISSIONS=None, LOCK=None, VMS=None, TEMPLATE=None, **kwargs_):
        super(VROUTERSub, self).__init__(ID, UID, GID, UNAME, GNAME, NAME, PERMISSIONS, LOCK, VMS, TEMPLATE,  **kwargs_)
supermod.VROUTER.subclass = VROUTERSub
# end class VROUTERSub


class ZONE_POOLSub(TemplatedType, supermod.ZONE_POOL):
    def __init__(self, ZONE=None, **kwargs_):
        super(ZONE_POOLSub, self).__init__(ZONE,  **kwargs_)
supermod.ZONE_POOL.subclass = ZONE_POOLSub
# end class ZONE_POOLSub


class ZONESub(TemplatedType, supermod.ZONE):
    def __init__(self, ID=None, NAME=None, STATE=None, TEMPLATE=None, SERVER_POOL=None, **kwargs_):
        super(ZONESub, self).__init__(ID, NAME, STATE, TEMPLATE, SERVER_POOL,  **kwargs_)
supermod.ZONE.subclass = ZONESub
# end class ZONESub


class DATASTORETypeSub(TemplatedType, supermod.DATASTOREType):
    def __init__(self, ID=None, IMAGES=None, IMAGES_USED=None, SIZE=None, SIZE_USED=None, **kwargs_):
        super(DATASTORETypeSub, self).__init__(ID, IMAGES, IMAGES_USED, SIZE, SIZE_USED,  **kwargs_)
supermod.DATASTOREType.subclass = DATASTORETypeSub
# end class DATASTORETypeSub


class NETWORKTypeSub(TemplatedType, supermod.NETWORKType):
    def __init__(self, ID=None, LEASES=None, LEASES_USED=None, **kwargs_):
        super(NETWORKTypeSub, self).__init__(ID, LEASES, LEASES_USED,  **kwargs_)
supermod.NETWORKType.subclass = NETWORKTypeSub
# end class NETWORKTypeSub


class VMTypeSub(TemplatedType, supermod.VMType):
    def __init__(self, CLUSTER_IDS=None, CPU=None, CPU_USED=None, MEMORY=None, MEMORY_USED=None, PCI_DEV=None, PCI_DEV_USED=None, PCI_NIC=None, PCI_NIC_USED=None, RUNNING_CPU=None, RUNNING_CPU_USED=None, RUNNING_MEMORY=None, RUNNING_MEMORY_USED=None, RUNNING_PCI_DEV=None, RUNNING_PCI_DEV_USED=None, RUNNING_PCI_NIC=None, RUNNING_PCI_NIC_USED=None, RUNNING_VMS=None, RUNNING_VMS_USED=None, SYSTEM_DISK_SIZE=None, SYSTEM_DISK_SIZE_USED=None, VMS=None, VMS_USED=None, **kwargs_):
        super(VMTypeSub, self).__init__(CLUSTER_IDS, CPU, CPU_USED, MEMORY, MEMORY_USED, PCI_DEV, PCI_DEV_USED, PCI_NIC, PCI_NIC_USED, RUNNING_CPU, RUNNING_CPU_USED, RUNNING_MEMORY, RUNNING_MEMORY_USED, RUNNING_PCI_DEV, RUNNING_PCI_DEV_USED, RUNNING_PCI_NIC, RUNNING_PCI_NIC_USED, RUNNING_VMS, RUNNING_VMS_USED, SYSTEM_DISK_SIZE, SYSTEM_DISK_SIZE_USED, VMS, VMS_USED,  **kwargs_)
supermod.VMType.subclass = VMTypeSub
# end class VMTypeSub


class IMAGETypeSub(TemplatedType, supermod.IMAGEType):
    def __init__(self, ID=None, RVMS=None, RVMS_USED=None, **kwargs_):
        super(IMAGETypeSub, self).__init__(ID, RVMS, RVMS_USED,  **kwargs_)
supermod.IMAGEType.subclass = IMAGETypeSub
# end class IMAGETypeSub


class MONITORINGTypeSub(TemplatedType, supermod.MONITORINGType):
    def __init__(self, CPU=None, CPU_FORECAST=None, CPU_FORECAST_FAR=None, DISKRDBYTES=None, DISKRDBYTES_BW=None, DISKRDBYTES_BW_FORECAST=None, DISKRDBYTES_BW_FORECAST_FAR=None, DISKRDIOPS=None, DISKRDIOPS_BW=None, DISKRDIOPS_BW_FORECAST=None, DISKRDIOPS_BW_FORECAST_FAR=None, DISKWRBYTES=None, DISKWRBYTES_BW=None, DISKWRBYTES_BW_FORECAST=None, DISKWRBYTES_BW_FORECAST_FAR=None, DISKWRIOPS=None, DISKWRIOPS_BW=None, DISKWRIOPS_BW_FORECAST=None, DISKWRIOPS_BW_FORECAST_FAR=None, DISK_SIZE=None, ID=None, MEMORY=None, MEMORY_FORECAST=None, MEMORY_FORECAST_FAR=None, NETRX=None, NETRX_BW=None, NETRX_BW_FORECAST=None, NETRX_BW_FORECAST_FAR=None, NETTX=None, NETTX_BW=None, NETTX_BW_FORECAST=None, NETTX_BW_FORECAST_FAR=None, TIMESTAMP=None, **kwargs_):
        super(MONITORINGTypeSub, self).__init__(CPU, CPU_FORECAST, CPU_FORECAST_FAR, DISKRDBYTES, DISKRDBYTES_BW, DISKRDBYTES_BW_FORECAST, DISKRDBYTES_BW_FORECAST_FAR, DISKRDIOPS, DISKRDIOPS_BW, DISKRDIOPS_BW_FORECAST, DISKRDIOPS_BW_FORECAST_FAR, DISKWRBYTES, DISKWRBYTES_BW, DISKWRBYTES_BW_FORECAST, DISKWRBYTES_BW_FORECAST_FAR, DISKWRIOPS, DISKWRIOPS_BW, DISKWRIOPS_BW_FORECAST, DISKWRIOPS_BW_FORECAST_FAR, DISK_SIZE, ID, MEMORY, MEMORY_FORECAST, MEMORY_FORECAST_FAR, NETRX, NETRX_BW, NETRX_BW_FORECAST, NETRX_BW_FORECAST_FAR, NETTX, NETTX_BW, NETTX_BW_FORECAST, NETTX_BW_FORECAST_FAR, TIMESTAMP,  **kwargs_)
supermod.MONITORINGType.subclass = MONITORINGTypeSub
# end class MONITORINGTypeSub


class DISK_SIZETypeSub(TemplatedType, supermod.DISK_SIZEType):
    def __init__(self, ID=None, SIZE=None, **kwargs_):
        super(DISK_SIZETypeSub, self).__init__(ID, SIZE,  **kwargs_)
supermod.DISK_SIZEType.subclass = DISK_SIZETypeSub
# end class DISK_SIZETypeSub


class TEMPLATETypeSub(TemplatedType, supermod.TEMPLATEType):
    def __init__(self, AUTOMATIC_DS_REQUIREMENTS=None, AUTOMATIC_NIC_REQUIREMENTS=None, AUTOMATIC_REQUIREMENTS=None, CLONING_TEMPLATE_ID=None, CONTEXT=None, CPU=None, CPU_COST=None, DISK=None, DISK_COST=None, EMULATOR=None, FEATURES=None, HYPERV_OPTIONS=None, GRAPHICS=None, VIDEO=None, IMPORTED=None, INPUT=None, MEMORY=None, MEMORY_COST=None, MEMORY_MAX=None, MEMORY_SLOTS=None, MEMORY_RESIZE_MODE=None, NIC=None, NIC_ALIAS=None, NIC_DEFAULT=None, NUMA_NODE=None, OS=None, PCI=None, QEMU_GA_EXEC=None, RAW=None, SECURITY_GROUP_RULE=None, SNAPSHOT=None, SPICE_OPTIONS=None, SUBMIT_ON_HOLD=None, TEMPLATE_ID=None, TM_MAD_SYSTEM=None, TOPOLOGY=None, TPM=None, MEMORY_ENCRYPTION=None, VCPU=None, VCPU_MAX=None, VMGROUP=None, VMID=None, VROUTER_ID=None, VROUTER_KEEPALIVED_ID=None, VROUTER_KEEPALIVED_PASSWORD=None, SCHED_ACTION=None, **kwargs_):
        super(TEMPLATETypeSub, self).__init__(AUTOMATIC_DS_REQUIREMENTS, AUTOMATIC_NIC_REQUIREMENTS, AUTOMATIC_REQUIREMENTS, CLONING_TEMPLATE_ID, CONTEXT, CPU, CPU_COST, DISK, DISK_COST, EMULATOR, FEATURES, HYPERV_OPTIONS, GRAPHICS, VIDEO, IMPORTED, INPUT, MEMORY, MEMORY_COST, MEMORY_MAX, MEMORY_SLOTS, MEMORY_RESIZE_MODE, NIC, NIC_ALIAS, NIC_DEFAULT, NUMA_NODE, OS, PCI, QEMU_GA_EXEC, RAW, SECURITY_GROUP_RULE, SNAPSHOT, SPICE_OPTIONS, SUBMIT_ON_HOLD, TEMPLATE_ID, TM_MAD_SYSTEM, TOPOLOGY, TPM, MEMORY_ENCRYPTION, VCPU, VCPU_MAX, VMGROUP, VMID, VROUTER_ID, VROUTER_KEEPALIVED_ID, VROUTER_KEEPALIVED_PASSWORD, SCHED_ACTION,  **kwargs_)
supermod.TEMPLATEType.subclass = TEMPLATETypeSub
# end class TEMPLATETypeSub


class VIDEOTypeSub(TemplatedType, supermod.VIDEOType):
    def __init__(self, TYPE=None, IOMMU=None, ATS=None, VRAM=None, RESOLUTION=None, **kwargs_):
        super(VIDEOTypeSub, self).__init__(TYPE, IOMMU, ATS, VRAM, RESOLUTION,  **kwargs_)
supermod.VIDEOType.subclass = VIDEOTypeSub
# end class VIDEOTypeSub


class NICTypeSub(TemplatedType, supermod.NICType):
    def __init__(self, anytypeobjs_=None, **kwargs_):
        super(NICTypeSub, self).__init__(anytypeobjs_,  **kwargs_)
supermod.NICType.subclass = NICTypeSub
# end class NICTypeSub


class NIC_ALIASTypeSub(TemplatedType, supermod.NIC_ALIASType):
    def __init__(self, anytypeobjs_=None, **kwargs_):
        super(NIC_ALIASTypeSub, self).__init__(anytypeobjs_,  **kwargs_)
supermod.NIC_ALIASType.subclass = NIC_ALIASTypeSub
# end class NIC_ALIASTypeSub


class QEMU_GA_EXECTypeSub(TemplatedType, supermod.QEMU_GA_EXECType):
    def __init__(self, COMMAND=None, PID=None, RETURN_CODE=None, STATUS=None, STDERR=None, STDIN=None, STDOUT=None, **kwargs_):
        super(QEMU_GA_EXECTypeSub, self).__init__(COMMAND, PID, RETURN_CODE, STATUS, STDERR, STDIN, STDOUT,  **kwargs_)
supermod.QEMU_GA_EXECType.subclass = QEMU_GA_EXECTypeSub
# end class QEMU_GA_EXECTypeSub


class SNAPSHOTTypeSub(TemplatedType, supermod.SNAPSHOTType):
    def __init__(self, ACTION=None, ACTIVE=None, HYPERVISOR_ID=None, NAME=None, SNAPSHOT_ID=None, SYSTEM_DISK_SIZE=None, TIME=None, **kwargs_):
        super(SNAPSHOTTypeSub, self).__init__(ACTION, ACTIVE, HYPERVISOR_ID, NAME, SNAPSHOT_ID, SYSTEM_DISK_SIZE, TIME,  **kwargs_)
supermod.SNAPSHOTType.subclass = SNAPSHOTTypeSub
# end class SNAPSHOTTypeSub


class TPMTypeSub(TemplatedType, supermod.TPMType):
    def __init__(self, MODEL=None, **kwargs_):
        super(TPMTypeSub, self).__init__(MODEL,  **kwargs_)
supermod.TPMType.subclass = TPMTypeSub
# end class TPMTypeSub


class MEMORY_ENCRYPTIONTypeSub(TemplatedType, supermod.MEMORY_ENCRYPTIONType):
    def __init__(self, TYPE=None, **kwargs_):
        super(MEMORY_ENCRYPTIONTypeSub, self).__init__(TYPE,  **kwargs_)
supermod.MEMORY_ENCRYPTIONType.subclass = MEMORY_ENCRYPTIONTypeSub
# end class MEMORY_ENCRYPTIONTypeSub


class HISTORY_RECORDSTypeSub(TemplatedType, supermod.HISTORY_RECORDSType):
    def __init__(self, HISTORY=None, **kwargs_):
        super(HISTORY_RECORDSTypeSub, self).__init__(HISTORY,  **kwargs_)
supermod.HISTORY_RECORDSType.subclass = HISTORY_RECORDSTypeSub
# end class HISTORY_RECORDSTypeSub


class HISTORYTypeSub(TemplatedType, supermod.HISTORYType):
    def __init__(self, OID=None, SEQ=None, HOSTNAME=None, HID=None, CID=None, STIME=None, ETIME=None, VM_MAD=None, TM_MAD=None, DS_ID=None, PLAN_ID=None, ACTION_ID=None, PSTIME=None, PETIME=None, RSTIME=None, RETIME=None, ESTIME=None, EETIME=None, ACTION=None, UID=None, GID=None, REQUEST_ID=None, **kwargs_):
        super(HISTORYTypeSub, self).__init__(OID, SEQ, HOSTNAME, HID, CID, STIME, ETIME, VM_MAD, TM_MAD, DS_ID, PLAN_ID, ACTION_ID, PSTIME, PETIME, RSTIME, RETIME, ESTIME, EETIME, ACTION, UID, GID, REQUEST_ID,  **kwargs_)
supermod.HISTORYType.subclass = HISTORYTypeSub
# end class HISTORYTypeSub


class SNAPSHOTSTypeSub(TemplatedType, supermod.SNAPSHOTSType):
    def __init__(self, ALLOW_ORPHANS=None, CURRENT_BASE=None, DISK_ID=None, NEXT_SNAPSHOT=None, SNAPSHOT=None, **kwargs_):
        super(SNAPSHOTSTypeSub, self).__init__(ALLOW_ORPHANS, CURRENT_BASE, DISK_ID, NEXT_SNAPSHOT, SNAPSHOT,  **kwargs_)
supermod.SNAPSHOTSType.subclass = SNAPSHOTSTypeSub
# end class SNAPSHOTSTypeSub


class SNAPSHOTType1Sub(TemplatedType, supermod.SNAPSHOTType1):
    def __init__(self, ACTIVE=None, CHILDREN=None, DATE=None, ID=None, NAME=None, PARENT=None, SIZE=None, **kwargs_):
        super(SNAPSHOTType1Sub, self).__init__(ACTIVE, CHILDREN, DATE, ID, NAME, PARENT, SIZE,  **kwargs_)
supermod.SNAPSHOTType1.subclass = SNAPSHOTType1Sub
# end class SNAPSHOTType1Sub


class BACKUPSTypeSub(TemplatedType, supermod.BACKUPSType):
    def __init__(self, BACKUP_CONFIG=None, BACKUP_IDS=None, **kwargs_):
        super(BACKUPSTypeSub, self).__init__(BACKUP_CONFIG, BACKUP_IDS,  **kwargs_)
supermod.BACKUPSType.subclass = BACKUPSTypeSub
# end class BACKUPSTypeSub


class BACKUP_CONFIGTypeSub(TemplatedType, supermod.BACKUP_CONFIGType):
    def __init__(self, BACKUP_JOB_ID=None, BACKUP_VOLATILE=None, DISK_IDS=None, FS_FREEZE=None, INCREMENTAL_BACKUP_ID=None, INCREMENT_MODE=None, INTERACTIVE=None, KEEP_LAST=None, LAST_BACKUP_ID=None, LAST_BACKUP_SIZE=None, LAST_BRIDGE=None, LAST_DATASTORE_ID=None, LAST_INCREMENT_ID=None, MODE=None, **kwargs_):
        super(BACKUP_CONFIGTypeSub, self).__init__(BACKUP_JOB_ID, BACKUP_VOLATILE, DISK_IDS, FS_FREEZE, INCREMENTAL_BACKUP_ID, INCREMENT_MODE, INTERACTIVE, KEEP_LAST, LAST_BACKUP_ID, LAST_BACKUP_SIZE, LAST_BRIDGE, LAST_DATASTORE_ID, LAST_INCREMENT_ID, MODE,  **kwargs_)
supermod.BACKUP_CONFIGType.subclass = BACKUP_CONFIGTypeSub
# end class BACKUP_CONFIGTypeSub


class ACLTypeSub(TemplatedType, supermod.ACLType):
    def __init__(self, ID=None, USER=None, RESOURCE=None, RIGHTS=None, ZONE=None, STRING=None, **kwargs_):
        super(ACLTypeSub, self).__init__(ID, USER, RESOURCE, RIGHTS, ZONE, STRING,  **kwargs_)
supermod.ACLType.subclass = ACLTypeSub
# end class ACLTypeSub


class PARAMETERSTypeSub(TemplatedType, supermod.PARAMETERSType):
    def __init__(self, PARAMETER=None, **kwargs_):
        super(PARAMETERSTypeSub, self).__init__(PARAMETER,  **kwargs_)
supermod.PARAMETERSType.subclass = PARAMETERSTypeSub
# end class PARAMETERSTypeSub


class PARAMETERTypeSub(TemplatedType, supermod.PARAMETERType):
    def __init__(self, POSITION=None, TYPE=None, VALUE=None, **kwargs_):
        super(PARAMETERTypeSub, self).__init__(POSITION, TYPE, VALUE,  **kwargs_)
supermod.PARAMETERType.subclass = PARAMETERTypeSub
# end class PARAMETERTypeSub


class EXTRATypeSub(TemplatedType, supermod.EXTRAType):
    def __init__(self, anytypeobjs_=None, **kwargs_):
        super(EXTRATypeSub, self).__init__(anytypeobjs_,  **kwargs_)
supermod.EXTRAType.subclass = EXTRATypeSub
# end class EXTRATypeSub


class TEMPLATEType2Sub(TemplatedType, supermod.TEMPLATEType2):
    def __init__(self, BACKUP_VMS=None, BACKUP_VOLATILE=None, DATASTORE_ID=None, DISK_IDS=None, ERROR=None, EXECUTION=None, FS_FREEZE=None, KEEP_LAST=None, MODE=None, RESET=None, SCHED_ACTION=None, **kwargs_):
        super(TEMPLATEType2Sub, self).__init__(BACKUP_VMS, BACKUP_VOLATILE, DATASTORE_ID, DISK_IDS, ERROR, EXECUTION, FS_FREEZE, KEEP_LAST, MODE, RESET, SCHED_ACTION,  **kwargs_)
supermod.TEMPLATEType2.subclass = TEMPLATEType2Sub
# end class TEMPLATEType2Sub


class PLANTypeSub(TemplatedType, supermod.PLANType):
    def __init__(self, ID=None, STATE=None, ACTION=None, **kwargs_):
        super(PLANTypeSub, self).__init__(ID, STATE, ACTION,  **kwargs_)
supermod.PLANType.subclass = PLANTypeSub
# end class PLANTypeSub


class ACTIONTypeSub(TemplatedType, supermod.ACTIONType):
    def __init__(self, ID=None, VM_ID=None, STATE=None, OPERATION=None, HOST_ID=None, DS_ID=None, TIMESTAMP=None, **kwargs_):
        super(ACTIONTypeSub, self).__init__(ID, VM_ID, STATE, OPERATION, HOST_ID, DS_ID, TIMESTAMP,  **kwargs_)
supermod.ACTIONType.subclass = ACTIONTypeSub
# end class ACTIONTypeSub


class GROUPTypeSub(TemplatedType, supermod.GROUPType):
    def __init__(self, ID=None, NAME=None, TEMPLATE=None, USERS=None, ADMINS=None, **kwargs_):
        super(GROUPTypeSub, self).__init__(ID, NAME, TEMPLATE, USERS, ADMINS,  **kwargs_)
supermod.GROUPType.subclass = GROUPTypeSub
# end class GROUPTypeSub


class QUOTASTypeSub(TemplatedType, supermod.QUOTASType):
    def __init__(self, ID=None, DATASTORE_QUOTA=None, NETWORK_QUOTA=None, VM_QUOTA=None, IMAGE_QUOTA=None, **kwargs_):
        super(QUOTASTypeSub, self).__init__(ID, DATASTORE_QUOTA, NETWORK_QUOTA, VM_QUOTA, IMAGE_QUOTA,  **kwargs_)
supermod.QUOTASType.subclass = QUOTASTypeSub
# end class QUOTASTypeSub


class VLAN_RULESTypeSub(TemplatedType, supermod.VLAN_RULESType):
    def __init__(self, ID=None, RULE=None, **kwargs_):
        super(VLAN_RULESTypeSub, self).__init__(ID, RULE,  **kwargs_)
supermod.VLAN_RULESType.subclass = VLAN_RULESTypeSub
# end class VLAN_RULESTypeSub


class RULETypeSub(TemplatedType, supermod.RULEType):
    def __init__(self, ID=None, SCOPE=None, VNTEMPLATE=None, **kwargs_):
        super(RULETypeSub, self).__init__(ID, SCOPE, VNTEMPLATE,  **kwargs_)
supermod.RULEType.subclass = RULETypeSub
# end class RULETypeSub


class DEFAULT_GROUP_QUOTASTypeSub(TemplatedType, supermod.DEFAULT_GROUP_QUOTASType):
    def __init__(self, DATASTORE_QUOTA=None, NETWORK_QUOTA=None, VM_QUOTA=None, IMAGE_QUOTA=None, **kwargs_):
        super(DEFAULT_GROUP_QUOTASTypeSub, self).__init__(DATASTORE_QUOTA, NETWORK_QUOTA, VM_QUOTA, IMAGE_QUOTA,  **kwargs_)
supermod.DEFAULT_GROUP_QUOTASType.subclass = DEFAULT_GROUP_QUOTASTypeSub
# end class DEFAULT_GROUP_QUOTASTypeSub


class VM_QUOTATypeSub(TemplatedType, supermod.VM_QUOTAType):
    def __init__(self, VM=None, **kwargs_):
        super(VM_QUOTATypeSub, self).__init__(VM,  **kwargs_)
supermod.VM_QUOTAType.subclass = VM_QUOTATypeSub
# end class VM_QUOTATypeSub


class VMType3Sub(TemplatedType, supermod.VMType3):
    def __init__(self, CPU=None, CPU_USED=None, MEMORY=None, MEMORY_USED=None, PCI_DEV=None, PCI_DEV_USED=None, PCI_NIC=None, PCI_NIC_USED=None, RUNNING_CPU=None, RUNNING_CPU_USED=None, RUNNING_MEMORY=None, RUNNING_MEMORY_USED=None, RUNNING_PCI_DEV=None, RUNNING_PCI_DEV_USED=None, RUNNING_PCI_NIC=None, RUNNING_PCI_NIC_USED=None, RUNNING_VMS=None, RUNNING_VMS_USED=None, SYSTEM_DISK_SIZE=None, SYSTEM_DISK_SIZE_USED=None, VMS=None, VMS_USED=None, **kwargs_):
        super(VMType3Sub, self).__init__(CPU, CPU_USED, MEMORY, MEMORY_USED, PCI_DEV, PCI_DEV_USED, PCI_NIC, PCI_NIC_USED, RUNNING_CPU, RUNNING_CPU_USED, RUNNING_MEMORY, RUNNING_MEMORY_USED, RUNNING_PCI_DEV, RUNNING_PCI_DEV_USED, RUNNING_PCI_NIC, RUNNING_PCI_NIC_USED, RUNNING_VMS, RUNNING_VMS_USED, SYSTEM_DISK_SIZE, SYSTEM_DISK_SIZE_USED, VMS, VMS_USED,  **kwargs_)
supermod.VMType3.subclass = VMType3Sub
# end class VMType3Sub


class VLAN_RULESType4Sub(TemplatedType, supermod.VLAN_RULESType4):
    def __init__(self, ID=None, RULE=None, **kwargs_):
        super(VLAN_RULESType4Sub, self).__init__(ID, RULE,  **kwargs_)
supermod.VLAN_RULESType4.subclass = VLAN_RULESType4Sub
# end class VLAN_RULESType4Sub


class RULEType5Sub(TemplatedType, supermod.RULEType5):
    def __init__(self, ID=None, SCOPE=None, VNTEMPLATE=None, **kwargs_):
        super(RULEType5Sub, self).__init__(ID, SCOPE, VNTEMPLATE,  **kwargs_)
supermod.RULEType5.subclass = RULEType5Sub
# end class RULEType5Sub


class DEFAULT_GROUP_QUOTASType6Sub(TemplatedType, supermod.DEFAULT_GROUP_QUOTASType6):
    def __init__(self, DATASTORE_QUOTA=None, NETWORK_QUOTA=None, VM_QUOTA=None, IMAGE_QUOTA=None, **kwargs_):
        super(DEFAULT_GROUP_QUOTASType6Sub, self).__init__(DATASTORE_QUOTA, NETWORK_QUOTA, VM_QUOTA, IMAGE_QUOTA,  **kwargs_)
supermod.DEFAULT_GROUP_QUOTASType6.subclass = DEFAULT_GROUP_QUOTASType6Sub
# end class DEFAULT_GROUP_QUOTASType6Sub


class VM_QUOTAType7Sub(TemplatedType, supermod.VM_QUOTAType7):
    def __init__(self, VM=None, **kwargs_):
        super(VM_QUOTAType7Sub, self).__init__(VM,  **kwargs_)
supermod.VM_QUOTAType7.subclass = VM_QUOTAType7Sub
# end class VM_QUOTAType7Sub


class VMType8Sub(TemplatedType, supermod.VMType8):
    def __init__(self, CLUSTER_IDS=None, CPU=None, CPU_USED=None, MEMORY=None, MEMORY_USED=None, PCI_DEV=None, PCI_DEV_USED=None, PCI_NIC=None, PCI_NIC_USED=None, RUNNING_CPU=None, RUNNING_CPU_USED=None, RUNNING_MEMORY=None, RUNNING_MEMORY_USED=None, RUNNING_PCI_DEV=None, RUNNING_PCI_DEV_USED=None, RUNNING_PCI_NIC=None, RUNNING_PCI_NIC_USED=None, RUNNING_VMS=None, RUNNING_VMS_USED=None, SYSTEM_DISK_SIZE=None, SYSTEM_DISK_SIZE_USED=None, VMS=None, VMS_USED=None, **kwargs_):
        super(VMType8Sub, self).__init__(CLUSTER_IDS, CPU, CPU_USED, MEMORY, MEMORY_USED, PCI_DEV, PCI_DEV_USED, PCI_NIC, PCI_NIC_USED, RUNNING_CPU, RUNNING_CPU_USED, RUNNING_MEMORY, RUNNING_MEMORY_USED, RUNNING_PCI_DEV, RUNNING_PCI_DEV_USED, RUNNING_PCI_NIC, RUNNING_PCI_NIC_USED, RUNNING_VMS, RUNNING_VMS_USED, SYSTEM_DISK_SIZE, SYSTEM_DISK_SIZE_USED, VMS, VMS_USED,  **kwargs_)
supermod.VMType8.subclass = VMType8Sub
# end class VMType8Sub


class TEMPLATEType9Sub(TemplatedType, supermod.TEMPLATEType9):
    def __init__(self, ARGUMENTS=None, ARGUMENTS_STDIN=None, CALL=None, COMMAND=None, LCM_STATE=None, REMOTE=None, RESOURCE=None, STATE=None, **kwargs_):
        super(TEMPLATEType9Sub, self).__init__(ARGUMENTS, ARGUMENTS_STDIN, CALL, COMMAND, LCM_STATE, REMOTE, RESOURCE, STATE,  **kwargs_)
supermod.TEMPLATEType9.subclass = TEMPLATEType9Sub
# end class TEMPLATEType9Sub


class HOOKLOGTypeSub(TemplatedType, supermod.HOOKLOGType):
    def __init__(self, HOOK_EXECUTION_RECORD=None, **kwargs_):
        super(HOOKLOGTypeSub, self).__init__(HOOK_EXECUTION_RECORD,  **kwargs_)
supermod.HOOKLOGType.subclass = HOOKLOGTypeSub
# end class HOOKLOGTypeSub


class HOOK_EXECUTION_RECORDTypeSub(TemplatedType, supermod.HOOK_EXECUTION_RECORDType):
    def __init__(self, HOOK_ID=None, EXECUTION_ID=None, TIMESTAMP=None, ARGUMENTS=None, EXECUTION_RESULT=None, REMOTE_HOST=None, RETRY=None, **kwargs_):
        super(HOOK_EXECUTION_RECORDTypeSub, self).__init__(HOOK_ID, EXECUTION_ID, TIMESTAMP, ARGUMENTS, EXECUTION_RESULT, REMOTE_HOST, RETRY,  **kwargs_)
supermod.HOOK_EXECUTION_RECORDType.subclass = HOOK_EXECUTION_RECORDTypeSub
# end class HOOK_EXECUTION_RECORDTypeSub


class EXECUTION_RESULTTypeSub(TemplatedType, supermod.EXECUTION_RESULTType):
    def __init__(self, COMMAND=None, STDOUT=None, STDERR=None, CODE=None, **kwargs_):
        super(EXECUTION_RESULTTypeSub, self).__init__(COMMAND, STDOUT, STDERR, CODE,  **kwargs_)
supermod.EXECUTION_RESULTType.subclass = EXECUTION_RESULTTypeSub
# end class EXECUTION_RESULTTypeSub


class HOST_SHARETypeSub(TemplatedType, supermod.HOST_SHAREType):
    def __init__(self, MEM_USAGE=None, CPU_USAGE=None, TOTAL_MEM=None, TOTAL_CPU=None, MAX_MEM=None, MAX_CPU=None, RUNNING_VMS=None, VMS_THREAD=None, DATASTORES=None, PCI_DEVICES=None, NUMA_NODES=None, **kwargs_):
        super(HOST_SHARETypeSub, self).__init__(MEM_USAGE, CPU_USAGE, TOTAL_MEM, TOTAL_CPU, MAX_MEM, MAX_CPU, RUNNING_VMS, VMS_THREAD, DATASTORES, PCI_DEVICES, NUMA_NODES,  **kwargs_)
supermod.HOST_SHAREType.subclass = HOST_SHARETypeSub
# end class HOST_SHARETypeSub


class DATASTORESTypeSub(TemplatedType, supermod.DATASTORESType):
    def __init__(self, DISK_USAGE=None, DS=None, FREE_DISK=None, MAX_DISK=None, USED_DISK=None, **kwargs_):
        super(DATASTORESTypeSub, self).__init__(DISK_USAGE, DS, FREE_DISK, MAX_DISK, USED_DISK,  **kwargs_)
supermod.DATASTORESType.subclass = DATASTORESTypeSub
# end class DATASTORESTypeSub


class DSTypeSub(TemplatedType, supermod.DSType):
    def __init__(self, FREE_MB=None, ID=None, TOTAL_MB=None, USED_MB=None, REPLICA_CACHE=None, REPLICA_CACHE_SIZE=None, REPLICA_IMAGES=None, **kwargs_):
        super(DSTypeSub, self).__init__(FREE_MB, ID, TOTAL_MB, USED_MB, REPLICA_CACHE, REPLICA_CACHE_SIZE, REPLICA_IMAGES,  **kwargs_)
supermod.DSType.subclass = DSTypeSub
# end class DSTypeSub


class PCI_DEVICESTypeSub(TemplatedType, supermod.PCI_DEVICESType):
    def __init__(self, PCI=None, **kwargs_):
        super(PCI_DEVICESTypeSub, self).__init__(PCI,  **kwargs_)
supermod.PCI_DEVICESType.subclass = PCI_DEVICESTypeSub
# end class PCI_DEVICESTypeSub


class PCITypeSub(TemplatedType, supermod.PCIType):
    def __init__(self, ADDRESS=None, BUS=None, CLASS=None, CLASS_NAME=None, DEVICE=None, DEVICE_NAME=None, DOMAIN=None, FUNCTION=None, IFNAME=None, NUMA_NODE=None, PROFILES=None, SHORT_ADDRESS=None, SLOT=None, SRIOV=None, SRIOV_NUM=None, TYPE=None, UUID=None, VENDOR=None, VENDOR_NAME=None, VMID=None, **kwargs_):
        super(PCITypeSub, self).__init__(ADDRESS, BUS, CLASS, CLASS_NAME, DEVICE, DEVICE_NAME, DOMAIN, FUNCTION, IFNAME, NUMA_NODE, PROFILES, SHORT_ADDRESS, SLOT, SRIOV, SRIOV_NUM, TYPE, UUID, VENDOR, VENDOR_NAME, VMID,  **kwargs_)
supermod.PCIType.subclass = PCITypeSub
# end class PCITypeSub


class NUMA_NODESTypeSub(TemplatedType, supermod.NUMA_NODESType):
    def __init__(self, NODE=None, **kwargs_):
        super(NUMA_NODESTypeSub, self).__init__(NODE,  **kwargs_)
supermod.NUMA_NODESType.subclass = NUMA_NODESTypeSub
# end class NUMA_NODESTypeSub


class NODETypeSub(TemplatedType, supermod.NODEType):
    def __init__(self, CORE=None, HUGEPAGE=None, MEMORY=None, NODE_ID=None, **kwargs_):
        super(NODETypeSub, self).__init__(CORE, HUGEPAGE, MEMORY, NODE_ID,  **kwargs_)
supermod.NODEType.subclass = NODETypeSub
# end class NODETypeSub


class CORETypeSub(TemplatedType, supermod.COREType):
    def __init__(self, CPUS=None, DEDICATED=None, FREE=None, ID=None, **kwargs_):
        super(CORETypeSub, self).__init__(CPUS, DEDICATED, FREE, ID,  **kwargs_)
supermod.COREType.subclass = CORETypeSub
# end class CORETypeSub


class HUGEPAGETypeSub(TemplatedType, supermod.HUGEPAGEType):
    def __init__(self, PAGES=None, SIZE=None, USAGE=None, **kwargs_):
        super(HUGEPAGETypeSub, self).__init__(PAGES, SIZE, USAGE,  **kwargs_)
supermod.HUGEPAGEType.subclass = HUGEPAGETypeSub
# end class HUGEPAGETypeSub


class MEMORYTypeSub(TemplatedType, supermod.MEMORYType):
    def __init__(self, DISTANCE=None, TOTAL=None, USAGE=None, **kwargs_):
        super(MEMORYTypeSub, self).__init__(DISTANCE, TOTAL, USAGE,  **kwargs_)
supermod.MEMORYType.subclass = MEMORYTypeSub
# end class MEMORYTypeSub


class MONITORINGType10Sub(TemplatedType, supermod.MONITORINGType10):
    def __init__(self, TIMESTAMP=None, ID=None, CAPACITY=None, SYSTEM=None, NUMA_NODE=None, **kwargs_):
        super(MONITORINGType10Sub, self).__init__(TIMESTAMP, ID, CAPACITY, SYSTEM, NUMA_NODE,  **kwargs_)
supermod.MONITORINGType10.subclass = MONITORINGType10Sub
# end class MONITORINGType10Sub


class CAPACITYTypeSub(TemplatedType, supermod.CAPACITYType):
    def __init__(self, FREE_CPU=None, FREE_CPU_FORECAST=None, FREE_CPU_FORECAST_FAR=None, FREE_MEMORY=None, FREE_MEMORY_FORECAST=None, FREE_MEMORY_FORECAST_FAR=None, USED_CPU=None, USED_CPU_FORECAST=None, USED_CPU_FORECAST_FAR=None, USED_MEMORY=None, USED_MEMORY_FORECAST=None, USED_MEMORY_FORECAST_FAR=None, **kwargs_):
        super(CAPACITYTypeSub, self).__init__(FREE_CPU, FREE_CPU_FORECAST, FREE_CPU_FORECAST_FAR, FREE_MEMORY, FREE_MEMORY_FORECAST, FREE_MEMORY_FORECAST_FAR, USED_CPU, USED_CPU_FORECAST, USED_CPU_FORECAST_FAR, USED_MEMORY, USED_MEMORY_FORECAST, USED_MEMORY_FORECAST_FAR,  **kwargs_)
supermod.CAPACITYType.subclass = CAPACITYTypeSub
# end class CAPACITYTypeSub


class SYSTEMTypeSub(TemplatedType, supermod.SYSTEMType):
    def __init__(self, NETRX=None, NETRX_BW=None, NETRX_BW_FORECAST=None, NETRX_BW_FORECAST_FAR=None, NETTX=None, NETTX_BW=None, NETTX_BW_FORECAST=None, NETTX_BW_FORECAST_FAR=None, **kwargs_):
        super(SYSTEMTypeSub, self).__init__(NETRX, NETRX_BW, NETRX_BW_FORECAST, NETRX_BW_FORECAST_FAR, NETTX, NETTX_BW, NETTX_BW_FORECAST, NETTX_BW_FORECAST_FAR,  **kwargs_)
supermod.SYSTEMType.subclass = SYSTEMTypeSub
# end class SYSTEMTypeSub


class NUMA_NODETypeSub(TemplatedType, supermod.NUMA_NODEType):
    def __init__(self, HUGEPAGE=None, MEMORY=None, NODE_ID=None, **kwargs_):
        super(NUMA_NODETypeSub, self).__init__(HUGEPAGE, MEMORY, NODE_ID,  **kwargs_)
supermod.NUMA_NODEType.subclass = NUMA_NODETypeSub
# end class NUMA_NODETypeSub


class HUGEPAGEType11Sub(TemplatedType, supermod.HUGEPAGEType11):
    def __init__(self, FREE=None, SIZE=None, **kwargs_):
        super(HUGEPAGEType11Sub, self).__init__(FREE, SIZE,  **kwargs_)
supermod.HUGEPAGEType11.subclass = HUGEPAGEType11Sub
# end class HUGEPAGEType11Sub


class MEMORYType12Sub(TemplatedType, supermod.MEMORYType12):
    def __init__(self, FREE=None, USED=None, **kwargs_):
        super(MEMORYType12Sub, self).__init__(FREE, USED,  **kwargs_)
supermod.MEMORYType12.subclass = MEMORYType12Sub
# end class MEMORYType12Sub


class SNAPSHOTSType13Sub(TemplatedType, supermod.SNAPSHOTSType13):
    def __init__(self, ALLOW_ORPHANS=None, CURRENT_BASE=None, NEXT_SNAPSHOT=None, SNAPSHOT=None, **kwargs_):
        super(SNAPSHOTSType13Sub, self).__init__(ALLOW_ORPHANS, CURRENT_BASE, NEXT_SNAPSHOT, SNAPSHOT,  **kwargs_)
supermod.SNAPSHOTSType13.subclass = SNAPSHOTSType13Sub
# end class SNAPSHOTSType13Sub


class SNAPSHOTType14Sub(TemplatedType, supermod.SNAPSHOTType14):
    def __init__(self, CHILDREN=None, ACTIVE=None, DATE=None, ID=None, NAME=None, PARENT=None, SIZE=None, **kwargs_):
        super(SNAPSHOTType14Sub, self).__init__(CHILDREN, ACTIVE, DATE, ID, NAME, PARENT, SIZE,  **kwargs_)
supermod.SNAPSHOTType14.subclass = SNAPSHOTType14Sub
# end class SNAPSHOTType14Sub


class BACKUP_INCREMENTSTypeSub(TemplatedType, supermod.BACKUP_INCREMENTSType):
    def __init__(self, INCREMENT=None, **kwargs_):
        super(BACKUP_INCREMENTSTypeSub, self).__init__(INCREMENT,  **kwargs_)
supermod.BACKUP_INCREMENTSType.subclass = BACKUP_INCREMENTSTypeSub
# end class BACKUP_INCREMENTSTypeSub


class INCREMENTTypeSub(TemplatedType, supermod.INCREMENTType):
    def __init__(self, DATE=None, ID=None, PARENT_ID=None, SIZE=None, SOURCE=None, TYPE=None, **kwargs_):
        super(INCREMENTTypeSub, self).__init__(DATE, ID, PARENT_ID, SIZE, SOURCE, TYPE,  **kwargs_)
supermod.INCREMENTType.subclass = INCREMENTTypeSub
# end class INCREMENTTypeSub


class MONITORINGType15Sub(TemplatedType, supermod.MONITORINGType15):
    def __init__(self, CPU=None, DISKRDBYTES=None, DISKRDIOPS=None, DISKWRBYTES=None, DISKWRIOPS=None, DISK_SIZE=None, ID=None, MEMORY=None, NETRX=None, NETTX=None, TIMESTAMP=None, **kwargs_):
        super(MONITORINGType15Sub, self).__init__(CPU, DISKRDBYTES, DISKRDIOPS, DISKWRBYTES, DISKWRIOPS, DISK_SIZE, ID, MEMORY, NETRX, NETTX, TIMESTAMP,  **kwargs_)
supermod.MONITORINGType15.subclass = MONITORINGType15Sub
# end class MONITORINGType15Sub


class DISK_SIZEType16Sub(TemplatedType, supermod.DISK_SIZEType16):
    def __init__(self, ID=None, SIZE=None, **kwargs_):
        super(DISK_SIZEType16Sub, self).__init__(ID, SIZE,  **kwargs_)
supermod.DISK_SIZEType16.subclass = DISK_SIZEType16Sub
# end class DISK_SIZEType16Sub


class AUTH_MADTypeSub(TemplatedType, supermod.AUTH_MADType):
    def __init__(self, AUTHN=None, EXECUTABLE=None, **kwargs_):
        super(AUTH_MADTypeSub, self).__init__(AUTHN, EXECUTABLE,  **kwargs_)
supermod.AUTH_MADType.subclass = AUTH_MADTypeSub
# end class AUTH_MADTypeSub


class AUTH_MAD_CONFTypeSub(TemplatedType, supermod.AUTH_MAD_CONFType):
    def __init__(self, DRIVER_MANAGED_GROUPS=None, DRIVER_MANAGED_GROUP_ADMIN=None, MAX_TOKEN_TIME=None, NAME=None, PASSWORD_CHANGE=None, PASSWORD_REQUIRED=None, **kwargs_):
        super(AUTH_MAD_CONFTypeSub, self).__init__(DRIVER_MANAGED_GROUPS, DRIVER_MANAGED_GROUP_ADMIN, MAX_TOKEN_TIME, NAME, PASSWORD_CHANGE, PASSWORD_REQUIRED,  **kwargs_)
supermod.AUTH_MAD_CONFType.subclass = AUTH_MAD_CONFTypeSub
# end class AUTH_MAD_CONFTypeSub


class DATASTORE_MADTypeSub(TemplatedType, supermod.DATASTORE_MADType):
    def __init__(self, ARGUMENTS=None, EXECUTABLE=None, **kwargs_):
        super(DATASTORE_MADTypeSub, self).__init__(ARGUMENTS, EXECUTABLE,  **kwargs_)
supermod.DATASTORE_MADType.subclass = DATASTORE_MADTypeSub
# end class DATASTORE_MADTypeSub


class DBTypeSub(TemplatedType, supermod.DBType):
    def __init__(self, BACKEND=None, COMPARE_BINARY=None, CONNECTIONS=None, DB_NAME=None, PASSWD=None, PORT=None, SERVER=None, USER=None, TIMEOUT=None, **kwargs_):
        super(DBTypeSub, self).__init__(BACKEND, COMPARE_BINARY, CONNECTIONS, DB_NAME, PASSWD, PORT, SERVER, USER, TIMEOUT,  **kwargs_)
supermod.DBType.subclass = DBTypeSub
# end class DBTypeSub


class DEFAULT_COSTTypeSub(TemplatedType, supermod.DEFAULT_COSTType):
    def __init__(self, CPU_COST=None, DISK_COST=None, MEMORY_COST=None, **kwargs_):
        super(DEFAULT_COSTTypeSub, self).__init__(CPU_COST, DISK_COST, MEMORY_COST,  **kwargs_)
supermod.DEFAULT_COSTType.subclass = DEFAULT_COSTTypeSub
# end class DEFAULT_COSTTypeSub


class DS_MAD_CONFTypeSub(TemplatedType, supermod.DS_MAD_CONFType):
    def __init__(self, DATASTORE_CAPACITY_CHECK=None, MARKETPLACE_ACTIONS=None, NAME=None, PERSISTENT_ONLY=None, REQUIRED_ATTRS=None, **kwargs_):
        super(DS_MAD_CONFTypeSub, self).__init__(DATASTORE_CAPACITY_CHECK, MARKETPLACE_ACTIONS, NAME, PERSISTENT_ONLY, REQUIRED_ATTRS,  **kwargs_)
supermod.DS_MAD_CONFType.subclass = DS_MAD_CONFTypeSub
# end class DS_MAD_CONFTypeSub


class FEDERATIONTypeSub(TemplatedType, supermod.FEDERATIONType):
    def __init__(self, MASTER_ONED=None, MODE=None, SERVER_ID=None, ZONE_ID=None, **kwargs_):
        super(FEDERATIONTypeSub, self).__init__(MASTER_ONED, MODE, SERVER_ID, ZONE_ID,  **kwargs_)
supermod.FEDERATIONType.subclass = FEDERATIONTypeSub
# end class FEDERATIONTypeSub


class HM_MADTypeSub(TemplatedType, supermod.HM_MADType):
    def __init__(self, ARGUMENTS=None, EXECUTABLE=None, **kwargs_):
        super(HM_MADTypeSub, self).__init__(ARGUMENTS, EXECUTABLE,  **kwargs_)
supermod.HM_MADType.subclass = HM_MADTypeSub
# end class HM_MADTypeSub


class HOOK_LOG_CONFTypeSub(TemplatedType, supermod.HOOK_LOG_CONFType):
    def __init__(self, LOG_RETENTION=None, **kwargs_):
        super(HOOK_LOG_CONFTypeSub, self).__init__(LOG_RETENTION,  **kwargs_)
supermod.HOOK_LOG_CONFType.subclass = HOOK_LOG_CONFTypeSub
# end class HOOK_LOG_CONFTypeSub


class IM_MADTypeSub(TemplatedType, supermod.IM_MADType):
    def __init__(self, ARGUMENTS=None, EXECUTABLE=None, NAME=None, THREADS=None, **kwargs_):
        super(IM_MADTypeSub, self).__init__(ARGUMENTS, EXECUTABLE, NAME, THREADS,  **kwargs_)
supermod.IM_MADType.subclass = IM_MADTypeSub
# end class IM_MADTypeSub


class IPAM_MADTypeSub(TemplatedType, supermod.IPAM_MADType):
    def __init__(self, ARGUMENTS=None, EXECUTABLE=None, **kwargs_):
        super(IPAM_MADTypeSub, self).__init__(ARGUMENTS, EXECUTABLE,  **kwargs_)
supermod.IPAM_MADType.subclass = IPAM_MADTypeSub
# end class IPAM_MADTypeSub


class LOGTypeSub(TemplatedType, supermod.LOGType):
    def __init__(self, DEBUG_LEVEL=None, SYSTEM=None, USE_VMS_LOCATION=None, **kwargs_):
        super(LOGTypeSub, self).__init__(DEBUG_LEVEL, SYSTEM, USE_VMS_LOCATION,  **kwargs_)
supermod.LOGType.subclass = LOGTypeSub
# end class LOGTypeSub


class MARKET_MADTypeSub(TemplatedType, supermod.MARKET_MADType):
    def __init__(self, ARGUMENTS=None, EXECUTABLE=None, **kwargs_):
        super(MARKET_MADTypeSub, self).__init__(ARGUMENTS, EXECUTABLE,  **kwargs_)
supermod.MARKET_MADType.subclass = MARKET_MADTypeSub
# end class MARKET_MADTypeSub


class MARKET_MAD_CONFTypeSub(TemplatedType, supermod.MARKET_MAD_CONFType):
    def __init__(self, APP_ACTIONS=None, NAME=None, PUBLIC=None, REQUIRED_ATTRS=None, SUNSTONE_NAME=None, **kwargs_):
        super(MARKET_MAD_CONFTypeSub, self).__init__(APP_ACTIONS, NAME, PUBLIC, REQUIRED_ATTRS, SUNSTONE_NAME,  **kwargs_)
supermod.MARKET_MAD_CONFType.subclass = MARKET_MAD_CONFTypeSub
# end class MARKET_MAD_CONFTypeSub


class RAFTTypeSub(TemplatedType, supermod.RAFTType):
    def __init__(self, BROADCAST_TIMEOUT_MS=None, ELECTION_TIMEOUT_MS=None, LIMIT_PURGE=None, LOG_PURGE_TIMEOUT=None, LOG_RETENTION=None, XMLRPC_TIMEOUT_MS=None, **kwargs_):
        super(RAFTTypeSub, self).__init__(BROADCAST_TIMEOUT_MS, ELECTION_TIMEOUT_MS, LIMIT_PURGE, LOG_PURGE_TIMEOUT, LOG_RETENTION, XMLRPC_TIMEOUT_MS,  **kwargs_)
supermod.RAFTType.subclass = RAFTTypeSub
# end class RAFTTypeSub


class SCHED_MADTypeSub(TemplatedType, supermod.SCHED_MADType):
    def __init__(self, ARGUMENTS=None, EXECUTABLE=None, **kwargs_):
        super(SCHED_MADTypeSub, self).__init__(ARGUMENTS, EXECUTABLE,  **kwargs_)
supermod.SCHED_MADType.subclass = SCHED_MADTypeSub
# end class SCHED_MADTypeSub


class TM_MADTypeSub(TemplatedType, supermod.TM_MADType):
    def __init__(self, ARGUMENTS=None, EXECUTABLE=None, **kwargs_):
        super(TM_MADTypeSub, self).__init__(ARGUMENTS, EXECUTABLE,  **kwargs_)
supermod.TM_MADType.subclass = TM_MADTypeSub
# end class TM_MADTypeSub


class TM_MAD_CONFTypeSub(TemplatedType, supermod.TM_MAD_CONFType):
    def __init__(self, ALLOW_ORPHANS=None, CLONE_TARGET=None, CLONE_TARGET_SHARED=None, CLONE_TARGET_SSH=None, DISK_TYPE=None, DISK_TYPE_SHARED=None, DISK_TYPE_SSH=None, DRIVER=None, DS_MIGRATE=None, DS_LIVE_MIGRATE=None, DS_MIGRATE_SNAP=None, LN_TARGET=None, LN_TARGET_SHARED=None, LN_TARGET_SSH=None, NAME=None, PERSISTENT_SNAPSHOTS=None, SHARED=None, TM_MAD_SYSTEM=None, **kwargs_):
        super(TM_MAD_CONFTypeSub, self).__init__(ALLOW_ORPHANS, CLONE_TARGET, CLONE_TARGET_SHARED, CLONE_TARGET_SSH, DISK_TYPE, DISK_TYPE_SHARED, DISK_TYPE_SSH, DRIVER, DS_MIGRATE, DS_LIVE_MIGRATE, DS_MIGRATE_SNAP, LN_TARGET, LN_TARGET_SHARED, LN_TARGET_SSH, NAME, PERSISTENT_SNAPSHOTS, SHARED, TM_MAD_SYSTEM,  **kwargs_)
supermod.TM_MAD_CONFType.subclass = TM_MAD_CONFTypeSub
# end class TM_MAD_CONFTypeSub


class VLAN_IDSTypeSub(TemplatedType, supermod.VLAN_IDSType):
    def __init__(self, RESERVED=None, START=None, **kwargs_):
        super(VLAN_IDSTypeSub, self).__init__(RESERVED, START,  **kwargs_)
supermod.VLAN_IDSType.subclass = VLAN_IDSTypeSub
# end class VLAN_IDSTypeSub


class VM_MADTypeSub(TemplatedType, supermod.VM_MADType):
    def __init__(self, ARGUMENTS=None, DEFAULT=None, EXECUTABLE=None, NAME=None, SUNSTONE_NAME=None, TYPE=None, KEEP_SNAPSHOTS=None, COLD_NIC_ATTACH=None, LIVE_RESIZE=None, **kwargs_):
        super(VM_MADTypeSub, self).__init__(ARGUMENTS, DEFAULT, EXECUTABLE, NAME, SUNSTONE_NAME, TYPE, KEEP_SNAPSHOTS, COLD_NIC_ATTACH, LIVE_RESIZE,  **kwargs_)
supermod.VM_MADType.subclass = VM_MADTypeSub
# end class VM_MADTypeSub


class VNC_PORTSTypeSub(TemplatedType, supermod.VNC_PORTSType):
    def __init__(self, RESERVED=None, START=None, **kwargs_):
        super(VNC_PORTSTypeSub, self).__init__(RESERVED, START,  **kwargs_)
supermod.VNC_PORTSType.subclass = VNC_PORTSTypeSub
# end class VNC_PORTSTypeSub


class VN_MAD_CONFTypeSub(TemplatedType, supermod.VN_MAD_CONFType):
    def __init__(self, BRIDGE_TYPE=None, NAME=None, **kwargs_):
        super(VN_MAD_CONFTypeSub, self).__init__(BRIDGE_TYPE, NAME,  **kwargs_)
supermod.VN_MAD_CONFType.subclass = VN_MAD_CONFTypeSub
# end class VN_MAD_CONFTypeSub


class VXLAN_IDSTypeSub(TemplatedType, supermod.VXLAN_IDSType):
    def __init__(self, START=None, **kwargs_):
        super(VXLAN_IDSTypeSub, self).__init__(START,  **kwargs_)
supermod.VXLAN_IDSType.subclass = VXLAN_IDSTypeSub
# end class VXLAN_IDSTypeSub


class TEMPLATEType17Sub(TemplatedType, supermod.TEMPLATEType17):
    def __init__(self, DESCRIPTION=None, RULE=None, **kwargs_):
        super(TEMPLATEType17Sub, self).__init__(DESCRIPTION, RULE,  **kwargs_)
supermod.TEMPLATEType17.subclass = TEMPLATEType17Sub
# end class TEMPLATEType17Sub


class RULEType18Sub(TemplatedType, supermod.RULEType18):
    def __init__(self, PROTOCOL=None, RULE_TYPE=None, **kwargs_):
        super(RULEType18Sub, self).__init__(PROTOCOL, RULE_TYPE,  **kwargs_)
supermod.RULEType18.subclass = RULEType18Sub
# end class RULEType18Sub


class SHOWBACKTypeSub(TemplatedType, supermod.SHOWBACKType):
    def __init__(self, VMID=None, VMNAME=None, UID=None, GID=None, UNAME=None, GNAME=None, YEAR=None, MONTH=None, CPU_COST=None, MEMORY_COST=None, DISK_COST=None, TOTAL_COST=None, HOURS=None, RHOURS=None, **kwargs_):
        super(SHOWBACKTypeSub, self).__init__(VMID, VMNAME, UID, GID, UNAME, GNAME, YEAR, MONTH, CPU_COST, MEMORY_COST, DISK_COST, TOTAL_COST, HOURS, RHOURS,  **kwargs_)
supermod.SHOWBACKType.subclass = SHOWBACKTypeSub
# end class SHOWBACKTypeSub


class USERTypeSub(TemplatedType, supermod.USERType):
    def __init__(self, ID=None, GID=None, GROUPS=None, GNAME=None, NAME=None, PASSWORD=None, AUTH_DRIVER=None, ENABLED=None, LOGIN_TOKEN=None, TEMPLATE=None, **kwargs_):
        super(USERTypeSub, self).__init__(ID, GID, GROUPS, GNAME, NAME, PASSWORD, AUTH_DRIVER, ENABLED, LOGIN_TOKEN, TEMPLATE,  **kwargs_)
supermod.USERType.subclass = USERTypeSub
# end class USERTypeSub


class GROUPSTypeSub(TemplatedType, supermod.GROUPSType):
    def __init__(self, ID=None, **kwargs_):
        super(GROUPSTypeSub, self).__init__(ID,  **kwargs_)
supermod.GROUPSType.subclass = GROUPSTypeSub
# end class GROUPSTypeSub


class LOGIN_TOKENTypeSub(TemplatedType, supermod.LOGIN_TOKENType):
    def __init__(self, TOKEN=None, EXPIRATION_TIME=None, EGID=None, **kwargs_):
        super(LOGIN_TOKENTypeSub, self).__init__(TOKEN, EXPIRATION_TIME, EGID,  **kwargs_)
supermod.LOGIN_TOKENType.subclass = LOGIN_TOKENTypeSub
# end class LOGIN_TOKENTypeSub


class QUOTASType19Sub(TemplatedType, supermod.QUOTASType19):
    def __init__(self, ID=None, DATASTORE_QUOTA=None, NETWORK_QUOTA=None, VM_QUOTA=None, IMAGE_QUOTA=None, **kwargs_):
        super(QUOTASType19Sub, self).__init__(ID, DATASTORE_QUOTA, NETWORK_QUOTA, VM_QUOTA, IMAGE_QUOTA,  **kwargs_)
supermod.QUOTASType19.subclass = QUOTASType19Sub
# end class QUOTASType19Sub


class DEFAULT_USER_QUOTASTypeSub(TemplatedType, supermod.DEFAULT_USER_QUOTASType):
    def __init__(self, DATASTORE_QUOTA=None, NETWORK_QUOTA=None, VM_QUOTA=None, IMAGE_QUOTA=None, **kwargs_):
        super(DEFAULT_USER_QUOTASTypeSub, self).__init__(DATASTORE_QUOTA, NETWORK_QUOTA, VM_QUOTA, IMAGE_QUOTA,  **kwargs_)
supermod.DEFAULT_USER_QUOTASType.subclass = DEFAULT_USER_QUOTASTypeSub
# end class DEFAULT_USER_QUOTASTypeSub


class VM_QUOTAType20Sub(TemplatedType, supermod.VM_QUOTAType20):
    def __init__(self, VM=None, **kwargs_):
        super(VM_QUOTAType20Sub, self).__init__(VM,  **kwargs_)
supermod.VM_QUOTAType20.subclass = VM_QUOTAType20Sub
# end class VM_QUOTAType20Sub


class VMType21Sub(TemplatedType, supermod.VMType21):
    def __init__(self, CPU=None, CPU_USED=None, MEMORY=None, MEMORY_USED=None, PCI_DEV=None, PCI_DEV_USED=None, PCI_NIC=None, PCI_NIC_USED=None, RUNNING_CPU=None, RUNNING_CPU_USED=None, RUNNING_MEMORY=None, RUNNING_MEMORY_USED=None, RUNNING_PCI_DEV=None, RUNNING_PCI_DEV_USED=None, RUNNING_PCI_NIC=None, RUNNING_PCI_NIC_USED=None, RUNNING_VMS=None, RUNNING_VMS_USED=None, SYSTEM_DISK_SIZE=None, SYSTEM_DISK_SIZE_USED=None, VMS=None, VMS_USED=None, **kwargs_):
        super(VMType21Sub, self).__init__(CPU, CPU_USED, MEMORY, MEMORY_USED, PCI_DEV, PCI_DEV_USED, PCI_NIC, PCI_NIC_USED, RUNNING_CPU, RUNNING_CPU_USED, RUNNING_MEMORY, RUNNING_MEMORY_USED, RUNNING_PCI_DEV, RUNNING_PCI_DEV_USED, RUNNING_PCI_NIC, RUNNING_PCI_NIC_USED, RUNNING_VMS, RUNNING_VMS_USED, SYSTEM_DISK_SIZE, SYSTEM_DISK_SIZE_USED, VMS, VMS_USED,  **kwargs_)
supermod.VMType21.subclass = VMType21Sub
# end class VMType21Sub


class GROUPSType22Sub(TemplatedType, supermod.GROUPSType22):
    def __init__(self, ID=None, **kwargs_):
        super(GROUPSType22Sub, self).__init__(ID,  **kwargs_)
supermod.GROUPSType22.subclass = GROUPSType22Sub
# end class GROUPSType22Sub


class LOGIN_TOKENType23Sub(TemplatedType, supermod.LOGIN_TOKENType23):
    def __init__(self, TOKEN=None, EXPIRATION_TIME=None, EGID=None, **kwargs_):
        super(LOGIN_TOKENType23Sub, self).__init__(TOKEN, EXPIRATION_TIME, EGID,  **kwargs_)
supermod.LOGIN_TOKENType23.subclass = LOGIN_TOKENType23Sub
# end class LOGIN_TOKENType23Sub


class DEFAULT_USER_QUOTASType24Sub(TemplatedType, supermod.DEFAULT_USER_QUOTASType24):
    def __init__(self, DATASTORE_QUOTA=None, NETWORK_QUOTA=None, VM_QUOTA=None, IMAGE_QUOTA=None, **kwargs_):
        super(DEFAULT_USER_QUOTASType24Sub, self).__init__(DATASTORE_QUOTA, NETWORK_QUOTA, VM_QUOTA, IMAGE_QUOTA,  **kwargs_)
supermod.DEFAULT_USER_QUOTASType24.subclass = DEFAULT_USER_QUOTASType24Sub
# end class DEFAULT_USER_QUOTASType24Sub


class VM_QUOTAType25Sub(TemplatedType, supermod.VM_QUOTAType25):
    def __init__(self, VM=None, **kwargs_):
        super(VM_QUOTAType25Sub, self).__init__(VM,  **kwargs_)
supermod.VM_QUOTAType25.subclass = VM_QUOTAType25Sub
# end class VM_QUOTAType25Sub


class VMType26Sub(TemplatedType, supermod.VMType26):
    def __init__(self, CPU=None, CPU_USED=None, MEMORY=None, MEMORY_USED=None, PCI_DEV=None, PCI_DEV_USED=None, PCI_NIC=None, PCI_NIC_USED=None, RUNNING_CPU=None, RUNNING_CPU_USED=None, RUNNING_MEMORY=None, RUNNING_MEMORY_USED=None, RUNNING_PCI_DEV=None, RUNNING_PCI_DEV_USED=None, RUNNING_PCI_NIC=None, RUNNING_PCI_NIC_USED=None, RUNNING_VMS=None, RUNNING_VMS_USED=None, SYSTEM_DISK_SIZE=None, SYSTEM_DISK_SIZE_USED=None, VMS=None, VMS_USED=None, **kwargs_):
        super(VMType26Sub, self).__init__(CPU, CPU_USED, MEMORY, MEMORY_USED, PCI_DEV, PCI_DEV_USED, PCI_NIC, PCI_NIC_USED, RUNNING_CPU, RUNNING_CPU_USED, RUNNING_MEMORY, RUNNING_MEMORY_USED, RUNNING_PCI_DEV, RUNNING_PCI_DEV_USED, RUNNING_PCI_NIC, RUNNING_PCI_NIC_USED, RUNNING_VMS, RUNNING_VMS_USED, SYSTEM_DISK_SIZE, SYSTEM_DISK_SIZE_USED, VMS, VMS_USED,  **kwargs_)
supermod.VMType26.subclass = VMType26Sub
# end class VMType26Sub


class CLUSTERSTypeSub(TemplatedType, supermod.CLUSTERSType):
    def __init__(self, CLUSTER=None, **kwargs_):
        super(CLUSTERSTypeSub, self).__init__(CLUSTER,  **kwargs_)
supermod.CLUSTERSType.subclass = CLUSTERSTypeSub
# end class CLUSTERSTypeSub


class CLUSTERTypeSub(TemplatedType, supermod.CLUSTERType):
    def __init__(self, ZONE_ID=None, CLUSTER_ID=None, **kwargs_):
        super(CLUSTERTypeSub, self).__init__(ZONE_ID, CLUSTER_ID,  **kwargs_)
supermod.CLUSTERType.subclass = CLUSTERTypeSub
# end class CLUSTERTypeSub


class HOSTSTypeSub(TemplatedType, supermod.HOSTSType):
    def __init__(self, HOST=None, **kwargs_):
        super(HOSTSTypeSub, self).__init__(HOST,  **kwargs_)
supermod.HOSTSType.subclass = HOSTSTypeSub
# end class HOSTSTypeSub


class HOSTTypeSub(TemplatedType, supermod.HOSTType):
    def __init__(self, ZONE_ID=None, HOST_ID=None, **kwargs_):
        super(HOSTTypeSub, self).__init__(ZONE_ID, HOST_ID,  **kwargs_)
supermod.HOSTType.subclass = HOSTTypeSub
# end class HOSTTypeSub


class DATASTORESType27Sub(TemplatedType, supermod.DATASTORESType27):
    def __init__(self, DATASTORE=None, **kwargs_):
        super(DATASTORESType27Sub, self).__init__(DATASTORE,  **kwargs_)
supermod.DATASTORESType27.subclass = DATASTORESType27Sub
# end class DATASTORESType27Sub


class DATASTOREType28Sub(TemplatedType, supermod.DATASTOREType28):
    def __init__(self, ZONE_ID=None, DATASTORE_ID=None, **kwargs_):
        super(DATASTOREType28Sub, self).__init__(ZONE_ID, DATASTORE_ID,  **kwargs_)
supermod.DATASTOREType28.subclass = DATASTOREType28Sub
# end class DATASTOREType28Sub


class VNETSTypeSub(TemplatedType, supermod.VNETSType):
    def __init__(self, VNET=None, **kwargs_):
        super(VNETSTypeSub, self).__init__(VNET,  **kwargs_)
supermod.VNETSType.subclass = VNETSTypeSub
# end class VNETSTypeSub


class VNETTypeSub(TemplatedType, supermod.VNETType):
    def __init__(self, ZONE_ID=None, VNET_ID=None, **kwargs_):
        super(VNETTypeSub, self).__init__(ZONE_ID, VNET_ID,  **kwargs_)
supermod.VNETType.subclass = VNETTypeSub
# end class VNETTypeSub


class ROLESTypeSub(TemplatedType, supermod.ROLESType):
    def __init__(self, ROLE=None, **kwargs_):
        super(ROLESTypeSub, self).__init__(ROLE,  **kwargs_)
supermod.ROLESType.subclass = ROLESTypeSub
# end class ROLESTypeSub


class ROLETypeSub(TemplatedType, supermod.ROLEType):
    def __init__(self, HOST_AFFINED=None, HOST_ANTI_AFFINED=None, ID=None, NAME=None, POLICY=None, VMS=None, **kwargs_):
        super(ROLETypeSub, self).__init__(HOST_AFFINED, HOST_ANTI_AFFINED, ID, NAME, POLICY, VMS,  **kwargs_)
supermod.ROLEType.subclass = ROLETypeSub
# end class ROLETypeSub


class VMType29Sub(TemplatedType, supermod.VMType29):
    def __init__(self, ID=None, UID=None, GID=None, UNAME=None, GNAME=None, NAME=None, LAST_POLL=None, STATE=None, LCM_STATE=None, RESCHED=None, STIME=None, ETIME=None, DEPLOY_ID=None, LOCK=None, TEMPLATE=None, MONITORING=None, USER_TEMPLATE=None, HISTORY_RECORDS=None, **kwargs_):
        super(VMType29Sub, self).__init__(ID, UID, GID, UNAME, GNAME, NAME, LAST_POLL, STATE, LCM_STATE, RESCHED, STIME, ETIME, DEPLOY_ID, LOCK, TEMPLATE, MONITORING, USER_TEMPLATE, HISTORY_RECORDS,  **kwargs_)
supermod.VMType29.subclass = VMType29Sub
# end class VMType29Sub


class TEMPLATEType30Sub(TemplatedType, supermod.TEMPLATEType30):
    def __init__(self, CPU=None, MEMORY=None, VCPU=None, DISK=None, NIC=None, GRAPHICS=None, **kwargs_):
        super(TEMPLATEType30Sub, self).__init__(CPU, MEMORY, VCPU, DISK, NIC, GRAPHICS,  **kwargs_)
supermod.TEMPLATEType30.subclass = TEMPLATEType30Sub
# end class TEMPLATEType30Sub


class NICType31Sub(TemplatedType, supermod.NICType31):
    def __init__(self, anytypeobjs_=None, **kwargs_):
        super(NICType31Sub, self).__init__(anytypeobjs_,  **kwargs_)
supermod.NICType31.subclass = NICType31Sub
# end class NICType31Sub


class MONITORINGType32Sub(TemplatedType, supermod.MONITORINGType32):
    def __init__(self, anytypeobjs_=None, **kwargs_):
        super(MONITORINGType32Sub, self).__init__(anytypeobjs_,  **kwargs_)
supermod.MONITORINGType32.subclass = MONITORINGType32Sub
# end class MONITORINGType32Sub


class HISTORY_RECORDSType33Sub(TemplatedType, supermod.HISTORY_RECORDSType33):
    def __init__(self, HISTORY=None, **kwargs_):
        super(HISTORY_RECORDSType33Sub, self).__init__(HISTORY,  **kwargs_)
supermod.HISTORY_RECORDSType33.subclass = HISTORY_RECORDSType33Sub
# end class HISTORY_RECORDSType33Sub


class HISTORYType34Sub(TemplatedType, supermod.HISTORYType34):
    def __init__(self, OID=None, SEQ=None, HOSTNAME=None, HID=None, CID=None, DS_ID=None, VM_MAD=None, TM_MAD=None, ACTION=None, **kwargs_):
        super(HISTORYType34Sub, self).__init__(OID, SEQ, HOSTNAME, HID, CID, DS_ID, VM_MAD, TM_MAD, ACTION,  **kwargs_)
supermod.HISTORYType34.subclass = HISTORYType34Sub
# end class HISTORYType34Sub


class VNETType35Sub(TemplatedType, supermod.VNETType35):
    def __init__(self, ID=None, UID=None, GID=None, UNAME=None, GNAME=None, NAME=None, LOCK=None, PERMISSIONS=None, CLUSTERS=None, BRIDGE=None, BRIDGE_TYPE=None, STATE=None, PREV_STATE=None, PARENT_NETWORK_ID=None, TEMPLATE_ID=None, VN_MAD=None, PHYDEV=None, VLAN_ID=None, OUTER_VLAN_ID=None, VLAN_ID_AUTOMATIC=None, OUTER_VLAN_ID_AUTOMATIC=None, USED_LEASES=None, VROUTERS=None, UPDATED_VMS=None, OUTDATED_VMS=None, UPDATING_VMS=None, ERROR_VMS=None, TEMPLATE=None, AR_POOL=None, **kwargs_):
        super(VNETType35Sub, self).__init__(ID, UID, GID, UNAME, GNAME, NAME, LOCK, PERMISSIONS, CLUSTERS, BRIDGE, BRIDGE_TYPE, STATE, PREV_STATE, PARENT_NETWORK_ID, TEMPLATE_ID, VN_MAD, PHYDEV, VLAN_ID, OUTER_VLAN_ID, VLAN_ID_AUTOMATIC, OUTER_VLAN_ID_AUTOMATIC, USED_LEASES, VROUTERS, UPDATED_VMS, OUTDATED_VMS, UPDATING_VMS, ERROR_VMS, TEMPLATE, AR_POOL,  **kwargs_)
supermod.VNETType35.subclass = VNETType35Sub
# end class VNETType35Sub


class AR_POOLTypeSub(TemplatedType, supermod.AR_POOLType):
    def __init__(self, AR=None, **kwargs_):
        super(AR_POOLTypeSub, self).__init__(AR,  **kwargs_)
supermod.AR_POOLType.subclass = AR_POOLTypeSub
# end class AR_POOLTypeSub


class ARTypeSub(TemplatedType, supermod.ARType):
    def __init__(self, ALLOCATED=None, AR_ID=None, CVLANS=None, GLOBAL_PREFIX=None, IP=None, MAC=None, NEXT_INDEX=None, PARENT_NETWORK_AR_ID=None, SHARED=None, SIZE=None, TYPE=None, VLAN_ID=None, ULA_PREFIX=None, VN_MAD=None, **kwargs_):
        super(ARTypeSub, self).__init__(ALLOCATED, AR_ID, CVLANS, GLOBAL_PREFIX, IP, MAC, NEXT_INDEX, PARENT_NETWORK_AR_ID, SHARED, SIZE, TYPE, VLAN_ID, ULA_PREFIX, VN_MAD,  **kwargs_)
supermod.ARType.subclass = ARTypeSub
# end class ARTypeSub


class AR_POOLType36Sub(TemplatedType, supermod.AR_POOLType36):
    def __init__(self, AR=None, **kwargs_):
        super(AR_POOLType36Sub, self).__init__(AR,  **kwargs_)
supermod.AR_POOLType36.subclass = AR_POOLType36Sub
# end class AR_POOLType36Sub


class ARType37Sub(TemplatedType, supermod.ARType37):
    def __init__(self, AR_ID=None, CVLANS=None, GLOBAL_PREFIX=None, IP=None, MAC=None, NEXT_INDEX=None, PARENT_NETWORK_AR_ID=None, SHARED=None, SIZE=None, TYPE=None, VLAN_ID=None, ULA_PREFIX=None, VN_MAD=None, MAC_END=None, IP_END=None, IP6_ULA=None, IP6_ULA_END=None, IP6_GLOBAL=None, IP6_GLOBAL_END=None, IP6=None, IP6_END=None, PORT_START=None, PORT_SIZE=None, USED_LEASES=None, LEASES=None, **kwargs_):
        super(ARType37Sub, self).__init__(AR_ID, CVLANS, GLOBAL_PREFIX, IP, MAC, NEXT_INDEX, PARENT_NETWORK_AR_ID, SHARED, SIZE, TYPE, VLAN_ID, ULA_PREFIX, VN_MAD, MAC_END, IP_END, IP6_ULA, IP6_ULA_END, IP6_GLOBAL, IP6_GLOBAL_END, IP6, IP6_END, PORT_START, PORT_SIZE, USED_LEASES, LEASES,  **kwargs_)
supermod.ARType37.subclass = ARType37Sub
# end class ARType37Sub


class LEASESTypeSub(TemplatedType, supermod.LEASESType):
    def __init__(self, LEASE=None, **kwargs_):
        super(LEASESTypeSub, self).__init__(LEASE,  **kwargs_)
supermod.LEASESType.subclass = LEASESTypeSub
# end class LEASESTypeSub


class LEASETypeSub(TemplatedType, supermod.LEASEType):
    def __init__(self, IP=None, IP6=None, IP6_GLOBAL=None, IP6_LINK=None, IP6_ULA=None, MAC=None, VM=None, VNET=None, VROUTER=None, **kwargs_):
        super(LEASETypeSub, self).__init__(IP, IP6, IP6_GLOBAL, IP6_LINK, IP6_ULA, MAC, VM, VNET, VROUTER,  **kwargs_)
supermod.LEASEType.subclass = LEASETypeSub
# end class LEASETypeSub


class ZONETypeSub(TemplatedType, supermod.ZONEType):
    def __init__(self, ID=None, NAME=None, STATE=None, TEMPLATE=None, SERVER_POOL=None, **kwargs_):
        super(ZONETypeSub, self).__init__(ID, NAME, STATE, TEMPLATE, SERVER_POOL,  **kwargs_)
supermod.ZONEType.subclass = ZONETypeSub
# end class ZONETypeSub


class TEMPLATEType38Sub(TemplatedType, supermod.TEMPLATEType38):
    def __init__(self, ENDPOINT=None, **kwargs_):
        super(TEMPLATEType38Sub, self).__init__(ENDPOINT,  **kwargs_)
supermod.TEMPLATEType38.subclass = TEMPLATEType38Sub
# end class TEMPLATEType38Sub


class SERVER_POOLTypeSub(TemplatedType, supermod.SERVER_POOLType):
    def __init__(self, SERVER=None, **kwargs_):
        super(SERVER_POOLTypeSub, self).__init__(SERVER,  **kwargs_)
supermod.SERVER_POOLType.subclass = SERVER_POOLTypeSub
# end class SERVER_POOLTypeSub


class SERVERTypeSub(TemplatedType, supermod.SERVERType):
    def __init__(self, ENDPOINT=None, ID=None, NAME=None, **kwargs_):
        super(SERVERTypeSub, self).__init__(ENDPOINT, ID, NAME,  **kwargs_)
supermod.SERVERType.subclass = SERVERTypeSub
# end class SERVERTypeSub


class TEMPLATEType39Sub(TemplatedType, supermod.TEMPLATEType39):
    def __init__(self, ENDPOINT=None, **kwargs_):
        super(TEMPLATEType39Sub, self).__init__(ENDPOINT,  **kwargs_)
supermod.TEMPLATEType39.subclass = TEMPLATEType39Sub
# end class TEMPLATEType39Sub


class SERVER_POOLType40Sub(TemplatedType, supermod.SERVER_POOLType40):
    def __init__(self, SERVER=None, **kwargs_):
        super(SERVER_POOLType40Sub, self).__init__(SERVER,  **kwargs_)
supermod.SERVER_POOLType40.subclass = SERVER_POOLType40Sub
# end class SERVER_POOLType40Sub


class SERVERType41Sub(TemplatedType, supermod.SERVERType41):
    def __init__(self, ENDPOINT=None, ID=None, NAME=None, STATE=None, TERM=None, VOTEDFOR=None, COMMIT=None, LOG_INDEX=None, FEDLOG_INDEX=None, **kwargs_):
        super(SERVERType41Sub, self).__init__(ENDPOINT, ID, NAME, STATE, TERM, VOTEDFOR, COMMIT, LOG_INDEX, FEDLOG_INDEX,  **kwargs_)
supermod.SERVERType41.subclass = SERVERType41Sub
# end class SERVERType41Sub


def get_root_tag(node):
    tag = supermod.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = None
    rootClass = supermod.GDSClassesMapping.get(tag)
    if rootClass is None and hasattr(supermod, tag):
        rootClass = getattr(supermod, tag)
    return tag, rootClass


def parse(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'HISTORY_RECORDS'
        rootClass = supermod.HISTORY_RECORDS
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
##     if not silence:
##         sys.stdout.write('<?xml version="1.0" ?>\n')
##         rootObj.export(
##             sys.stdout, 0, name_=rootTag,
##             namespacedef_='',
##             pretty_print=True)
    return rootObj


def parseEtree(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'HISTORY_RECORDS'
        rootClass = supermod.HISTORY_RECORDS
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    mapping = {}
    rootElement = rootObj.to_etree(None, name_=rootTag, mapping_=mapping)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
##     if not silence:
##         content = etree_.tostring(
##             rootElement, pretty_print=True,
##             xml_declaration=True, encoding="utf-8")
##         sys.stdout.write(content)
##         sys.stdout.write('\n')
    return rootObj, rootElement, mapping, reverse_mapping


def parseString(inString, silence=False):
    if sys.version_info.major == 2:
        from StringIO import StringIO
    else:
        from io import BytesIO as StringIO
    parser = None
    rootNode= parsexmlstring_(inString, parser)
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'HISTORY_RECORDS'
        rootClass = supermod.HISTORY_RECORDS
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        rootNode = None
##     if not silence:
##         sys.stdout.write('<?xml version="1.0" ?>\n')
##         rootObj.export(
##             sys.stdout, 0, name_=rootTag,
##             namespacedef_='')
    return rootObj


def parseLiteral(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'HISTORY_RECORDS'
        rootClass = supermod.HISTORY_RECORDS
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
##     if not silence:
##         sys.stdout.write('#from supbind import *\n\n')
##         sys.stdout.write('from . import supbind as model_\n\n')
##         sys.stdout.write('rootObj = model_.rootClass(\n')
##         rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
##         sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    parse(infilename)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()
