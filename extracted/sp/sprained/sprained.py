#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 K. Richard Pixley.
# See LICENSE for details.
#
# Time-stamp: <02-Mar-2010 13:07:03 PST by rich@noir.com>

"""
Sprained is an integration between U{SpreadModule<http://pypi.python.org/pypi/SpreadModule>},
which is a python interface to U{the spread toolkit<http://spread.org>},
which provides an implementation of virtual synchrony, and U{twisted<http://twistedmatrix.com>},
which provides an asynchronous programming structure.

Please note that sprained has nothing to do with spreadsheets nor does
it have anything to do with the other twisted project with the
unfortunate name of"spread", (which has nothing to do with either
spreadsheets nor virtual synchrony).
"""

from __future__ import unicode_literals

__docformat__ = 'epytext'

import os

from collections import deque

import spread

from metaserializer import SerializerFromMagic
from metaserializer.msyaml import YAML

serializer = YAML()

from zope.interface import implements

from twisted.internet.interfaces import IWriteDescriptor, IReadDescriptor, IReadWriteDescriptor, IReactorFDSet
from twisted.internet.error import ConnectionDone
from twisted.internet.defer import Deferred, AlreadyCalledError

valid_message_types = set(range(1<<16))
valid_message_reasons = set((spread.CAUSED_BY_JOIN,
                             spread.CAUSED_BY_LEAVE,
                             spread.CAUSED_BY_DISCONNECT,
                             spread.CAUSED_BY_NETWORK,
                             0)) # zero represents transitional membership messages

class RegularMsgCopy(object):
    """
    This class stands in for copies of spread.RegularMsgType since
    that type can't be copied or subclassed.
    """
    def __init__(self, sender, groups, message, msg_type, endian):
        assert (sender == None) or isinstance(sender, bytes)
        self.sender = sender

        assert isinstance(groups, tuple) and all([((g == None) or isinstance(g, bytes)) for g in groups])
        self.groups = groups

        assert isinstance(message, bytes)
        self.message = message

        assert msg_type in valid_message_types
        self.msg_type = msg_type

        assert isinstance(endian, int)
        self.endian = endian

    @staticmethod
    def copy(message):
        assert isinstance(message, RegularMsgCopy) or isinstance(message, spread.RegularMsgType)
        return RegularMsgCopy(message.sender,
                              message.groups,
                              message.message,
                              message.msg_type,
                              message.endian)

    def flatten(self):
        """
        """
        return {'__type__': 'RegularMsgCopy',
                'sender': self.sender,
                'groups': self.groups,
                'message': self.message,
                'msg_type': self.msg_type,
                'endian': self.endian,
                }

    @staticmethod
    def unflatten(d):
        return RegularMsgCopy(d['sender'],
                              d['groups'],
                              d['message'],
                              d['msg_type'],
                              d['endian'])

class MembershipMsgCopy(object):
    """
    This class stands in for copies of spread.MembershipMsgType since
    that type can't be copied or subclassed.
    """
    ### group_id is intentionally omitted.  This is an opaque type
    ### which is apparently never consumed.  And attempting to
    ### serialize it with pyyaml causes dumps.
    def __init__(self, reason, group, members, extra):
        assert reason in valid_message_reasons
        self.reason = reason

        assert (group == None) or isinstance(group, bytes)
        self.group = group

        assert isinstance(members, tuple) and all([((m == None) or isinstance(m, bytes)) for m in members])
        self.members = members

        assert isinstance(extra, tuple) and all([((m == None) or isinstance(m, bytes)) for m in extra])
        self.extra = extra

    @staticmethod
    def copy(message):
        assert isinstance(message, MembershipMsgCopy) or isinstance(message, spread.MembershipMsgType)

        return MembershipMsgCopy(message.reason,
                                 message.group,
                                 message.members,
                                 message.extra)

    def flatten(self):
        """
        """
        return {'__type__': 'MembershipMsgCopy',
                'reason': self.reason,
                'group': self.group,
                # 'group_id': self.group_id,
                'members': self.members,
                'extra': self.extra,
                }

    @staticmethod
    def unflatten(d):
        return MembershipMsgCopy(d['reason'],
                                 d['group'],
                                 d['members'],
                                 d['extra'])

class MsgCopy(object):
    """
    Factory for copying MsgType messages.
    """
    def __new__(cls, message):
        if isinstance(message, spread.RegularMsgType) or isinstance(message, RegularMsgCopy):
            return RegularMsgCopy.copy(message)
        elif isinstance(message, spread.MembershipMsgType) or isinstance(message, MembershipMsgCopy):
            return MembershipMsgCopy.copy(message)
        else:
            raise NotImplementedError, 'Not implemented for class {0}'.format(message.__class__.__name__)

    @staticmethod
    def unflatten(d):
        if d['__type__'] == 'RegularMsgCopy':
            return RegularMsgCopy.unflatten(d)
        else:
            return MembershipMsgCopy.unflatten(d)

# @ivar queuemax: describes the maximum number of outgoing messages
# we allow in the queue.  We raise QueueOverflow if we hit this.
# @type queuemax: C{int}
queuemax = 409600

class QueueOverflow(Exception):
    """
    raised when L{queuemax} is reached.
    """
    pass

class Recorder(object):
    """
    Represents a record descriptor.
    """
    implements(IWriteDescriptor)

    _defaultSerializer = YAML()

    # FIXME: I'm not sure if input should be buffered or not.  Dunno
    # if buffering works on O_NONBLOCK or even whether it matters in
    # twisted.
    def __init__(self, mailbox, filename):
        assert isinstance(mailbox, Mailbox)
        self.mailbox = mailbox

        assert isinstance(filename, unicode)
        self._filename = filename

        self._outqueue = deque([])
        self._input_file = None

        appending = os.path.exists(self._filename)
        self._fileno = os.open(self._filename, os.O_RDWR | os.O_NONBLOCK | os.O_CREAT)
        if appending:
            magic = os.read(self._fileno, 1)
            self._serializer = SerializerFromMagic(magic)
            os.lseek(self._fileno, 0, os.SEEK_END) # append to any existing file
        else:
            self._serializer = self._defaultSerializer
            if os.write(self._fileno, self._serializer.magic) != 1:
                raise Exception('write failed')

    def encode(self, object):
        pass

    def decode(self, inputfile):
        pass

    def fileno(self):
        return self._fileno

    def write(self, message):
        if len(self._outqueue) >= queuemax:
            raise QueueOverflow

        assert(len(self._outqueue) < queuemax)

        if not self._outqueue:
            self.mailbox.reactor.addWriter(self)

        self._outqueue.append(message)

    def doWrite(self):
        message = MsgCopy(self._outqueue.popleft())
        us = self.mailbox.private_group()

        if isinstance(message, RegularMsgCopy):
            if message.sender == us:
                message.sender = None

            # lists not sets here because I want to preserve order and
            # frequency.
            grouplist = list(message.groups)
            while us in grouplist:
                grouplist[grouplist.index(us)] = None
            message.groups = tuple(grouplist)

        elif isinstance(message, MembershipMsgCopy):
            grouplist = list(message.members)
            while us in grouplist:
                grouplist[grouplist.index(us)] = None
            message.members = tuple(grouplist)

            grouplist = list(message.extra)
            while us in grouplist:
                grouplist[grouplist.index(us)] = None
            message.extra = tuple(grouplist)

        else:
            raise NotImplementedError, 'unrecognized type {0}'.format(message.__class__.__name__)

        encoded = self._serializer.dumpb(message.flatten())
        bytes_sent = os.write(self._fileno, encoded)

        if bytes_sent != len(encoded):
            raise Exception('bad write {0}/{1}'.format(bytes_sent, len(encoded)))

        if not self._outqueue:
            self.mailbox.reactor.removeWriter(self)

        return None

    def connectionLost(self, whatever):
        os.close(self._fileno)

    def logPrefix(self):
        return self.__class__.__name__


class Player(object):
    """
    Represents a playback descriptor.
    """
    implements(IReadDescriptor)

    def __init__(self, mailbox, filename):
        """
        @param mailbox: the mailbox associated with this Player.
        @type mailbox: L{Mailbox}

        @param filename: the filename to be read by this Player.
        @type filename: C{unicode}
        """
        assert isinstance(mailbox, Mailbox)
        self.mailbox = mailbox

        assert isinstance(filename, unicode)
        self._filename = filename

        self._fileno = os.open(filename, os.O_RDONLY | os.O_NONBLOCK)
        magic = os.read(self._fileno, 1)
        self._serializer = SerializerFromMagic(magic)

        self._input_file = os.fdopen(self._fileno, 'rb')
        self.mailbox.reactor.addReader(self)
        
    def fileno(self):
        return self._fileno

    def connectionLost(self, whatever):
        self._input_file.close()
        # when the player is done, the mailbox is done.
        self.mailbox.reactor.callLater(0, self.mailbox.reactor.stop)

    def logPrefix(self):
        return self.__class__.__name__

    def doRead(self):
        message = self._serializer.load(self._input_file)

        if message == None:
            return ConnectionDone

        message = MsgCopy.unflatten(message)
        us = self.mailbox.private_group()

        if isinstance(message, RegularMsgCopy):
            if message.sender == None:
                message.sender = us

            while None in message.groups:
                message.groups[message.groups.index(None)] = us

        elif isinstance(message, MembershipMsgCopy):
            while None in message.members:
                message.members[message.members.index(None)] = us

            while None in message.extra:
                message.extra[message.extra.index(None)] = us
 
        else:
            raise NotImplementedError, 'unrecognized type {0}'.format(message.__class__.__name__)

        self.mailbox._dispatch(message)


class Mailbox(object):
    """
    U{Twisted<http://twistedmatrix.com>} calls this a factory, except
    that factories listen on a socket and spawn new instances of
    protocols.
    U{SpreadModule<http://pypi.python.org/pypi/SpreadModule>} calls it
    a U{spread.MailboxType}, which is closer to relevant for Sprained.

    This object corresponds to a single connection to a spread server.
    It's primary job is to manage that connection which includes
    making it, breaking it, sending outgoing messages, and dispatching
    incoming messages on to the appropriate subscribers, (which are
    somewhat analogous to twisted's protocols).

    @ivar reactor:
    @type reactor: an object which implements L{twisted.internet.interfaces.IReactorFDSet}

    @ivar _spread_name:
    @type _spread_name: see L{__init__}

    @ivar _priority:
    @type _priority: see L{__init__}

    @ivar _membership:
    @type _membership: see L{__init__}

    @ivar _groups: a C{dict} by C{unicode} group name to which this
    object is listening of C{dict}.  The subC{dict}s are by class,
    (L{RegularMsgCopy} or L{MembershipMsgCopy}), of C{sets} of
    callbacks.

    @type _groups: C{dict}

    @ivar _outqueue:
    @type _outqueue: a C{collection.deque} of C{bytes} messages waiting to be sent.

    @ivar _mb:
    @type _mb: the underlying L{spread.MailboxType} for this connection.
    """

    implements(IReadWriteDescriptor)

    def __init__(self,
                 myreactor,
                 spread_name='{0}'.format(spread.DEFAULT_SPREAD_PORT),
                 private_name='',
                 priority=0,
                 membership=True,
                 record='',
                 playback=''
                 ):
        """
        Some of these derive directly from L{SpreadModule}.

        Currently known formats for recording/playback to/from a log file are:

        - L{Mailbox.RecordingFormat.Pickle} for the use of the python standard L{pickle} module.
        - L{Mailbox.RecordingFormat.JSON} for the use of the python standard L{json} module.

        @param myreactor:
        @type myreactor: an object which implements L{twisted.internet.interfaces.IReactorFDSet}

        @param spread_name:
        @type spread_name: a C{unicode} specifying the port and host of
        the spread daemon to use, of the form"<port>@<hostname>" or
        "<port>", where <port> is an integer port number (typically the constant
        DEFAULT_SPREAD_PORT) represented as a string, and <hostname> specifies
        the host where the daemon runs, typically"localhost".  The default is the
        default Spread port and host.

        @param private_name:
        @type private_name: a C{unicode} specifying the name under which this client is to be
        known; the default is a private name made up by Spread

        @param priority:
        @type priority: C{int} - 0 or 1, currently unused; default 0

        @param membership:
        @type membership: C{bool} - if true, then request receipt of membership change messages.

        @param record: when this is set, it is expected to be a valid
        file name.  All incoming messages are both dispatched as usual
        as well as being appended to this log file.  The file is
        created if it does not exist.

        @type record: C{unicode}

        @param playback: when this is set, it is expected to be a
        valid, existing file name.  Instead of reading messages from
        the network as usual, messages are read from this file and
        then dispatched.
 
        @type playback: C{unicode}
        """

        assert IReactorFDSet.providedBy(myreactor)
        self.reactor = myreactor

        assert isinstance(spread_name, unicode)
        self._spread_name = spread_name

        assert isinstance(private_name, unicode)

        assert isinstance(priority, int)
        self._priority = priority

        assert isinstance(membership, bool)
        if membership:
            self._membership = 1
        else:
            self._membership = 0

        self._groups = {}
        self._outqueue = deque([])

        assert isinstance(record, unicode)
        self._record = record

        self._mb = spread.connect(self._spread_name, private_name, self._priority, self._membership)

        if self._record:
            self._recorder = Recorder(self, self._record)

        assert isinstance(playback, unicode)
        self._playback = playback

        if self._playback:
            self._playbacker = Player(self, self._playback)
        else:
            self.reactor.addReader(self)

        self._onClose = Deferred()

    ### A Mailbox can end in either of two ways.  Either it is ended
    ### gracefully with Mailbox.rm(), in which case the reactor should
    ### continue to run.  OR the reactor is stopped, in which case it
    ### will call connectionLost on us and the reactor will be useless
    ### thereafter.  connectionLost will also be called if we lose our
    ### connection to our spread server(?)

    def _shutdown(self):
        if not self._playback:
            self.reactor.removeReader(self)

    def rm(self):
        self._shutdown()
        self._mb.disconnect()
        self._onClose.callback(None)

    def connectionLost(self, exception):
        """
        called by the reactor when it is time to relinquish a connection.
        """
        self._shutdown()

        if self._membership:
            # FIXME: may need to wait for disconnect message
            pass

    def onClose(self):
        """
        Return a L{Deferred} which will be called when this mailbox is closed.
        """
        return self._onClose

    def fileno(self):
        """
        return the file descriptor of the underlying L{spread.MailboxType}
        """
        return self._mb.fileno()

    def private_group(self):
        """
        return the the private group name assigned to this connection by the spread
        daemon (see the SP_connect man page).
        """
        return bytes(self._mb.private_group)

    def logPrefix(self):
        """
        a requirement for implementing L{IReadWriteDescriptor}.  I'm not
        sure when it's used.
        """
        return self.__class__.__name__

    def doRead(self):
        """
        called from the reactor when our file descriptor is readable.
        """
        incoming = self._mb.receive()

        # copy it immediately.  This allows others to copy easily
        # later and potentially to subclass.
        incoming = MsgCopy(incoming)

        return self._dispatch(incoming)


    def _dispatch(self, incoming):
        """
        dispatch a message.
        """

        if self._record:
            self._recorder.write(incoming)

        retval = False

        if isinstance(incoming, RegularMsgCopy):
            for group in incoming.groups:
                if ((group in self._groups)
                    and (RegularMsgCopy in self._groups[group])):
                    for (callback, args, kwargs) in self._groups[group][RegularMsgCopy].copy():
                        kwargs = serializer.loadb(kwargs)
                        new = callback(incoming, *args, **kwargs)
                        retval = retval or new
        elif isinstance(incoming, MembershipMsgCopy):
            if ((incoming.group in self._groups)
                and (MembershipMsgCopy in self._groups[incoming.group])):
                for (callback, args, kwargs) in self._groups[incoming.group][MembershipMsgCopy].copy():
                    kwargs = serializer.loadb(kwargs)
                    new = callback(incoming, *args, **kwargs)
                    retval = retval or new
        else:
            raise Exception('unrecognized message type')

        return retval


    def multicast(self, service, groups, outgoing='', msg_type=0):
        """
        send a message.

        @param service:
        @type service: one of the integer constants (see the SP_multicast man
        page for their meaning): L{spread.UNRELIABLE_MESS},
        L{spread.RELIABLE_MESS}, L{spread.FIFO_MESS}, L{spread.CAUSAL_MESS},
        L{spread.AGREED_MESS}, L{spread.SAFE_MESS}.

        @param groups:
        @type groups: a C{tuple} of C{bytes} of group names.

        @param outgoing: the outgoing message.
        @type outgoing: C{unicode}

        @param msg_type:
        @type msg_type: C{int} (must be 16-bit int)
        """
        
        self.validateGroups(groups)
        if len(self._outqueue) >= queuemax:
            raise QueueOverflow
        assert(len(self._outqueue) < queuemax)

        if not self._outqueue:
            self.reactor.addWriter(self)

        self._outqueue.append((service, groups, outgoing, msg_type))

    def doWrite(self):
        """
        called from the reactor when our file descriptor is writable and we've
        been asked to be notified of that fact.
        """
        q = self._outqueue.popleft()
        self._mb.multigroup_multicast(*q)

        if not self._outqueue:
            self.reactor.removeWriter(self)

        return None

    @staticmethod
    def validateGroups(groups):
        """
        validate a tuple of groups using assert
        """
        assert(isinstance(groups, tuple))
        for g in groups:
            assert(isinstance(g, bytes))

    def regularSubscribe(self, groups, callback, *args, **kwargs):
        """
        add a callback to the set of callables which will be called on
        receipt of regular messages on the specified groups.

        @param groups:
        @type groups: a C{tuple} of C{bytes} group names.

        @param callback:
        @type callback: a callable.

        @param args:
        @param kwargs:
        """
        self.validateGroups(groups)
        assert callable(callback)

        for group in groups:
            needJoin = False

            if group not in self._groups:
                self._groups[group] = {}
                needJoin = True

            if RegularMsgCopy not in self._groups[group]:
                self._groups[group][RegularMsgCopy] = set()

            self._groups[group][RegularMsgCopy] |= set(((callback, args, serializer.dumpb(kwargs)),))

            if (group != self.private_group()):
                if (needJoin
                    or ((MembershipMsgCopy in self._groups[group])
                        and all(isinstance(s, self._LastHurrah) for s in self._groups[group][MembershipMsgCopy]))):
                    self._mb.join(group)

    def membershipSubscribe(self, groups, callback, *args, **kwargs):
        """
        add a callback to the set of callables which will be called on
        receipt of membership messages on the specified groups.

        @param groups:
        @type groups: a C{tuple} of C{bytes} group names.

        @param callback:
        @type callback: a callable.

        @param args:
        @param kwargs:
        """
        self.validateGroups(groups)
        assert callable(callback)

        for group in groups:
            needJoin = False

            if group not in self._groups:
                self._groups[group] = {}
                needJoin = True

            if MembershipMsgCopy not in self._groups[group]:
                self._groups[group][MembershipMsgCopy] = set()

            if all(isinstance(s, self._LastHurrah) for s in self._groups[group][MembershipMsgCopy]):
                needJoin = True

            self._groups[group][MembershipMsgCopy] |= set(((callback, args, serializer.dumpb(kwargs)),))

            if ((group != self.private_group())
                and needJoin):
                self._mb.join(group)

    def regularUnsubscribe(self, groups, callback, *args, **kwargs):
        """
        remove a callback from the set of objects to receive regular
        messages on the specified groups.

        @param groups:
        @type groups: a C{tuple} of C{bytes} group names.

        @param callback:
        @type callback: a callable.

        @param args:
        @param kwargs:
        """
        self.validateGroups(groups)
        assert callable(callback)

        for group in groups:
            assert group in self._groups
            assert RegularMsgCopy in self._groups[group]

            self._groups[group][RegularMsgCopy] -= set(((callback, args, serializer.dumpb(kwargs)),))

            # if no more listeners, then delete entry
            if not self._groups[group][RegularMsgCopy]:
                del self._groups[group][RegularMsgCopy]

            # if no more entries, then unsubscribe.  (In this case, no
            # one is listening for membership messages so no last
            # hurrah needed.)
            if not self._groups[group]:
                if group != self.private_group():
                    self._mb.leave(group)

                del self._groups[group]

    def _lastHurrah(self, incoming, group, lastOneOutTheDoor):
        if ((incoming.reason == spread.CAUSED_BY_LEAVE)
            and (incoming.group == group)):
            (callback, args, kwargs) = lastOneOutTheDoor
            kwargs = serializer.loadb(kwargs)
            callback(*args, **kwargs)
            self.unsubscribeMembership((group,), self._lastHurrah, group, lastOneOutTheDoor)

    def membershipUnsubscribe(self, groups, callback, *args, **kwargs):
        """
        remove a callback from the set of objects to receive
        membership messages on the specified groups.

        @param groups:
        @type groups: a C{tuple} of C{bytes} group names.

        @param callback:
        @type callback: a callable.

        @param args:
        @param kwargs:
        """
        self.validateGroups(groups)
        assert callable(callback)

        for group in groups:
            assert group in self._groups
            assert MembershipMsgCopy in self._groups[group]

            lastOneOutTheDoor = (callback, args, serializer.dumpb(kwargs))
            self._groups[group][MembershipMsgCopy] -= set(lastOneOutTheDoor)

            # if no more listeners, then delete entry
            if not self._groups[group][MembershipMsgCopy]:
                del self._groups[group][MembershipMsgCopy]

            # if no more listeners of any type, then set up for a last hurrah
            if not self._groups[group]:
                if group != self.private_group():
                    if callback != self._lastHurrah:
                        self.subscribe((group,), self._lastHurrah, group, lastOneOutTheDoor)
                    self._mb.leave(group)
                else:
                    del self._groups[group]

    def private_name(self):
        return self._mb.private_name


class DispatchingSubscriber(object):
    """
    This object represents a conventional L{Mailbox} subscriber.  It
    dispatches messages received on specific groups on the basis of
    L{RegularMsgCopy.msg_type} or L{MembershipMsgCopy.reason}.

    @ivar mailbox:
    @type mailbox: L{Mailbox}

    @ivar _regularCallbacks:
    @type _regularCallbacks: a C{dict} of C{set} by callback where the
    C{set} describes the L{RegularMsgCopy.msg_type}s of interest.

    @ivar _membershipCallbacks:
    @type _membershipCallbacks: a C{dict} of C{set} by callback where the
    C{set} describes the L{MembershipMsgCopy.reasons}s of interest.
    """

    # LATER: it might be more efficient here to keep a list of
    # (ranges, [callback, callback]) but it would also be more work.

    def __init__(self, mailbox, groups):
        """
        @param mailbox:
        @type mailbox: L{Mailbox}

        @param groups:
        @type groups: a C{tuple} of C{bytes} of group names.
        """

        assert isinstance(mailbox, Mailbox)
        self.mailbox = mailbox

        self.mailbox.validateGroups(groups)
        self._groups = groups

        self._regularCallbacks = []
        self._membershipCallbacks = []

        self._onClose = Deferred()
        
        # LATER: might want to add supersets here so we can quickly
        # tell if we have anything to dispatch.

        self.mailbox.regularSubscribe(groups, self.regularReceive)
        self.mailbox.membershipSubscribe(groups, self.membershipReceive)

    def onClose(self):
        return self._onClose

    def rm(self):
        # order is important here in order to obviate the last hurrah.
        self.mailbox.membershipUnsubscribe(self._groups, self.membershipReceive)
        self.mailbox.regularUnsubscribe(self._groups, self.regularReceive)

        self._onClose.callback(None)

    def _validate(self):
        """
        Validate everything we can about this object.  Intended for
        debugging and development, not production use.
        """
        assert isinstance(self.mailbox, Mailbox)
        self.mailbox.validateGroups(self._groups)

        assert isinstance(self._regularCallbacks, list)
        for (key, types) in self._regularCallbacks:
            assert isinstance(types, set)
            assert types <= valid_message_types
            (callback, args, kwargs) = key
            assert callable(callback)
            assert isinstance(args, tuple)
            assert isinstance(dict, kwargs)

        assert isinstance(self._membershipCallbacks, list)
        for (key, types) in self._membershipCallbacks:
            assert isinstance(types, set)
            assert types <= valid_message_reasons
            (callback, args, kwargs) = key
            assert callable(callback)
            assert isinstance(args, tuple)
            assert isinstance(dict, kwargs)

    def _validateKey(self, key):
        assert isinstance(key, tuple)
        assert len(key) is 3
        (callback, args, kwargs) = key
        assert callable(callback)
        assert isinstance(args, tuple)
        assert isinstance(kwargs, dict)

    def _find(self, target_list, target_key):
        """
        Search the list for an entry that matches key.  Return the entry or None.
        
        @param target_list:
        @type target_list: either L{self._regularCallbacks} or L{self._membershipCallbacks}.

        @param target_key:
        @type target_key: a C{tuple} of (callback, args, kwargs).
        """
        assert (target_list is self._regularCallbacks) or (target_list is self._membershipCallbacks)
        self._validateKey(target_key)

        for i in target_list:
            (key, values) = i
            if key == target_key:
                return i

        return None

    def _register(self, registry, callback, domain, args, kwargs):
        assert (registry is self._regularCallbacks) or (registry is self._membershipCallbacks)
        assert callable(callback)
        assert isinstance(domain, set)

        key = (callback, args, kwargs)
        entry = self._find(registry, key)
        if entry:
            (key, types) = entry
            types |= domain
        else:
            registry.append((key, domain.copy()))


    def _unregister(self, registry, callback, domain, args, kwargs):
        assert (registry is self._regularCallbacks) or (registry is self._membershipCallbacks)
        assert callable(callback)
        assert isinstance(domain, set)

        key = (callback, args, kwargs)
        entry = self._find(registry, key)
        if entry:
            (key, types) = entry
            types -= domain
            if not types:
                registry.remove(entry)
        

    def regularRegister(self, callback, msg_range, *args, **kwargs):
        """
        Add a callback to the set of callbacks which will be called on
        receipt of L{RegularMsgCopy}s on our groups with
        L{RegularMsgCopy.msg_type}s in the specified msg_range.

        Arguments are the same as for L{unregisterRegular}.

        @param callback:
        @type callback: callable object with args (message, ...)

        @param msg_range:
        @type msg_range: either a C{2-tuple} of the low and high message type
        numbers, (inclusive), or a C{set} of L{RegularMsgCopy.msg_type}s.
        """
        assert callable(callback)
        assert isinstance(msg_range, (set, tuple))

        if isinstance(msg_range, tuple):
            msg_range = set(xrange(msg_range[0], msg_range[1] + 1))

        self._register(self._regularCallbacks, callback, msg_range, args, kwargs)

    def regularUnregister(self, callback, msg_range, *args, **kwargs):
        """
        Remove a callback from the list of callbacks which will be
        called on receipt of L{RegularMsgCopy}s on our groups
        with L{RegularMsgCopy.msg_type}s in the msg_range.

        Arguments are the same as for L{enrollRegular}.

        @param callback:
        @type callback: callable object with args (message, ...)

        @param msg_range:
        @type msg_range: C{set} of L{RegularMsgCopy.msg_type}s.
        """
        assert callable(callback)
        assert isinstance(msg_range, (set, tuple))

        if isinstance(msg_range, tuple):
            msg_range = set(xrange(msg_range[0], msg_range[1] + 1))

        self._unregister(self._regularCallbacks, callback, msg_range, args, kwargs)

    def regularReceive(self, message):
        """
        called by L{Mailbox} when our group receives a L{RegularMsgCopy}.
        """
        assert isinstance(message, RegularMsgCopy)
        for entry in self._regularCallbacks[:]:
            (key, types) = entry
            if message.msg_type in types:
                (callback, args, kwargs) = key
                callback(message, *args, **kwargs)

    def membershipRegister(self, callback, reasons, *args, **kwargs):
        """
        Add a callback to the list of callbacks which will be called
        on receipt of L{MembershipMsgCopy}s on our groups with
        L{MembershipMsgCopy.reason}s in the specified set of
        reasons.

        Arguments are the same as for L{unregisterMembership}.

        @param callback:
        @type callback: callable object with args (message, ...)

        @param reasons:
        @type reasons: a C{set} of L{MembershipMsgCopy.reason}s.
        """
        assert callable(callback)
        assert isinstance(reasons, set)

        self._register(self._membershipCallbacks, callback, reasons, args, kwargs)


    def membershipUnregister(self, callback, reasons, *args, **kwargs):
        """
        Remove a callback from the list of callbacks which will be
        called on receipt of L{MembershipMsgCopy}s on our
        groups for the specified L{MembershipMsgCopy.reason}s.

        Arguments are the same as for L{registerMembership}.

        @param callback:
        @type callback: callable object with args (message, ...)

        @param reasons:
        @type reasons: C{set} of L{MembershipMsgCopy.reason}s.
        """
        assert callable(callback)
        assert isinstance(reasons, set)

        self._unregister(self._membershipCallbacks, callback, reasons, args, kwargs)

    def membershipReceive(self, message):
        """
        called by L{Mailbox} when our group receives a L{MembershipMsgCopy}.
        """
        assert isinstance(message, MembershipMsgCopy)
        for entry in self._membershipCallbacks[:]:
            (key, types) = entry
            if message.reason in types:
                (callback, args, kwargs) = key
                callback(message, *args, **kwargs)

    def multicast(self, service, outgoing='', msg_type=0):
        """
        send a message to our groups

        @param service:
        @type service: one of the integer constants (see the SP_multicast man
        page for their meaning): L{spread.UNRELIABLE_MESS},
        L{spread.RELIABLE_MESS}, L{spread.FIFO_MESS}, L{spread.CAUSAL_MESS},
        L{spread.AGREED_MESS}, L{spread.SAFE_MESS}.

        @param outgoing: the outgoing message.
        @type outgoing: C{bytes}

        @param msg_type:
        @type msg_type: C{int} (must be 16-bit int)
        """
        self.mailbox.multicast(service, self._groups, outgoing, msg_type)

    def private_group(self):
        """
        Return the private group associated with this object.
        """
        return self.mailbox.private_group()
