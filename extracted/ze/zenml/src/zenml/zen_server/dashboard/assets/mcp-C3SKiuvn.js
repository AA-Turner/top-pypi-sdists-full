import{o as e}from"./rolldown-runtime-BCiCTKAo.js";import{t}from"./react-D2YmWxFb.js";import{t as n}from"./button-COwrIhD-.js";import{r}from"./utils-CinycaQR.js";import{u as i}from"./useOpenChangeComplete-_x48rcIt.js";import{Kt as a,n as o,t as s}from"./CopyButton-YfTXN4o6.js";import{n as c,r as l}from"./serializeValue-AMAkJ5kG.js";import{t as u}from"./link-ByW4LJra.js";import{t as d}from"./input-DbjImulk.js";import{i as f,n as p,r as m,t as h}from"./tabs-CyWLelSl.js";import{t as g}from"./segmented-choice-Cl_sCtUu.js";import{Q as _,St as v,j as y,mt as b,pt as x}from"./index-DACdppmF.js";var S=e(t(),1),C=`zenmldocker/mcp-zenml:latest`,w={LOGLEVEL:`WARNING`,NO_COLOR:`1`,ZENML_LOGGING_COLORS_DISABLED:`true`,ZENML_LOGGING_VERBOSITY:`WARN`,ZENML_ENABLE_RICH_TRACEBACK:`false`,PYTHONUNBUFFERED:`1`,PYTHONIOENCODING:`UTF-8`};function T(e){return e?[`-e`,`ZENML_ACTIVE_PROJECT_ID=${e}`]:[]}function E(e){return e?`\n\t-e ZENML_ACTIVE_PROJECT_ID=${e} \\`:``}function D(e){return e?`\n\t\t\t"-e","ZENML_ACTIVE_PROJECT_ID=${e}",`:``}function O(e){return e?`,\n\t\t"ZENML_ACTIVE_PROJECT_ID": "${e}"`:``}function k(e){return e?`\n\t--env ZENML_ACTIVE_PROJECT_ID=${e} \\`:``}function A(){return Object.entries(w).flatMap(([e,t])=>[`-e`,`${e}=${t}`])}function j(e){let t=JSON.stringify(e);if(typeof window<`u`&&typeof window.btoa==`function`)return window.btoa(t);if(typeof Buffer<`u`)return Buffer.from(t,`utf-8`).toString(`base64`);throw Error(`No base64 implementation available`)}function M(e,t,n){return[`run`,`-i`,`--rm`,`-e`,`ZENML_STORE_URL=${e}`,`-e`,`ZENML_STORE_API_KEY=${t}`,...T(n),...A(),C]}function N(e,t,n){let r={name:`zenml`,command:`docker`,args:M(e,t,n)};return`vscode:mcp/install?${encodeURIComponent(JSON.stringify(r))}`}function P(e,t,n){return`cursor://anysphere.cursor-deeplink/mcp/install?name=zenml&config=${j({command:`docker`,args:M(e,t,n),type:`stdio`})}`}function F(e,t,n){let r={name:`zenml`,command:`docker`,args:M(e,t,n)};return`code --add-mcp "${JSON.stringify(r).replaceAll(`"`,`\\"`)}"`}var I=(e,t,n)=>JSON.stringify({mcpServers:{zenml:{command:`docker`,args:[`run`,`-i`,`--rm`,`-e`,`ZENML_STORE_URL=${e}`,`-e`,`ZENML_STORE_API_KEY=${t}`,...T(n),...A(),C]}}},null,2),L=(e,t,n)=>JSON.stringify({mcpServers:{zenml:{command:`/usr/local/bin/uv`,args:[`run`,`path/to/mcp-zenml/server/zenml_server.py`],env:{...w,ZENML_STORE_URL:e,ZENML_STORE_API_KEY:t,...n?{ZENML_ACTIVE_PROJECT_ID:n}:{}}}}},null,2);function R(e,t,n){let r=I(e,t,n),i=L(e,t,n);return[{name:`VS Code`,value:`vscode`,methods:[{title:`Deep link`,type:`install-link`,url:N(e,t,n),description:`Click the link to add the Docker-driven MCP server to VS Code.`,steps:[`Click Install in VS Code above`,`VS Code will prompt you to install the server`]},{title:`Docker`,type:`code`,code:F(e,t,n),description:`Use the VS Code CLI to install the ZenML MCP Server.`,steps:[`Run the command in your terminal`,`The server will be added to your VS Code configuration`]},{title:`uv`,type:`code`,code:`code --add-mcp '{\n  "name": "zenml",\n  "command": "/usr/local/bin/uv",\n  "args": ["run", "/path/to/mcp-zenml/server/zenml_server.py"],\n  "env": {\n    "LOGLEVEL": "WARNING",\n    "NO_COLOR": "1",\n    "ZENML_LOGGING_COLORS_DISABLED": "true",\n    "ZENML_LOGGING_VERBOSITY": "WARN",\n    "ZENML_ENABLE_RICH_TRACEBACK": "false",\n    "PYTHONUNBUFFERED": "1",\n    "PYTHONIOENCODING": "UTF-8",\n    "ZENML_STORE_URL": "${e}",\n    "ZENML_STORE_API_KEY": "${t}"${n?`,\n    "ZENML_ACTIVE_PROJECT_ID": "${n}"`:``}\n  }\n}'`,description:`Use the VS Code CLI with uv to install the ZenML MCP Server.`,steps:["Clone the repository: `git clone --depth 1 --branch main https://github.com/zenml-io/mcp-zenml.git`","Ensure `uv` is installed globally","Update the command to point to your `uv` and repository paths",`Run the command in your terminal`]}]},{name:`Claude Desktop`,value:`claude-desktop`,methods:[{title:`.mcpb file`,type:`releases-link`,description:`Install the packaged server from its latest release.`,url:`https://github.com/zenml-io/mcp-zenml/releases`,steps:[`Visit https://github.com/zenml-io/mcp-zenml/releases and click on the latest release`,`Download the mcp-zenml.mcpb file from the Assets section`,`Open Claude Desktop and drag the .mcpb file onto the icon`,`Click the "Disabled" button to enable the MCP server`]},{title:`Docker`,type:`code`,code:r,description:"Add to `claude_desktop_config.json`.",steps:["Add the configuration to your `claude_desktop_config.json` file","This file is usually located in `Application Support/Claude` directory","If you already have MCP servers configured, only add the `zenml` section"]},{title:`uv`,type:`code`,code:i,description:"Add to `claude_desktop_config.json`, with your own `uv` and repository paths.",steps:["Clone the repository: `git clone --depth 1 --branch main https://github.com/zenml-io/mcp-zenml.git`","Ensure `uv` is installed globally on your system","Add the configuration to your `claude_desktop_config.json` file","Update the `command` and `args` to point to where `uv` is installed and where you cloned the repository"],note:`You will need to update the command and args paths to match your local installation.`}],troubleshooting:`If the MCP server is not installed correctly, Claude Desktop will tell you it doesn't have access to the ZenML tools. Check the logs for any errors.`},{name:`Cursor`,value:`cursor`,methods:[{title:`Deep link`,type:`install-link`,url:P(e,t,n),description:`Click to add the ZenML MCP server to Cursor.`,steps:[`Click Install in Cursor above`,`Cursor will prompt you to install the server`]},{title:`Docker`,type:`code`,code:`mkdir -p ~/.cursor && \\
if [ -f ~/.cursor/mcp.json ]; then \\
	cp ~/.cursor/mcp.json ~/.cursor/mcp.json.backup && \\
	jq '.mcpServers.zenml = {
	"command":"docker",
	"args":["run","-i","--rm",
			"-e","ZENML_STORE_URL=${e}",
			"-e","ZENML_STORE_API_KEY=${t}",${D(n)}
			"-e","LOGLEVEL=WARNING",
			"-e","NO_COLOR=1",
			"-e","ZENML_LOGGING_COLORS_DISABLED=true",
			"-e","ZENML_LOGGING_VERBOSITY=WARN",
			"-e","ZENML_ENABLE_RICH_TRACEBACK=false",
			"-e","PYTHONUNBUFFERED=1",
			"-e","PYTHONIOENCODING=UTF-8",
			"${C}"],
	"type":"stdio"
	}' ~/.cursor/mcp.json > ~/.cursor/mcp.json.tmp && \\
	mv ~/.cursor/mcp.json.tmp ~/.cursor/mcp.json; \\
else \\
	echo '{"mcpServers":{}}' | jq '.mcpServers.zenml = {
	"command":"docker",
	"args":["run","-i","--rm",
			"-e","ZENML_STORE_URL=${e}",
			"-e","ZENML_STORE_API_KEY=${t}",${D(n)}
			"-e","LOGLEVEL=WARNING",
			"-e","NO_COLOR=1",
			"-e","ZENML_LOGGING_COLORS_DISABLED=true",
			"-e","ZENML_LOGGING_VERBOSITY=WARN",
			"-e","ZENML_ENABLE_RICH_TRACEBACK=false",
			"-e","PYTHONUNBUFFERED=1",
			"-e","PYTHONIOENCODING=UTF-8",
			"${C}"],
	"type":"stdio"
	}' > ~/.cursor/mcp.json; \\
fi`,description:`Use this CLI command to install the ZenML MCP Server in Cursor.`,steps:[`Run the command in your terminal`,"The server will be added to `~/.cursor/mcp.json`"]},{title:`uv`,type:`code`,code:`mkdir -p ~/.cursor && \\
if [ -f ~/.cursor/mcp.json ]; then \\
	cp ~/.cursor/mcp.json ~/.cursor/mcp.json.backup && \\
	jq '.mcpServers.zenml = {
	"command": "/usr/local/bin/uv",
	"args": ["run", "path/to/mcp-zenml/server/zenml_server.py"],
	"env": {
		"LOGLEVEL": "WARNING",
		"NO_COLOR": "1",
		"ZENML_LOGGING_COLORS_DISABLED": "true",
		"ZENML_LOGGING_VERBOSITY": "WARN",
		"ZENML_ENABLE_RICH_TRACEBACK": "false",
		"PYTHONUNBUFFERED": "1",
		"PYTHONIOENCODING": "UTF-8",
		"ZENML_STORE_URL": "${e}",
		"ZENML_STORE_API_KEY": "${t}"${O(n)}
	}
	}' ~/.cursor/mcp.json > ~/.cursor/mcp.json.tmp && \\
	mv ~/.cursor/mcp.json.tmp ~/.cursor/mcp.json; \\
else \\
	echo '{"mcpServers":{}}' | jq '.mcpServers.zenml = {
	"command": "/usr/local/bin/uv",
	"args": ["run", "path/to/mcp-zenml/server/zenml_server.py"],
	"env": {
		"LOGLEVEL": "WARNING",
		"NO_COLOR": "1",
		"ZENML_LOGGING_COLORS_DISABLED": "true",
		"ZENML_LOGGING_VERBOSITY": "WARN",
		"ZENML_ENABLE_RICH_TRACEBACK": "false",
		"PYTHONUNBUFFERED": "1",
		"PYTHONIOENCODING": "UTF-8",
		"ZENML_STORE_URL": "${e}",
		"ZENML_STORE_API_KEY": "${t}"${O(n)}
	}
	}' > ~/.cursor/mcp.json; \\
fi`,description:`Use this CLI command to install the ZenML MCP Server with uv in Cursor.`,steps:["Clone the repository: `git clone --depth 1 --branch main https://github.com/zenml-io/mcp-zenml.git`","Ensure `uv` is installed globally","Update the command to point to your `uv` and repository paths",`Run the command in your terminal`]}]},{name:`Claude Code`,value:`claude-code`,methods:[{title:`Docker`,type:`code`,code:`# Add for your current project (local scope)
claude mcp add zenml -- \\
	docker run -i --rm \\
	-e ZENML_STORE_URL=${e} \\
	-e ZENML_STORE_API_KEY=${t} \\${E(n)}
	-e LOGLEVEL=WARNING \\
	-e NO_COLOR=1 \\
	-e ZENML_LOGGING_COLORS_DISABLED=true \\
	-e ZENML_LOGGING_VERBOSITY=WARN \\
	-e ZENML_ENABLE_RICH_TRACEBACK=false \\
	-e PYTHONUNBUFFERED=1 \\
	-e PYTHONIOENCODING=UTF-8 \\
	${C}`,description:`Install the ZenML MCP Server using the Claude CLI.`,steps:[`Run the command in your terminal for local scope`,"For user-scoped installation, add `--scope user` flag after `zenml`"],note:"User scope: `claude mcp add zenml --scope user --` [rest of command]"},{title:`uv`,type:`code`,code:`# Add for your current project (local scope)
claude mcp add zenml \\
	--env LOGLEVEL=WARNING \\
	--env NO_COLOR=1 \\
	--env ZENML_LOGGING_COLORS_DISABLED=true \\
	--env ZENML_LOGGING_VERBOSITY=WARN \\
	--env ZENML_ENABLE_RICH_TRACEBACK=false \\
	--env PYTHONUNBUFFERED=1 \\
	--env PYTHONIOENCODING=UTF-8 \\
	--env ZENML_STORE_URL=${e} \\
	--env ZENML_STORE_API_KEY=${t} \\${k(n)}
	-- /usr/local/bin/uv run /path/to/mcp-zenml/server/zenml_server.py`,description:`Install the ZenML MCP Server with uv using the Claude CLI.`,steps:["Clone the repository: `git clone --depth 1 --branch main https://github.com/zenml-io/mcp-zenml.git`","Ensure `uv` is installed globally","Update the command to point to your `uv` and repository paths",`Run the command in your terminal`,"For user-scoped installation, add `--scope user` flag after `zenml`"]}],troubleshooting:"Use the `/mcp` command inside claude to check connection status and trigger reconnect if needed."},{name:`OpenAI Codex`,value:`codex`,methods:[{title:`Docker`,type:`code`,code:`codex mcp add zenml docker run -i --rm \\
	-e ZENML_STORE_URL=${e} \\
	-e ZENML_STORE_API_KEY=${t} \\${E(n)}
	-e LOGLEVEL=WARNING \\
	-e NO_COLOR=1 \\
	-e ZENML_LOGGING_COLORS_DISABLED=true \\
	-e ZENML_LOGGING_VERBOSITY=WARN \\
	-e ZENML_ENABLE_RICH_TRACEBACK=false \\
	-e PYTHONUNBUFFERED=1 \\
	-e PYTHONIOENCODING=UTF-8 \\
	${C}`,description:`Install the ZenML MCP Server using the Codex CLI.`,steps:[`Run the command in your terminal`]},{title:`uv`,type:`code`,code:`codex mcp add zenml /usr/local/bin/uv run path/to/mcp-zenml/server/zenml_server.py \\
	--env LOGLEVEL=WARNING \\
	--env NO_COLOR=1 \\
	--env ZENML_LOGGING_COLORS_DISABLED=true \\
	--env ZENML_LOGGING_VERBOSITY=WARN \\
	--env ZENML_ENABLE_RICH_TRACEBACK=false \\
	--env PYTHONUNBUFFERED=1 \\
	--env PYTHONIOENCODING=UTF-8 \\
	--env ZENML_STORE_URL=${e} \\
	--env ZENML_STORE_API_KEY=${t}${n?` \\`:``}${n?k(n).replace(` \\`,``):``}`,description:`Install the ZenML MCP Server with uv using the Codex CLI.`,steps:["Clone the repository: `git clone --depth 1 --branch main https://github.com/zenml-io/mcp-zenml.git`","Ensure `uv` is installed globally","Update the command to point to your `uv` and repository paths",`Run the command in your terminal`]}],troubleshooting:"Use the `/mcp` command inside codex to check connection status and trigger reconnect if needed."},{name:`Other Clients`,value:`other`,methods:[{title:`Docker`,type:`code`,code:r,description:`Use this JSON configuration for any MCP client that supports Docker-based servers.`,steps:[`Insert this configuration where your application requires MCP server registration`,"Update `ZENML_STORE_URL`, `ZENML_STORE_API_KEY`, and `ZENML_ACTIVE_PROJECT_ID` with your values"]},{title:`uv`,type:`code`,code:i,description:"Use this JSON configuration for any MCP client that supports local execution with `uv`.",steps:["Clone the repository: `git clone --depth 1 --branch main https://github.com/zenml-io/mcp-zenml.git`","Ensure `uv` is installed globally","Update the `command` and `args` paths to match your installation","Update `ZENML_STORE_URL`, `ZENML_STORE_API_KEY`, and `ZENML_ACTIVE_PROJECT_ID` with your values",`Insert this configuration where your application requires MCP server registration`]}]}]}var z=new Set([`https:`,`http:`,`vscode:`,`cursor:`]);function B(e){if(!e)return!1;try{let t=new URL(e),n=t.protocol;return!(!z.has(n)||n===`cursor:`&&t.hostname!==`anysphere.cursor-deeplink`)}catch{return!1}}var V=r();function H({clients:e}){let[t,n]=(0,S.useState)({});return(0,V.jsxs)(h,{defaultValue:e[0]?.value,className:`flex flex-col gap-4`,children:[(0,V.jsx)(m,{variant:`line`,"aria-label":`Client`,className:`justify-start`,children:e.map(e=>(0,V.jsx)(f,{value:e.value,className:`flex-none`,children:e.name},e.value))}),e.map(e=>(0,V.jsx)(p,{value:e.value,children:(0,V.jsx)(U,{client:e,methodIndex:t[e.value]??0,onMethodChange:t=>n(n=>({...n,[e.value]:t}))})},e.value))]})}function U({client:e,methodIndex:t,onMethodChange:n}){let r=e.methods[t]??e.methods[0];return(0,V.jsxs)(`div`,{className:`flex flex-col gap-3`,children:[e.methods.length>1&&(0,V.jsx)(g,{size:`sm`,"aria-label":`How to install in ${e.name}`,value:String(t),onValueChange:e=>n(Number(e)),options:e.methods.map((e,t)=>({value:String(t),label:e.title,tone:`neutral`}))}),r&&(0,V.jsx)(W,{method:r,clientName:e.name}),e.troubleshooting&&(0,V.jsx)(`p`,{className:`text-label text-muted-foreground-text`,children:(0,V.jsx)(_,{text:e.troubleshooting})})]})}function W({method:e,clientName:t}){let r=e.type===`code`?e.code:null,s=e.type!==`code`&&B(e.url)?e.url:null,{copied:c,copy:l}=o();return(0,V.jsxs)(V.Fragment,{children:[(0,V.jsxs)(`div`,{className:`flex min-h-8 items-center gap-2`,children:[(0,V.jsx)(`p`,{className:`flex-1 text-body text-foreground`,children:(0,V.jsx)(_,{text:e.description})}),r&&(0,V.jsxs)(n,{variant:`outline`,size:`sm`,onClick:()=>l(r),children:[c?(0,V.jsx)(i,{className:`size-3.5`}):(0,V.jsx)(a,{className:`size-3.5`}),c?`Copied`:`Copy`]}),s&&(0,V.jsxs)(n,{size:`sm`,render:(0,V.jsx)(`a`,{href:s,target:`_blank`,rel:`noopener noreferrer`}),children:[(0,V.jsx)(v,{className:`size-3.5`,"aria-hidden":!0}),e.type===`install-link`?`Install in ${t}`:`Open releases`]})]}),r&&(0,V.jsx)(`pre`,{tabIndex:0,className:`overflow-x-auto rounded-lg border border-border bg-muted p-4 font-mono text-value leading-5 text-foreground`,children:r}),e.steps.length>0&&(0,V.jsx)(`ol`,{className:`flex list-decimal flex-col gap-1 pl-5 text-body text-muted-foreground-text`,children:e.steps.map(e=>(0,V.jsx)(`li`,{children:(0,V.jsx)(_,{text:e})},e))}),e.note&&(0,V.jsx)(`p`,{className:`text-label text-muted-foreground-text`,children:(0,V.jsx)(_,{text:e.note})})]})}var G=`https://docs.zenml.io/user-guides/best-practices/mcp-chat-with-server`;function K({scope:e,target:t,children:n}){return(0,V.jsxs)(`div`,{className:`flex max-w-190 flex-col gap-6`,children:[(0,V.jsxs)(`header`,{className:`flex min-h-8 flex-col gap-0.5`,children:[(0,V.jsx)(`span`,{className:`text-label text-muted-foreground-text`,children:e}),(0,V.jsx)(`h1`,{className:`truncate text-h20 font-medium text-foreground`,children:`MCP`})]}),(0,V.jsxs)(`p`,{className:`text-body text-muted-foreground-text`,children:[`Connect an IDE or AI assistant to this `,t,` through the ZenML MCP server, which runs on your machine.`,` `,(0,V.jsx)(`a`,{href:G,target:`_blank`,rel:`noreferrer noopener`,className:`text-primary-text underline-offset-2 hover:underline`,children:`Learn more`})]}),n]})}function q({target:e,serverUrl:t,projectPicker:n}){let r=`${e.charAt(0).toUpperCase()}${e.slice(1)} URL`;return(0,V.jsxs)(`section`,{className:`flex flex-col gap-2`,children:[(0,V.jsx)(`h2`,{className:`text-label font-medium text-muted-foreground`,children:`Server`}),(0,V.jsxs)(x,{children:[(0,V.jsxs)(b,{label:r,description:`Where the server connects`,children:[(0,V.jsx)(`span`,{className:`min-w-0 flex-1 truncate font-mono text-body text-foreground`,children:t}),(0,V.jsx)(s,{text:t,label:`Copy ${e} URL`})]}),n&&(0,V.jsx)(b,{label:`Project`,description:`Where the server works`,children:n})]})]})}function J({token:e,onTokenChange:t,options:r}){let[i,a]=(0,S.useState)(!1),[o,u]=(0,S.useState)(null);function f(e){t(e),u(null),e||a(!1)}return(0,V.jsxs)(`section`,{className:`flex flex-col gap-2`,children:[(0,V.jsx)(`h2`,{className:`text-label font-medium text-muted-foreground`,children:r.title}),(0,V.jsxs)(x,{children:[o&&(0,V.jsx)(y,{message:`Token created and added to the setup below. Copy it now, it won't be shown again.`,value:o}),(0,V.jsxs)(`div`,{className:`flex items-center gap-2 p-4`,children:[(0,V.jsxs)(`div`,{className:`relative min-w-0 flex-1`,children:[(0,V.jsx)(d,{type:e&&!i?`password`:`text`,value:e??``,onChange:e=>f(e.target.value||null),placeholder:r.placeholder,"aria-label":r.inputLabel,autoComplete:`off`,spellCheck:!1,className:`pr-16 font-mono`}),e&&(0,V.jsxs)(`div`,{className:`absolute top-1/2 right-1 flex -translate-y-1/2 items-center`,children:[(0,V.jsx)(n,{variant:`ghost`,size:`icon-sm`,"aria-label":i?`Hide token`:`Show token`,onClick:()=>a(e=>!e),children:i?(0,V.jsx)(l,{className:`size-3.5`}):(0,V.jsx)(c,{className:`size-3.5`})}),(0,V.jsx)(s,{text:e,label:`Copy token`})]})]}),e&&(0,V.jsx)(n,{variant:`outline`,onClick:()=>f(null),children:`Remove`})]}),(0,V.jsxs)(`div`,{className:`flex flex-wrap items-center justify-between gap-3 border-t border-muted bg-footer px-4 py-3`,children:[(0,V.jsxs)(`p`,{className:`text-label text-muted-foreground-text`,children:[e?r.filledHint:r.emptyHint,r.help&&(0,V.jsxs)(V.Fragment,{children:[` `,r.help]})]}),r.create?.(e=>{t(e),u(e)})]})]})]})}var Y=(0,S.createContext)(null);function X({children:e,...t}){return(0,V.jsx)(Y.Provider,{value:t,children:e})}function Z(){let e=(0,S.useContext)(Y);if(!e)throw Error(`useMcpRoute must be used within a McpRouteProvider`);return e}var Q=`your_api_key_here`;function $(){let{scope:e,target:t,serverUrl:n,project:r,token:i}=Z(),[a,o]=(0,S.useState)(null),s=r?.id??``,c=(0,S.useMemo)(()=>R(n,a||Q,s),[n,a,s]);return(0,V.jsxs)(K,{scope:e,target:t,children:[(0,V.jsx)(q,{target:t,serverUrl:n,projectPicker:r?.picker}),(0,V.jsx)(J,{token:a,onTokenChange:o,options:i}),(0,V.jsx)(H,{clients:c})]})}function ee(){return(0,V.jsx)(X,{scope:`Server`,target:`server`,serverUrl:window.location.origin,token:{title:`API key`,inputLabel:`API key`,placeholder:`Paste a service account API key`,emptyHint:`Paste an API key from a service account, and the setup below includes it.`,filledHint:`The setup below includes this API key.`,help:(0,V.jsx)(u,{to:`/settings/service-accounts`,className:`text-primary-text underline-offset-2 hover:underline`,children:`Manage service accounts`})},children:(0,V.jsx)($,{})})}var te=ee;export{te as component};