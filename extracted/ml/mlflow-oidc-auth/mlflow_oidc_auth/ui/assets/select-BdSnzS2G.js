import{i as e,o as t,r as n}from"./button-DJ30HgDO.js";e();var r=t(n(),1);const i=({label:e,error:t,options:n,className:i=``,containerClassName:a=``,id:o,ref:s,reserveErrorSpace:c=!1,...l})=>{let u=t||(c?`\xA0`:null);return(0,r.jsxs)(`div`,{className:a,children:[e&&(0,r.jsxs)(`label`,{htmlFor:o,className:`block text-sm font-medium text-text-primary dark:text-text-primary-dark mb-1`,children:[e,l.required&&`*`]}),(0,r.jsx)(`select`,{ref:s,id:o,className:`w-full px-3 py-2 border rounded-md focus:outline-none
            text-ui-text dark:text-ui-text-dark
            bg-ui-bg dark:bg-ui-bg-dark
            border-ui-border dark:border-ui-border-dark
            focus:border-btn-primary dark:focus:border-btn-primary-dark
            transition duration-150 ease-in-out cursor-pointer
            disabled:opacity-70 disabled:cursor-not-allowed
            custom-select
            ${t?`border-red-500 focus:border-red-500 dark:border-red-500 dark:focus:border-red-500`:``}
            ${i}`,...l,children:n.map(e=>{let t=typeof e==`string`?e:e.label,n=typeof e==`string`?e:e.value;return(0,r.jsx)(`option`,{value:n,children:t},n)})}),u&&(0,r.jsx)(`p`,{className:`mt-1 text-sm ${t?`text-red-500`:`invisible`}`,children:u})]})};i.displayName=`Select`;export{i as t};