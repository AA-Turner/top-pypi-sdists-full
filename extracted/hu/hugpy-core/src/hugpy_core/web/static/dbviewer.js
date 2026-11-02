
(() => {
 const $=id=>document.getElementById(id), api='/api/llm/db', state={source:null,sources:[],tables:[],table:null,schema:'public',offset:0,limit:50,columns:[],rows:[],hasMore:false,focusColumn:'',focusValue:''}, tableCache=new Map();
 let searchVersion=0;
 function searchable(value){return value!==null&&value!==undefined&&typeof value!=='object'&&String(value)!==''&&String(value).length<=200}
 function exactFields(value,needle,path='',out=[]){
  if(value&&typeof value==='object'){for(const [key,item] of Object.entries(value))exactFields(item,needle,path?`${path}.${key}`:key,out)}
  else if(value!==null&&value!==undefined){
   if(String(value)===needle)out.push(path);
   else if(typeof value==='string'&&/^[\[{]/.test(value.trim())){try{exactFields(JSON.parse(value),needle,path,out)}catch{}}
  }
  return out;
 }
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 async function get(path){const r=await fetch(api+path,{credentials:'same-origin'});const d=await r.json();if(!r.ok)throw Error(d.error||`HTTP ${r.status}`);return d}
 function query(obj){return '?'+new URLSearchParams(obj)}
 async function loadSources(){const d=await get('/sources');state.sources=d.sources||[];$('source').replaceChildren(...state.sources.map(s=>{const o=document.createElement('option');o.value=s.id;o.textContent=`${s.name} · ${s.package||s.engine}`;return o}));if(!state.sources.length)throw Error('No configured database sources.');const requested=new URLSearchParams(location.search).get('source');state.source=state.sources.some(s=>s.id===requested)?requested:state.sources[0].id;$('source').value=state.source;await loadTables()}
 async function tablesFor(source){if(tableCache.has(source))return tableCache.get(source);const d=await get('/tables'+query({source}));const ts=d.tables||[];tableCache.set(source,ts);return ts}
 async function loadTables(){state.source=$('source').value;state.table=null;state.offset=0;$('tables').textContent='Loading tables…';state.tables=await tablesFor(state.source);renderTables();const p=new URLSearchParams(location.search);if(p.get('table')&&state.tables.some(t=>t.name===p.get('table'))){state.focusColumn=p.get('column')||'';state.focusValue=p.get('value')||'';$('filter').value=state.focusValue;await chooseTable(p.get('table'),p.get('schema')||'public',true)}else if(state.tables.length)await chooseTable(state.tables[0].name,state.tables[0].schema||'public')}
 function renderTables(){const box=$('tables');box.replaceChildren();for(const t of state.tables){const b=document.createElement('button');b.textContent=`${t.name}${t.kind==='view'?' · view':''}`;b.title=`${t.schema||'main'}.${t.name}`;b.className=state.table===t.name?'active':'';b.onclick=()=>chooseTable(t.name,t.schema||'public');box.append(b)}}
 async function chooseTable(table,schema,keepFilter=false){state.table=table;state.schema=schema;state.offset=keepFilter?0:0;if(!keepFilter){state.focusColumn='';state.focusValue=''}renderTables();await loadRows()}
 async function loadRows(){if(!state.table)return;$('title').textContent=`${state.source} · ${state.schema}.${state.table}`;$('grid').className='notice';$('grid').textContent='Loading rows…';searchVersion++;$('matches').replaceChildren();try{const args={source:state.source,schema:state.schema,table:state.table,limit:state.limit,offset:state.offset};const q=$('filter').value.trim();if(q)args.q=q;if(state.focusColumn&&state.focusValue){args.column=state.focusColumn;args.q=state.focusValue}const d=await get('/rows'+query(args));state.columns=d.columns||[];state.rows=d.rows||[];state.hasMore=!!d.has_more;renderGrid();$('meta').textContent=`${state.rows.length} rows shown · offset ${state.offset}${q?' · filtered':''}`;$('page').textContent=`${Math.floor(state.offset/state.limit)+1} · ${state.limit} per page`;history.replaceState(null,'',`/dbviewer?${new URLSearchParams({source:state.source,table:state.table,schema:state.schema,...(state.focusColumn?{column:state.focusColumn,value:state.focusValue}:{})})}`)}catch(e){$('grid').className='notice error';$('grid').textContent=e.message}}
 function pointerButton(key,value){if(!searchable(value))return null;const b=document.createElement('button');b.className='pointer';b.textContent='↗ find matches';b.title=`Find exact matches for ${key}: ${String(value).slice(0,100)}`;b.onclick=()=>resolve(key,value);return b}
 function pointerEntries(value,out=[],path=''){if(Array.isArray(value)){value.forEach((v,i)=>pointerEntries(v,out,`${path}[${i}]`));return out}if(value&&typeof value==='object'){for(const [k,v] of Object.entries(value)){const p=path?`${path}.${k}`:k;if(searchable(v))out.push({key:k,value:v,path:p});pointerEntries(v,out,p)}}return out}
 function renderValue(parent,key,value){const wrap=document.createElement('div');wrap.className='cell';wrap.textContent=value===null?'NULL':(typeof value==='object'?JSON.stringify(value,null,2):String(value));const refs=pointerEntries(value);if(refs.length){const links=document.createElement('div');for(const ref of refs){const b=pointerButton(ref.key,ref.value);if(b){b.title=`${ref.path} → ${String(ref.value)}`;links.append(b)}}wrap.append(links)}else{const b=pointerButton(key,value);if(b)wrap.append(b)}parent.append(wrap)}
 function renderGrid(){const box=$('grid');box.className='';if(!state.rows.length){box.className='notice';box.textContent='No rows match.';return}const table=document.createElement('table'),head=document.createElement('thead'),hr=document.createElement('tr');for(const c of state.columns){const th=document.createElement('th');th.textContent=c.name+(c.primary_key?' 🔑':'');if(c.primary_key)th.className='pk';hr.append(th)}head.append(hr);table.append(head);const body=document.createElement('tbody');for(const row of state.rows){const tr=document.createElement('tr');for(const c of state.columns){const td=document.createElement('td');if(c.name===state.focusColumn&&String(row[c.name])===state.focusValue)td.className='highlight';renderValue(td,c.name,row[c.name]);tr.append(td)}body.append(tr)}table.append(body);box.replaceChildren(table);$('prev').disabled=state.offset===0;$('next').disabled=!state.hasMore}
 async function resolve(key,value){
  const version=++searchVersion, needle=String(value), box=$('matches');
  box.replaceChildren();
  const status=document.createElement('div');status.className='notice';box.append(status);
  let scanned=0, count=0;const failures=[];
  const update=()=>{status.textContent=`${count} matching row${count===1?'':'s'} · ${scanned}/${state.sources.length} sources searched · ${key} = ${needle.slice(0,160)}${failures.length?' · Unavailable: '+failures.join(', '):''}`};update();
  await Promise.allSettled(state.sources.map(async src=>{
   let cursor='';const seen=new Set();
   try{
    do{
     const d=await get('/search'+query({source:src.id,q:needle,...(cursor?{cursor}:{})}));
     if(version!==searchVersion)return;
     for(const hit of d.matches||[]){
      const fields=exactFields(hit.row,needle);if(!fields.length)continue;
      count++;
      const entry=document.createElement('div'), button=document.createElement('button'), preview=document.createElement('pre');
      button.textContent=`${src.name} · ${hit.schema||'main'}.${hit.table} · ${fields.join(', ')}`;
      button.title='Open this table filtered by the matching value';
      preview.textContent=JSON.stringify(hit.row,null,2);
      button.onclick=async()=>{try{
       $('source').value=src.id;state.source=src.id;state.tables=await tablesFor(src.id);
       state.focusColumn='';state.focusValue='';$('filter').value=needle;
       await chooseTable(hit.table,hit.schema||'main',true);
       $('grid').scrollIntoView({block:'start',behavior:'smooth'});
      }catch(e){showError(e)}};
      entry.append(button,preview);box.append(entry);
     }
     const next=d.next_cursor||'';
     if(next&&seen.has(next))throw Error('Search cursor did not advance');
     seen.add(next);cursor=next;update();
    }while(cursor);
   }catch(e){if(version===searchVersion)failures.push(`${src.name} (${e.message})`)}
   finally{if(version===searchVersion){scanned++;update()}}
  }));
 }
 $('source').onchange=()=>loadTables().catch(showError);$('apply').onclick=()=>{state.offset=0;loadRows()};$('filter').onkeydown=e=>{if(e.key==='Enter'){$('apply').click()}};$('prev').onclick=()=>{state.offset=Math.max(0,state.offset-state.limit);loadRows()};$('next').onclick=()=>{state.offset+=state.limit;loadRows()};function showError(e){$('grid').className='notice error';$('grid').textContent=e.message}
 loadSources().catch(showError);
})();

