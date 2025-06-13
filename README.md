# <samp>LiminalLoop ⛃⛂</samp>

| <a href="https://dduyg.github.io/LiminalLoop/" target="_blank"><img width="21" height="21" src="https://img.icons8.com/?size=100&id=1713&format=png&color=C3BABA"/></a> | <a href="https://dduyg.github.io/LiminalLoop/05/" target="_blank"><img width="30" height="30" src="https://img.icons8.com/?size=100&id=35322&format=png&color=C4B0B2"/></a> | <a href="https://dduyg.github.io/LiminalLoop/07" target="_blank"><img width="30" height="30" src="https://img.icons8.com/?size=100&id=35326&format=png&color=C3BABA"/></a> |
|-------------------------------------------------|-------------------------------------------------|-------------------------------------------------|
| <a href="https://dduyg.github.io/LiminalLoop/08" target="_blank"><img width="30" height="30" src="https://img.icons8.com/?size=100&id=35328&format=png&color=C4B0B2"/></a> | <a href="https://dduyg.github.io/LiminalLoop/09" target="_blank"><img width="30" height="30" src="https://img.icons8.com/?size=100&id=35330&format=png&color=C3BABA"/></a> | <a href="https://dduyg.github.io/LiminalLoop/12" target="_blank"><img width="30" height="30" src="https://img.icons8.com/?size=100&id=35337&format=png&color=C3BABA"/></a> |

> internet__moods

```html
<i class="fas fa-circle"></i>
<i class="fas fa-square"></i>
<i class="fas fa-database"></i>
```

```html
<a href="../14/">➾</a>
<a href="../">▶</a>
```

<br>

<details>
<summary>&nbsp;<code>🪄 responsive font-size</code></summary>
<br>

> *To make the font size of your website responsive and look good on different screen sizes, you can adopt several strategies. The goal is to ensure text readability while adapting the size dynamically for different devices like mobile phones, tablets, and desktop monitors. Here are the key approaches to achieve this:*

## 1. Use Relative Units

Using relative units for font sizing, such as `em`, `rem`, or `vw`, allows the text to scale with the screen size, ensuring better responsiveness.

- **`rem` (Root Em)**: This is relative to the root element (`<html>`) font size. It's a stable choice for responsive typography.
- **`vw` (Viewport Width)**: This is relative to the viewport width. For example, `1vw` is 1% of the width of the viewport.

### Example CSS:

```css
html {
    font-size: 16px; /* Set the base font size for larger screens */
}

body {
    font-size: 1rem; /* The body text size will be 16px as 1rem = 16px */
    line-height: 1.6; /* Use a consistent line-height for readability */
}

@media (max-width: 1200px) {
    html {
        font-size: 15px; /* Slightly reduce font size on large tablets */
    }
}

@media (max-width: 768px) {
    html {
        font-size: 14px; /* Smaller font size for tablets */
    }
}

@media (max-width: 480px) {
    html {
        font-size: 13px; /* Adjust for smaller screens (mobile devices) */
    }
}
```

## 2. Fluid Typography (Using `vw`)

Another modern approach is using viewport-based units like `vw` to create **fluid typography**, meaning the text will scale according to the screen width.

### Example CSS:

```css
body {
    font-size: calc(1rem + 1vw); /* Combines a base size with a size relative to the viewport */
}
```

In this example, `calc(1rem + 1vw)` means that the font size will increase as the viewport width grows. The `1rem` ensures a base font size, and the `1vw` scales the text according to the viewport width.

## 3. Use Media Queries for Fine Control

For better control over typography across devices, use **media queries** to define specific font sizes for different screen widths.

### Example CSS with Media Queries:

```css
body {
    font-size: 1rem; /* Default for larger screens */
}

@media (max-width: 1200px) {
    body {
        font-size: 0.9rem; /* Slightly smaller for large tablets */
    }
}

@media (max-width: 768px) {
    body {
        font-size: 0.8rem; /* Smaller font for tablets */
    }
}

@media (max-width: 480px) {
    body {
        font-size: 0.75rem; /* Small font for mobile phones */
    }
}
```

## 4. Line Height and Letter Spacing

Maintaining good **line-height** and **letter-spacing** is important for readability. As you scale font sizes, ensure that line-height is appropriately set:

```css
body {
    line-height: 1.6; /* Ensures readability with proper spacing between lines */
    letter-spacing: 0.02em; /* Slightly adjusts the space between letters */
}
```

## 5. Consider Using CSS Clamp

The `clamp()` function allows you to set a dynamic font size with minimum and maximum limits:

```css
body {
    font-size: clamp(1rem, 2vw + 1rem, 2rem); /* Minimum 1rem, scales with viewport width, maximum 2rem */
}
```

This is a powerful approach because it combines fluid scaling with fixed boundaries, ensuring text doesn't become too small or too large.

<br><br>

<details>
<summary>&nbsp; <code>Common System Fonts</code> </summary>
<br>
  
```css
/* Sans-serif fonts */
font-family: "Arial", "Helvetica", sans-serif;
font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
font-family: "Verdana", Geneva, sans-serif;
font-family: "Tahoma", Geneva, sans-serif;
font-family: "Trebuchet MS", Helvetica, sans-serif;
font-family: "Arial Black", Gadget, sans-serif;
font-family: "Impact", Charcoal, sans-serif;
font-family: "Comic Sans MS", cursive, sans-serif;
font-family: "Arial Narrow", sans-serif;
font-family: "Century Gothic", sans-serif;
font-family: "Franklin Gothic Medium", "Arial Narrow", Arial, sans-serif;
font-family: "Optima", sans-serif;
```

```css
/* Serif fonts */
font-family: "Times New Roman", Times, serif;
font-family: "Times", Times New Roman, serif;
font-family: "Georgia", serif;
font-family: "Palatino Linotype", "Book Antiqua", Palatino, serif;
font-family: "Book Antiqua", Palatino, serif;
font-family: "Garamond", serif;
font-family: "Baskerville", "Baskerville Old Face", "Hoefler Text", Garamond, "Times New Roman", serif;
font-family: "Cambria", Georgia, serif;
font-family: "Didot", serif;
font-family: "Rockwell", serif;
```

```css
/* Monospace fonts */
font-family: "Courier New", Courier, monospace;
font-family: "Courier", monospace;
font-family: "Lucida Console", Monaco, monospace;
font-family: "Monaco", monospace;
font-family: "Consolas", monospace;
font-family: "Menlo", monospace;
font-family: "Liberation Mono", monospace;
font-family: "Andale Mono", monospace;
font-family: "PT Mono", monospace;
/* ★★ */ font-family: "Roboto Mono", monospace;
font-family: "Source Code Pro", monospace;
font-family: "Inconsolata", monospace;
font-family: "IBM Plex Mono", monospace;
font-family: "Fira Mono", monospace;
```

</details>

<hr>
</details>

<details>
<summary>&nbsp;<code>🌆 .md <i>buttons</i></code></summary>

# Key Binding Buttons
*You can use the* `<kbd>` *tag.*

<br>

### Link Outside
*The whole button is clickable, but doesn't have any color.*

[<kbd> <br> Title <br> </kbd>][Link]

<br>

```markdown
[<kbd> <br> Title <br> </kbd>][Link]
```

```markdown
[Link]: # 'Link with example title.'
```
 
<br>

### Link Inside

*The button text is link colored, but only the text is clickable.*

<kbd> <br> [Title][Link] <br> </kbd>

<br>

```markdown
<kbd> <br> [Title][Link] <br> </kbd>
```

```markdown
[Link]: # 'Link with example title.'
```

<br>


<!---------------------------------------------------------------------------->

[Link]: #

# Shield Buttons
*You can use **Badges** as buttons.*

[![Button Click]][Link] 
[![Button Hover]][Link] 

<br>

```markdown
[![Button Example]][Link]
```

```markdown
<!----------------------------------------------------------------------------->
```

```markdown
[Link]: # 'Link with example title.'
```

```markdown
<!---------------------------------[ Buttons ]--------------------------------->
```

```markdown
[Button Example]: https://img.shields.io/badge/Title-37a779?style=for-the-badge
```

<br>

### Icons
*You can also use icons to indicate intent.*

[![Button Icon]][Link] 

<br>

```markdown
[![Button Icon]][Link]
```

```markdown
<!----------------------------------------------------------------------------->
```

```markdown
[Link]: # 'Link with example title.'
```

```markdown
<!---------------------------------[ Buttons ]--------------------------------->
```

```markdown
[Button Icon]: https://img.shields.io/badge/Installation-EF2D5E?style=for-the-badge&logoColor=white&logo=Files
```

<br>
<br>


<!---------------------------------------------------------------------------->

[Button Hover]: https://img.shields.io/badge/Hover_Over_Me!-37a779?style=for-the-badge
[Button Click]: https://img.shields.io/badge/Click_Me!-37a779?style=for-the-badge
[Button Icon]: https://img.shields.io/badge/Installation-EF2D5E?style=for-the-badge&logoColor=white&logo=Files

[Link]: # 'Link with example title.'

<hr>
</details>

<details>
<summary>&nbsp;<code>🎴🏀 .js <i>comments</i></code></summary>

# JavaScript comments

```jsx
// =========================
//      Topic Introduction
// =========================
```


```jsx
/*******************************
          Topic Introduction
*******************************/
```

```javascript
// ---------------------------------------- \\
 //      Anchor Hover Effects for Body Copy    \\
// -------------------------------------------- \\
```

```jsx
/**********************************************
 *                                            *
 *              Topic Introduction            *
 *                                            *
 **********************************************/
```

```jsx
/* 
   _________ infoDropdown _________ 
  |                                | 
  |   here text text text text ''  | 
  |   here text text text text ''  | 
  |   here text text text text ''  | 
  |                                | 
  |                                | 
  |   here text text text text ''  |
  |   here text text text text ''  | 
  |                                | 
  |________________________________|
*/
```


```jsx
// Topic Introduction
// ------------------
```


```jsx
///////////////////////////////////////////////////////
////// Title-related Code
///////////////////////////////////////////////////////
```

```jsx
// ••••• Title-related Code •••••
```

```jsx
// >>> Title-related Code <<<
```

```jsx
// ====================================
// Title-related Code
// ====================================
```

```jsx
/*
 * ~~~ Title-related Code ~~~
 */
```

```jsx
// ------------ Title-related Code ------------
```

```jsx
/****************************************
 *           Title-related Code
 ****************************************/
```

```jsx
// ************** Input Handling **************
```

```jsx
// ============== Configuration ==============
```

```jsx
// ~~~~~~~~~~~~~~ Utility Functions ~~~~~~~~~~~~~~
```

```jsx
// ///////////////// Constants /////////////////
```

```jsx
// ^^^^^^^^^^^^^^ Data Structures ^^^^^^^^^^^^^^
```

```jsx
// ```````````````` Testing ````````````````
```

```jsx
// :::::::::::::::: Database Operations ::::::::::::::::
```

```jsx
// ------------------------
// Section: Animation Logic
// ------------------------
```

```jsx
// ******************************
// Section: User Interaction Logic
// ******************************
```

```jsx
/*
  +--------------------------+
  | Section: Rendering Logic |
  +--------------------------+
*/
```

```jsx
// ------------------------------
// Section: Event Handling Logic
// ------------------------------
```

```jsx
/******************************************************************
 ** Parameters for controlling various aspects of the simulation ~~
 ** ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ~~
 */
// Fill color for points; currently set to black
let pointFillColor = 0;
/******************************************************************/
```

</details>

<details>
<summary>&nbsp;<code>🧱 terminal colorPalettes</code></summary>
<br>
<img src="https://raw.githubusercontent.com/dduyg/LiminalLoop/refs/heads/main/01/vscode-example.png" width="250">
<img src="https://raw.githubusercontent.com/dduyg/LiminalLoop/refs/heads/main/01/vim-example.png" width="250">
<img src="https://raw.githubusercontent.com/dduyg/LiminalLoop/refs/heads/main/01/specimen_2.png" width="250">
<img src="https://raw.githubusercontent.com/dduyg/LiminalLoop/refs/heads/main/01/emacs-example.png" width="250">
<img src="https://raw.githubusercontent.com/dduyg/LiminalLoop/refs/heads/main/01/helix-example.png" width="250">
<img src="https://raw.githubusercontent.com/dduyg/LiminalLoop/refs/heads/main/01/color01combi.jpeg" width="250">
<img src="https://raw.githubusercontent.com/dduyg/LiminalLoop/refs/heads/main/01/color02combi.jpg" width="250">
<img src="https://raw.githubusercontent.com/dduyg/LiminalLoop/refs/heads/main/01/colorcombi03-comicmono.jpg" width="250">   
</details>

<details>
<summary>&nbsp;<code>🌐 jsDelivr CDN with GitHub</code></summary>
<br>

jsDelivr allows you to serve *any static file* from a *public GitHub repository*—fast, free, and reliable. This is useful for:
- Web projects
- Hosting assets (scripts, styles, media)
- Sharing static content without backend setup

## 🔧 jsDelivr GitHub URL Format
```
https://cdn.jsdelivr.net/gh/<username>/<repo>@<branch-or-commit>/<path/to/file>
```

- `@<branch>` (like `@main`) is optional; it defaults to the default branch.
- `@<commit>` is recommended for production use to avoid surprises when files change.

## ✅ Usage Examples

### 🟨 JavaScript File
GitHub Path:
```
https://github.com/user/my-repo/blob/main/js/main.js
```

jsDelivr URL:
```
https://cdn.jsdelivr.net/gh/user/my-repo/js/main.js
```

**Use in HTML:**
```html
<script src="https://cdn.jsdelivr.net/gh/user/my-repo/js/main.js"></script>
```

### 🟦 CSS File
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/user/my-repo/css/style.css">
```

### 🟪 Font File (`woff2`, `ttf`)
```css
@font-face {
  font-family: 'MyFont';
  src: url('https://cdn.jsdelivr.net/gh/user/my-repo/fonts/my-font.woff2') format('woff2');
  font-weight: normal;
  font-style: normal;
}
```

### 🟥 Image (`.png`, `.jpg`, `.svg`)

```html
<img src="https://cdn.jsdelivr.net/gh/user/my-repo/images/logo.png" alt="Logo">
```

### 🟩 Video File (`.mp4`)
```html
<video controls>
  <source src="https://cdn.jsdelivr.net/gh/user/my-repo/videos/demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>
```

### 🟫 JSON File
```
fetch("https://cdn.jsdelivr.net/gh/user/my-repo/data/config.json")
  .then(res => res.json())
  .then(data => console.log(data));
```

## 📌 Pinning to a Commit (Best Practice)
To prevent breaking changes when files are updated, pin the file to a **specific commit**.

1. Go to the GitHub file.
2. Click the file → click the "Copy permalink" (with commit hash).
3. Replace `main` with the commit hash:

**Example:**
```
https://cdn.jsdelivr.net/gh/user/my-repo@a1b2c3d4/js/main.js
```

## 💡 Tips
- Files must be in **public** repositories.
- Use the `gh/` prefix for GitHub; there's also support for `npm` and `WordPress`.
- jsDelivr automatically uses the best CDN node worldwide for fast delivery.
- 🧠 Works for all public files including SVG, MP3, ZIP, JSON, etc.

## 🔗 Real Example from Your Case

**GitHub File:**
```
https://raw.githubusercontent.com/dduyg/LiminalLoop/main/06/kemalizm.mp4
```

**jsDelivr URL:**
```
https://cdn.jsdelivr.net/gh/dduyg/LiminalLoop/06/kemalizm.mp4
```

**Usage:**
```html
<video controls>
  <source src="https://cdn.jsdelivr.net/gh/dduyg/LiminalLoop/06/kemalizm.mp4" type="video/mp4">
</video>
```

## 🧪 Test Your Links
To verify a jsDelivr link:

- Open it in the browser.
- Check DevTools → Network to confirm it's loading via CDN.

</details>
