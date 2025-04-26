/*
 * Copyright 2022 Collabora Ltd.
 * SPDX-License-Identifier: MIT
 */

#include <dbus-gmain/dbus-gmain.h>

int
main (void)
{
  DBusConnection *conn = dbus_bus_get (DBUS_BUS_SESSION, NULL);
  _my_set_up_connection (conn, NULL);
  return 0;
}
