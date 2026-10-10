const { chromium } = require('/workspace/tools/node_modules/playwright-core');
const http=require('http'),fs=require('fs'),path=require('path');
const root=require("path").resolve(__dirname,".."); const T={".html":"text/html",".css":"text/css",".js":"text/javascript",".webp":"image/webp",".jpg":"image/jpeg",".png":"image/png",".xml":"application/xml",".txt":"text/plain"};
const srv=http.createServer((q,r)=>{let f=path.join(root,decodeURIComponent(q.url.split('?')[0]));if(f.endsWith('/'))f+='index.html';if(!fs.existsSync(f)){f=root+'/404.html';}r.writeHead(200,{'content-type':T[path.extname(f)]||'application/octet-stream'});r.end(fs.readFileSync(f))}).listen(8798);
const axe=fs.readFileSync('/workspace/tools/node_modules/axe-core/axe.min.js','utf8');
let FAILS=[];
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
for(const [pg,vp] of [['/',{width:390,height:844}],['/',{width:768,height:1024}],['/',{width:1280,height:800}],['/',{width:1440,height:900}],['/missing',{width:390,height:844}]]){
 const ctx=await b.newContext({viewport:vp});const p=await ctx.newPage();let bytes=0,reqs=[];
 p.on('response',async r=>{try{const bb=await r.body();bytes+=bb.length;reqs.push([r.url().replace('http://127.0.0.1:8798',''),bb.length])}catch(e){}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
 await p.goto('http://127.0.0.1:8798'+pg,{waitUntil:'networkidle'});await p.waitForTimeout(500);
 const ov=await p.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth);
 const small=await p.evaluate(()=>[...document.querySelectorAll('a,button')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.height<24||r.width<24)}).map(e=>e.textContent.trim().slice(0,20)+':'+Math.round(e.getBoundingClientRect().width)+'x'+Math.round(e.getBoundingClientRect().height)));
 console.log(`== ${pg} ${vp.width}x${vp.height} overflowX=${ov} firstLoadBytes=${bytes} reqs=${reqs.length} errors=${JSON.stringify(errs)}`);
 if(vp.width===390&&pg==='/')console.log(' requests:',JSON.stringify(reqs));
 if(pg==='/missing'){const fb=await p.evaluate(()=>{const f=document.querySelector('footer');return f?Math.round(f.getBoundingClientRect().bottom):0});console.log(' 404 footer bottom',fb,'viewport',vp.height);if(fb<vp.height-1)FAILS.push('404 footer not at bottom');}
 if(small.length){console.log(' small targets:',JSON.stringify(small));FAILS.push('small targets '+vp.width+' '+pg);}
 if(ov>0)FAILS.push('overflow '+vp.width); if(errs.length)FAILS.push('console errors '+pg);
 if(vp.width===1280||pg==='/missing'){await p.addScriptTag({content:axe});const res=await p.evaluate(async()=>{const r=await axe.run(document,{runOnly:['wcag2a','wcag2aa','best-practice']});return r.violations.map(v=>({id:v.id,impact:v.impact,n:v.nodes.length,ex:v.nodes.slice(0,3).map(n=>n.target.join(' ')+' | '+(n.failureSummary||'').split('\n').slice(1,2).join(''))}))});console.log(' axe:',JSON.stringify(res,null,1)); if(res.length)FAILS.push('axe violations '+pg);}
 await ctx.close();}
// reduced motion
const ctx=await b.newContext({viewport:{width:1280,height:800},reducedMotion:'reduce'});const p=await ctx.newPage();await p.goto('http://127.0.0.1:8798/',{waitUntil:'networkidle'});
const anim=await p.evaluate(()=>[...document.querySelectorAll('*')].filter(e=>{const s=getComputedStyle(e);return s.animationName!=='none'&&s.animationName!==''}).map(e=>e.className+':'+getComputedStyle(e).animationName));
console.log('reduced-motion running animations:',JSON.stringify(anim)); if(anim.length)FAILS.push('animations under reduced motion');
await b.close();srv.close(); if(FAILS.length){console.log('AUDIT FAIL:',FAILS.join('; '));process.exit(1)} console.log('AUDIT PASS');})();
