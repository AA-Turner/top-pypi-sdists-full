#!/usr/bin/env bash
# The desktop session of one Cloud Computer, started by the browser-worker
# entrypoint (as browser-worker) once the X display answers: Openbox manages
# windows (and maximizes the agent's Chrome inside the work area), pcmanfm draws
# the wallpaper and the desktop icons (Chrome, Terminal, Files), and tint2 is
# the taskbar. Each piece is checked and its state logged.
set -u

export DISPLAY="${DISPLAY:-:99}"
home="${HOME:-/home/browser-worker}"
xdg="${CLOUD_COMPUTER_XDG:-/etc/xdg/cloud-computer}"
xsetroot -solid "#0f172a" 2>/dev/null || true

# Desktop customizations survive every new build (owner ruling 16): each piece
# reads the PERSON's config in their home (EFS); the build only seeds its
# default there when the person has none. Openbox's config is the file obconf
# edits, so it must be theirs. The one platform rule it needs (the agent's
# Chrome maximized in the work area) is put back if their file lacks it.
openbox_rc="${home}/.config/openbox/rc.xml"
mkdir -p "${home}/.config/openbox" "${home}/.config/tint2"
[[ -s "${openbox_rc}" ]] || cp "${xdg}/openbox-rc.xml" "${openbox_rc}"
if ! grep -q 'class="matrx-agent-chrome"' "${openbox_rc}"; then
  awk '{print} /<applications>/ && !done {print "<application class=\"matrx-agent-chrome\" type=\"normal\"><maximized>yes</maximized><focus>yes</focus></application>"; done=1}' \
    "${openbox_rc}" > "${openbox_rc}.new" && mv -f "${openbox_rc}.new" "${openbox_rc}"
fi
tint2_rc="${home}/.config/tint2/tint2rc"
[[ -s "${tint2_rc}" ]] || cp "${xdg}/tint2rc" "${tint2_rc}"
openbox --sm-disable --config-file "${openbox_rc}" >/tmp/openbox.log 2>&1 &

for _ in $(seq 1 50); do
  if xprop -root _NET_SUPPORTING_WM_CHECK 2>/dev/null | grep -q "window id"; then
    break
  fi
  sleep 0.1
done

# NumLock on from the start (the stream client never toggles it), checked.
numlockx on 2>/dev/null || true
if ! xset q 2>/dev/null | grep -q "Num Lock: *on"; then
  xdotool key Num_Lock 2>/dev/null || true
fi
numlock_state="$(xset q 2>/dev/null | grep -q 'Num Lock: *on' && echo on || echo off)"

# The screen never blanks (an agent's CDP commands are no X input), checked.
xset s off s noblank -dpms 2>/dev/null || true
blank_state="$(xset q 2>/dev/null | grep -q 'timeout: *0 ' && echo off || echo on)"

# Desktop icons: the platform's three launchers, put back if a person deleted
# them (anything else they keep on the desktop is theirs and untouched).
desktop_dir="${HOME:-/home/browser-worker}/Desktop"
mkdir -p "${desktop_dir}"
for launcher in cloud-computer-chrome cloud-computer-terminal cloud-computer-files; do
  source_file="/usr/share/applications/${launcher}.desktop"
  target="${desktop_dir}/${launcher}.desktop"
  if [[ -r "${source_file}" && ! -e "${target}" ]]; then
    cp "${source_file}" "${target}" && chmod 0755 "${target}"
  fi
done

# pcmanfm reads its desktop settings only from the person's config dir: seed
# the platform defaults there once (their own later changes are kept).
pcmanfm_dir="${HOME:-/home/browser-worker}/.config/pcmanfm/cloud-computer"
mkdir -p "${pcmanfm_dir}"
[[ -e "${pcmanfm_dir}/desktop-items-0.conf" ]] || cp /etc/xdg/pcmanfm/cloud-computer/desktop-items-0.conf "${pcmanfm_dir}/desktop-items-0.conf"
pcmanfm --desktop --profile=cloud-computer >/tmp/pcmanfm.log 2>&1 &
tint2 -c "${tint2_rc}" >/tmp/tint2.log 2>&1 &

ready=1
for _ in $(seq 1 50); do
  ready=1
  xprop -root _NET_SUPPORTING_WM_CHECK 2>/dev/null | grep -q "window id" || ready=0
  pgrep -x tint2 >/dev/null || ready=0
  pgrep -f "pcmanfm --desktop" >/dev/null || ready=0
  [[ "${ready}" == "1" ]] && break
  sleep 0.1
done
if [[ "${ready}" == "1" ]]; then
  echo "cloud-computer desktop ready epoch_ms=$(date +%s%3N) wm=openbox taskbar=tint2 desktop=pcmanfm numlock=${numlock_state} blanking=${blank_state}"
else
  echo "cloud-computer desktop INCOMPLETE: wm=$(pgrep -x openbox >/dev/null && echo up || echo down) taskbar=$(pgrep -x tint2 >/dev/null && echo up || echo down) desktop=$(pgrep -f 'pcmanfm --desktop' >/dev/null && echo up || echo down); see /tmp/tint2.log /tmp/pcmanfm.log" >&2
fi
wait
