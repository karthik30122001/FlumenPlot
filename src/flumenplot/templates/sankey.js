// ─── Constants injected by Python at build time ───────────────────────────
// In production these globals come from the inline <script> block in template.html:
//   const RAW_DATA_1      = {{DATA_1}};
//   const RAW_DATA_0_5    = {{DATA_0.5}};
//   const RAW_DATA_0_1    = {{DATA_0.1}};
//   const HIGHLIGHT_PATH  = {{PATH}};
//   const HIGHLIGHT_COLOR = "{{HIGH_COLOR}}";
//
// In dev.html they are hardcoded or fetched from dev_data.json.
// ──────────────────────────────────────────────────────────────────────────

const ranks = ["Kingdom", "Phylum", "Class", "Order", "Family", "Genus", "Species"];

// let chart = echarts.init(document.getElementById('chart'));
let currentNodeLimit = null;
let currentDepth = 2;
let currentData = "data_1";
let currentNode = "";
let currentPath = [];

// ─── Instance factory ──────────────────────────────────────────────────────
// Each chart canvas gets its own echarts instance + its own clicked-node
// state, but they share the controls above and can sync highlight state.
 
function createSankeyInstance(domId, dataSource) {
  return {
    domId,
    chart: null,
    data: dataSource,       // the full DATA object for this instance's sample
    currentNode: "",        // last clicked node name, drives ancestor highlight
  };
}
 
let instanceA = createSankeyInstance("chartA", DATA);
let instanceB = createSankeyInstance("chartB", DATA1);
 
const instances = [instanceA, instanceB];


// ─── Filtering ────────────────────────────────────────────────────────────

function filterByDepth(data, maxDepth) {
  const allowedRanks = new Set(ranks.slice(0, maxDepth + 1));
  const nodes = data.nodes.filter(n => allowedRanks.has(n.rank));
  const names = new Set(nodes.map(n => n.name));
  const links = data.links.filter(l => names.has(l.source) && names.has(l.target));
  return { nodes, links };
}

function filterByNodeLimit(data, maxNodes) {
  const keptNodes = [];
  for (const rank of ranks) {
    const rankNodes = data.nodes
      .filter(n => n.rank === rank)
      .sort((a, b) => b.value - a.value)
      .slice(0, maxNodes ?? Infinity);
    keptNodes.push(...rankNodes);
  }
  const names = new Set(keptNodes.map(n => n.name));
  const nodes = data.nodes.filter(n => names.has(n.name));
  const links = data.links;
  return { nodes, links };
}

// ─── Path / highlight helpers ─────────────────────────────────────────────

function getParents(nodeId, links, path = []) {
  const node = links
    .filter(l => l.target === nodeId)
    .map(l => l.source);
  path.push(nodeId);
  if (node.length === 0) {
    return path;
  } else {
    return getParents(node[0], links, path);
  }
}

// ─── Chart options ────────────────────────────────────────────────────────

function makeSankeyOptions(instance) {
  const data = instance.data[currentData]
  const truncatedData = filterByNodeLimit(data, currentNodeLimit);
  const filteredData  = filterByDepth(truncatedData, currentDepth);

  let customNodes = HIGHLIGHT_PATH.length > 0
    ? HIGHLIGHT_PATH
    : currentPath.filter(name => filteredData.nodes.some(n => n.name === name));

  let highlightNodes = new Set(customNodes);
  let highlightEdges = new Set(
    customNodes
      .map((node, i) =>
        i < customNodes.length - 1
          ? `${customNodes[i]}→${customNodes[i + 1]}`
          : null
      )
      .filter(Boolean)
  );

  const styledNodes = filteredData.nodes.map(n => {
    if (highlightNodes.has(n.name)) {
      return { ...n, itemStyle: { color: HIGHLIGHT_COLOR, opacity: 1 } };
    }
    return n;
  });

  const styledLinks = filteredData.links.map(l => {
    const key = `${l.source}→${l.target}`;
    if (highlightEdges.has(key)) {
      return { ...l, lineStyle: { color: HIGHLIGHT_COLOR, opacity: 0.65 } };
    }
    return { ...l, lineStyle: {} };
  });
  
  instance._filteredData = filteredData

  return {
    tooltip: {
      trigger: 'item',
      triggerOn: 'mousemove',
      formatter: function (params) {
        return `
          <b>${params.name}</b><br/>
          Relative abundance: ${params.data.percent.toPrecision(4)} %<br/>
          Rank: ${params.data.rank}
        `;
      }
    },
    series: [{
      type: 'sankey',
      nodeGap: 25,
      nodeAlign: 'left',
      layoutIterations: 0,
      emphasis: { focus: 'adjacency' },
      label: {
        show: true,
        silent: true,
        fontSize: 17,
        textBorderColor: 'transparent',
        lineHeight: 15,
        formatter: function (params) {
          const reads = typeof params.value === 'number'
            ? params.value.toPrecision(4)
            : 'NA';
          return `${params.data.label}\n${reads} %`;
        }
      },
      lineStyle: {
        curveness: 0.30,
        color: 'source'
      },
      data: styledNodes,
      links: styledLinks,
      levels: [
        { depth: 0, itemStyle: { color: '#aba4fe' }, lineStyle: { color: '#aba4fe', opacity: 0.6 } },
        { depth: 1, itemStyle: { color: '#b3cde3' }, lineStyle: { color: '#b3cde3', opacity: 0.6 } },
        { depth: 2, itemStyle: { color: '#abf4d3' }, lineStyle: { color: '#abf4d3', opacity: 0.6 } },
        { depth: 3, itemStyle: { color: '#abf4a3' }, lineStyle: { color: '#abf4a3', opacity: 0.6 } },
        { depth: 4, itemStyle: { color: '#94F38F' }, lineStyle: { color: '#94F28F', opacity: 0.6 } },
        { depth: 5, itemStyle: { color: '#8FCE00' }, lineStyle: { color: '#8FCE00', opacity: 0.6 } },
      ],
    }]
  };
}

// ─── Render ───────────────────────────────────────────────────────────────

function rerenderChart(instance) {
  const dom = document.getElementById(instance.domId);
 
  if (instance.chart) instance.chart.dispose();
  instance.chart = echarts.init(dom);
 
  instance.chart.on('click', { seriesType: 'sankey', dataType: 'node' }, (params) => {
    setClickedNode(instance, params.name);
  });
 
  instance.chart.on('contextmenu', { seriesType: 'sankey', dataType: 'node' }, (params) => {
    params.event.event.preventDefault();
    const path = getParents(params.name, instance._filteredData.links).reverse();
    navigator.clipboard.writeText(path.join("\n")).then(() => {
      showToast('Path copied to clipboard!');
    });
  });

  instance.chart.setOption(makeSankeyOptions(instance));
}

function rerenderAll() {
  instances.forEach(rerenderChart);
}


// ─── Cross-chart highlight sync ────────────────────────────────────────────
// makeSankeyOptions reads the global `currentNode`, so updating it once and
// re-rendering both instances is enough to sync the highlight across charts.
 
function setClickedNode(sourceInstance, nodeName) {
  currentNode = nodeName;
  currentPath = getParents(nodeName, sourceInstance._filteredData.links).reverse();
  instances.forEach(inst => {
    inst.chart.setOption(makeSankeyOptions(inst));
  });
}
 

// ─── Toast ────────────────────────────────────────────────────────────────

function showToast(message) {
  const toast = document.createElement('div');
  toast.innerText = message;
  toast.style.cssText = `
    position: fixed;
    bottom: 24px;
    left: 50%;
    transform: translateX(-50%);
    background: #333;
    color: white;
    padding: 10px 20px;
    border-radius: 8px;
    z-index: 9999;
    font-size: 14px;
    opacity: 1;
    transition: opacity 0.5s ease;
  `;
  document.body.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 500);
  }, 3000);
}

// ─── Controls ─────────────────────────────────────────────────────────────


function set1reads() {
  currentData = "data_1";
  rerenderAll();
  ['but1','but2','but3'].forEach(id => document.getElementById(id).style.backgroundColor = '');
  document.getElementById('but1').style.backgroundColor = '#d3d3d3';
}
 
function set05reads() {
  currentData = "data_0_5";
  rerenderAll();
  ['but1','but2','but3'].forEach(id => document.getElementById(id).style.backgroundColor = '');
  document.getElementById('but2').style.backgroundColor = '#d3d3d3';
}
 
function set01reads() {
  currentData = "data_0_1";
  rerenderAll();
  ['but1','but2','but3'].forEach(id => document.getElementById(id).style.backgroundColor = '');
  document.getElementById('but3').style.backgroundColor = '#d3d3d3';
}
 
function onDepthChange() {
  currentDepth = Number(document.getElementById("depthSelect").value);
  rerenderAll();
}
 
function onLimitChange() {
  const sliderVals = [1, 5, 10, 15, 20, 25, null];
  currentNodeLimit = sliderVals[document.getElementById("nodeLimit").value];
  document.getElementById("nodeLimitToolTip").textContent = currentNodeLimit ?? "Max";
  rerenderAll();
}
 
// ─── Init ─────────────────────────────────────────────────────────────────

rerenderAll()
