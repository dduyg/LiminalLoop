---
title: Machine Learning Maestro — Compose with Transformers.js
theme: [dashboard]
toc: false
---

```html
<style>
  :root {
    --mm-pink: #D33D8F;
    --mm-pink-pale: #F5DDEE;
    --mm-navy: #292A36;
    --mm-blue: #5671D0;
  }
  @font-face {
    font-family: 'Benton Sans';
    src: url('https://cdn.jsdelivr.net/gh/dduyg/LiminalLoop/fonts/benton-sans-regular.woff2') format('woff2');
    font-weight: normal;
    font-style: normal;
  }
  body, .observablehq {
    font-family: "Benton Sans", sans-serif;
    line-height: 1.5;
  }
  h1, h2, h3, h4, h5 {
    font-family: 'IBM Plex Mono', monospace;
  }
  h1 { color: var(--mm-pink); }
  h2, h3, h4 { margin-top: 32px; }
  hr {
    margin: 44px auto;
    width: 100px;
    height: 6px;
    background: var(--mm-pink);
    border: none;
    box-shadow: none;
  }
  p code, li code { color: var(--mm-blue); font-size: 18px; }
  a { color: black; font-weight: bold; display: inline-block; }
  .mm-controls {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    gap: 10px;
    margin-top: 12px;
  }
  .mm-controls button {
    -webkit-appearance: none;
    display: inline-block;
    padding: 6px 14px;
    font-size: 14px;
    text-transform: uppercase;
    cursor: pointer;
    background: white;
    color: var(--mm-navy);
    min-width: 100px;
    border: 4px solid var(--mm-pink-pale);
    font-weight: bold;
    letter-spacing: 1px;
    font-family: inherit;
  }
  .mm-controls button:disabled { opacity: 0.5; cursor: default; }
  .mm-tag {
    padding: 6px 14px;
    text-transform: uppercase;
    background: var(--mm-pink-pale);
    color: var(--mm-navy);
    border: 4px solid var(--mm-pink-pale);
    font-weight: bold;
    text-align: center;
    letter-spacing: 1px;
    font-size: 14px;
  }
  .mm-canvas-container, .mm-frame {
    border: 5px solid var(--mm-pink-pale) !important;
    overflow-x: auto;
    margin-top: -5px;
    padding: 14px;
  }
  .mm-toc { list-style-type: none; margin: 0; padding: 0; border-left: 8px solid var(--mm-pink-pale); padding-left: 14px; margin-top: 24px; }
  .mm-toc li a { font-weight: normal; text-decoration: none; margin-bottom: 4px; }
  textarea.mm-prompt {
    width: 100%;
    box-sizing: border-box;
    font-family: "IBM Plex Mono", monospace;
    font-size: 15px;
    padding: 14px;
    border: 5px solid var(--mm-pink-pale);
    resize: vertical;
  }
</style>
```

<h1>Making your browser make music (with Transformers.js)</h1>

<p>A while back the go-to for "AI music, but in a browser tab" was Magenta.js. It's basically retired now, so this
is the update: same tutorial, same vibe, but built around
<a href="https://huggingface.co/docs/transformers.js/index">Transformers.js</a> and
<a href="https://huggingface.co/facebook/musicgen-small">MusicGen</a> instead. Type a prompt, wait a bit, get a
little audio clip — all running on your machine, no API key, no server.</p>

<p>One thing to get used to if you're coming from Magenta: it's a different kind of "note."</p>
<ul>
  <li>Magenta dealt in <strong>symbolic</strong> music — a <code>NoteSequence</code> is just pitch-and-timing data,
    basically MIDI. Lightweight, and easy to draw as a piano roll.</li>
  <li>MusicGen deals in <strong>actual audio</strong> — you type a description, it spits out a waveform. No notes
    to inspect, so instead of a piano roll we're just drawing the waveform.</li>
</ul>

<h2>Table of contents</h2>
<ul class="mm-toc">
  <li><a href="#step0">Step 0: Loading the library</a></li>
  <li><a href="#step1">Step 1: A text-to-music pipeline</a></li>
  <li><a href="#step2">Step 2: Generating and playing audio</a></li>
  <li><a href="#step3">Step 3: Visualizing the waveform</a></li>
  <li><a href="#step4">Step 4: Tuning generation</a></li>
</ul>

<h2 id="step0">Step 0: Get the library in</h2>
<p>One of the nice things about Observable — you just <code>import</code> from npm, right inside a cell. No
fussing with <code>&lt;script&gt;</code> tags in a head element; it downloads, resolves, and everything downstream
just picks it up.</p>

```js
import { pipeline } from "npm:@huggingface/transformers";
```

<p>Heads up: the first time this runs, it's pulling down the MusicGen-small weights — quantized, but still around
300&nbsp;MB. That's the price of "runs entirely in the browser." It'll cache after that first load, so it's a
one-time tax per visitor.</p>

<h2 id="step1">Step 1: Set up the pipeline</h2>
<p>Almost everything in <code>@huggingface/transformers</code> boils down to a <code>pipeline</code> — tell it
what task you want and which checkpoint to use, and it hands you back a function you can just call. If you've used
Magenta before, this'll feel familiar: load a checkpoint, then ask it to do the thing.</p>

```js
const generatorPromise = pipeline(
  "text-to-audio",
  "Xenova/musicgen-small",
  { dtype: "q8" } // quantized for browser bandwidth/memory
);
```

```js
const generator = view(
  Inputs.button("Load model", {
    reduce: async () => {
      const gen = await generatorPromise;
      return gen;
    }
  })
);
```

<h2 id="step2">Step 2: Actually make some noise</h2>
<p>Mess with the prompt below, it's fun. <code>guidance_scale</code> is basically MusicGen's version of
Magenta's temperature knob — crank it up and the model sticks close to what you typed, dial it down and it starts
wandering off and doing its own thing.</p>

```js
const prompt = view(
  Inputs.textarea({
    value: "lo-fi chillhop beat with vinyl crackle and a mellow piano loop",
    label: "Prompt",
    rows: 2,
    width: "100%"
  })
);
```

```js
const guidanceScale = view(
  Inputs.range([1, 5], { step: 0.5, value: 3, label: "Guidance scale" })
);
```

<div class="mm-controls">
  <button id="mm-generate-btn">Generate</button>
  <div class="mm-tag">~10–30s on CPU</div>
</div>

```js
const generateClicks = view(
  Inputs.button("Generate", { label: "Generate" })
);
```

```js
const audioResult = (async () => {
  generateClicks; // re-run this cell whenever the button is clicked
  if (!generator) return null;
  const output = await generator(prompt, {
    guidance_scale: guidanceScale,
    max_new_tokens: 256 // keep clips short for a browser demo
  });
  return output; // { audio: Float32Array, sampling_rate: number }
})();
```

```js
audioResult
  ? html`<div class="mm-frame">${await audioBufferToPlayer(audioResult)}</div>`
  : html`<p><em>Load the model above, then hit Generate.</em></p>`
```

```js
// Turns { audio, sampling_rate } into a playable <audio> element,
// the MusicGen equivalent of Magenta's mm.Player.
async function audioBufferToPlayer({ audio, sampling_rate }) {
  const ctx = new OfflineAudioContext(1, audio.length, sampling_rate);
  const buffer = ctx.createBuffer(1, audio.length, sampling_rate);
  buffer.copyToChannel(audio, 0);

  const wavBlob = encodeWav(buffer);
  const url = URL.createObjectURL(wavBlob);
  const el = document.createElement("audio");
  el.controls = true;
  el.src = url;
  return el;
}

function encodeWav(buffer) {
  const numChannels = 1;
  const sampleRate = buffer.sampleRate;
  const samples = buffer.getChannelData(0);
  const bytesPerSample = 2;
  const blockAlign = numChannels * bytesPerSample;
  const dataSize = samples.length * bytesPerSample;
  const arr = new ArrayBuffer(44 + dataSize);
  const view = new DataView(arr);

  const writeStr = (offset, s) => { for (let i = 0; i < s.length; i++) view.setUint8(offset + i, s.charCodeAt(i)); };
  writeStr(0, "RIFF");
  view.setUint32(4, 36 + dataSize, true);
  writeStr(8, "WAVE");
  writeStr(12, "fmt ");
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, numChannels, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * blockAlign, true);
  view.setUint16(32, blockAlign, true);
  view.setUint16(34, 16, true);
  writeStr(36, "data");
  view.setUint32(40, dataSize, true);

  let offset = 44;
  for (let i = 0; i < samples.length; i++, offset += 2) {
    const s = Math.max(-1, Math.min(1, samples[i]));
    view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7fff, true);
  }
  return new Blob([arr], { type: "audio/wav" });
}
```

<h2 id="step3">Step 3: Give it something to look at</h2>
<p>Magenta had that piano roll that lit up note by note — nice touch, but it needs symbolic data we don't have
here. So instead we just draw the raw waveform. Same pink frame, same idea though: something to watch while you
listen.</p>

```js
const waveformCanvas = (() => {
  const canvas = document.createElement("canvas");
  canvas.width = 760;
  canvas.height = 140;
  return canvas;
})();
```

```js
{
  const ctx = waveformCanvas.getContext("2d");
  ctx.clearRect(0, 0, waveformCanvas.width, waveformCanvas.height);
  ctx.fillStyle = "#F5DDEE";
  ctx.fillRect(0, 0, waveformCanvas.width, waveformCanvas.height);

  if (audioResult) {
    const { audio } = audioResult;
    const step = Math.ceil(audio.length / waveformCanvas.width);
    const mid = waveformCanvas.height / 2;
    ctx.strokeStyle = "#D33D8F";
    ctx.lineWidth = 2;
    ctx.beginPath();
    for (let x = 0; x < waveformCanvas.width; x++) {
      const i = x * step;
      let min = 1, max = -1;
      for (let j = 0; j < step && i + j < audio.length; j++) {
        const v = audio[i + j];
        if (v < min) min = v;
        if (v > max) max = v;
      }
      ctx.moveTo(x, mid + min * mid);
      ctx.lineTo(x, mid + max * mid);
    }
    ctx.stroke();
  }
  invalidation.then(() => {}); // keep cell reactive on re-run
}
```

<div class="mm-canvas-container">${waveformCanvas}</div>

<h2 id="step4">Step 4: Knobs worth knowing</h2>
<p>Quick cheat sheet, Magenta-to-MusicGen translation:</p>
<ul>
  <li><code>guidance_scale</code> — think of it as temperature, flipped. Higher = sticks to your prompt.
    Lower = goes off and improvises.</li>
  <li><code>max_new_tokens</code> — how long the clip is. MusicGen chews through roughly 50 tokens per second
    of audio, so 256 tokens ≈ 5 seconds. Want it longer? Bump this up — just know it'll take longer to generate too.</li>
  <li><code>dtype</code> — how compressed the model weights are (<code>q8</code>, <code>q4</code>, <code>fp16</code>).
    Same trade-off as picking a smaller Magenta checkpoint: lighter download, faster inference, a bit less fidelity.</li>
</ul>

<hr>

<p>If you want to keep poking at this:</p>
<ul>
  <li>the <a href="https://huggingface.co/docs/transformers.js/index">Transformers.js docs</a></li>
  <li>the <a href="https://huggingface.co/spaces/Xenova/musicgen-web">MusicGen Web</a> demo this is based on</li>
  <li>the <a href="https://huggingface.co/models?library=transformers.js&pipeline_tag=text-to-audio">full list</a>
    of text-to-audio checkpoints Transformers.js supports, in case MusicGen-small isn't quite your sound</li>
</ul>
