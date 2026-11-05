/* Who sent this process a signal: an SA_SIGINFO handler saves the sender's pid, uid and si_code,
 * and this process's parent, at delivery, then runs the handler it stood in front of (CPython's).
 * Python handlers get only the signal number (DESIGN.md). release.yml builds it per arch;
 * signal_sender.py loads it with ctypes. */
#include <errno.h>
#include <signal.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

#define SLOTS 65
/* The chained handler's own flags that change how it runs; SA_SIGINFO is ours. */
#define KEPT_FLAGS (SA_RESTART | SA_ONSTACK | SA_NODEFER | SA_RESETHAND)

static struct sigaction previous[SLOTS];
/* The handler first wrapped (CPython's own): the only one a re-arm stands in front of again. A
 * native handler set since (faulthandler.register(chain=True)) may chain back to the recorder,
 * and wrapping it would loop recorder -> it -> recorder until the stack runs out. */
static void (*wrapped[SLOTS])(int);
static volatile pid_t last_pid[SLOTS];
static volatile uid_t last_uid[SLOTS];
static volatile int last_code[SLOTS];
/* The parent at delivery: a supervisor that signals and exits must still read as the parent. */
static volatile pid_t last_parent[SLOTS];
/* Bumped after the values above, so a reader can tell a fresh sender from none. */
static volatile unsigned long received[SLOTS];

static void record(int sig, siginfo_t *info, void *context) {
    int saved = errno;
    if (sig <= 0 || sig >= SLOTS) return;
    last_pid[sig] = info ? info->si_pid : 0;
    last_uid[sig] = info ? info->si_uid : 0;
    last_code[sig] = info ? info->si_code : 0;
    last_parent[sig] = getppid();
    received[sig] += 1;
    const struct sigaction *prev = &previous[sig];
    if (prev->sa_flags & SA_SIGINFO) {
        if (prev->sa_sigaction) prev->sa_sigaction(sig, info, context);
    } else if (prev->sa_handler != SIG_DFL && prev->sa_handler != SIG_IGN) {
        prev->sa_handler(sig);
    }
    errno = saved;
}

/* 2 armed now, 1 already armed, 0 nothing to stand in front of (default, ignored, or not the
 * handler first wrapped), -1 error. */
int probe_sender_arm(int sig) {
    struct sigaction current, mine;
    if (sig <= 0 || sig >= SLOTS) return -1;
    if (sigaction(sig, NULL, &current) != 0) return -1;
    if ((current.sa_flags & SA_SIGINFO) && current.sa_sigaction == record) return 1;
    if (current.sa_flags & SA_SIGINFO) return 0;
    if (current.sa_handler == SIG_DFL || current.sa_handler == SIG_IGN) return 0;
    if (wrapped[sig] != NULL && current.sa_handler != wrapped[sig]) return 0;
    wrapped[sig] = current.sa_handler;
    memset(&mine, 0, sizeof mine);
    mine.sa_sigaction = record;
    mine.sa_mask = current.sa_mask;
    mine.sa_flags = SA_SIGINFO | (current.sa_flags & KEPT_FLAGS);
    previous[sig] = current;
    return sigaction(sig, &mine, NULL) == 0 ? 2 : -1;
}

/* 1 while the recorder is the handler `sig` has, else 0. */
int probe_sender_is_armed(int sig) {
    struct sigaction current;
    if (sig <= 0 || sig >= SLOTS || sigaction(sig, NULL, &current) != 0) return 0;
    return (current.sa_flags & SA_SIGINFO) && current.sa_sigaction == record;
}

/* How many times `sig` arrived since load; the last sender's pid, uid, si_code and the parent. */
unsigned long probe_sender_last(int sig, int *pid, unsigned int *uid, int *code, int *parent) {
    if (sig <= 0 || sig >= SLOTS) return 0;
    unsigned long count = received[sig];
    *pid = (int)last_pid[sig];
    *uid = (unsigned int)last_uid[sig];
    *code = last_code[sig];
    *parent = (int)last_parent[sig];
    return count;
}
