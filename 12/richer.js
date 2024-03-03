function convertCase(type) {
  var inputText = document.getElementById('inputText').value;
  var outputText = '';

  switch (type) {
    case 'uppercase':
      outputText = inputText.toUpperCase();
      break;
    case 'lowercase':
      outputText = inputText.toLowerCase();
      break;
    case 'titlecase':
      outputText = inputText.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
      break;
    case 'capitalizedcase':
      outputText = inputText.toLowerCase().replace(/^\w|\s\w/g, function(c) { return c.toUpperCase(); });
      break;
    case 'sentencecase':
      outputText = inputText.charAt(0).toUpperCase() + inputText.slice(1).toLowerCase();
      break;
    case 'spacehyphen':
      outputText = inputText.replace(/ /g, '-');
      break;
    case 'hyphenspace':
      outputText = inputText.replace(/-/g, ' ');
      break;
    case 'spaceunderscore':
      outputText = inputText.replace(/ /g, '_');
      break;
    case 'underscorespace':
      outputText = inputText.replace(/_/g, ' ');
      break;
    case 'camelcase':
      outputText = inputText.replace(/\W+(.)/g, function(match, chr) {
        return chr.toUpperCase();
      });
      outputText = outputText.charAt(0).toLowerCase() + outputText.slice(1);
      break;
    default:
      outputText = inputText;
  }

  document.getElementById('outputText').textContent = outputText;
}

function copyText() {
  var outputText = document.getElementById('outputText');
  var range = document.createRange();
  range.selectNode(outputText);
  window.getSelection().removeAllRanges();
  window.getSelection().addRange(range);
  document.execCommand('copy');
  window.getSelection().removeAllRanges();
  alert('Text copied to clipboard!');
}
