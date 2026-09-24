import{i as e}from"./rolldown-runtime-Dd_uD5pT.js";import{m as t,p as n}from"./utils-CRVOceX-.js";import{t as r}from"./check-Bttd4z5p.js";import{t as i}from"./CollapsibleCard-fuM_8G-D.js";import{t as a}from"./copy-CBaaoOY3.js";import{t as o}from"./eye-off-CZdGf4Xl.js";import{t as s}from"./eye-D1qx5xz6.js";import{t as c}from"./routes-DM-ZUc34.js";import{t as l}from"./button-CewZD7rC.js";import{Ft as u,G as d,H as f,L as p,M as m,Mt as h,Nn as g,Nt as _,Pt as v,R as y,U as b,V as x,W as S,at as C,nr as w,ot as T,xt as E,z as D}from"./index-ClLsmNAr.js";import{t as O}from"./CodeSnippet-bj9q3GiY.js";import{t as k}from"./Infobox-QC9ojRbf.js";var A=e(t(),1),j=n();function M({token:e,onTokenChange:t}){let[n,i]=(0,A.useState)(!1),{copied:u,copy:d}=m(),f=!!e;return(0,j.jsxs)(`div`,{className:`space-y-4`,children:[(0,j.jsxs)(`div`,{className:`space-y-1`,children:[(0,j.jsx)(`div`,{className:`flex items-center gap-2`,children:(0,j.jsx)(`h2`,{className:`text-lg font-semibold`,children:`Add an API key to authenticate MCP clients`})}),(0,j.jsx)(`p`,{className:`text-muted-foreground text-sm`,children:`Paste an existing API key created from a Service Account. This key will be used in the client configuration snippets below.`}),(0,j.jsxs)(`p`,{className:`text-muted-foreground -mt-2 text-sm`,children:[`You can manage API keys on the`,` `,(0,j.jsx)(g,{to:c.settings.service_accounts.overview,className:`text-primary-text hover:text-primary-text/80 underline underline-offset-4`,children:`Service Accounts`}),` `,`settings page.`]})]}),(0,j.jsxs)(`div`,{className:`flex flex-col gap-2 sm:flex-row sm:items-center`,children:[(0,j.jsxs)(`div`,{className:`relative`,children:[(0,j.jsx)(C,{type:f&&!n?`password`:`text`,value:e??``,onChange:e=>t(e.target.value||null),placeholder:`Paste your API key here`,className:`bg-muted w-full font-mono sm:w-110 ${f&&`pr-11`}`}),f?(0,j.jsxs)(`div`,{className:`absolute top-1/2 right-1 flex -translate-y-1/2 items-center gap-0.5`,children:[(0,j.jsx)(T,{icon:n?(0,j.jsx)(o,{className:`size-4`}):(0,j.jsx)(s,{className:`size-4`}),label:n?`Hide token`:`Show token`,variant:`ghost`,size:`icon-xs`,onClick:()=>i(e=>!e)}),(0,j.jsx)(T,{icon:u?(0,j.jsx)(r,{className:`size-4`}):(0,j.jsx)(a,{className:`size-4`}),label:u?`Copied`:`Copy token`,variant:`ghost`,size:`icon-xs`,onClick:()=>{e&&d(e)}})]}):null]}),f&&(0,j.jsx)(l,{variant:`destructive`,onClick:()=>{t(null),i(!1)},children:`Remove`})]})]})}var N=`zenmldocker/mcp-zenml:latest`,P={LOGLEVEL:`WARNING`,NO_COLOR:`1`,ZENML_LOGGING_COLORS_DISABLED:`true`,ZENML_LOGGING_VERBOSITY:`WARN`,ZENML_ENABLE_RICH_TRACEBACK:`false`,PYTHONUNBUFFERED:`1`,PYTHONIOENCODING:`UTF-8`};function F(e){return e?[`-e`,`ZENML_ACTIVE_PROJECT_ID=${e}`]:[]}function I(e){return e?`\n\t-e ZENML_ACTIVE_PROJECT_ID=${e} \\`:``}function L(e){return e?`\n\t\t\t"-e","ZENML_ACTIVE_PROJECT_ID=${e}",`:``}function R(e){return e?`,\n\t\t"ZENML_ACTIVE_PROJECT_ID": "${e}"`:``}function z(e){return e?`\n\t--env ZENML_ACTIVE_PROJECT_ID=${e} \\`:``}function B(){return Object.entries(P).flatMap(([e,t])=>[`-e`,`${e}=${t}`])}function V(e){let t=JSON.stringify(e);if(typeof window<`u`&&typeof window.btoa==`function`)return window.btoa(t);if(typeof Buffer<`u`)return Buffer.from(t,`utf-8`).toString(`base64`);throw Error(`No Base64 encoder available`)}function H(e,t,n){return[`run`,`-i`,`--rm`,`-e`,`ZENML_STORE_URL=${e}`,`-e`,`ZENML_STORE_API_KEY=${t}`,...F(n),...B(),N]}function U(e,t,n){let r={name:`zenml`,command:`docker`,args:H(e,t,n)};return`vscode:mcp/install?${encodeURIComponent(JSON.stringify(r))}`}function W(e,t,n){return`cursor://anysphere.cursor-deeplink/mcp/install?name=zenml&config=${V({command:`docker`,args:H(e,t,n),type:`stdio`})}`}function G(e,t,n){let r={name:`zenml`,command:`docker`,args:H(e,t,n)};return`code --add-mcp "${JSON.stringify(r).replace(/"/g,`\\"`)}"`}var K=(e,t,n)=>JSON.stringify({mcpServers:{zenml:{command:`docker`,args:[`run`,`-i`,`--rm`,`-e`,`ZENML_STORE_URL=${e}`,`-e`,`ZENML_STORE_API_KEY=${t}`,...F(n),...B(),N]}}},null,2),q=(e,t,n)=>JSON.stringify({mcpServers:{zenml:{command:`/usr/local/bin/uv`,args:[`run`,`path/to/mcp-zenml/server/zenml_server.py`],env:{...P,ZENML_STORE_URL:e,ZENML_STORE_API_KEY:t,...n?{ZENML_ACTIVE_PROJECT_ID:n}:{}}}}},null,2);function J(e,t,n){let r=n??``,i=K(e,t,r),a=q(e,t,r);return[{name:`VS Code`,value:`vscode`,methods:[{title:`Automatic Registration (Deep Link)`,type:`automatic`,hasDeepLink:!0,deepLinkUrl:U(e,t,r),description:`Click the link to add the Docker-driven MCP server to VS Code.`,steps:[`Click the 'Install via Link' button above`,`VS Code will prompt you to install the server`]},{title:`Manual Method (Docker CLI)`,type:`cli`,bashCommand:G(e,t,r),description:`Use the VS Code CLI to install the ZenML MCP Server.`,steps:[`Run the command in your terminal`,`The server will be added to your VS Code configuration`]},{title:`Manual Method (uv CLI)`,type:`cli`,bashCommand:`code --add-mcp '{\n  "name": "zenml",\n  "command": "/usr/local/bin/uv",\n  "args": ["run", "/path/to/mcp-zenml/server/zenml_server.py"],\n  "env": {\n    "LOGLEVEL": "WARNING",\n    "NO_COLOR": "1",\n    "ZENML_LOGGING_COLORS_DISABLED": "true",\n    "ZENML_LOGGING_VERBOSITY": "WARN",\n    "ZENML_ENABLE_RICH_TRACEBACK": "false",\n    "PYTHONUNBUFFERED": "1",\n    "PYTHONIOENCODING": "UTF-8",\n    "ZENML_STORE_URL": "${e}",\n    "ZENML_STORE_API_KEY": "${t}"${r?`,\n    "ZENML_ACTIVE_PROJECT_ID": "${r}"`:``}\n  }\n}'`,description:`Use the VS Code CLI with uv to install the ZenML MCP Server.`,steps:["Clone the repository: `git clone --depth 1 --branch main https://github.com/zenml-io/mcp-zenml.git`","Ensure `uv` is installed globally","Update the command to point to your `uv` and repository paths",`Run the command in your terminal`]}]},{name:`Claude Desktop`,value:`claude-desktop`,methods:[{title:`Automatic Registration (.mcpb file)`,type:`mcpb`,hasDeepLink:!0,deepLinkUrl:`https://github.com/zenml-io/mcp-zenml/releases`,steps:[`Visit https://github.com/zenml-io/mcp-zenml/releases and click on the latest release`,`Download the mcp-zenml.mcpb file from the Assets section`,`Open Claude Desktop and drag the .mcpb file onto the icon`,`Click the "Disabled" button to enable the MCP server`]},{title:`Manual Method (Docker)`,type:`docker`,config:i,steps:["Add the configuration to your `claude_desktop_config.json` file","This file is usually located in `Application Support/Claude` directory","If you already have MCP servers configured, only add the `zenml` section"]},{title:`Manual Method (uv)`,type:`uv`,config:a,steps:["Clone the repository: `git clone --depth 1 --branch main https://github.com/zenml-io/mcp-zenml.git`","Ensure `uv` is installed globally on your system","Add the configuration to your `claude_desktop_config.json` file","Update the `command` and `args` to point to where `uv` is installed and where you cloned the repository"],note:`You will need to update the command and args paths to match your local installation.`}],troubleshooting:`If the MCP server is not installed correctly, Claude Desktop will tell you it doesn't have access to the ZenML tools. Check the logs for any errors.`},{name:`Cursor`,value:`cursor`,methods:[{title:`Automatic Registration (Deep Link)`,type:`automatic`,hasDeepLink:!0,deepLinkUrl:W(e,t,r),description:`Click to add the ZenML MCP server to Cursor.`,steps:[`Click the 'Install via Link' button above`,`Cursor will prompt you to install the server`]},{title:`Manual Method (Docker)`,type:`docker`,bashCommand:`mkdir -p ~/.cursor && \\
if [ -f ~/.cursor/mcp.json ]; then \\
	cp ~/.cursor/mcp.json ~/.cursor/mcp.json.backup && \\
	jq '.mcpServers.zenml = {
	"command":"docker",
	"args":["run","-i","--rm",
			"-e","ZENML_STORE_URL=${e}",
			"-e","ZENML_STORE_API_KEY=${t}",${L(r)}
			"-e","LOGLEVEL=WARNING",
			"-e","NO_COLOR=1",
			"-e","ZENML_LOGGING_COLORS_DISABLED=true",
			"-e","ZENML_LOGGING_VERBOSITY=WARN",
			"-e","ZENML_ENABLE_RICH_TRACEBACK=false",
			"-e","PYTHONUNBUFFERED=1",
			"-e","PYTHONIOENCODING=UTF-8",
			"${N}"],
	"type":"stdio"
	}' ~/.cursor/mcp.json > ~/.cursor/mcp.json.tmp && \\
	mv ~/.cursor/mcp.json.tmp ~/.cursor/mcp.json; \\
else \\
	echo '{"mcpServers":{}}' | jq '.mcpServers.zenml = {
	"command":"docker",
	"args":["run","-i","--rm",
			"-e","ZENML_STORE_URL=${e}",
			"-e","ZENML_STORE_API_KEY=${t}",${L(r)}
			"-e","LOGLEVEL=WARNING",
			"-e","NO_COLOR=1",
			"-e","ZENML_LOGGING_COLORS_DISABLED=true",
			"-e","ZENML_LOGGING_VERBOSITY=WARN",
			"-e","ZENML_ENABLE_RICH_TRACEBACK=false",
			"-e","PYTHONUNBUFFERED=1",
			"-e","PYTHONIOENCODING=UTF-8",
			"${N}"],
	"type":"stdio"
	}' > ~/.cursor/mcp.json; \\
fi`,description:`Use this CLI command to install the ZenML MCP Server in Cursor.`,steps:[`Run the command in your terminal`,"The server will be added to `~/.cursor/mcp.json`"]},{title:`Manual Method (uv)`,type:`uv`,bashCommand:`mkdir -p ~/.cursor && \\
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
		"ZENML_STORE_API_KEY": "${t}"${R(r)}
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
		"ZENML_STORE_API_KEY": "${t}"${R(r)}
	}
	}' > ~/.cursor/mcp.json; \\
fi`,description:`Use this CLI command to install the ZenML MCP Server with uv in Cursor.`,steps:["Clone the repository: `git clone --depth 1 --branch main https://github.com/zenml-io/mcp-zenml.git`","Ensure `uv` is installed globally","Update the command to point to your `uv` and repository paths",`Run the command in your terminal`]}]},{name:`Claude Code`,value:`claude-code`,methods:[{title:`Manual Method (Docker)`,type:`cli`,bashCommand:`# Add for your current project (local scope)
claude mcp add zenml -- \\
	docker run -i --rm \\
	-e ZENML_STORE_URL=${e} \\
	-e ZENML_STORE_API_KEY=${t} \\${I(r)}
	-e LOGLEVEL=WARNING \\
	-e NO_COLOR=1 \\
	-e ZENML_LOGGING_COLORS_DISABLED=true \\
	-e ZENML_LOGGING_VERBOSITY=WARN \\
	-e ZENML_ENABLE_RICH_TRACEBACK=false \\
	-e PYTHONUNBUFFERED=1 \\
	-e PYTHONIOENCODING=UTF-8 \\
	${N}`,description:`Install the ZenML MCP Server using the Claude CLI.`,steps:[`Run the command in your terminal for local scope`,"For user-scoped installation, add `--scope user` flag after `zenml`"],note:"User scope: `claude mcp add zenml --scope user --` [rest of command]"},{title:`Manual Method (uv)`,type:`cli`,bashCommand:`# Add for your current project (local scope)
claude mcp add zenml \\
	--env LOGLEVEL=WARNING \\
	--env NO_COLOR=1 \\
	--env ZENML_LOGGING_COLORS_DISABLED=true \\
	--env ZENML_LOGGING_VERBOSITY=WARN \\
	--env ZENML_ENABLE_RICH_TRACEBACK=false \\
	--env PYTHONUNBUFFERED=1 \\
	--env PYTHONIOENCODING=UTF-8 \\
	--env ZENML_STORE_URL=${e} \\
	--env ZENML_STORE_API_KEY=${t} \\${z(r)}
	-- /usr/local/bin/uv run /path/to/mcp-zenml/server/zenml_server.py`,description:`Install the ZenML MCP Server with uv using the Claude CLI.`,steps:["Clone the repository: `git clone --depth 1 --branch main https://github.com/zenml-io/mcp-zenml.git`","Ensure `uv` is installed globally","Update the command to point to your `uv` and repository paths",`Run the command in your terminal`,"For user-scoped installation, add `--scope user` flag after `zenml`"]}],troubleshooting:"Use the `/mcp` command inside claude to check connection status and trigger reconnect if needed."},{name:`OpenAI Codex`,value:`codex`,methods:[{title:`Manual Method (Docker)`,type:`cli`,bashCommand:`codex mcp add zenml docker run -i --rm \\
	-e ZENML_STORE_URL=${e} \\
	-e ZENML_STORE_API_KEY=${t} \\${I(r)}
	-e LOGLEVEL=WARNING \\
	-e NO_COLOR=1 \\
	-e ZENML_LOGGING_COLORS_DISABLED=true \\
	-e ZENML_LOGGING_VERBOSITY=WARN \\
	-e ZENML_ENABLE_RICH_TRACEBACK=false \\
	-e PYTHONUNBUFFERED=1 \\
	-e PYTHONIOENCODING=UTF-8 \\
	${N}`,description:`Install the ZenML MCP Server using the Codex CLI.`,steps:[`Run the command in your terminal`]},{title:`Manual Method (uv)`,type:`cli`,bashCommand:`codex mcp add zenml /usr/local/bin/uv run path/to/mcp-zenml/server/zenml_server.py \\
	--env LOGLEVEL=WARNING \\
	--env NO_COLOR=1 \\
	--env ZENML_LOGGING_COLORS_DISABLED=true \\
	--env ZENML_LOGGING_VERBOSITY=WARN \\
	--env ZENML_ENABLE_RICH_TRACEBACK=false \\
	--env PYTHONUNBUFFERED=1 \\
	--env PYTHONIOENCODING=UTF-8 \\
	--env ZENML_STORE_URL=${e} \\
	--env ZENML_STORE_API_KEY=${t}${r?` \\`:``}${r?z(r).replace(` \\`,``):``}`,description:`Install the ZenML MCP Server with uv using the Codex CLI.`,steps:["Clone the repository: `git clone --depth 1 --branch main https://github.com/zenml-io/mcp-zenml.git`","Ensure `uv` is installed globally","Update the command to point to your `uv` and repository paths",`Run the command in your terminal`]}],troubleshooting:"Use the `/mcp` command inside codex to check connection status and trigger reconnect if needed."},{name:`Other Clients`,value:`other`,methods:[{title:`Docker Installation`,type:`docker`,config:i,description:`Use this JSON configuration for any MCP client that supports Docker-based servers.`,steps:[`Insert this configuration where your application requires MCP server registration`,"Update `ZENML_STORE_URL`, `ZENML_STORE_API_KEY`, and `ZENML_ACTIVE_PROJECT_ID` with your values"]},{title:`Non-Docker Installation (uv)`,type:`uv`,config:a,description:"Use this JSON configuration for any MCP client that supports local execution with `uv`.",steps:["Clone the repository: `git clone --depth 1 --branch main https://github.com/zenml-io/mcp-zenml.git`","Ensure `uv` is installed globally","Update the `command` and `args` paths to match your installation","Update `ZENML_STORE_URL`, `ZENML_STORE_API_KEY`, and `ZENML_ACTIVE_PROJECT_ID` with your values",`Insert this configuration where your application requires MCP server registration`]}]}]}var Y=new Set([`https:`,`http:`,`vscode:`,`cursor:`]);function X(e){if(!e)return!1;try{let t=new URL(e),n=t.protocol;return!(!Y.has(n)||n===`cursor:`&&t.hostname!==`anysphere.cursor-deeplink`)}catch{return!1}}function Z({method:e}){let t=e.type===`automatic`||e.type===`mcpb`,n=e.type===`automatic`?`Install via Link`:`Open Link`,r=e.hasDeepLink&&e.deepLinkUrl&&X(e.deepLinkUrl);return(0,j.jsx)(i,{initialOpen:t,title:e.title,children:(0,j.jsxs)(`div`,{className:`space-y-4`,children:[e.description&&(0,j.jsx)(`p`,{className:`text-muted-foreground text-sm`,children:e.description}),r&&(0,j.jsxs)(l,{render:(0,j.jsx)(`a`,{href:e.deepLinkUrl,target:`_blank`,rel:`noopener noreferrer`}),className:`inline-flex`,children:[(0,j.jsx)(w,{className:`size-4`,"aria-hidden":!0}),n]}),e.steps.length>0&&(0,j.jsxs)(`div`,{className:`space-y-2`,children:[(0,j.jsx)(`h5`,{className:`text-sm font-medium`,children:`Installation Steps:`}),(0,j.jsx)(`div`,{className:`space-y-2 text-sm`,children:e.steps.map((e,t)=>(0,j.jsxs)(`div`,{className:`flex items-start gap-2`,children:[(0,j.jsx)(`span`,{className:`bg-muted flex size-5 shrink-0 items-center justify-center rounded-full text-xs font-medium`,children:t+1}),(0,j.jsx)(E,{markdown:e,className:`text-muted-foreground`})]},t))})]}),e.config&&(0,j.jsxs)(`div`,{className:`space-y-2`,children:[(0,j.jsx)(`h5`,{className:`text-sm font-medium`,children:`Configuration:`}),(0,j.jsx)(O,{code:e.config,highlightCode:!0,language:`json`,wrap:!0,fullWidth:!0})]}),e.bashCommand&&(0,j.jsxs)(`div`,{className:`space-y-2`,children:[(0,j.jsx)(`h5`,{className:`text-sm font-medium`,children:`Command:`}),(0,j.jsx)(O,{code:e.bashCommand,highlightCode:!0,language:`bash`,wrap:!0,fullWidth:!0})]}),e.note&&(0,j.jsx)(k,{intent:`primary`,children:(0,j.jsx)(`p`,{className:`text-sm`,children:e.note})})]})})}function Q({ide:e}){return(0,j.jsxs)(`div`,{className:`space-y-4`,children:[(0,j.jsxs)(`div`,{className:`space-y-1`,children:[(0,j.jsxs)(`h3`,{className:`text-base font-semibold`,children:[e.name,` Setup`]}),(0,j.jsx)(`p`,{className:`text-muted-foreground text-sm`,children:`Choose an installation method below and follow the instructions.`})]}),(0,j.jsx)(`div`,{className:`space-y-3`,children:e.methods.map((t,n)=>(0,j.jsx)(Z,{method:t},`${e.value}-${t.type}-${n}`))}),e.troubleshooting&&(0,j.jsx)(k,{intent:`neutral`,children:(0,j.jsxs)(`div`,{className:`space-y-1`,children:[(0,j.jsx)(`h4`,{className:`text-sm font-semibold`,children:`Troubleshooting`}),(0,j.jsx)(`p`,{className:`text-sm`,children:e.troubleshooting})]})})]})}function $({endpointUrl:e,token:t,projectId:n}){let r=(0,A.useMemo)(()=>J(e,t,n),[e,t,n]);return(0,j.jsxs)(`div`,{className:`space-y-4`,children:[(0,j.jsxs)(`div`,{className:`flex flex-col gap-1`,children:[(0,j.jsxs)(`div`,{className:`flex items-center gap-2`,children:[(0,j.jsx)(`h2`,{className:`text-lg font-semibold`,children:`Client Configuration`}),(0,j.jsx)(`a`,{href:`https://docs.zenml.io/user-guides/best-practices/mcp-chat-with-server`,target:`_blank`,rel:`noreferrer noopener`,className:`text-primary-text hover:text-primary-text/80 text-sm underline underline-offset-4`,children:`Learn More`})]}),(0,j.jsx)(`p`,{className:`text-muted-foreground text-sm`,children:`Choose your IDE or AI assistant and follow the installation instructions below.`})]}),(0,j.jsx)(`div`,{className:`border-border overflow-hidden rounded-lg border`,children:(0,j.jsxs)(h,{defaultValue:`vscode`,className:`w-full gap-0`,children:[(0,j.jsx)(v,{className:`border-border grid w-full grid-cols-6 rounded-none border-b`,variant:`line`,children:r.map(e=>(0,j.jsx)(u,{value:e.value,className:`rounded-none after:bottom-[-1px]`,children:e.name},e.value))}),r.map(e=>(0,j.jsx)(_,{value:e.value,className:`p-5`,children:(0,j.jsx)(Q,{ide:e})},e.value))]})})]})}function ee({onDismiss:e}){return(0,j.jsxs)(b,{variant:`success`,onDismiss:e,children:[(0,j.jsx)(d,{children:`Your configuration has been updated`}),(0,j.jsx)(S,{children:`Configuration links and code snippets now include your API key.`})]})}function te(){let[e,t]=(0,A.useState)(null),[n,r]=(0,A.useState)(!1),i=e=>{t(e),r(!!e)},a=window.location.origin;return(0,j.jsxs)(p,{children:[(0,j.jsxs)(x,{children:[(0,j.jsx)(f,{className:`text-lg`,children:`MCP`}),(0,j.jsx)(D,{children:`Model Context Protocol settings for connecting IDEs and AI assistants to your ZenML Server.`})]}),(0,j.jsx)(y,{children:(0,j.jsxs)(`div`,{className:`space-y-8`,children:[(0,j.jsx)(M,{token:e,onTokenChange:i}),n&&e?(0,j.jsx)(ee,{onDismiss:()=>r(!1)}):null,(0,j.jsx)(`div`,{className:`border-border border-t`}),(0,j.jsx)($,{endpointUrl:a,token:e||`your_api_key_here`})]})})]})}export{te as default};