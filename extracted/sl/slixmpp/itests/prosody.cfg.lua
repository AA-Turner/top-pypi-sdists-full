daemonize = true
pidfile = "/run/prosody/prosody.pid"

admins = { }
modules_enabled = {
    "disco"; -- Service discovery
    "roster"; -- Allow users to have a roster. Recommended ;)
    "saslauth"; -- Authentication for clients and servers. Recommended if you want to log in.
    "tls"; -- Add support for secure TLS on c2s/s2s connections
    "blocklist"; -- Allow users to block communications with other users
    "bookmarks"; -- Synchronise the list of open rooms between clients
    "carbons"; -- Keep multiple online clients in sync
    "dialback"; -- Support for verifying remote servers using DNS
    "limits"; -- Enable bandwidth limiting for XMPP connections
    "pep"; -- Allow users to store public and private data in their account
    "private"; -- Legacy account storage mechanism (XEP-0049)
    "smacks"; -- Stream management and resumption (XEP-0198)
    "vcard4"; -- User profiles (stored in PEP)
    "vcard_legacy"; -- Conversion between legacy vCard and PEP Avatar, vcard
    "csi_simple"; -- Simple but effective traffic optimizations for mobile devices
    "invites"; -- Create and manage invites
    "invites_adhoc"; -- Allow admins/users to create invitations via their client
    "invites_register"; -- Allows invited users to create accounts
    "ping"; -- Replies to XMPP pings with pongs
    "register"; -- Allow users to register on this server using a client and change passwords
    "time"; -- Let others know the time here on this server
    "uptime"; -- Report how long server has been running
    "version"; -- Replies to server version requests
    "mam"; -- Store recent messages to allow multi-device synchronization
    "admin_adhoc"; -- Allows administration via an XMPP client that supports ad-hoc commands
    "admin_shell"; -- Allow secure administration via 'prosodyctl shell'
    "service_outage_status"; -- XEP-0455
    "http_files"; -- Serve static files, for XEP-0455
}

-- XEP-0455
outage_status_urls = { "https://prosody:5281/files/status.json" }
http_files_dir = { "/var/www" }

c2s_direct_tls_ports = { 5223 }

authentication = "internal_hashed"

archive_expires_after = "1w" -- Remove archived messages after 1 week

log = {{levels = {min = 'debug'}, to = 'console'}}

certificates = "certs"

component_interfaces = { '*' }  -- terrible idea in general, but OK for CI

VirtualHost "prosody"

Component "muc.prosody" "muc"
    modules_enabled = {
        "muc_mam",
        "muc_moderation",
    }

Component "upload.prosody" "http_file_share"
    http_host = "prosody"

Component "slixmpp.prosody"
    component_secret = "secret"
