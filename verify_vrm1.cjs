const { chromium } = require('playwright-core');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage();
  const errs=[]; p.on('console',m=>{if(m.type()==='error')errs.push(m.text());}); p.on('pageerror',e=>errs.push('PE: '+e.message));
  await p.goto('file:///root/vrm1-preview.html'); await p.waitForTimeout(500);
  for (const lang of ['fr','en','nl']) {
    await p.evaluate(l=>{document.body.setAttribute('data-active-lang',l);document.querySelectorAll('[data-lang]').forEach(e=>{e.style.display=e.getAttribute('data-lang')===l?'':'none';});},lang);
    await p.waitForTimeout(120);
    const leaks=await p.evaluate(l=>{let n=0;document.querySelectorAll('.module-body [data-lang]').forEach(e=>{if(e.getAttribute('data-lang')!==l&&e.offsetParent!==null)n++;});return n;},lang);
    console.log('leaks['+lang+']=',leaks);
  }
  const read=()=>p.evaluate(()=>({var:document.getElementById('vr-var').textContent,es:document.getElementById('vr-es').textContent,ratio:document.getElementById('vr-ratio').textContent,tail:document.getElementById('vr-tail').textContent,paths:document.getElementById('var-chart').querySelectorAll('path').length}));
  // defaults mu=-20 sig=30 X=99 -> VaR 49.79, ES 59.96
  console.log('defaults (mu-20 sig30 X99):', JSON.stringify(await read()), '(expect VaR 49.79, ES 59.96, tail 1.0%)');
  // X=97.5 (FRTB) 
  await p.evaluate(()=>{const e=document.getElementById('vr-x');e.value='97.5';e.dispatchEvent(new Event('input'));});
  await p.waitForTimeout(60);
  console.log('X=97.5:', JSON.stringify(await read()), '(expect VaR<49.79, ES>VaR, tail 2.5%)');
  const clean=errs.filter(e=>!/ERR_FILE_NOT_FOUND/.test(e));
  console.log('console errors:', clean.length, clean.slice(0,4));
  console.log('em-dash in body:', await p.evaluate(()=>document.querySelector('.module-body').innerText.includes('—')));
  await b.close();
})();
