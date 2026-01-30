import{j as t}from"./@radix-Da0HZyg8.js";import{a as m}from"./@monaco-editor-xs6rrDBC.js";import{l as I,r as R,I as M,B as c,S as _,m as b,bN as S,M as T,aq as j,br as A,ar as G,au as k,a as D,k as P}from"./index-5CE1yoTL.js";import{S as Z}from"./eye-eI-BtIGe.js";import{S as B}from"./eye-off-DKA61dAg.js";import{L as w}from"./@react-router-BEwS6i40.js";import{I as C}from"./Infobox-DQUJxLQz.js";import{C as p}from"./CodeSnippet-BTWWMvCC.js";import{C as U}from"./CollapsibleCard-BSAO4yQQ.js";import"./@elkjs-D2DP-mPJ.js";import"./@tanstack-BRZ8pkCt.js";import"./@reactflow-CEST3EX2.js";import"./@zod-yP6IINRw.js";import"./alert-triangle-C7ryTF32.js";function z({token:e,onTokenChange:s}){const[r,n]=m.useState(!1),{copied:o,copyToClipboard:a}=I(),i=!!e,v="Paste your API key here",g=()=>{e&&a(e)},y=()=>{s(null),n(!1)};return t.jsxs("div",{className:"space-y-4",children:[t.jsxs("div",{className:"space-y-1",children:[t.jsx("div",{className:"flex items-center gap-2",children:t.jsx("h2",{className:"text-text-lg font-semibold",children:"Add an API key to authenticate MCP clients"})}),t.jsx("p",{className:"text-text-sm text-theme-text-secondary",children:"Paste an existing API key created from a Service Account. This key will be used in the client configuration snippets below."}),t.jsxs("p",{className:"-mt-2 text-text-sm text-theme-text-secondary",children:["You can manage API keys on the"," ",t.jsx(w,{to:R.settings.service_accounts.overview,className:"link text-theme-text-brand",children:"Service Accounts"})," ","settings page."]})]}),t.jsxs("div",{className:"flex flex-col gap-2 sm:flex-row sm:items-center",children:[t.jsxs("div",{className:"relative",children:[t.jsx(M,{type:i&&!r?"password":"text",value:e??"",onChange:d=>s(d.target.value||null),placeholder:v,className:`w-full border-theme-border-moderate bg-theme-surface-tertiary font-mono text-text-md text-theme-text-secondary sm:w-[440px] ${i&&"pr-11"}`}),i?t.jsxs("div",{className:"absolute right-1 top-1/2 flex -translate-y-1/2 items-center gap-0.5",children:[t.jsx(c,{intent:"secondary",emphasis:"minimal",onClick:()=>n(d=>!d),className:"flex size-5 items-center justify-center p-0",children:r?t.jsxs(t.Fragment,{children:[t.jsx("span",{className:"sr-only",children:"Hide token"}),t.jsx(B,{width:16,height:16,className:"fill-neutral-500"})]}):t.jsxs(t.Fragment,{children:[t.jsx("span",{className:"sr-only",children:"Show token"}),t.jsx(Z,{width:16,height:16,className:"fill-neutral-500"})]})}),t.jsxs(c,{intent:"secondary",emphasis:"minimal",onClick:g,className:"flex size-5 items-center justify-center p-0","aria-describedby":"token-copy-status",children:[o?t.jsx(_,{width:16,height:16,className:"shrink-0 fill-neutral-500"}):t.jsx(b,{width:16,height:16,className:"shrink-0 fill-neutral-500"}),t.jsx("span",{className:"sr-only",children:o?"Copied":"Copy"})]})]}):null]}),i&&t.jsx(c,{intent:"danger",emphasis:"subtle",size:"md",onClick:y,children:"Remove"})]})]})}const l="zenmldocker/mcp-zenml:latest",f={LOGLEVEL:"WARNING",NO_COLOR:"1",ZENML_LOGGING_COLORS_DISABLED:"true",ZENML_LOGGING_VERBOSITY:"WARN",ZENML_ENABLE_RICH_TRACEBACK:"false",PYTHONUNBUFFERED:"1",PYTHONIOENCODING:"UTF-8"};function O(e){return e?["-e",`ZENML_ACTIVE_PROJECT_ID=${e}`]:[]}function h(e){return e?`
	-e ZENML_ACTIVE_PROJECT_ID=${e} \\`:""}function N(e){return e?`
			"-e","ZENML_ACTIVE_PROJECT_ID=${e}",`:""}function E(e){return e?`,
		"ZENML_ACTIVE_PROJECT_ID": "${e}"`:""}function L(e){return e?`
	--env ZENML_ACTIVE_PROJECT_ID=${e} \\`:""}function x(){return Object.entries(f).flatMap(([e,s])=>["-e",`${e}=${s}`])}function $(e){const s=JSON.stringify(e);if(typeof window<"u"&&typeof window.btoa=="function")return window.btoa(s);if(typeof Buffer<"u")return Buffer.from(s,"utf-8").toString("base64");throw new Error("No Base64 encoder available")}function u(e,s,r){return["run","-i","--rm","-e",`ZENML_STORE_URL=${e}`,"-e",`ZENML_STORE_API_KEY=${s}`,...O(r),...x(),l]}function Y(e,s,r){const n={name:"zenml",command:"docker",args:u(e,s,r)};return`vscode:mcp/install?${encodeURIComponent(JSON.stringify(n))}`}function V(e,s,r){const n={command:"docker",args:u(e,s,r),type:"stdio"},o=$(n);return`cursor://anysphere.cursor-deeplink/mcp/install?name=${encodeURIComponent("zenml")}&config=${o}`}function F(e,s,r){const n={name:"zenml",command:"docker",args:u(e,s,r)};return`code --add-mcp "${JSON.stringify(n).replace(/"/g,'\\"')}"`}const H=(e,s,r)=>JSON.stringify({mcpServers:{zenml:{command:"docker",args:["run","-i","--rm","-e",`ZENML_STORE_URL=${e}`,"-e",`ZENML_STORE_API_KEY=${s}`,...O(r),...x(),l]}}},null,2),K=(e,s,r)=>JSON.stringify({mcpServers:{zenml:{command:"/usr/local/bin/uv",args:["run","path/to/mcp-zenml/server/zenml_server.py"],env:{...f,ZENML_STORE_URL:e,ZENML_STORE_API_KEY:s,...r?{ZENML_ACTIVE_PROJECT_ID:r}:{}}}}},null,2);function W(e,s,r){const n=r??"",o=H(e,s,n),a=K(e,s,n);return[{name:"VS Code",value:"vscode",methods:[{title:"Automatic Registration (Deep Link)",type:"automatic",hasDeepLink:!0,deepLinkUrl:Y(e,s,n),description:"Click the link to add the Docker-driven MCP server to VS Code.",steps:["Click the 'Install via Link' button above","VS Code will prompt you to install the server"]},{title:"Manual Method (Docker CLI)",type:"cli",bashCommand:F(e,s,n),description:"Use the VS Code CLI to install the ZenML MCP Server.",steps:["Run the command in your terminal","The server will be added to your VS Code configuration"]},{title:"Manual Method (uv CLI)",type:"cli",bashCommand:`code --add-mcp '{
  "name": "zenml",
  "command": "/usr/local/bin/uv",
  "args": ["run", "/path/to/mcp-zenml/server/zenml_server.py"],
  "env": {
    "LOGLEVEL": "WARNING",
    "NO_COLOR": "1",
    "ZENML_LOGGING_COLORS_DISABLED": "true",
    "ZENML_LOGGING_VERBOSITY": "WARN",
    "ZENML_ENABLE_RICH_TRACEBACK": "false",
    "PYTHONUNBUFFERED": "1",
    "PYTHONIOENCODING": "UTF-8",
    "ZENML_STORE_URL": "${e}",
    "ZENML_STORE_API_KEY": "${s}"${n?`,
    "ZENML_ACTIVE_PROJECT_ID": "${n}"`:""}
  }
}'`,description:"Use the VS Code CLI with uv to install the ZenML MCP Server.",steps:["Clone the repository: `git clone --depth 1 --branch main https://github.com/zenml-io/mcp-zenml.git`","Ensure `uv` is installed globally","Update the command to point to your `uv` and repository paths","Run the command in your terminal"]}]},{name:"Claude Desktop",value:"claude-desktop",methods:[{title:"Automatic Registration (.mcpb file)",type:"mcpb",hasDeepLink:!0,deepLinkUrl:"https://github.com/zenml-io/mcp-zenml/releases",steps:["Visit https://github.com/zenml-io/mcp-zenml/releases and click on the latest release","Download the mcp-zenml.mcpb file from the Assets section","Open Claude Desktop and drag the .mcpb file onto the icon",'Click the "Disabled" button to enable the MCP server']},{title:"Manual Method (Docker)",type:"docker",config:o,steps:["Add the configuration to your `claude_desktop_config.json` file","This file is usually located in `Application Support/Claude` directory","If you already have MCP servers configured, only add the `zenml` section"]},{title:"Manual Method (uv)",type:"uv",config:a,steps:["Clone the repository: `git clone --depth 1 --branch main https://github.com/zenml-io/mcp-zenml.git`","Ensure `uv` is installed globally on your system","Add the configuration to your `claude_desktop_config.json` file","Update the `command` and `args` to point to where `uv` is installed and where you cloned the repository"],note:"You will need to update the command and args paths to match your local installation."}],troubleshooting:"If the MCP server is not installed correctly, Claude Desktop will tell you it doesn't have access to the ZenML tools. Check the logs for any errors."},{name:"Cursor",value:"cursor",methods:[{title:"Automatic Registration (Deep Link)",type:"automatic",hasDeepLink:!0,deepLinkUrl:V(e,s,n),description:"Click to add the ZenML MCP server to Cursor.",steps:["Click the 'Install via Link' button above","Cursor will prompt you to install the server"]},{title:"Manual Method (Docker)",type:"docker",bashCommand:`mkdir -p ~/.cursor && \\
if [ -f ~/.cursor/mcp.json ]; then \\
	cp ~/.cursor/mcp.json ~/.cursor/mcp.json.backup && \\
	jq '.mcpServers.zenml = {
	"command":"docker",
	"args":["run","-i","--rm",
			"-e","ZENML_STORE_URL=${e}",
			"-e","ZENML_STORE_API_KEY=${s}",${N(n)}
			"-e","LOGLEVEL=WARNING",
			"-e","NO_COLOR=1",
			"-e","ZENML_LOGGING_COLORS_DISABLED=true",
			"-e","ZENML_LOGGING_VERBOSITY=WARN",
			"-e","ZENML_ENABLE_RICH_TRACEBACK=false",
			"-e","PYTHONUNBUFFERED=1",
			"-e","PYTHONIOENCODING=UTF-8",
			"${l}"],
	"type":"stdio"
	}' ~/.cursor/mcp.json > ~/.cursor/mcp.json.tmp && \\
	mv ~/.cursor/mcp.json.tmp ~/.cursor/mcp.json; \\
else \\
	echo '{"mcpServers":{}}' | jq '.mcpServers.zenml = {
	"command":"docker",
	"args":["run","-i","--rm",
			"-e","ZENML_STORE_URL=${e}",
			"-e","ZENML_STORE_API_KEY=${s}",${N(n)}
			"-e","LOGLEVEL=WARNING",
			"-e","NO_COLOR=1",
			"-e","ZENML_LOGGING_COLORS_DISABLED=true",
			"-e","ZENML_LOGGING_VERBOSITY=WARN",
			"-e","ZENML_ENABLE_RICH_TRACEBACK=false",
			"-e","PYTHONUNBUFFERED=1",
			"-e","PYTHONIOENCODING=UTF-8",
			"${l}"],
	"type":"stdio"
	}' > ~/.cursor/mcp.json; \\
fi`,description:"Use this CLI command to install the ZenML MCP Server in Cursor.",steps:["Run the command in your terminal","The server will be added to `~/.cursor/mcp.json`"]},{title:"Manual Method (uv)",type:"uv",bashCommand:`mkdir -p ~/.cursor && \\
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
		"ZENML_STORE_API_KEY": "${s}"${E(n)}
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
		"ZENML_STORE_API_KEY": "${s}"${E(n)}
	}
	}' > ~/.cursor/mcp.json; \\
fi`,description:"Use this CLI command to install the ZenML MCP Server with uv in Cursor.",steps:["Clone the repository: `git clone --depth 1 --branch main https://github.com/zenml-io/mcp-zenml.git`","Ensure `uv` is installed globally","Update the command to point to your `uv` and repository paths","Run the command in your terminal"]}]},{name:"Claude Code",value:"claude-code",methods:[{title:"Manual Method (Docker)",type:"cli",bashCommand:`# Add for your current project (local scope)
claude mcp add zenml -- \\
	docker run -i --rm \\
	-e ZENML_STORE_URL=${e} \\
	-e ZENML_STORE_API_KEY=${s} \\${h(n)}
	-e LOGLEVEL=WARNING \\
	-e NO_COLOR=1 \\
	-e ZENML_LOGGING_COLORS_DISABLED=true \\
	-e ZENML_LOGGING_VERBOSITY=WARN \\
	-e ZENML_ENABLE_RICH_TRACEBACK=false \\
	-e PYTHONUNBUFFERED=1 \\
	-e PYTHONIOENCODING=UTF-8 \\
	${l}`,description:"Install the ZenML MCP Server using the Claude CLI.",steps:["Run the command in your terminal for local scope","For user-scoped installation, add `--scope user` flag after `zenml`"],note:"User scope: `claude mcp add zenml --scope user --` [rest of command]"},{title:"Manual Method (uv)",type:"cli",bashCommand:`# Add for your current project (local scope)
claude mcp add zenml \\
	--env LOGLEVEL=WARNING \\
	--env NO_COLOR=1 \\
	--env ZENML_LOGGING_COLORS_DISABLED=true \\
	--env ZENML_LOGGING_VERBOSITY=WARN \\
	--env ZENML_ENABLE_RICH_TRACEBACK=false \\
	--env PYTHONUNBUFFERED=1 \\
	--env PYTHONIOENCODING=UTF-8 \\
	--env ZENML_STORE_URL=${e} \\
	--env ZENML_STORE_API_KEY=${s} \\${L(n)}
	-- /usr/local/bin/uv run /path/to/mcp-zenml/server/zenml_server.py`,description:"Install the ZenML MCP Server with uv using the Claude CLI.",steps:["Clone the repository: `git clone --depth 1 --branch main https://github.com/zenml-io/mcp-zenml.git`","Ensure `uv` is installed globally","Update the command to point to your `uv` and repository paths","Run the command in your terminal","For user-scoped installation, add `--scope user` flag after `zenml`"]}],troubleshooting:"Use the `/mcp` command inside claude to check connection status and trigger reconnect if needed."},{name:"OpenAI Codex",value:"codex",methods:[{title:"Manual Method (Docker)",type:"cli",bashCommand:`codex mcp add zenml docker run -i --rm \\
	-e ZENML_STORE_URL=${e} \\
	-e ZENML_STORE_API_KEY=${s} \\${h(n)}
	-e LOGLEVEL=WARNING \\
	-e NO_COLOR=1 \\
	-e ZENML_LOGGING_COLORS_DISABLED=true \\
	-e ZENML_LOGGING_VERBOSITY=WARN \\
	-e ZENML_ENABLE_RICH_TRACEBACK=false \\
	-e PYTHONUNBUFFERED=1 \\
	-e PYTHONIOENCODING=UTF-8 \\
	${l}`,description:"Install the ZenML MCP Server using the Codex CLI.",steps:["Run the command in your terminal"]},{title:"Manual Method (uv)",type:"cli",bashCommand:`codex mcp add zenml /usr/local/bin/uv run path/to/mcp-zenml/server/zenml_server.py \\
	--env LOGLEVEL=WARNING \\
	--env NO_COLOR=1 \\
	--env ZENML_LOGGING_COLORS_DISABLED=true \\
	--env ZENML_LOGGING_VERBOSITY=WARN \\
	--env ZENML_ENABLE_RICH_TRACEBACK=false \\
	--env PYTHONUNBUFFERED=1 \\
	--env PYTHONIOENCODING=UTF-8 \\
	--env ZENML_STORE_URL=${e} \\
	--env ZENML_STORE_API_KEY=${s}${n?" \\":""}${n?L(n).replace(" \\",""):""}`,description:"Install the ZenML MCP Server with uv using the Codex CLI.",steps:["Clone the repository: `git clone --depth 1 --branch main https://github.com/zenml-io/mcp-zenml.git`","Ensure `uv` is installed globally","Update the command to point to your `uv` and repository paths","Run the command in your terminal"]}],troubleshooting:"Use the `/mcp` command inside codex to check connection status and trigger reconnect if needed."},{name:"Other Clients",value:"other",methods:[{title:"Docker Installation",type:"docker",config:o,description:"Use this JSON configuration for any MCP client that supports Docker-based servers.",steps:["Insert this configuration where your application requires MCP server registration","Update `ZENML_STORE_URL`, `ZENML_STORE_API_KEY`, and `ZENML_ACTIVE_PROJECT_ID` with your values"]},{title:"Non-Docker Installation (uv)",type:"uv",config:a,description:"Use this JSON configuration for any MCP client that supports local execution with `uv`.",steps:["Clone the repository: `git clone --depth 1 --branch main https://github.com/zenml-io/mcp-zenml.git`","Ensure `uv` is installed globally","Update the `command` and `args` paths to match your installation","Update `ZENML_STORE_URL`, `ZENML_STORE_API_KEY`, and `ZENML_ACTIVE_PROJECT_ID` with your values","Insert this configuration where your application requires MCP server registration"]}]}]}const J=new Set(["https:","http:","vscode:","cursor:"]);function q(e){if(!e)return!1;try{const s=new URL(e),r=s.protocol;return!(!J.has(r)||r==="cursor:"&&s.hostname!=="anysphere.cursor-deeplink")}catch{return!1}}function Q({method:e}){const s=e.type==="automatic"||e.type==="mcpb",r=e.type==="automatic"?"Install via Link":"Open Link",n=e.hasDeepLink&&e.deepLinkUrl&&q(e.deepLinkUrl);return t.jsx(U,{initialOpen:s,title:e.title,children:t.jsxs("div",{className:"space-y-4",children:[e.description&&t.jsx("p",{className:"text-text-sm text-theme-text-secondary",children:e.description}),n&&t.jsx(c,{asChild:!0,size:"md",emphasis:"bold",intent:"primary",className:"inline-flex",children:t.jsxs("a",{href:e.deepLinkUrl,target:"_blank",rel:"noopener noreferrer",children:[t.jsx(S,{className:"h-4 w-4 fill-current"}),r]})}),e.steps.length>0&&t.jsxs("div",{className:"space-y-2",children:[t.jsx("h5",{className:"text-text-sm font-medium",children:"Installation Steps:"}),t.jsx("div",{className:"space-y-2 text-text-sm",children:e.steps.map((o,a)=>t.jsxs("div",{className:"flex items-start gap-2",children:[t.jsx("span",{className:"rounded-full flex h-5 w-5 shrink-0 items-center justify-center bg-theme-surface-secondary text-text-xs font-medium",children:a+1}),t.jsx(T,{markdown:o,className:"text-theme-text-secondary"})]},a))})]}),e.config&&t.jsxs("div",{className:"space-y-2",children:[t.jsx("h5",{className:"text-text-sm font-medium",children:"Configuration:"}),t.jsx(p,{code:e.config,highlightCode:!0,language:"json",wrap:!0,fullWidth:!0})]}),e.bashCommand&&t.jsxs("div",{className:"space-y-2",children:[t.jsx("h5",{className:"text-text-sm font-medium",children:"Command:"}),t.jsx(p,{code:e.bashCommand,highlightCode:!0,language:"bash",wrap:!0,fullWidth:!0})]}),e.note&&t.jsx(C,{intent:"primary",children:t.jsx("p",{className:"text-text-sm",children:e.note})})]})})}function X({ide:e}){return t.jsxs("div",{className:"space-y-4",children:[t.jsxs("div",{className:"space-y-1",children:[t.jsxs("h3",{className:"text-text-md font-semibold",children:[e.name," Setup"]}),t.jsx("p",{className:"text-text-sm text-theme-text-secondary",children:"Choose an installation method below and follow the instructions."})]}),t.jsx("div",{className:"space-y-3",children:e.methods.map((s,r)=>t.jsx(Q,{method:s},`${e.value}-${s.type}-${r}`))}),e.troubleshooting&&t.jsx(C,{intent:"neutral",children:t.jsxs("div",{className:"space-y-1",children:[t.jsx("h4",{className:"text-text-sm font-semibold",children:"Troubleshooting"}),t.jsx("p",{className:"text-text-sm",children:e.troubleshooting})]})})]})}function ee({endpointUrl:e,token:s,projectId:r}){const n=m.useMemo(()=>W(e,s,r),[e,s,r]);return t.jsxs("div",{className:"space-y-6",children:[t.jsxs("div",{className:"flex flex-col gap-1",children:[t.jsxs("div",{className:"flex items-center gap-2",children:[t.jsx("h2",{className:"text-text-lg font-semibold",children:"Client Configuration"}),t.jsx("a",{href:"https://docs.zenml.io/user-guides/best-practices/mcp-chat-with-server",target:"_blank",rel:"noreferrer noopener",className:"text-text-sm text-primary-400 hover:text-primary-500",children:"Learn More"})]}),t.jsx("p",{className:"text-text-sm text-theme-text-secondary",children:"Choose your IDE or AI assistant and follow the installation instructions below."})]}),t.jsx("div",{className:"flex flex-col rounded-md border border-theme-border-moderate",children:t.jsxs(j,{defaultValue:"vscode",className:"w-full",children:[t.jsx(A,{className:"grid w-full grid-cols-6",children:n.map(o=>t.jsx(G,{value:o.value,className:"text-text-sm",children:o.name},o.value))}),n.map(o=>t.jsx(k,{value:o.value,className:"mt-0 border-0 p-5",children:t.jsx(X,{ide:o})},o.value))]})})]})}function te({onDismiss:e}){return t.jsxs("div",{className:"flex w-full items-center justify-between gap-2 rounded-md border border-success-300 bg-success-50 px-4 py-3 text-success-900",children:[t.jsxs("div",{className:"flex items-center gap-2",children:[t.jsx(_,{className:"size-5 shrink-0 fill-current"}),t.jsx("p",{className:"font-semibold",children:"Your configuration has been updated"}),t.jsx("p",{className:"text-text-sm",children:"Configuration links and code snippets now include your API key."})]}),t.jsx("button",{type:"button",onClick:e,"aria-label":"Dismiss notification",children:t.jsx(D,{className:"size-5 fill-current"})})]})}function Ee(){const[e,s]=m.useState(null),[r,n]=m.useState(!1),o=i=>{s(i),n(!!i)},a=window.location.origin;return t.jsxs(P,{className:"space-y-5 p-5",children:[t.jsxs("div",{className:"space-y-2",children:[t.jsx("h1",{className:"text-text-xl font-semibold",children:"MCP"}),t.jsx("p",{className:"text-text-sm text-theme-text-secondary",children:"Model Context Protocol settings for connecting IDEs and AI assistants to your ZenML Server."})]}),t.jsx(z,{token:e,onTokenChange:o}),r&&e?t.jsx(te,{onDismiss:()=>n(!1)}):null,t.jsx("div",{className:"border-t border-theme-border-moderate"}),t.jsx(ee,{endpointUrl:a,token:e||"your_api_key_here"})]})}export{Ee as default};
