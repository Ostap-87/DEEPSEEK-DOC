import { spawn } from 'node:child_process';
import { pathToFileURL } from 'node:url';
import net from 'node:net';
import crypto from 'node:crypto';

const CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const port=9700+Math.floor(Math.random()*200);
const chrome=spawn(CHROME,['--headless=new','--no-sandbox','--disable-gpu','--disable-crash-reporter','--disable-breakpad','--crash-dumps-dir=/tmp/dshdumps','--user-data-dir=/tmp/dshprobe2','--window-size=680,1200',`--remote-debugging-port=${port}`,'about:blank'],{stdio:'ignore'});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let wsUrl;
for(let i=0;i<100;i++){try{const r=await fetch(`http://127.0.0.1:${port}/json/version`);const j=await r.json();if(j.webSocketDebuggerUrl){wsUrl=j.webSocketDebuggerUrl.replace('localhost','127.0.0.1');break;}}catch{}await sleep(120);}

// minimal ws
function connect(u){const {hostname,port:pt,pathname}=new URL(u);const key=crypto.randomBytes(16).toString('base64');
return new Promise((res,rej)=>{const s=net.connect(+pt,hostname,()=>{s.write(`GET ${pathname} HTTP/1.1\r\nHost: ${hostname}:${pt}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: ${key}\r\nSec-WebSocket-Version: 13\r\n\r\n`);});
let buf=Buffer.alloc(0),up=false;const hs={msg:[],close:[]};const api={send(o){const p=Buffer.from(JSON.stringify(o));const mask=crypto.randomBytes(4);let h;if(p.length<126){h=Buffer.alloc(2);h[1]=0x80|p.length}else{h=Buffer.alloc(4);h[1]=0x80|126;h.writeUInt16BE(p.length,2)}h[0]=0x81;const m=Buffer.from(p.map((b,i)=>b^mask[i%4]));s.write(Buffer.concat([h,mask,m]))},on(e,f){hs[e].push(f)}};
s.on('data',c=>{buf=Buffer.concat([buf,c]);if(!up){const i=buf.indexOf('\r\n\r\n');if(i<0)return;up=true;buf=buf.slice(i+4);res(api);}
for(;;){if(buf.length<2)return;const b1=buf[1];const op=buf[0]&0x0f;let len=b1&0x7f,off=2;if(len===126){if(buf.length<4)return;len=buf.readUInt16BE(2);off=4}else if(len===127){if(buf.length<10)return;len=Number(buf.readBigUInt64BE(2));off=10}if(buf.length<off+len)return;const d=buf.slice(off,off+len);buf=buf.slice(off+len);if(op===1)hs.msg.forEach(f=>f(d.toString('utf8')));else if(op===8){s.end();hs.close.forEach(f=>f())}}});});}

const ws=await connect(wsUrl);
let id=1;const pend=new Map();const ls=[];
ws.on('msg',t=>{const m=JSON.parse(t);if(m.id&&pend.has(m.id)){const{res,rej}=pend.get(m.id);pend.delete(m.id);m.error?rej(new Error(JSON.stringify(m.error))):res(m.result)}else if(m.method){ls.forEach(f=>f(m))}});
const send=(method,params={},sd)=>{const i=id++;const p={id:i,method,params};if(sd)p.sessionId=sd;ws.send(p);return new Promise((res,rej)=>pend.set(i,{res,rej}))};
const once=m=>new Promise(r=>{const l=x=>{if(x.method===m){ls.splice(ls.indexOf(l),1);r(x.params)}};ls.push(l)});
const {targetId}=await send('Target.createTarget',{url:'about:blank'});
const {sessionId}=await send('Target.attachToTarget',{targetId,flatten:true});
await send('Page.enable',{},sessionId);
await send('Emulation.setEmulatedMedia',{media:'print'},sessionId);
const loaded=once('Page.loadEventFired');
await send('Page.navigate',{url:pathToFileURL(process.argv[2]).href},sessionId);
await loaded; await sleep(400);
const r=await send('Runtime.evaluate',{expression:process.argv[3]||"document.body.scrollHeight",returnByValue:true},sessionId);
console.log(JSON.stringify(r.result.value,null,1));
ws.close&&ws.close(); chrome.kill('SIGKILL'); process.exit(0);
