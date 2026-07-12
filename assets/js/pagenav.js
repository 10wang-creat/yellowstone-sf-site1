/* 手機快速導覽：自動產生跳轉列、區塊收合、回頂端
   用法：在頁面設定 window.PAGENAV = { selector:'.tips-section', labelMax:6 }; 再引入本檔 */
(function(){
  var cfg = window.PAGENAV || {};
  if(!cfg.selector) return;
  var secs = Array.prototype.slice.call(document.querySelectorAll(cfg.selector));
  var bar = document.getElementById('pnBar');

  secs.forEach(function(sec, i){
    var head = sec.querySelector('h2, h3, h4');
    if(!head) return;

    // 找出 section 底下「包含標題」的直接子元素，收合時只留它
    var keep = head;
    while(keep.parentNode && keep.parentNode !== sec) keep = keep.parentNode;
    keep.setAttribute('data-pn-head','');

    if(!sec.id) sec.id = 'pn-' + i;
    sec.classList.add('pn-sec');
    if(cfg.collapse !== false) sec.classList.add('pn-collapsed');

    // 產生跳轉鈕（標籤取標題的中文片段）；cfg.noChips=true 時只收合、不自動產生鈕
    if(bar && !cfg.noChips){
      var raw = head.textContent.replace(/\s+/g,' ').trim();
      var mm = raw.match(/[㐀-鿿]{2,}/);
      var label = mm ? mm[0] : raw;
      var max = cfg.labelMax || 6;
      if(label.length > max) label = label.slice(0, max);
      var chip = document.createElement('a');
      chip.href = '#' + sec.id;
      chip.className = 'pn-chip';
      chip.textContent = label;
      chip.addEventListener('click', function(e){
        e.preventDefault();
        sec.classList.remove('pn-collapsed');
        sec.scrollIntoView({behavior:'smooth', block:'start'});
      });
      bar.appendChild(chip);
    }

    // 標題加箭頭 + 點擊收合
    head.insertAdjacentHTML('beforeend', '<span class="pn-arrow">▾</span>');
    keep.addEventListener('click', function(e){
      if(e.target.closest('a')) return; // 不攔截標題內的連結
      sec.classList.toggle('pn-collapsed');
    });
  });

  var ea = document.getElementById('pnExpand');
  var ca = document.getElementById('pnCollapse');
  if(ea) ea.addEventListener('click', function(){ secs.forEach(function(s){ s.classList.remove('pn-collapsed'); }); });
  if(ca) ca.addEventListener('click', function(){ secs.forEach(function(s){ s.classList.add('pn-collapsed'); }); window.scrollTo({top:0,behavior:'smooth'}); });

  var top = document.getElementById('pnTop');
  if(top){
    window.addEventListener('scroll', function(){ (window.scrollY > 400) ? top.classList.add('pn-show') : top.classList.remove('pn-show'); });
    top.addEventListener('click', function(){ window.scrollTo({top:0, behavior:'smooth'}); });
  }
})();
