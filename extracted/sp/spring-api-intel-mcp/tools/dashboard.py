import json
import os
from core.logger import get_logger
from core.indexer import CodeIndex
from tools.project_info import get_project_info

logger = get_logger("dashboard")

async def generate_dashboard(
    index: CodeIndex,
    project_root: str,
    spring_boot_url: str,
    streams: tuple
) -> str:
    """
    Generate a self-contained HTML dashboard for a Spring Boot codebase.
    Includes architecture diagram, dependency graph, tech stack, and class summaries.
    Uses sampling to generate the project description and key insights.
    """

    project_data = get_project_info(project_root)
    project_name = os.path.basename(project_root)

    layers = _build_layer_data(index)

    dep_graph = _build_dependency_graph(index)

    tech = _extract_tech(project_data)

    key_classes = _build_class_summaries(index)

    endpoint_stats = _build_endpoint_stats(index)

    description = ""
    insights = []

    #validation check for streams
    streams_ready=(
        streams is not None
        and len(streams) == 2
        and streams[0] is not None
        and streams[1] is not None
    )

    if streams_ready:
      try:
          from core.sampling import request_summary
          read_stream, write_stream = streams

          context = f"""
  Project name: {project_name}
  Tech stack: {tech.get('spring_boot', 'unknown')} Spring Boot, Java {tech.get('java', 'unknown')}
  Controllers: {', '.join(layers['controllers'])}
  Services: {', '.join(layers['services'])}
  Repositories: {', '.join(layers['repositories'])}
  Endpoints: {len(index.endpoints)} total
  Classes: {len(index.classes)} total
  """
          desc_prompt = (
              f"{context}\n\n"
              "Write 2-3 sentences describing what this Spring Boot project does, "
              "its purpose, and its main business domains. Be specific and technical. "
              "Do not use generic filler phrases."
          )
          description = await request_summary(read_stream, write_stream, desc_prompt)

          insights_prompt = (
              f"{context}\n\n"
              "List exactly 4 key architectural observations about this project. "
              "Each should be one sentence, specific, and useful to a new developer. "
              "Format as JSON array of strings. Example: "
              '[\"Auth is handled via JWT in a dedicated AuthController\", ...]'
          )
          insights_raw = await request_summary(read_stream, write_stream, insights_prompt)
          try:
              start = insights_raw.find("[")
              end = insights_raw.rfind("]") + 1
              if start >= 0 and end > start:
                  insights = json.loads(insights_raw[start:end])
          except Exception:
              insights = [insights_raw] if insights_raw else []

      except Exception:
        description = f"{project_name} — Spring Boot project"
        insights = []

    html = _render_html(
        project_name=project_name,
        description=description,
        tech=tech,
        layers=layers,
        dep_graph=dep_graph,
        key_classes=key_classes,
        endpoint_stats=endpoint_stats,
        insights=insights,
    )

    output_path = os.path.join(project_root, "dashboard.html")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        import webbrowser
        webbrowser.open(f"file:///{output_path.replace(os.sep, '/')}")
        logger.info(f"Dashboard generated: {output_path}")
        return f"Dashboard generated and opened in your browser.\nFile: {output_path}"
    except Exception as e:
        logger.error(f"Error writing dashboard: {e}")
        return f"Error writing dashboard: {e}\n\nHTML content:\n{html[:500]}..."


def _build_layer_data(index: CodeIndex) -> dict:
    controllers, services, repositories, models = [], [], [], []
    for name, info in index.classes.items():
        anns = [a.lower() for a in info.annotations]
        if "restcontroller" in anns or "controller" in anns:
            controllers.append(name)
        elif "service" in anns:
            services.append(name)
        elif "repository" in anns:
            repositories.append(name)
        elif "entity" in anns or "document" in anns:
            models.append(name)
    return {
        "controllers": sorted(controllers),
        "services": sorted(services),
        "repositories": sorted(repositories),
        "models": sorted(models),
    }


def _build_dependency_graph(index: CodeIndex) -> list[dict]:
    edges = []
    for name, info in index.classes.items():
        for dep in info.dependencies:
            dep_class = dep[0].upper() + dep[1:]
            if dep_class in index.classes:
                edges.append({"from": name, "to": dep_class})
    return edges


def _extract_tech(project_data: str) -> dict:
    tech = {}
    for line in project_data.splitlines():
        if "Java version" in line:
            tech["java"] = line.split(":")[-1].strip()
        elif "Spring Boot" in line:
            tech["spring_boot"] = line.split(":")[-1].strip()
        elif "Build tool" in line:
            tech["build_tool"] = line.split(":")[-1].strip()
        elif "Project" in line and ":" in line:
            tech["project"] = line.split(":")[-1].strip()
    return tech


def _build_class_summaries(index: CodeIndex) -> list[dict]:
    summaries = []
    for name, info in index.classes.items():
        anns = info.annotations
        role = "Other"
        if any(a in ["RestController", "Controller"] for a in anns):
            role = "Controller"
        elif "Service" in anns:
            role = "Service"
        elif "Repository" in anns:
            role = "Repository"
        elif "Entity" in anns:
            role = "Entity"
        summaries.append({
            "name": name,
            "role": role,
            "methods": len(info.methods),
            "dependencies": info.dependencies,
            "annotations": anns[:4],
        })
    return sorted(summaries, key=lambda x: (
        ["Controller", "Service", "Repository", "Entity", "Other"].index(x["role"])
    ))


def _build_endpoint_stats(index: CodeIndex) -> dict:
    by_method = {}
    by_controller = {}
    for ep in index.endpoints:
        by_method[ep.http_method] = by_method.get(ep.http_method, 0) + 1
        by_controller[ep.controller_class] = by_controller.get(ep.controller_class, 0) + 1
    return {"by_method": by_method, "by_controller": by_controller}


def _render_html(
    project_name, description, tech, layers,
    dep_graph, key_classes, endpoint_stats, insights
) -> str:
    layers_json = json.dumps(layers)
    dep_graph_json = json.dumps(dep_graph)
    endpoint_stats_json = json.dumps(endpoint_stats)
    key_classes_json = json.dumps(key_classes)
    insights_json = json.dumps(insights)
    tech_json = json.dumps(tech)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{project_name} — Architecture Dashboard</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; line-height: 1.6; }}
  .header {{ background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border-bottom: 1px solid #334155; padding: 2rem 2.5rem; }}
  .header h1 {{ font-size: 1.75rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.25rem; }}
  .header .subtitle {{ color: #94a3b8; font-size: 0.95rem; max-width: 700px; margin-top: 0.5rem; }}
  .badge {{ display: inline-block; padding: 0.2rem 0.6rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; margin-right: 0.4rem; margin-top: 0.5rem; }}
  .badge-blue {{ background: #1e40af22; color: #60a5fa; border: 1px solid #1e40af55; }}
  .badge-green {{ background: #16653422; color: #4ade80; border: 1px solid #16653455; }}
  .badge-amber {{ background: #92400e22; color: #fbbf24; border: 1px solid #92400e55; }}
  .badge-purple {{ background: #4c1d9522; color: #c084fc; border: 1px solid #4c1d9555; }}
  .grid {{ display: grid; gap: 1.5rem; padding: 2rem 2.5rem; max-width: 1400px; margin: 0 auto; }}
  .grid-2 {{ grid-template-columns: 1fr 1fr; }}
  .grid-3 {{ grid-template-columns: 1fr 1fr 1fr; }}
  .card {{ background: #1e293b; border: 1px solid #334155; border-radius: 12px; overflow: hidden; }}
  .card-header {{ padding: 1rem 1.25rem; border-bottom: 1px solid #334155; display: flex; align-items: center; gap: 0.5rem; }}
  .card-header h2 {{ font-size: 0.9rem; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; }}
  .card-body {{ padding: 1.25rem; }}
  .stat-row {{ display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid #1e293b; }}
  .stat-row:last-child {{ border-bottom: none; }}
  .stat-label {{ color: #94a3b8; font-size: 0.875rem; }}
  .stat-value {{ color: #f1f5f9; font-weight: 600; font-size: 0.875rem; }}
  .layer-box {{ border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 0.75rem; }}
  .layer-controller {{ background: #1e3a5f33; border: 1px solid #1e3a5f; }}
  .layer-service {{ background: #16453433; border: 1px solid #164534; }}
  .layer-repository {{ background: #3d1a7833; border: 1px solid #3d1a78; }}
  .layer-model {{ background: #4a1d2033; border: 1px solid #4a1d20; }}
  .layer-title {{ font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.4rem; }}
  .layer-controller .layer-title {{ color: #60a5fa; }}
  .layer-service .layer-title {{ color: #4ade80; }}
  .layer-repository .layer-title {{ color: #c084fc; }}
  .layer-model .layer-title {{ color: #fb923c; }}
  .layer-items {{ display: flex; flex-wrap: wrap; gap: 0.35rem; }}
  .chip {{ font-size: 0.75rem; padding: 0.2rem 0.5rem; border-radius: 6px; background: #0f172a; color: #cbd5e1; border: 1px solid #334155; cursor: default; }}
  .chip:hover {{ border-color: #60a5fa; color: #60a5fa; }}
  .arrow {{ text-align: center; color: #475569; font-size: 1.2rem; margin: 0.25rem 0; }}
  svg#depgraph {{ width: 100%; height: 340px; }}
  .node circle {{ stroke-width: 2; cursor: pointer; }}
  .node text {{ font-size: 11px; fill: #cbd5e1; pointer-events: none; }}
  .link {{ stroke: #334155; stroke-width: 1.5; fill: none; marker-end: url(#arrowhead); }}
  .class-table {{ width: 100%; border-collapse: collapse; font-size: 0.8rem; }}
  .class-table th {{ text-align: left; color: #64748b; font-weight: 600; padding: 0.4rem 0.6rem; border-bottom: 1px solid #334155; text-transform: uppercase; font-size: 0.7rem; letter-spacing: 0.05em; }}
  .class-table td {{ padding: 0.45rem 0.6rem; border-bottom: 1px solid #1e293b; vertical-align: top; }}
  .class-table tr:hover td {{ background: #ffffff08; }}
  .role-pill {{ font-size: 0.7rem; padding: 0.15rem 0.45rem; border-radius: 4px; font-weight: 600; }}
  .role-Controller {{ background: #1e3a5f55; color: #60a5fa; }}
  .role-Service {{ background: #16453455; color: #4ade80; }}
  .role-Repository {{ background: #3d1a7855; color: #c084fc; }}
  .role-Entity {{ background: #4a1d2055; color: #fb923c; }}
  .role-Other {{ background: #1e293b; color: #64748b; }}
  .insight {{ display: flex; gap: 0.75rem; padding: 0.6rem 0; border-bottom: 1px solid #1e293b; align-items: flex-start; }}
  .insight:last-child {{ border-bottom: none; }}
  .insight-dot {{ width: 6px; height: 6px; border-radius: 50%; background: #60a5fa; margin-top: 0.45rem; flex-shrink: 0; }}
  .insight-text {{ font-size: 0.875rem; color: #cbd5e1; }}
  .method-bar {{ display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem; }}
  .method-label {{ width: 60px; font-size: 0.75rem; font-weight: 700; }}
  .GET {{ color: #4ade80; }} .POST {{ color: #60a5fa; }} .PUT {{ color: #fbbf24; }} .DELETE {{ color: #f87171; }} .PATCH {{ color: #c084fc; }}
  .bar-track {{ flex: 1; background: #0f172a; border-radius: 4px; height: 8px; overflow: hidden; }}
  .bar-fill {{ height: 100%; border-radius: 4px; transition: width 0.8s ease; }}
  .GET-fill {{ background: #4ade80; }} .POST-fill {{ background: #60a5fa; }} .PUT-fill {{ background: #fbbf24; }} .DELETE-fill {{ background: #f87171; }} .PATCH-fill {{ background: #c084fc; }}
  .bar-count {{ font-size: 0.75rem; color: #64748b; width: 20px; text-align: right; }}
  @media (max-width: 900px) {{ .grid-2, .grid-3 {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>

<div class="header">
  <h1>{project_name}</h1>
  <p class="subtitle" id="description">Loading project description...</p>
  <div id="badges"></div>
</div>

<div class="grid grid-3">

  <!-- Tech Stack -->
  <div class="card">
    <div class="card-header"><h2>Tech Stack</h2></div>
    <div class="card-body" id="tech-stack"></div>
  </div>

  <!-- Endpoint Methods -->
  <div class="card">
    <div class="card-header"><h2>Endpoints by Method</h2></div>
    <div class="card-body" id="endpoint-methods"></div>
  </div>

  <!-- Key Insights -->
  <div class="card">
    <div class="card-header"><h2>Key Insights</h2></div>
    <div class="card-body" id="insights"></div>
  </div>

</div>

<div class="grid grid-2">

  <!-- Architecture Layers -->
  <div class="card">
    <div class="card-header"><h2>Architecture Layers</h2></div>
    <div class="card-body" id="layers"></div>
  </div>

  <!-- Dependency Graph -->
  <div class="card">
    <div class="card-header"><h2>Dependency Graph</h2></div>
    <div class="card-body" style="padding:0">
      <svg id="depgraph">
        <defs>
          <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="6" refY="3" orient="auto">
            <polygon points="0 0, 8 3, 0 6" fill="#475569"/>
          </marker>
        </defs>
      </svg>
    </div>
  </div>

</div>

<div class="grid">
  <!-- Class Table -->
  <div class="card">
    <div class="card-header"><h2>Class Overview</h2></div>
    <div class="card-body" style="padding:0; overflow-x:auto;">
      <table class="class-table">
        <thead>
          <tr>
            <th style="padding-left:1.25rem">Class</th>
            <th>Role</th>
            <th>Methods</th>
            <th>Dependencies</th>
          </tr>
        </thead>
        <tbody id="class-table-body"></tbody>
      </table>
    </div>
  </div>
</div>

<script>
const layers = {layers_json};
const depGraph = {dep_graph_json};
const endpointStats = {endpoint_stats_json};
const keyClasses = {key_classes_json};
const insights = {insights_json};
const tech = {tech_json};
const description = {json.dumps(description)};

// Description
document.getElementById('description').textContent = description || '{project_name} — Spring Boot project';

// Badges
const badgeEl = document.getElementById('badges');
const counts = [
  [layers.controllers.length + ' Controllers', 'badge-blue'],
  [layers.services.length + ' Services', 'badge-green'],
  [layers.repositories.length + ' Repositories', 'badge-purple'],
  [Object.values(endpointStats.by_method).reduce((a,b)=>a+b,0) + ' Endpoints', 'badge-amber'],
];
counts.forEach(([label, cls]) => {{
  const b = document.createElement('span');
  b.className = 'badge ' + cls;
  b.textContent = label;
  badgeEl.appendChild(b);
}});

// Tech stack
const techEl = document.getElementById('tech-stack');
const techItems = [
  ['Java', tech.java || 'unknown'],
  ['Spring Boot', tech.spring_boot || 'unknown'],
  ['Build Tool', tech.build_tool || 'unknown'],
  ['Project', tech.project || '{project_name}'],
  ['Total Classes', keyClasses.length],
];
techItems.forEach(([k, v]) => {{
  techEl.innerHTML += `<div class="stat-row"><span class="stat-label">${{k}}</span><span class="stat-value">${{v}}</span></div>`;
}});

// Endpoint methods bar chart
const epEl = document.getElementById('endpoint-methods');
const maxCount = Math.max(...Object.values(endpointStats.by_method), 1);
Object.entries(endpointStats.by_method).forEach(([method, count]) => {{
  epEl.innerHTML += `
    <div class="method-bar">
      <span class="method-label ${{method}}">${{method}}</span>
      <div class="bar-track"><div class="bar-fill ${{method}}-fill" style="width:${{(count/maxCount*100).toFixed(0)}}%"></div></div>
      <span class="bar-count">${{count}}</span>
    </div>`;
}});

// Insights
const insightEl = document.getElementById('insights');
if (insights.length > 0) {{
  insights.forEach(text => {{
    insightEl.innerHTML += `<div class="insight"><div class="insight-dot"></div><span class="insight-text">${{text}}</span></div>`;
  }});
}} else {{
  insightEl.innerHTML = '<p style="color:#64748b;font-size:0.875rem">Run with sampling enabled to generate insights.</p>';
}}

// Architecture layers
const layerEl = document.getElementById('layers');
const layerConfig = [
  ['controllers', 'Controller', 'HTTP Layer', 'layer-controller'],
  ['services',    'Service',    'Business Logic', 'layer-service'],
  ['repositories','Repository', 'Data Layer', 'layer-repository'],
  ['models',      'Model',      'Domain Models', 'layer-model'],
];
layerConfig.forEach(([key, label, subtitle, cls], i) => {{
  const items = layers[key];
  if (!items || items.length === 0) return;
  if (i > 0) layerEl.innerHTML += '<div class="arrow">↓</div>';
  layerEl.innerHTML += `
    <div class="layer-box ${{cls}}">
      <div class="layer-title">${{label}} — ${{subtitle}}</div>
      <div class="layer-items">${{items.map(n => `<span class="chip">${{n}}</span>`).join('')}}</div>
    </div>`;
}});

// Class table
const tbody = document.getElementById('class-table-body');
keyClasses.slice(0, 40).forEach(c => {{
  const deps = c.dependencies.slice(0,3).join(', ') || '—';
  tbody.innerHTML += `
    <tr>
      <td style="padding-left:1.25rem;color:#f1f5f9;font-weight:500">${{c.name}}</td>
      <td><span class="role-pill role-${{c.role}}">${{c.role}}</span></td>
      <td style="color:#64748b">${{c.methods}}</td>
      <td style="color:#64748b">${{deps}}</td>
    </tr>`;
}});

// Dependency graph with D3 force layout
(function() {{
  const nodes = [...new Set(depGraph.flatMap(e => [e.from, e.to]))].map(id => ({{id}}));
  const links = depGraph.map(e => ({{source: e.from, target: e.to}}));
  if (nodes.length === 0) return;

  const svg = d3.select('#depgraph');
  const width = svg.node().parentElement.clientWidth || 600;
  const height = 340;
  svg.attr('viewBox', `0 0 ${{width}} ${{height}}`);

  const colorMap = {{}};
  keyClasses.forEach(c => colorMap[c.name] = {{
    Controller: '#60a5fa', Service: '#4ade80',
    Repository: '#c084fc', Entity: '#fb923c'
  }}[c.role] || '#64748b');

  const sim = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(links).id(d => d.id).distance(90))
    .force('charge', d3.forceManyBody().strength(-180))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collision', d3.forceCollide(36));

  const link = svg.append('g').selectAll('line')
    .data(links).join('line').attr('class', 'link');

  const node = svg.append('g').selectAll('g')
    .data(nodes).join('g').attr('class', 'node')
    .call(d3.drag()
      .on('start', (e, d) => {{ if (!e.active) sim.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; }})
      .on('drag',  (e, d) => {{ d.fx = e.x; d.fy = e.y; }})
      .on('end',   (e, d) => {{ if (!e.active) sim.alphaTarget(0); d.fx = null; d.fy = null; }}));

  node.append('circle').attr('r', 18)
    .attr('fill', d => (colorMap[d.id] || '#64748b') + '33')
    .attr('stroke', d => colorMap[d.id] || '#64748b');

  node.append('text').attr('dy', 30).attr('text-anchor', 'middle')
    .text(d => d.id.replace(/Controller|Service|Repository/g, m => m[0]));

  sim.on('tick', () => {{
    link.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
    node.attr('transform', d => `translate(${{d.x}},${{d.y}})`);
  }});
}})();
</script>
</body>
</html>"""