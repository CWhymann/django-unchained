(() => {
  "use strict";

  const STORE_KEY = "django-unchained-v1";
  const RANKS = [
    [0, "Greenhorn"],
    [50, "Revolverheld"],
    [110, "Kopfgeldjäger"],
    [170, "Sheriff"],
    [240, "Django Unchained"],
  ];
  const TYPE_LABEL = {
    quiz: "QUIZ",
    live: "LIVE-REQUEST",
    fill: "LÜCKENCODE",
    bug: "BUG-JAGD",
    order: "REIHENFOLGE",
  };
  const ASKS = [
    "Hör zu, Fremder: ",
    "Na los: ",
    "Jetzt wird es spannend: ",
    "Frage vom Cowboy: ",
  ];
  const CHEERS = [
    "Kein Chaos. Nur Kontrolle.",
    "DRY ist keine Sünde. Es ist eine Lebenseinstellung.",
    "Mein Code. Meine Regeln. Keine Ketten.",
    "Ich bin ich. Und wiederhole mich nicht.",
    "Sauber gezogen, Fremder!",
  ];
  const JEERS = [
    "Daneben, Fremder. Und wenn es mal hängt: git push und weiter.",
    "Schematisch ist schön. Aber echte Freiheit liegt in sauberem Code.",
    "Nicht ganz. Versuch es noch einmal, ich habe Zeit.",
    "Autsch. Auch Revolverhelden müssen üben.",
  ];
  const NUDGES = [
    "Na, Fremder? Klick auf mich, wenn du einen Tipp brauchst.",
    "Wenn es mal hängt, hilft ein Tipp. Du weißt, wo ich stehe.",
  ];

  const $ = (sel) => document.querySelector(sel);
  const pick = (list) => list[Math.floor(Math.random() * list.length)];
  const el = (tag, cls, text) => {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text !== undefined) node.textContent = text;
    return node;
  };

  let missions = [];
  let state = loadState();
  let cur = null; // { mi, idx }
  let run = null; // { attempts, hint, fired }
  let nudgeTimer = null;

  // ---------- Fortschritt (localStorage) ----------

  function loadState() {
    try {
      const saved = JSON.parse(localStorage.getItem(STORE_KEY));
      if (saved && saved.done) return saved;
    } catch (e) {
      /* ignorieren */
    }
    return { done: {} };
  }
  function saveState() {
    try {
      localStorage.setItem(STORE_KEY, JSON.stringify(state));
    } catch (e) {
      /* ignorieren */
    }
  }
  const totalXp = () => Object.values(state.done).reduce((a, b) => a + b, 0);
  const allExercises = () => missions.flatMap((m) => m.exercises);
  const missionDone = (m) => m.exercises.every((e) => e.id in state.done);
  const missionUnlocked = (i) => i === 0 || missionDone(missions[i - 1]);

  // ---------- Der Cowboy ----------

  const cowboy = (() => {
    const box = $("#cowboy");
    const avatar = $("#avatar");
    const bubble = $("#bubble");
    const text = $("#bubble-text");
    let token = 0;
    const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

    function anim(cls, ms) {
      avatar.classList.remove("cheer", "shake", "tip");
      void avatar.offsetWidth;
      avatar.classList.add(cls);
      setTimeout(() => avatar.classList.remove(cls), ms);
    }

    async function say(msg) {
      const mine = ++token;
      bubble.classList.add("show");
      text.textContent = "";
      avatar.classList.add("talking");
      for (let i = 0; i < msg.length; i++) {
        if (mine !== token) return;
        text.textContent += msg[i];
        await sleep(msg[i] === " " ? 16 : 22);
      }
      if (mine === token) avatar.classList.remove("talking");
    }

    async function sayAll(list) {
      const start = token + 1;
      for (let i = 0; i < list.length; i++) {
        await say(list[i]);
        if (token !== start + i) return;
        if (i < list.length - 1) {
          await sleep(1100);
          if (token !== start + i) return;
        }
      }
    }

    function enter() {
      box.classList.add("in");
      setTimeout(() => anim("tip", 900), 900);
    }

    return {
      say,
      sayAll,
      enter,
      cheer: () => anim("cheer", 900),
      shake: () => anim("shake", 550),
    };
  })();

  // ---------- HUD und Karte ----------

  function renderHud() {
    const xp = totalXp();
    const total = allExercises().length;
    const done = Object.keys(state.done).length;
    let rank = RANKS[0][1];
    RANKS.forEach(([min, name]) => {
      if (xp >= min) rank = name;
    });
    $("#rank").textContent = rank;
    $("#xp").textContent = xp + " XP · " + done + " / " + total + " Übungen";
    $("#bar").style.width = (total ? (done / total) * 100 : 0) + "%";
  }

  function renderMap() {
    const map = $("#map");
    map.replaceChildren();
    missions.forEach((m, i) => {
      const done = m.exercises.filter((e) => e.id in state.done).length;
      const open = missionUnlocked(i);
      const card = el(
        "button",
        "mission" +
          (open ? "" : " locked") +
          (done === m.exercises.length ? " done" : ""),
      );
      card.type = "button";
      card.disabled = !open;
      card.append(
        el("span", "m-num", "MISSION " + (i + 1)),
        el("strong", "m-title", m.title),
        el("span", "m-section", m.section),
        el(
          "span",
          "m-prog",
          open
            ? done + " / " + m.exercises.length + " erledigt"
            : "🔒 Schließe zuerst die vorige Mission ab",
        ),
      );
      card.addEventListener("click", () => openMission(i));
      map.append(card);
    });
  }

  function openMission(i) {
    const m = missions[i];
    let idx = m.exercises.findIndex((e) => !(e.id in state.done));
    if (idx < 0) idx = 0;
    cur = { mi: i, idx };
    $("#map-wrap").hidden = true;
    $("#stage").hidden = false;
    window.scrollTo(0, 0);
    renderExercise(true);
  }

  function backToMap() {
    cur = null;
    clearTimeout(nudgeTimer);
    $("#stage").hidden = true;
    $("#map-wrap").hidden = false;
    renderHud();
    renderMap();
  }

  // ---------- Netzwerk ----------

  async function postJson(url, data) {
    const token = document.querySelector("[name=csrfmiddlewaretoken]").value;
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": token },
      credentials: "same-origin",
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("HTTP " + res.status);
    return res.json();
  }

  // ---------- Übungs-Bausteine ----------

  function buildOptions(ex) {
    let sel = null;
    let locked = false;
    const list = el("div", "options");
    const buttons = ex.options.map((label, i) => {
      const b = el("button", "option", label);
      b.type = "button";
      b.addEventListener("click", () => {
        if (locked) return;
        sel = i;
        buttons.forEach((x, j) => {
          x.classList.remove("good", "bad");
          x.classList.toggle("sel", j === i);
        });
      });
      list.append(b);
      return b;
    });
    return {
      node: list,
      get: () => sel,
      mark: (res) => {
        if (sel !== null)
          buttons[sel].classList.add(res.correct ? "good" : "bad");
      },
      lock: () => {
        locked = true;
      },
    };
  }

  function buildLive(ex, onFired) {
    const box = el("div", "live");
    const fire = el(
      "button",
      "fire",
      "🔫 Request abfeuern: " + ex.request.method + " " + ex.request.url,
    );
    fire.type = "button";
    const out = el("div", "out");
    box.append(fire, out);

    fire.addEventListener("click", async () => {
      out.replaceChildren(el("p", null, "… der Revolver wird gespannt …"));
      const opts = { method: ex.request.method, credentials: "same-origin" };
      if (ex.request.body) {
        const fd = new FormData();
        Object.entries(ex.request.body).forEach(([k, v]) => fd.append(k, v));
        opts.body = fd;
      }
      try {
        const res = await fetch(ex.request.url, opts);
        const type = res.headers.get("content-type") || "";
        const raw = await res.text();
        let body;
        if (type.includes("json")) {
          try {
            body = JSON.stringify(JSON.parse(raw), null, 2);
          } catch (e) {
            body = raw;
          }
        } else {
          const title = raw.match(/<title>([^<]*)<\/title>/i);
          body =
            "(" +
            (type.split(";")[0] || "Antwort") +
            ", " +
            raw.length +
            " Zeichen)" +
            (title ? "\nSeitentitel: " + title[1].trim() : "");
        }
        const line = el("div", "statusline");
        line.append(
          el(
            "span",
            "badge s" + String(res.status)[0],
            String(res.status) + " " + res.statusText,
          ),
          el("span", null, ex.request.method + " " + ex.request.url),
        );
        if (res.redirected)
          line.append(
            el(
              "span",
              null,
              "↪ weitergeleitet nach " + new URL(res.url).pathname,
            ),
          );
        out.replaceChildren(line, el("pre", null, body));
        onFired();
      } catch (e) {
        out.replaceChildren(
          el(
            "p",
            null,
            "Keine Antwort. Läuft python manage.py runserver noch?",
          ),
        );
      }
    });
    return box;
  }

  function buildFill(ex) {
    const pre = el("pre", "code fill");
    const inputs = [];
    ex.code.split(/(\[\[\d+\]\])/).forEach((part) => {
      const m = part.match(/^\[\[(\d+)\]\]$/);
      if (!m) {
        pre.append(document.createTextNode(part));
        return;
      }
      const inp = el("input", "blank");
      inp.type = "text";
      inp.size = 8;
      inp.spellcheck = false;
      inp.autocomplete = "off";
      inp.dataset.i = m[1];
      inp.addEventListener("input", () => {
        inp.size = Math.max(8, inp.value.length + 1);
        inp.classList.remove("good", "bad");
      });
      inputs.push(inp);
      pre.append(inp);
    });
    inputs.sort((a, b) => Number(a.dataset.i) - Number(b.dataset.i));
    return {
      node: pre,
      get: () =>
        inputs.some((i) => !i.value.trim()) ? null : inputs.map((i) => i.value),
      mark: (res) =>
        inputs.forEach((inp, k) => {
          inp.classList.remove("good", "bad");
          inp.classList.add(res.details && res.details[k] ? "good" : "bad");
        }),
      lock: () =>
        inputs.forEach((i) => {
          i.readOnly = true;
        }),
    };
  }

  function buildBug(ex) {
    let sel = null;
    let locked = false;
    const box = el("div", "code bug");
    const rows = ex.lines.map((text, i) => {
      const row = el("button", "line");
      row.type = "button";
      row.append(
        el("span", "ln", String(i + 1)),
        el("code", null, text || "\u00a0"),
      );
      row.addEventListener("click", () => {
        if (locked) return;
        sel = i + 1;
        rows.forEach((r) => r.classList.remove("sel", "good", "bad"));
        row.classList.add("sel");
      });
      box.append(row);
      return row;
    });
    return {
      node: box,
      get: () => sel,
      mark: (res) => {
        if (sel) rows[sel - 1].classList.add(res.correct ? "good" : "bad");
      },
      lock: () => {
        locked = true;
      },
    };
  }

  function buildOrder(ex) {
    let items = ex.items.slice();
    let locked = false;
    let dragFrom = null;
    const wrap = el("div");
    const list = el("ol", "order");
    const probes = ex.probes ? el("div", "probes") : null;
    wrap.append(list);
    if (probes) wrap.append(probes);

    function move(from, to) {
      if (locked || to < 0 || to >= items.length || from === to) return;
      const [moved] = items.splice(from, 1);
      items.splice(to, 0, moved);
      list.classList.remove("good-all", "bad-all");
      draw();
    }

    function drawProbes() {
      if (!probes) return;
      probes.replaceChildren(el("h3", null, "Proben: wohin führt welche URL?"));
      ex.probes.forEach((p) => {
        const hit = items.find((it) => new RegExp(it.re).test(p.url));
        const ok = !!hit && hit.id === p.expect;
        const row = el("div", "probe " + (ok ? "good" : "bad"));
        row.append(
          el("code", null, "/" + p.url),
          el("span", null, "→"),
          el("code", null, hit ? hit.label : "keine Route"),
          el("span", "mark", ok ? "✔" : "✘"),
        );
        probes.append(row);
      });
    }

    function draw() {
      list.replaceChildren();
      items.forEach((it, i) => {
        const li = el("li", "oitem");
        li.draggable = !locked;
        const up = el("button", "mini", "▲");
        const down = el("button", "mini", "▼");
        up.type = "button";
        down.type = "button";
        up.disabled = locked || i === 0;
        down.disabled = locked || i === items.length - 1;
        up.addEventListener("click", () => move(i, i - 1));
        down.addEventListener("click", () => move(i, i + 1));
        const ctl = el("span", "ctl");
        ctl.append(up, down);
        li.append(el("code", null, it.text), ctl);
        li.addEventListener("dragstart", (e) => {
          dragFrom = i;
          li.classList.add("drag");
          e.dataTransfer.effectAllowed = "move";
          e.dataTransfer.setData("text/plain", String(i));
        });
        li.addEventListener("dragend", () => li.classList.remove("drag"));
        li.addEventListener("dragover", (e) => e.preventDefault());
        li.addEventListener("drop", (e) => {
          e.preventDefault();
          if (dragFrom !== null) move(dragFrom, i);
          dragFrom = null;
        });
        list.append(li);
      });
      drawProbes();
    }

    draw();
    return {
      node: wrap,
      get: () => items.map((it) => it.id),
      mark: (res) => {
        list.classList.toggle("good-all", res.correct);
        list.classList.toggle("bad-all", !res.correct);
      },
      lock: () => {
        locked = true;
        draw();
      },
    };
  }

  // ---------- Übung anzeigen ----------

  function renderExercise(withIntro) {
    const m = missions[cur.mi];
    const ex = m.exercises[cur.idx];
    run = { attempts: 0, hint: false, fired: false };

    const stage = $("#stage");
    stage.replaceChildren();

    const back = el("button", "ghost", "← Karte");
    back.type = "button";
    back.addEventListener("click", backToMap);
    const dots = el("div", "dots");
    m.exercises.forEach((e, i) => {
      dots.append(
        el(
          "span",
          "dot" +
            (e.id in state.done ? " ok" : "") +
            (i === cur.idx ? " now" : ""),
        ),
      );
    });
    const bar = el("div", "stage-bar");
    bar.append(back, el("span", "stage-title", m.title), dots);

    const card = el("article", "card");
    card.append(
      el("span", "tag", TYPE_LABEL[ex.type]),
      el("h2", null, ex.title),
      el("p", "q", ex.q),
    );

    let body;
    if (ex.type === "quiz" || ex.type === "live") {
      body = buildOptions(ex);
      if (ex.type === "live") {
        card.append(
          buildLive(ex, () => {
            run.fired = true;
          }),
        );
      }
    } else if (ex.type === "fill") {
      body = buildFill(ex);
    } else if (ex.type === "bug") {
      body = buildBug(ex);
    } else {
      body = buildOrder(ex);
    }
    card.append(body.node);

    const result = el("div", "result");
    result.hidden = true;
    const hintBox = el("div", "hintbox");
    hintBox.hidden = true;

    const hintBtn = el("button", "ghost", "💡 Tipp");
    hintBtn.type = "button";
    const checkBtn = el("button", "primary", "Antworten");
    checkBtn.type = "button";
    const isLast = cur.idx === m.exercises.length - 1;
    const nextBtn = el(
      "button",
      "primary",
      isLast ? "Mission abschließen" : "Weiter ▶",
    );
    nextBtn.type = "button";
    nextBtn.hidden = true;
    const actions = el("div", "actions");
    actions.append(hintBtn, checkBtn, nextBtn);
    card.append(actions, hintBox, result);
    stage.append(bar, card);

    function showHint() {
      run.hint = true;
      const text = ex.hint || "Denk in Ruhe nach, Fremder.";
      hintBox.textContent = "Tipp vom Cowboy: " + text;
      hintBox.hidden = false;
      cowboy.say("Tipp vom Cowboy: " + text);
    }
    showHintCurrent = showHint;

    async function submit() {
      armNudge();
      if (ex.type === "live" && !run.fired) {
        cowboy.say("Erst abfeuern, Fremder! Drück auf den Revolver.");
        return;
      }
      const answer = body.get();
      if (answer === null) {
        cowboy.say("Da fehlt noch etwas. Beantworte erst die Frage.");
        return;
      }
      checkBtn.disabled = true;
      let res;
      try {
        res = await postJson("/api/check/", { id: ex.id, answer });
      } catch (e) {
        cowboy.say(
          "Der Server antwortet nicht. Läuft python manage.py runserver noch?",
        );
        checkBtn.disabled = false;
        return;
      }
      checkBtn.disabled = false;
      body.mark(res);
      result.hidden = false;
      result.replaceChildren();

      if (res.correct) {
        const gain = run.attempts === 0 && !run.hint ? 10 : 5;
        const first = !(ex.id in state.done);
        if (first) {
          state.done[ex.id] = gain;
          saveState();
        }
        renderHud();
        result.className = "result ok";
        result.append(
          el("strong", null, "✔ Treffer!" + (first ? " +" + gain + " XP" : "")),
          el("span", null, res.explain),
        );
        body.lock();
        checkBtn.hidden = true;
        hintBtn.hidden = true;
        nextBtn.hidden = false;
        nextBtn.focus();
        cowboy.cheer();
        cowboy.say(pick(CHEERS));
        const dot = stage.querySelectorAll(".dot")[cur.idx];
        if (dot) dot.classList.add("ok");
      } else {
        run.attempts += 1;
        result.className = "result bad";
        result.append(el("strong", null, "✘ Daneben."));
        if (run.attempts >= 2) {
          result.append(el("span", null, "Die Auflösung: " + res.explain));
        } else {
          result.append(
            el("span", null, "Versuch es noch einmal oder hol dir einen Tipp."),
          );
        }
        cowboy.shake();
        cowboy.say(pick(JEERS));
      }
    }

    hintBtn.addEventListener("click", showHint);
    checkBtn.addEventListener("click", submit);
    card.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && e.target.tagName === "INPUT") submit();
    });
    nextBtn.addEventListener("click", () => {
      if (!isLast) {
        cur.idx += 1;
        window.scrollTo(0, 0);
        renderExercise(false);
      } else {
        const finished = m;
        backToMap();
        cowboy.say(finished.outro);
      }
    });

    armNudge();
    const ask = pick(ASKS) + ex.q;
    cowboy.sayAll(withIntro ? [m.intro, ask] : [ask]);
  }

  let showHintCurrent = null;

  function armNudge() {
    clearTimeout(nudgeTimer);
    nudgeTimer = setTimeout(() => cowboy.say(pick(NUDGES)), 40000);
  }

  // ---------- Start ----------

  $("#avatar").addEventListener("click", () => {
    if (cur && showHintCurrent) showHintCurrent();
    else cowboy.say(pick(CHEERS));
  });

  $("#reset").addEventListener("click", () => {
    if (!confirm("Fortschritt wirklich löschen?")) return;
    state = { done: {} };
    saveState();
    backToMap();
    cowboy.say("Alles auf Anfang, Fremder. Kein Problem.");
  });

  async function init() {
    cowboy.enter();
    try {
      const res = await fetch("/api/missions/");
      missions = (await res.json()).missions;
    } catch (e) {
      cowboy.say(
        "Die Missionen sind nicht erreichbar. Läuft python manage.py runserver?",
      );
      return;
    }
    renderHud();
    renderMap();
    const started = Object.keys(state.done).length > 0;
    cowboy.sayAll(
      started
        ? ["Willkommen zurück, Fremder. Such dir eine Mission aus."]
        : [
            "Ich bin ich. Und wiederhole mich nicht.",
            "Willkommen bei Django Unchained, Fremder! Wähle deine erste Mission, ich stelle dir die Fragen.",
          ],
    );
  }

  init();
})();
