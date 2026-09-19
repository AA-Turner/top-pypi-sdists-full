#include <CoreFoundation/CoreFoundation.h>
#include <errno.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <sys/select.h>
#include <unistd.h>

/* Synthetic .app consumer: use the same current-application CF APIs as Chrome. */
int main(int argc, const char *argv[]) {
  if (argc != 3 || getuid() < 500 ||
      strncmp(argv[1], "com.runlayer.test.policy-publication.",
              sizeof("com.runlayer.test.policy-publication.") - 1) != 0 ||
      strncmp(argv[2], "com.runlayer.test.policy-publication.",
              sizeof("com.runlayer.test.policy-publication.") - 1) != 0) {
    return 2;
  }
  CFStringRef expected = CFStringCreateWithCString(
      NULL, argv[1], kCFStringEncodingUTF8);
  CFStringRef actual = CFBundleGetIdentifier(CFBundleGetMainBundle());
  if (actual == NULL || !CFEqual(actual, expected)) {
    fprintf(stderr, "synthetic app bundle identifier did not match\n");
    CFRelease(expected);
    return 3;
  }
  CFRelease(expected);
  CFStringRef unrelated = CFStringCreateWithCString(NULL, argv[2], kCFStringEncodingUTF8);
  char command[32];
  while (1) {
    CFRunLoopRunInMode(kCFRunLoopDefaultMode, 0.01, false);
    fd_set input;
    FD_ZERO(&input);
    FD_SET(STDIN_FILENO, &input);
    struct timeval timeout = {.tv_sec = 0, .tv_usec = 50000};
    int ready = select(STDIN_FILENO + 1, &input, NULL, NULL, &timeout);
    if (ready < 0) {
      if (errno == EINTR) {
        continue;
      }
      return 4;
    }
    if (ready == 0) {
      continue;
    }
    if (fgets(command, sizeof(command), stdin) == NULL ||
        strcmp(command, "quit\n") == 0) {
      break;
    }
    CFStringRef domain = strcmp(command, "unrelated\n") == 0
        ? unrelated : kCFPreferencesCurrentApplication;
    CFPreferencesAppSynchronize(domain);
    CFPropertyListRef value = CFPreferencesCopyAppValue(
        CFSTR("RunlayerSyntheticPolicyProbe"), domain);
    Boolean forced = CFPreferencesAppValueIsForced(
        CFSTR("RunlayerSyntheticPolicyProbe"), domain);
    if (value == NULL) {
      printf("{\"value\":null,\"forced\":%s}\n", forced ? "true" : "false");
    } else {
      char rendered[128];
      if (CFGetTypeID(value) != CFStringGetTypeID() ||
          !CFStringGetCString(value, rendered, sizeof(rendered), kCFStringEncodingUTF8) ||
          (strcmp(rendered, "created") != 0 && strcmp(rendered, "updated") != 0)) {
        CFRelease(value);
        return 6;
      }
      printf("{\"value\":\"%s\",\"forced\":%s}\n", rendered,
             forced ? "true" : "false");
      CFRelease(value);
    }
    fflush(stdout);
  }
  CFRelease(unrelated);
  return 0;
}
