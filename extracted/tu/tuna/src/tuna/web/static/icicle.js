// Color mapping for inlining styles in exported SVG
const COLOR_MAP = {
  color0: "#01579b",
  color1: "#0288d1",
  color2: "#0288d1",
  color3: "#bdbdbd",
};

class Icicle extends HTMLElement {
  #x;
  #y;
  #root;
  #rect;
  #clipRect;
  #text;
  #tspan1;
  #tspan2;
  #data;
  #svg;
  #rowHeight;
  #strokeWidth = 1;
  #resizeController;

  disconnectedCallback() {
    this.#resizeController?.abort();
  }

  connectedCallback() {
    this.#data = tunaData;
    this.#rowHeight = +this.getAttribute("row-height");
    this.#svg = d3.select(this).append("svg");
    this.#svg.style("width", "100%");
    this.#render();
    this.#setupExportButtons();
  }

  #setupExportButtons() {
    const svgButton = document.getElementById("exportSvgButton");
    const pngButton = document.getElementById("exportPngButton");
    const copyButton = document.getElementById("copyPngButton");

    if (svgButton) {
      svgButton.addEventListener("click", () => this.exportSvg());
    }
    if (pngButton) {
      pngButton.addEventListener("click", () => this.exportPng());
    }
    if (copyButton) {
      copyButton.addEventListener("click", () => this.copyPng(copyButton));
    }
  }

  get #exportBaseName() {
    const title = document.title;
    const prefix = "tuna - ";
    const filename = title.startsWith(prefix)
      ? title.slice(prefix.length)
      : "tuna";
    const basename = filename.split(/[/\\]/).pop();
    return basename.replace(/\.[^.]+$/, "");
  }

  #getSvgWithInlinedStyles() {
    const svgNode = this.#svg.node();
    const clone = svgNode.cloneNode(true);

    const width = svgNode.getBoundingClientRect().width;
    const height = parseFloat(svgNode.getAttribute("height"));
    const padding = 20;

    clone.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    clone.setAttribute("width", width + padding * 2);
    clone.setAttribute("height", height + padding * 2);
    clone.style.fontFamily =
      "-apple-system, BlinkMacSystemFont, avenir next, avenir, segoe ui, helvetica neue, Adwaita Sans, Cantarell, Ubuntu, roboto, noto, helvetica, arial, sans-serif";

    // Add white background with border
    const bg = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    bg.setAttribute("width", width + padding * 2);
    bg.setAttribute("height", height + padding * 2);
    bg.setAttribute("fill", "#ffffff");
    bg.setAttribute("stroke", "#dee2e6");
    bg.setAttribute("stroke-width", "1");
    clone.insertBefore(bg, clone.firstChild);

    // Wrap existing content in a group offset by padding
    const wrapper = document.createElementNS("http://www.w3.org/2000/svg", "g");
    wrapper.setAttribute("transform", `translate(${padding},${padding})`);
    [...clone.childNodes]
      .slice(1)
      .forEach((child) => wrapper.appendChild(child));
    clone.appendChild(wrapper);

    // Inline styles for all groups with color classes
    clone.querySelectorAll("g").forEach((g) => {
      for (const [className, fillColor] of Object.entries(COLOR_MAP)) {
        if (g.classList.contains(className)) {
          const rect = g.querySelector("rect");
          if (rect) {
            rect.setAttribute("fill", fillColor);
            rect.setAttribute("stroke", "#fff");
          }
          const clipRect = g.querySelector("clipPath rect");
          if (clipRect) {
            clipRect.setAttribute("fill", fillColor);
            clipRect.setAttribute("stroke", "#fff");
          }
        }
      }
    });

    return clone;
  }

  #triggerDownload(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = Object.assign(document.createElement("a"), {
      href: url,
      download: filename,
    });
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  exportSvg() {
    const svgString = new XMLSerializer().serializeToString(
      this.#getSvgWithInlinedStyles(),
    );
    this.#triggerDownload(
      new Blob([svgString], { type: "image/svg+xml" }),
      `${this.#exportBaseName}.svg`,
    );
  }

  #getPngBlob() {
    const clone = this.#getSvgWithInlinedStyles();
    const svgString = new XMLSerializer().serializeToString(clone);
    const width = parseFloat(clone.getAttribute("width"));
    const height = parseFloat(clone.getAttribute("height"));

    const canvas = document.createElement("canvas");
    const scale = 2; // Higher resolution
    canvas.width = width * scale;
    canvas.height = height * scale;
    const ctx = canvas.getContext("2d");
    ctx.scale(scale, scale);

    const url = URL.createObjectURL(
      new Blob([svgString], { type: "image/svg+xml" }),
    );

    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => {
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(0, 0, width, height);
        ctx.drawImage(img, 0, 0);
        URL.revokeObjectURL(url);
        canvas.toBlob((blob) => {
          if (blob) {
            resolve(blob);
          } else {
            reject(new Error("Failed to create PNG blob"));
          }
        }, "image/png");
      };
      img.onerror = () => {
        URL.revokeObjectURL(url);
        reject(new Error("Failed to load SVG image"));
      };
      img.src = url;
    });
  }

  exportPng() {
    this.#getPngBlob().then((blob) =>
      this.#triggerDownload(blob, `${this.#exportBaseName}.png`),
    );
  }

  copyPng(button) {
    const originalText = button.textContent;
    const restore = () => {
      setTimeout(() => {
        button.textContent = originalText;
      }, 1500);
    };
    // ClipboardItem accepts a Promise so Safari permits async blob generation
    // inside the user-gesture handler.
    const item = new ClipboardItem({
      "image/png": this.#getPngBlob(),
    });
    navigator.clipboard
      .write([item])
      .then(() => {
        button.textContent = "Copied!";
        restore();
      })
      .catch((err) => {
        console.error("Failed to copy PNG to clipboard:", err);
        button.textContent = "Copy failed";
        restore();
      });
  }

  get #width() {
    return this.#svg.node().getBoundingClientRect().width;
  }

  #render() {
    this.#root = d3
      .hierarchy(this.#data)
      .sum((d) => d.value)
      .sort((a, b) => b.value - a.value);

    this.#root.descendants().forEach((d, i) => {
      d.id = i;
    });

    document
      .getElementById("resetZoomButton")
      .addEventListener("click", () => this.#clicked(this.#root));

    const numLevels = this.#root.height + 1;
    const height = numLevels * this.#rowHeight + numLevels * this.#strokeWidth;
    this.#svg.attr("height", height);

    this.#x = d3.scaleLinear().range([0, this.#width]);
    this.#y = d3.scaleLinear().range([0, height]);

    const totalRuntime = this.#root.value;
    const fmtS = d3.format(".3f");
    const fmtPct = d3.format(".1%");
    const timeLabel = (d) =>
      d.data.text.length > 1
        ? d.data.text[1]
        : `${fmtS(d.value)} s  (${fmtPct(d.value / totalRuntime)})`;

    d3.partition()(this.#root);

    // Put text and rectangle into a group;
    // cf. <https://stackoverflow.com/a/6732550/353337>.
    const g = this.#svg
      .selectAll("g")
      .data(
        this.#root
          .descendants()
          .filter((d) => this.#x(d.x1) - this.#x(d.x0) > 1.0),
      )
      .enter()
      .append("g")
      .attr("class", (d) => "color" + d.data.color)
      .on("click", (evt, d) => this.#clicked(d));

    g.append("title").text((d) => `${d.data.text[0]} ${timeLabel(d)}`);

    this.#rect = g
      .append("rect")
      .attr("x", (d) => this.#x(d.x0))
      .attr("y", (d) => this.#y(d.y0))
      .attr("width", (d) => this.#x(d.x1) - this.#x(d.x0))
      .attr("height", this.#rowHeight);

    // First, the clip path, same as the rect.
    // It'd be nice to not have to repeat ourselves here, but the <use> suggestion from
    // <https://stackoverflow.com/q/23998457/353337> doesn't work.
    const cp = g.append("clipPath").attr("id", (d) => `cp${d.id}`);
    this.#clipRect = cp
      .append("rect")
      .attr("x", (d) => this.#x(d.x0))
      .attr("y", (d) => this.#y(d.y0))
      .attr("width", (d) => this.#x(d.x1) - this.#x(d.x0))
      .attr("height", this.#rowHeight);

    // Now the text. Multiline text is realized with <tspan> in SVG.
    this.#text = g
      .append("text")
      .attr("y", (d) => this.#y((d.y0 + d.y1) / 2))
      .attr("alignment-baseline", "middle")
      .attr("text-anchor", "middle")
      .attr("fill", "white")
      .attr("clip-path", (d) => `url(#cp${d.id})`);

    this.#tspan1 = this.#text
      .append("tspan")
      .text((d) => d.data.text[0])
      .attr("x", (d) => this.#x((d.x0 + d.x1) / 2));

    this.#tspan2 = this.#text
      .append("tspan")
      .text(timeLabel)
      .attr("x", (d) => this.#x((d.x0 + d.x1) / 2))
      .attr("dy", "1.5em");

    this.#resizeController = new AbortController();
    window.addEventListener("resize", () => this.#reposition(), {
      signal: this.#resizeController.signal,
    });
  }

  #reposition(trans = null) {
    const apply = (sel) => (trans ? sel.transition(trans) : sel);
    apply(this.#rect)
      .attr("x", (d) => this.#x(d.x0))
      .attr("y", (d) => this.#y(d.y0))
      .attr("width", (d) => this.#x(d.x1) - this.#x(d.x0));
    apply(this.#clipRect)
      .attr("x", (d) => this.#x(d.x0))
      .attr("y", (d) => this.#y(d.y0))
      .attr("width", (d) => this.#x(d.x1) - this.#x(d.x0));
    apply(this.#text).attr("y", (d) => this.#y((d.y0 + d.y1) / 2));
    apply(this.#tspan1).attr("x", (d) => this.#x((d.x0 + d.x1) / 2));
    apply(this.#tspan2).attr("x", (d) => this.#x((d.x0 + d.x1) / 2));
  }

  #clicked(d) {
    const offset = d.y0 ? 20 : 0;
    const numLevels = this.#root.height - d.depth;
    const newHeight =
      (numLevels + 1) * this.#rowHeight + (numLevels + 1) * this.#strokeWidth;
    this.#x.domain([d.x0, d.x1]).range([0, this.#width]);
    this.#y.domain([d.y0, 1]).range([offset, newHeight + offset]);
    this.#reposition(d3.transition().duration(300));
  }
}

try {
  customElements.define("x-icicle", Icicle);
} catch (err) {
  console.log(err);
  const h3 = document.createElement("h3");
  h3.innerHTML =
    "This site uses webcomponents which don't work in all browsers. Try this site in a browser that supports them.";
  document.body.appendChild(h3);
}
