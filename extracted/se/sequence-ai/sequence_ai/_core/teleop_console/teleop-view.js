/* teleop-view.js — what a robot's Teleoperation tab says and allows, apart from the page: node checks it without a browser
   (tools/check/test_teleop_view.mjs).

   In one sentence: who drives (the robot's own word, on its reliable channel) → one line, and which of Take, Release and Stop can be
   pressed → the connection's metrics() as the two figures the page shows.

   WHY only these: the tab is a picture, three buttons and how late the picture is.
 Its box for an action chunk and Send are gone: a
   person's chunks come from the API. */

export const TELEOP = 'teleop';

/* Whether teleop is on this robot's list: what makes the tab appear. */
export const listsTeleop = (robot) => Array.isArray(robot && robot.policies) && robot.policies.includes(TELEOP);

const connections = (robot) => (robot && Array.isArray(robot.connections) ? robot.connections.filter(Boolean) : []);

/* Whether the robot's code is connected with "teleop" among its names: the one thing a console can reach. A robot online on a policy
   alone answers an offer with robot_not_connected. {teleop_offer_create: "NOT EXISTS (SELECT 1 FROM PUBLIC.ROBOT_LINKS ..."} */
export const teleopOnline = (robot) => connections(robot).some((c) => c.policy === TELEOP);

/* One line of who drives. "model" is no one, on a robot connected to no policy: the SDK says so, and only the page knows which this is. */
export function whoLine(state, yours, robot) {
  const { driver, by } = state || {};
  if (driver === 'human') return yours ? 'You are driving' : `${by || 'Someone'} is driving`;
  if (driver === 'stopped') return by === 'plan' ? 'Stopped by its plan' : 'Stopped';
  return connections(robot).some((c) => c.policy !== TELEOP) ? 'Policy driving' : 'No one driving';
}

/* What can be pressed now. Stop whenever connected, for anyone, a person watching too; Take unless someone drives; Release by the one
   who drives, or from a stop, by anyone. */
export function controls({ connected, driver, yours, busy }) {
  const free = connected && !busy;
  return { take: free && driver !== 'human', release: free && (yours || driver === 'stopped'), stop: free };
}

/* A latency in milliseconds, as few digits as say it: under 10 ms to a tenth. */
const ms = (us) => {
  if (us === null || us === undefined) return null;
  const v = us / 1000;
  return v < 10 ? v.toFixed(1) : String(Math.round(v));
};
const pair = (l) => {
  const a = ms(l && l.p50);
  const b = ms(l && l.p95);
  if (a === null) return '—';
  return b === null ? `${a} ms` : `${a} / ${b} ms`;
};

/* The two figures, p50 / p95 where the window holds enough (2 samples for p50, 20 for p95), a dash until it does: Frame, and the round
   trip. Command was this page's own commands' one way, and it sends none now. */
export function latencyCells(metrics) {
  const l = (metrics && metrics.latency_us) || {};
  const rtt = ms(l.rtt_us && l.rtt_us.p50);
  return { frame: pair(l.frame_us), rtt: rtt === null ? '—' : `${rtt} ms` };
}
