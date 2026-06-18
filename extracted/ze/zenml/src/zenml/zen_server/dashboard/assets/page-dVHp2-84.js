import{i as e}from"./chunk-aKtaBQYM.js";import{a as t,i as n,j as r,k as i,o as a}from"./chunk-JSBRDJBE-DD67o4Z0.js";import{at as o,it as s,ot as c,rt as l}from"./dist-DCL-ttT6.js";import{t as u}from"./routes-DM-ZUc34.js";import{t as d}from"./copy-lxfFMhzU.js";import{A as f,Q as p,U as m,Z as h,hn as g,mt as _}from"./index-C7eyRJ5x.js";import{t as v}from"./CodeSnippet-D1WyMn6A.js";import{t as y}from"./eye-off-m_Lj7ISZ.js";import{t as b}from"./eye-DmBEnmAl.js";import{t as x}from"./CollapsibleCard-CWkH7mv2.js";import{t as S}from"./Infobox-DlXWkm0A.js";var C=e(r(),1),w=i();function T({token:e,onTokenChange:n}){let[r,i]=(0,C.useState)(!1),{copied:o,copyToClipboard:s}=f(),c=!!e;return(0,w.jsxs)(`div`,{className:`space-y-4`,children:[(0,w.jsxs)(`div`,{className:`space-y-1`,children:[(0,w.jsx)(`div`,{className:`flex items-center gap-2`,children:(0,w.jsx)(`h2`,{className:`text-text-lg font-semibold`,children:`Add an API key to authenticate MCP clients`})}),(0,w.jsx)(`p`,{className:`text-text-sm text-theme-text-secondary`,children:`Paste an existing API key created from a Service Account. This key will be used in the client configuration snippets below.`}),(0,w.jsxs)(`p`,{className:`-mt-2 text-text-sm text-theme-text-secondary`,children:[`You can manage API keys on the`,` `,(0,w.jsx)(g,{to:u.settings.service_accounts.overview,className:`link text-theme-text-brand`,children:`Service Accounts`}),` `,`settings page.`]})]}),(0,w.jsxs)(`div`,{className:`flex flex-col gap-2 sm:flex-row sm:items-center`,children:[(0,w.jsxs)(`div`,{className:`relative`,children:[(0,w.jsx)(a,{type:c&&!r?`password`:`text`,value:e??``,onChange:e=>n(e.target.value||null),placeholder:`Paste your API key here`,className:`w-full border-theme-border-moderate bg-theme-surface-tertiary font-mono text-text-md text-theme-text-secondary sm:w-[440px] ${c&&`pr-11`}`}),c?(0,w.jsxs)(`div`,{className:`absolute right-1 top-1/2 flex -translate-y-1/2 items-center gap-0.5`,children:[(0,w.jsx)(t,{intent:`secondary`,emphasis:`minimal`,onClick:()=>i(e=>!e),className:`flex size-5 items-center justify-center p-0`,children:r?(0,w.jsxs)(w.Fragment,{children:[(0,w.jsx)(`span`,{className:`sr-only`,children:`Hide token`}),(0,w.jsx)(y,{width:16,height:16,className:`fill-neutral-500`})]}):(0,w.jsxs)(w.Fragment,{children:[(0,w.jsx)(`span`,{className:`sr-only`,children:`Show token`}),(0,w.jsx)(b,{width:16,height:16,className:`fill-neutral-500`})]})}),(0,w.jsxs)(t,{intent:`secondary`,emphasis:`minimal`,onClick:()=>{e&&s(e)},className:`flex size-5 items-center justify-center p-0`,"aria-describedby":`token-copy-status`,children:[o?(0,w.jsx)(_,{width:16,height:16,className:`shrink-0 fill-neutral-500`}):(0,w.jsx)(d,{width:16,height:16,className:`shrink-0 fill-neutral-500`}),(0,w.jsx)(`span`,{className:`sr-only`,children:o?`Copied`:`Copy`})]})]}):null]}),c&&(0,w.jsx)(t,{intent:`danger`,emphasis:`subtle`,size:`md`,onClick:()=>{n(null),i(!1)},children:`Remove`})]})]})}var E=`zenmldocker/mcp-zenml:latest`,D={LOGLEVEL:`WARNING`,NO_COLOR:`1`,ZENML_LOGGING_COLORS_DISABLED:`true`,ZENML_LOGGING_VERBOSITY:`WARN`,ZENML_ENABLE_RICH_TRACEBACK:`false`,PYTHONUNBUFFERED:`1`,PYTHONIOENCODING:`UTF-8`};function O(e){return e?[`-e`,`ZENML_ACTIVE_PROJECT_ID=${e}`]:[]}function k(e){return e?`\n\t-e ZENML_ACTIVE_PROJECT_ID=${e} \\`:``}function A(e){return e?`\n\t\t\t"-e","ZENML_ACTIVE_PROJECT_ID=${e}",`:``}function j(e){return e?`,\n\t\t"ZENML_ACTIVE_PROJECT_ID": "${e}"`:``}function M(e){return e?`\n\t--env ZENML_ACTIVE_PROJECT_ID=${e} \\`:``}function N(){return Object.entries(D).flatMap(([e,t])=>[`-e`,`${e}=${t}`])}function P(e){let t=JSON.stringify(e);if(typeof window<`u`&&typeof window.btoa==`function`)return window.btoa(t);if(typeof Buffer<`u`)return Buffer.from(t,`utf-8`).toString(`base64`);throw Error(`No Base64 encoder available`)}function F(e,t,n){return[`run`,`-i`,`--rm`,`-e`,`ZENML_STORE_URL=${e}`,`-e`,`ZENML_STORE_API_KEY=${t}`,...O(n),...N(),E]}function I(e,t,n){let r={name:`zenml`,command:`docker`,args:F(e,t,n)};return`vscode:mcp/install?${encodeURIComponent(JSON.stringify(r))}`}function L(e,t,n){return`cursor://anysphere.cursor-deeplink/mcp/install?name=zenml&config=${P({command:`docker`,args:F(e,t,n),type:`stdio`})}`}function R(e,t,n){let r={name:`zenml`,command:`docker`,args:F(e,t,n)};return`code --add-mcp "${JSON.stringify(r).replace(/"/g,`\\"`)}"`}var z=(e,t,n)=>JSON.stringify({mcpServers:{zenml:{command:`docker`,args:[`run`,`-i`,`--rm`,`-e`,`ZENML_STORE_URL=${e}`,`-e`,`ZENML_STORE_API_KEY=${t}`,...O(n),...N(),E]}}},null,2),B=(e,t,n)=>JSON.stringify({mcpServers:{zenml:{command:`/usr/local/bin/uv`,args:[`run`,`path/to/mcp-zenml/server/zenml_server.py`],env:{...D,ZENML_STORE_URL:e,ZENML_STORE_API_KEY:t,...n?{ZENML_ACTIVE_PROJECT_ID:n}:{}}}}},null,2);function V(e,t,n){let r=n??``,i=z(e,t,r),a=B(e,t,r);return[{name:`VS Code`,value:`vscode`,methods:[{title:`Automatic Registration (Deep Link)`,type:`automatic`,hasDeepLink:!0,deepLinkUrl:I(e,t,r),description:`Click the link to add the Docker-driven MCP server to VS Code.`,steps:[`Click the 'Install via Link' button above`,`VS Code will prompt you to install the server`]},{title:`Manual Method (Docker CLI)`,type:`cli`,bashCommand:R(e,t,r),description:`Use the VS Code CLI to install the ZenML MCP Server.`,steps:[`Run the command in your terminal`,`The server will be added to your VS Code configuration`]},{title:`Manual Method (uv CLI)`,type:`cli`,bashCommand:`code --add-mcp '{\n  "name": "zenml",\n  "command": "/usr/local/bin/uv",\n  "args": ["run", "/path/to/mcp-zenml/server/zenml_server.py"],\n  "env": {\n    "LOGLEVEL": "WARNING",\n    "NO_COLOR": "1",\n    "ZENML_LOGGING_COLORS_DISABLED": "true",\n    "ZENML_LOGGING_VERBOSITY": "WARN",\n    "ZENML_ENABLE_RICH_TRACEBACK": "false",\n    "PYTHONUNBUFFERED": "1",\n    "PYTHONIOENCODING": "UTF-8",\n    "ZENML_STORE_URL": "${e}",\n    "ZENML_STORE_API_KEY": "${t}"${r?`,\n    "ZENML_ACTIVE_PROJECT_ID": "${r}"`:``}\n  }\n}'`,description:`Use the VS Code CLI with uv to install the ZenML MCP Server.`,steps:["Clone the repository: `git clone --depth 1 --branch main https://github.com/zenml-io/mcp-zenml.git`","Ensure `uv` is installed globally","Update the command to point to your `uv` and repository paths",`Run the command in your terminal`]}]},{name:`Claude Desktop`,value:`claude-desktop`,methods:[{title:`Automatic Registration (.mcpb file)`,type:`mcpb`,hasDeepLink:!0,deepLinkUrl:`https://github.com/zenml-io/mcp-zenml/releases`,steps:[`Visit https://github.com/zenml-io/mcp-zenml/releases and click on the latest release`,`Download the mcp-zenml.mcpb file from the Assets section`,`Open Claude Desktop and drag the .mcpb file onto the icon`,`Click the "Disabled" button to enable the MCP server`]},{title:`Manual Method (Docker)`,type:`docker`,config:i,steps:["Add the configuration to your `claude_desktop_config.json` file","This file is usually located in `Application Support/Claude` directory","If you already have MCP servers configured, only add the `zenml` section"]},{title:`Manual Method (uv)`,type:`uv`,config:a,steps:["Clone the repository: `git clone --depth 1 --branch main https://github.com/zenml-io/mcp-zenml.git`","Ensure `uv` is installed globally on your system","Add the configuration to your `claude_desktop_config.json` file","Update the `command` and `args` to point to where `uv` is installed and where you cloned the repository"],note:`You will need to update the command and args paths to match your local installation.`}],troubleshooting:`If the MCP server is not installed correctly, Claude Desktop will tell you it doesn't have access to the ZenML tools. Check the logs for any errors.`},{name:`Cursor`,value:`cursor`,methods:[{title:`Automatic Registration (Deep Link)`,type:`automatic`,hasDeepLink:!0,deepLinkUrl:L(e,t,r),description:`Click to add the ZenML MCP server to Cursor.`,steps:[`Click the 'Install via Link' button above`,`Cursor will prompt you to install the server`]},{title:`Manual Method (Docker)`,type:`docker`,bashCommand:`mkdir -p ~/.cursor && \\
if [ -f ~/.cursor/mcp.json ]; then \\
	cp ~/.cursor/mcp.json ~/.cursor/mcp.json.backup && \\
	jq '.mcpServers.zenml = {
	"command":"docker",
	"args":["run","-i","--rm",
			"-e","ZENML_STORE_URL=${e}",
			"-e","ZENML_STORE_API_KEY=${t}",${A(r)}
			"-e","LOGLEVEL=WARNING",
			"-e","NO_COLOR=1",
			"-e","ZENML_LOGGING_COLORS_DISABLED=true",
			"-e","ZENML_LOGGING_VERBOSITY=WARN",
			"-e","ZENML_ENABLE_RICH_TRACEBACK=false",
			"-e","PYTHONUNBUFFERED=1",
			"-e","PYTHONIOENCODING=UTF-8",
			"${E}"],
	"type":"stdio"
	}' ~/.cursor/mcp.json > ~/.cursor/mcp.json.tmp && \\
	mv ~/.cursor/mcp.json.tmp ~/.cursor/mcp.json; \\
else \\
	echo '{"mcpServers":{}}' | jq '.mcpServers.zenml = {
	"command":"docker",
	"args":["run","-i","--rm",
			"-e","ZENML_STORE_URL=${e}",
			"-e","ZENML_STORE_API_KEY=${t}",${A(r)}
			"-e","LOGLEVEL=WARNING",
			"-e","NO_COLOR=1",
			"-e","ZENML_LOGGING_COLORS_DISABLED=true",
			"-e","ZENML_LOGGING_VERBOSITY=WARN",
			"-e","ZENML_ENABLE_RICH_TRACEBACK=false",
			"-e","PYTHONUNBUFFERED=1",
			"-e","PYTHONIOENCODING=UTF-8",
			"${E}"],
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
		"ZENML_STORE_API_KEY": "${t}"${j(r)}
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
		"ZENML_STORE_API_KEY": "${t}"${j(r)}
	}
	}' > ~/.cursor/mcp.json; \\
fi`,description:`Use this CLI command to install the ZenML MCP Server with uv in Cursor.`,steps:["Clone the repository: `git clone --depth 1 --branch main https://github.com/zenml-io/mcp-zenml.git`","Ensure `uv` is installed globally","Update the command to point to your `uv` and repository paths",`Run the command in your terminal`]}]},{name:`Claude Code`,value:`claude-code`,methods:[{title:`Manual Method (Docker)`,type:`cli`,bashCommand:`# Add for your current project (local scope)
claude mcp add zenml -- \\
	docker run -i --rm \\
	-e ZENML_STORE_URL=${e} \\
	-e ZENML_STORE_API_KEY=${t} \\${k(r)}
	-e LOGLEVEL=WARNING \\
	-e NO_COLOR=1 \\
	-e ZENML_LOGGING_COLORS_DISABLED=true \\
	-e ZENML_LOGGING_VERBOSITY=WARN \\
	-e ZENML_ENABLE_RICH_TRACEBACK=false \\
	-e PYTHONUNBUFFERED=1 \\
	-e PYTHONIOENCODING=UTF-8 \\
	${E}`,description:`Install the ZenML MCP Server using the Claude CLI.`,steps:[`Run the command in your terminal for local scope`,"For user-scoped installation, add `--scope user` flag after `zenml`"],note:"User scope: `claude mcp add zenml --scope user --` [rest of command]"},{title:`Manual Method (uv)`,type:`cli`,bashCommand:`# Add for your current project (local scope)
claude mcp add zenml \\
	--env LOGLEVEL=WARNING \\
	--env NO_COLOR=1 \\
	--env ZENML_LOGGING_COLORS_DISABLED=true \\
	--env ZENML_LOGGING_VERBOSITY=WARN \\
	--env ZENML_ENABLE_RICH_TRACEBACK=false \\
	--env PYTHONUNBUFFERED=1 \\
	--env PYTHONIOENCODING=UTF-8 \\
	--env ZENML_STORE_URL=${e} \\
	--env ZENML_STORE_API_KEY=${t} \\${M(r)}
	-- /usr/local/bin/uv run /path/to/mcp-zenml/server/zenml_server.py`,description:`Install the ZenML MCP Server with uv using the Claude CLI.`,steps:["Clone the repository: `git clone --depth 1 --branch main https://github.com/zenml-io/mcp-zenml.git`","Ensure `uv` is installed globally","Update the command to point to your `uv` and repository paths",`Run the command in your terminal`,"For user-scoped installation, add `--scope user` flag after `zenml`"]}],troubleshooting:"Use the `/mcp` command inside claude to check connection status and trigger reconnect if needed."},{name:`OpenAI Codex`,value:`codex`,methods:[{title:`Manual Method (Docker)`,type:`cli`,bashCommand:`codex mcp add zenml docker run -i --rm \\
	-e ZENML_STORE_URL=${e} \\
	-e ZENML_STORE_API_KEY=${t} \\${k(r)}
	-e LOGLEVEL=WARNING \\
	-e NO_COLOR=1 \\
	-e ZENML_LOGGING_COLORS_DISABLED=true \\
	-e ZENML_LOGGING_VERBOSITY=WARN \\
	-e ZENML_ENABLE_RICH_TRACEBACK=false \\
	-e PYTHONUNBUFFERED=1 \\
	-e PYTHONIOENCODING=UTF-8 \\
	${E}`,description:`Install the ZenML MCP Server using the Codex CLI.`,steps:[`Run the command in your terminal`]},{title:`Manual Method (uv)`,type:`cli`,bashCommand:`codex mcp add zenml /usr/local/bin/uv run path/to/mcp-zenml/server/zenml_server.py \\
	--env LOGLEVEL=WARNING \\
	--env NO_COLOR=1 \\
	--env ZENML_LOGGING_COLORS_DISABLED=true \\
	--env ZENML_LOGGING_VERBOSITY=WARN \\
	--env ZENML_ENABLE_RICH_TRACEBACK=false \\
	--env PYTHONUNBUFFERED=1 \\
	--env PYTHONIOENCODING=UTF-8 \\
	--env ZENML_STORE_URL=${e} \\
	--env ZENML_STORE_API_KEY=${t}${r?` \\`:``}${r?M(r).replace(` \\`,``):``}`,description:`Install the ZenML MCP Server with uv using the Codex CLI.`,steps:["Clone the repository: `git clone --depth 1 --branch main https://github.com/zenml-io/mcp-zenml.git`","Ensure `uv` is installed globally","Update the command to point to your `uv` and repository paths",`Run the command in your terminal`]}],troubleshooting:"Use the `/mcp` command inside codex to check connection status and trigger reconnect if needed."},{name:`Other Clients`,value:`other`,methods:[{title:`Docker Installation`,type:`docker`,config:i,description:`Use this JSON configuration for any MCP client that supports Docker-based servers.`,steps:[`Insert this configuration where your application requires MCP server registration`,"Update `ZENML_STORE_URL`, `ZENML_STORE_API_KEY`, and `ZENML_ACTIVE_PROJECT_ID` with your values"]},{title:`Non-Docker Installation (uv)`,type:`uv`,config:a,description:"Use this JSON configuration for any MCP client that supports local execution with `uv`.",steps:["Clone the repository: `git clone --depth 1 --branch main https://github.com/zenml-io/mcp-zenml.git`","Ensure `uv` is installed globally","Update the `command` and `args` paths to match your installation","Update `ZENML_STORE_URL`, `ZENML_STORE_API_KEY`, and `ZENML_ACTIVE_PROJECT_ID` with your values",`Insert this configuration where your application requires MCP server registration`]}]}]}var H=new Set([`https:`,`http:`,`vscode:`,`cursor:`]);function U(e){if(!e)return!1;try{let t=new URL(e),n=t.protocol;return!(!H.has(n)||n===`cursor:`&&t.hostname!==`anysphere.cursor-deeplink`)}catch{return!1}}function W({method:e}){let n=e.type===`automatic`||e.type===`mcpb`,r=e.type===`automatic`?`Install via Link`:`Open Link`,i=e.hasDeepLink&&e.deepLinkUrl&&U(e.deepLinkUrl);return(0,w.jsx)(x,{initialOpen:n,title:e.title,children:(0,w.jsxs)(`div`,{className:`space-y-4`,children:[e.description&&(0,w.jsx)(`p`,{className:`text-text-sm text-theme-text-secondary`,children:e.description}),i&&(0,w.jsx)(t,{asChild:!0,size:`md`,emphasis:`bold`,intent:`primary`,className:`inline-flex`,children:(0,w.jsxs)(`a`,{href:e.deepLinkUrl,target:`_blank`,rel:`noopener noreferrer`,children:[(0,w.jsx)(h,{className:`h-4 w-4 fill-current`}),r]})}),e.steps.length>0&&(0,w.jsxs)(`div`,{className:`space-y-2`,children:[(0,w.jsx)(`h5`,{className:`text-text-sm font-medium`,children:`Installation Steps:`}),(0,w.jsx)(`div`,{className:`space-y-2 text-text-sm`,children:e.steps.map((e,t)=>(0,w.jsxs)(`div`,{className:`flex items-start gap-2`,children:[(0,w.jsx)(`span`,{className:`rounded-full flex h-5 w-5 shrink-0 items-center justify-center bg-theme-surface-secondary text-text-xs font-medium`,children:t+1}),(0,w.jsx)(p,{markdown:e,className:`text-theme-text-secondary`})]},t))})]}),e.config&&(0,w.jsxs)(`div`,{className:`space-y-2`,children:[(0,w.jsx)(`h5`,{className:`text-text-sm font-medium`,children:`Configuration:`}),(0,w.jsx)(v,{code:e.config,highlightCode:!0,language:`json`,wrap:!0,fullWidth:!0})]}),e.bashCommand&&(0,w.jsxs)(`div`,{className:`space-y-2`,children:[(0,w.jsx)(`h5`,{className:`text-text-sm font-medium`,children:`Command:`}),(0,w.jsx)(v,{code:e.bashCommand,highlightCode:!0,language:`bash`,wrap:!0,fullWidth:!0})]}),e.note&&(0,w.jsx)(S,{intent:`primary`,children:(0,w.jsx)(`p`,{className:`text-text-sm`,children:e.note})})]})})}function G({ide:e}){return(0,w.jsxs)(`div`,{className:`space-y-4`,children:[(0,w.jsxs)(`div`,{className:`space-y-1`,children:[(0,w.jsxs)(`h3`,{className:`text-text-md font-semibold`,children:[e.name,` Setup`]}),(0,w.jsx)(`p`,{className:`text-text-sm text-theme-text-secondary`,children:`Choose an installation method below and follow the instructions.`})]}),(0,w.jsx)(`div`,{className:`space-y-3`,children:e.methods.map((t,n)=>(0,w.jsx)(W,{method:t},`${e.value}-${t.type}-${n}`))}),e.troubleshooting&&(0,w.jsx)(S,{intent:`neutral`,children:(0,w.jsxs)(`div`,{className:`space-y-1`,children:[(0,w.jsx)(`h4`,{className:`text-text-sm font-semibold`,children:`Troubleshooting`}),(0,w.jsx)(`p`,{className:`text-text-sm`,children:e.troubleshooting})]})})]})}function K({endpointUrl:e,token:t,projectId:n}){let r=(0,C.useMemo)(()=>V(e,t,n),[e,t,n]);return(0,w.jsxs)(`div`,{className:`space-y-6`,children:[(0,w.jsxs)(`div`,{className:`flex flex-col gap-1`,children:[(0,w.jsxs)(`div`,{className:`flex items-center gap-2`,children:[(0,w.jsx)(`h2`,{className:`text-text-lg font-semibold`,children:`Client Configuration`}),(0,w.jsx)(`a`,{href:`https://docs.zenml.io/user-guides/best-practices/mcp-chat-with-server`,target:`_blank`,rel:`noreferrer noopener`,className:`text-text-sm text-primary-400 hover:text-primary-500`,children:`Learn More`})]}),(0,w.jsx)(`p`,{className:`text-text-sm text-theme-text-secondary`,children:`Choose your IDE or AI assistant and follow the installation instructions below.`})]}),(0,w.jsx)(`div`,{className:`flex flex-col rounded-md border border-theme-border-moderate`,children:(0,w.jsxs)(l,{defaultValue:`vscode`,className:`w-full`,children:[(0,w.jsx)(o,{className:`grid w-full grid-cols-6`,children:r.map(e=>(0,w.jsx)(c,{value:e.value,className:`text-text-sm`,children:e.name},e.value))}),r.map(e=>(0,w.jsx)(s,{value:e.value,className:`mt-0 border-0 p-5`,children:(0,w.jsx)(G,{ide:e})},e.value))]})})]})}function q({onDismiss:e}){return(0,w.jsxs)(`div`,{className:`flex w-full items-center justify-between gap-2 rounded-md border border-success-300 bg-success-50 px-4 py-3 text-success-900`,children:[(0,w.jsxs)(`div`,{className:`flex items-center gap-2`,children:[(0,w.jsx)(_,{className:`size-5 shrink-0 fill-current`}),(0,w.jsx)(`p`,{className:`font-semibold`,children:`Your configuration has been updated`}),(0,w.jsx)(`p`,{className:`text-text-sm`,children:`Configuration links and code snippets now include your API key.`})]}),(0,w.jsx)(`button`,{type:`button`,onClick:e,"aria-label":`Dismiss notification`,children:(0,w.jsx)(m,{className:`size-5 fill-current`})})]})}function J(){let[e,t]=(0,C.useState)(null),[r,i]=(0,C.useState)(!1),a=e=>{t(e),i(!!e)},o=window.location.origin;return(0,w.jsxs)(n,{className:`space-y-5 p-5`,children:[(0,w.jsxs)(`div`,{className:`space-y-2`,children:[(0,w.jsx)(`h1`,{className:`text-text-xl font-semibold`,children:`MCP`}),(0,w.jsx)(`p`,{className:`text-text-sm text-theme-text-secondary`,children:`Model Context Protocol settings for connecting IDEs and AI assistants to your ZenML Server.`})]}),(0,w.jsx)(T,{token:e,onTokenChange:a}),r&&e?(0,w.jsx)(q,{onDismiss:()=>i(!1)}):null,(0,w.jsx)(`div`,{className:`border-t border-theme-border-moderate`}),(0,w.jsx)(K,{endpointUrl:o,token:e||`your_api_key_here`})]})}export{J as default};