---
title: Making Music with MusicGen, Right in Your Browser
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

  /* Code cells. Observable's editor and its static code display both run on
     CodeMirror 6, which — unlike the CodeMirror 5 + dracula.css combo the
     original tutorial used — wraps everything in stable structural classes
     (.cm-editor / .cm-content / .cm-line) and tags tokens with .tok-* names
     from @codemirror/language's classHighlighter. Those are the real,
     non-hashed hooks to target, so the dark background + border live on the
     structural classes, and the dracula palette lives on the .tok-* tokens. */
  pre, .cm-editor, .cm-scroller {
    background: #282a36 !important;
    border: 5px solid var(--mm-pink-pale) !important;
    border-radius: 0 !important;
  }
  .cm-editor { padding: 14px !important; margin-top: -5px !important; overflow-x: auto; }
  .cm-content, .cm-line, pre code {
    color: #f8f8f2 !important;
    background: transparent !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 15px !important;
  }
  .cm-gutters { background: #282a36 !important; border: none !important; color: #6272a4 !important; }

  /* Dracula palette mapped onto CodeMirror 6's semantic tag classes. */
  .tok-keyword, .tok-operator, .tok-controlOperator, .tok-updateOperator,
  .tok-derefOperator, .tok-compareOperator, .tok-definitionOperator { color: #ff79c6 !important; }
  .tok-variableName, .tok-namespace { color: #50fa7b !important; }
  .tok-propertyName, .tok-attributeName, .tok-function { color: #8be9fd !important; }
  .tok-string, .tok-regexp, .tok-attributeValue { color: #f1fa8c !important; }
  .tok-atom, .tok-bool, .tok-number { color: #bd93f9 !important; }
  .tok-comment { color: #6272a4 !important; font-style: italic; }
  .tok-typeName, .tok-className, .tok-tagName { color: #ffb86c !important; }
  .tok-punctuation, .tok-bracket, .tok-angleBracket, .tok-meta { color: #f8f8f2 !important; }

  /* Same dracula palette again as a highlight.js fallback, in case any given
     block renders through that path instead of CM6 — harmless either way. */
  pre .hljs-comment, pre .hljs-quote { color: #6272a4 !important; font-style: italic; }
  pre .hljs-string, pre .hljs-doctag, pre .hljs-regexp { color: #f1fa8c !important; }
  pre .hljs-number, pre .hljs-literal { color: #bd93f9 !important; }
  pre .hljs-keyword, pre .hljs-operator, pre .hljs-punctuation { color: #ff79c6 !important; }
  pre .hljs-variable, pre .hljs-built_in, pre .hljs-title, pre .hljs-attr { color: #50fa7b !important; }
  pre .hljs-property, pre .hljs-attribute { color: #8be9fd !important; }
  pre .hljs-type, pre .hljs-class { color: #ffb86c !important; }
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
    background: #282a36;
    overflow-x: auto;
    margin-top: -5px;
    padding: 14px;
  }
  .mm-toc {
    list-style-type: none !important;
    margin: 0 !important;
    padding: 0 !important;
    border-left: 8px solid var(--mm-pink-pale) !important;
    padding-left: 14px !important;
    margin-top: 24px !important;
  }
  .mm-toc li { margin: 0 0 6px 0 !important; }
  .mm-toc li a { font-weight: normal; text-decoration: none; }
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

<h1>Making music with MusicGen, right in your browser</h1>

<p><a href="https://huggingface.co/facebook/musicgen-small">MusicGen</a> is Meta's text-to-music model — you type
a description, it hands you back an audio clip that (hopefully) sounds like what you asked for. The fun part is
that thanks to <a href="https://huggingface.co/docs/transformers.js/index">Transformers.js</a>, you can run the
whole thing directly in a browser tab. No API key, no backend, nothing leaves your machine.</p>

<p>Here's the shape of it: MusicGen doesn't work with notes or a score the way you might picture "AI music"
working. There's no MIDI, no piano roll under the hood. You give it a text prompt, it generates raw audio —
literally a waveform — token by token, the same basic way a language model generates text token by token, just
with audio tokens instead of words. That's the whole trick underneath everything below.</p>

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

```js echo
import { pipeline } from "npm:@huggingface/transformers";
```

<p>Heads up: the first time this runs, it's pulling down the MusicGen-small weights — quantized, but still around
300&nbsp;MB. That's the price of "runs entirely in the browser." It'll cache after that first load, so it's a
one-time tax per visitor.</p>

<h2 id="step1">Step 1: Set up the pipeline</h2>
<p>Almost everything in <code>@huggingface/transformers</code> boils down to a <code>pipeline</code> — tell it
what task you want and which checkpoint to use, and it hands you back a function you can just call. Here we're
using the <code>text-to-audio</code> task with <code>musicgen-small</code>, the lightest of the MusicGen
checkpoints (there's also a medium and large, if you've got the bandwidth and patience for them).</p>

```js echo
const generatorPromise = pipeline(
  "text-to-audio",
  "Xenova/musicgen-small",
  { dtype: "q8" } // quantized for browser bandwidth/memory
);
```

```js echo
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
<p>Mess with the prompt below, it's fun. <code>guidance_scale</code> controls how literally the model takes your
words — crank it up and it sticks close to what you typed, dial it down and it starts wandering off and doing its
own thing.</p>

```js echo
const prompt = view(
  Inputs.textarea({
    value: "lo-fi chillhop beat with vinyl crackle and a mellow piano loop",
    label: "Prompt",
    rows: 2,
    width: "100%"
  })
);
```

```js echo
const guidanceScale = view(
  Inputs.range([1, 5], { step: 0.5, value: 3, label: "Guidance scale" })
);
```

<div class="mm-controls">
  <button id="mm-generate-btn">Generate</button>
  <div class="mm-tag">~10–30s on CPU</div>
</div>

```js echo
const generateClicks = view(
  Inputs.button("Generate", { label: "Generate" })
);
```

```js echo
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

```js echo
audioResult
  ? html`<div class="mm-frame">${await audioBufferToPlayer(audioResult)}</div>`
  : html`<p><em>Load the model above, then hit Generate.</em></p>`
```

```js echo
// Turns { audio, sampling_rate } into a playable <audio> element.
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
<p>Since there's no note data to visualize, the natural thing to draw is the waveform itself — it's a nice, quick
way to see where a clip gets loud, quiet, or busy, and it makes the "this is real audio, not MIDI" point pretty
visually obvious.</p>

```js echo
const waveformCanvas = (() => {
  const canvas = document.createElement("canvas");
  canvas.width = 760;
  canvas.height = 140;
  return canvas;
})();
```

```js echo
{
  const ctx = waveformCanvas.getContext("2d");
  ctx.clearRect(0, 0, waveformCanvas.width, waveformCanvas.height);
  ctx.fillStyle = "#282a36";
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
<p>A quick cheat sheet for the settings that actually matter:</p>
<ul>
  <li><code>guidance_scale</code> — higher means the model sticks closer to your prompt; lower means it takes
    more creative liberties. Somewhere around 3 is a decent default; push it toward 4–5 if the output feels too
    loosely related to what you typed.</li>
  <li><code>max_new_tokens</code> — how long the clip is. MusicGen chews through roughly 50 tokens per second
    of audio, so 256 tokens ≈ 5 seconds. Want longer clips? Bump this up — just know generation time scales
    with it too.</li>
  <li><code>dtype</code> — how compressed the model weights are (<code>q8</code>, <code>q4</code>, <code>fp16</code>).
    Lighter dtypes mean a smaller download and faster inference, at some cost to audio fidelity. <code>q8</code>
    is a solid middle ground for a browser demo.</li>
</ul>

<hr>

<p>If you want to keep poking at this:</p>
<ul>
  <li>the <a href="https://huggingface.co/docs/transformers.js/index">Transformers.js docs</a></li>
  <li>the <a href="https://huggingface.co/spaces/Xenova/musicgen-web">MusicGen Web</a> demo this is based on</li>
  <li>the <a href="https://huggingface.co/models?library=transformers.js&pipeline_tag=text-to-audio">full list</a>
    of text-to-audio checkpoints Transformers.js supports, in case MusicGen-small isn't quite your sound</li>
</ul>
