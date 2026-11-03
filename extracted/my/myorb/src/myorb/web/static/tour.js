// The tour after setup (tour.py): a guide through the made-up day, one part of the screen at a
// time, with driver.js. It ends only on purpose: with its last button, which leads on to setting
// myOrb up, or with its × and then "End the tour". Esc, clicks beside it and closing the page do
// not end it; the step it was on is kept for next time.
//
// The public demo shows it too, once per browser (?tour in the address shows it again): there
// it ends with where to get myOrb, and leaves the demo to try.
(() => {
  const DEMO = document.body.dataset.tour === "demo";
  const KEY = DEMO ? "myorb-demo-tour-step" : "myorb-tour-step";
  const DONE = "myorb-demo-tour-done";
  const PADDING = 6;
  const TASKS = '#orb-widgets [hx-get="/welcome/widget/tasks/open"] .node';
  const name = () => document.querySelector(".core-name")?.textContent.trim() || "myOrb";

  // `pane`: the screen it is on when they are side by side on a phone (welcome.html).
  const steps = () => [
    {
      title: "Welcome to myOrb",
      text: "This is a made-up day, so you can see what myOrb does before you connect anything. Nothing here is yours, and nothing you do here is saved.",
    },
    {
      element: ".orb",
      // The numbers hang over the orb's edge: the lit part takes them in too.
      cover: "#orb-widgets .node",
      pane: 1,
      title: "Your day around the orb",
      text: "Each number is one source: unread email, pull requests, tasks, the weather and more. A ▲ marks one that needs you.",
    },
    {
      element: TASKS,
      pane: 1,
      title: "The details behind a number",
      text: "Click a number to see what is behind it. This one is your tasks.",
    },
    {
      element: "dialog[data-detail][open] .modal-body",
      opener: TASKS,
      title: "Your tasks, in detail",
      text: "Each with Done and Edit beside it. The numbers at the top filter the list, and ← and → move on to the next number's details. Emails, pull requests and the rest open the same way, each with its own actions.",
    },
    {
      element: ".side-left",
      pane: 0,
      title: "Today",
      text: "The day's schedule, your tasks, ticked off right here, and what needs you first.",
    },
    {
      element: ".clock-extra",
      pane: 1,
      title: "When to leave",
      text: "Your next event, and when to leave for it: by car with the traffic expected then, by public transport, or on foot when it is close.",
    },
    {
      element: ".core-brief",
      pane: 1,
      title: "The daily brief",
      text: `Every morning ${name()} writes what matters today, from all your sources. Daily brief opens it.`,
    },
    {
      element: "#report .report-body",
      opener: "[data-open-report]",
      dialog: "#report",
      title: "Your brief",
      text: "What needs you first, the day ahead and what changed since yesterday, in a few minutes of reading. A new one comes every morning.",
    },
    {
      element: "#report [data-read-aloud]",
      opener: "[data-open-report]",
      dialog: "#report",
      title: "Hear it read aloud",
      text: `Listen while you get ready: ${name()} reads the brief aloud, in the language you pick beside it.`,
    },
    {
      element: ".command-bar",
      pane: 1,
      title: `Ask ${name()}`,
      text: `Ask anything about your day, typed or spoken. ${name()} answers from your dashboard and adds tasks for you once you agree.`,
    },
    {
      element: "#ask .ask-log",
      opener: "[data-ask-quick]",
      dialog: "#ask",
      title: `Chat with ${name()}`,
      text: `Here Plan today asked ${name()} to plan the rest of the day. Ask a follow-up below, typed or by voice. Whatever ${name()} offers to do, such as adding a task, waits for your yes.`,
    },
    {
      element: ".side-right",
      pane: 2,
      title: "Quick actions and activity",
      text: "The questions you ask often, one click away, asking by voice, and what changed lately in your sources.",
    },
    {
      element: "#media-dock .dock-controls",
      title: "Music while you work",
      text: "Ambient music made on the spot, or any YouTube video or playlist you find with the magnifier. Beside it, the volume of the music and of the interface sounds, and the sounds on or off.",
    },
    {
      element: "[data-palette-open]",
      title: "Search everything",
      text: "Find any email, event, task or pull request, and run commands. ⌘K or Ctrl+K opens it from anywhere.",
    },
    {
      element: "dialog.palette[open] .palette-list",
      opener: "[data-palette-open]",
      dialog: "dialog.palette",
      type: "Pepper",
      title: "Found as you type",
      text: `“Pepper” finds the lunch with her, the task for her birthday, her email, a pull request and a Slack message. Enter opens the one chosen. Commands such as New task run from here too, and anything else goes to ${name()}.`,
    },
    DEMO
      ? {
          element: "#demo-note",
          title: "Make it yours",
          text: "myOrb is free and open source: run it on your own server, with your own services. Get myOrb shows how. Until then, the made-up day is yours to try.",
        }
      : {
          element: '.header-nav a[href="/integrations"]',
          title: "Now make it yours",
          text: "Next, connect an AI and your own services, step by step. The made-up day then makes way for yours.",
        },
  ];

  const stored = (count) => {
    try {
      return Math.min(Math.max(0, Number(localStorage.getItem(KEY)) || 0), count - 1);
    } catch {
      return 0;
    }
  };

  // Without storage the tour starts from its first step next time, and the demo shows it on
  // every visit.
  const store = (key, value) => {
    try {
      if (value === null) localStorage.removeItem(key);
      else localStorage.setItem(key, value);
    } catch {
      // Nothing kept.
    }
  };
  const recall = (key) => {
    try {
      return localStorage.getItem(key);
    } catch {
      return null;
    }
  };

  const remember = (index) => store(KEY, index === null ? null : String(index));

  // Phones show one screen of three at a time: the one with the step's part first.
  const narrow = () => {
    const nav = document.querySelector("[data-panes-nav]");
    return nav !== null && getComputedStyle(nav).display !== "none";
  };

  let guide = null;
  // The step's box as last drawn, and whether it is asking "End the tour?" now.
  let box = null;
  let asking = false;

  // Once the part is on the screen and stays where it is (or after a while without): slid in
  // with its screen, or loaded into a dialog just opened. So the box is placed by where it stays.
  const settled = (selector, then) => {
    const since = Date.now();
    let last = null;
    const check = () => {
      const box = selector && document.querySelector(selector)?.getBoundingClientRect();
      const at = box ? [box.left, box.top, box.height].map(Math.round).join() : null;
      const inView = box && box.height > 0 && box.left >= -1 && box.right <= innerWidth + 1;
      if ((inView && at === last) || Date.now() - since > 2500) then();
      else {
        last = at;
        setTimeout(check, 100);
      }
    };
    check();
  };

  // A step in a dialog opens it with its `opener`, as a click would (a number's details, the
  // brief, Ask with a quick action's answer, the search), and types its `type` there; any other
  // step closes it. A number's dialog is the one its button names.
  const dialogOf = (step) => {
    if (!step.opener) return null;
    if (step.dialog) return step.dialog;
    const named = document.querySelector(step.opener)?.dataset.open;
    return named ? `#${named}` : null;
  };

  // An open dialog is in the page's top layer, over everything else: the dimming and the box
  // move into it while a step shows, and back to the page before driver.js changes them, as it
  // expects them there.
  // Each moves only when it is elsewhere: put in again, it would start fading in anew, and the
  // page behind would flash.
  const moveTo = (host) => {
    for (const part of document.querySelectorAll(".driver-overlay, .driver-popover")) {
      if (part.parentElement !== host) host.append(part);
    }
  };
  const lift = () => {
    const host = document.querySelector("dialog[open]");
    if (host) moveTo(host);
  };
  const lower = () => moveTo(document.body);

  const dialogFor = (step) => {
    lower();
    const wanted = dialogOf(step);
    const open = document.querySelector("dialog[open]");
    if (open && !(wanted && open.matches(wanted))) open.close();
    if (wanted && !document.querySelector(wanted)?.open) {
      document.querySelector(step.opener)?.click();
    }
    const field = step.type && document.querySelector(`${wanted} input`);
    if (field && field.value !== step.type) {
      field.value = step.type;
      field.dispatchEvent(new Event("input", { bubbles: true }));
    }
  };

  // The room around the lit part: enough for what `cover` names to show whole.
  const padding = (step) => {
    const part = step.element && document.querySelector(step.element)?.getBoundingClientRect();
    if (!part || !step.cover) return PADDING;
    let room = PADDING;
    for (const element of document.querySelectorAll(step.cover)) {
      const box = element.getBoundingClientRect();
      if (!box.width) continue;
      const out = [
        part.top - box.top,
        box.bottom - part.bottom,
        part.left - box.left,
        box.right - part.right,
      ];
      room = Math.max(room, ...out.map((side) => Math.ceil(side) + PADDING));
    }
    return room;
  };

  const show = (index) => {
    remember(index);
    const go = () => {
      const config = guide.getConfig();
      guide.setConfig({ ...config, stagePadding: padding(config.steps[index]) });
      lower();
      if (guide.isActive()) guide.moveTo(index);
      else guide.drive(index);
    };
    const step = guide.getConfig().steps[index];
    dialogFor(step);
    if (step.opener) {
      settled(step.element, go);
    } else if (step.pane !== undefined && narrow()) {
      document.querySelector(`[data-pane="${step.pane}"]`)?.click();
      settled(step.element, go);
    } else {
      go();
    }
  };

  // The end, on purpose: on to the Get started steps, with the user's own data from then on.
  const finish = () => {
    remember(null);
    lower();
    if (DEMO) {
      document.querySelector("dialog[open]")?.close();
      store(DONE, "1");
      guide.destroy();
      return;
    }
    guide.destroy();
    const form = document.createElement("form");
    form.method = "post";
    form.action = "/tour/finish";
    document.body.append(form);
    form.submit();
  };

  const resume = () => {
    lower();
    guide.moveTo(guide.getActiveIndex() ?? 0);
  };

  // The × (or Esc) asks first, in the step's own box, with "Keep going" as the default.
  const confirmEnd = (popover) => {
    asking = true;
    popover.wrapper.querySelector(".tour-end")?.remove();
    popover.title.textContent = "End the tour?";
    popover.description.textContent = DEMO
      ? "The made-up day stays here to try on your own."
      : "You can take it again from Integrations. Next come the steps to set myOrb up.";
    popover.footer.replaceChildren();
    const keep = document.createElement("button");
    keep.type = "button";
    keep.className = "tour-btn tour-primary";
    keep.textContent = "Keep going";
    keep.addEventListener("click", resume);
    const end = document.createElement("button");
    end.type = "button";
    end.className = "tour-btn tour-danger";
    end.textContent = "End the tour";
    end.addEventListener("click", finish);
    popover.footer.append(end, keep);
    keep.focus();
  };

  const start = () => {
    if (!window.driver?.js || !document.getElementById("welcome")) return;
    // Each part is looked up when its step shows; one not on the page leaves the box centered.
    const list = steps().map(({ element, cover, pane, opener, dialog, type, title, text }) => ({
      element,
      cover,
      pane,
      opener,
      dialog,
      type,
      popover: { title, description: text },
    }));
    guide = window.driver.js.driver({
      steps: list,
      allowClose: false,
      allowKeyboardControl: false,
      disableActiveInteraction: true,
      showButtons: ["next", "previous"],
      showProgress: true,
      progressText: "{{current}} of {{total}}",
      nextBtnText: "Next",
      prevBtnText: "Back",
      doneBtnText: DEMO ? "Done" : "Set up myOrb",
      popoverClass: "myorb-tour",
      overlayColor: "#000",
      overlayOpacity: 0.72,
      stagePadding: PADDING,
      stageRadius: 12,
      onNextClick: () => {
        const index = guide.getActiveIndex() ?? 0;
        if (index >= list.length - 1) finish();
        else show(index + 1);
      },
      onPrevClick: () => show(Math.max(0, (guide.getActiveIndex() ?? 0) - 1)),
      onPopoverRender: (popover) => {
        box = popover;
        asking = false;
        // driver.js shows its own × only when it may close on its own; this one asks first.
        const end = document.createElement("button");
        end.type = "button";
        end.className = "tour-end";
        end.setAttribute("aria-label", "End the tour");
        end.title = "End the tour";
        end.textContent = "×";
        end.addEventListener("click", () => confirmEnd(popover));
        popover.wrapper.append(end);
        lift();
      },
    });
    show(stored(list.length));
  };

  // While it runs, ← and → step back and on, and Esc is its ×: it asks, and a second Esc keeps
  // going. Other keys go only to its box, so no shortcut opens anything behind it.
  const KEYS = { ArrowLeft: -1, ArrowRight: 1, Escape: 0 };
  document.addEventListener(
    "keydown",
    (event) => {
      if (!guide?.isActive()) return;
      const move = KEYS[event.key];
      if (move === undefined && event.target.closest?.(".driver-popover")) return;
      event.preventDefault();
      event.stopImmediatePropagation();
      if (move === undefined || event.repeat || !box) return;
      if (move === 0) {
        if (asking) resume();
        else confirmEnd(box);
        return;
      }
      if (asking) return;
      // Not past the last step: its button ends the tour, and only a click on it does.
      const index = (guide.getActiveIndex() ?? 0) + move;
      if (index >= 0 && index < guide.getConfig().steps.length) show(index);
    },
    true,
  );

  // Once the numbers around the orb are in place (or after a few seconds without them), so each
  // step finds its part where it stays.
  const begin = () => {
    if (DEMO) {
      if (new URLSearchParams(location.search).has("tour")) {
        store(DONE, null);
        remember(null);
      } else if (recall(DONE)) {
        return;
      }
    }
    const since = Date.now();
    const wait = () => {
      const loaded = document.querySelector("#orb-widgets:not([aria-busy])");
      if (loaded || Date.now() - since > 5000) setTimeout(start, 300);
      else setTimeout(wait, 200);
    };
    wait();
  };
  if (document.readyState === "complete") begin();
  else window.addEventListener("load", begin, { once: true });
})();
