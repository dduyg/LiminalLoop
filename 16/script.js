function convertToUpperCase() {
  const inputText = document.getElementById('inputText').value;
  const outputText = inputText.toUpperCase();
  document.getElementById('outputText').value = outputText;
}

function convertToLowerCase() {
  const inputText = document.getElementById('inputText').value;
  const outputText = inputText.toLowerCase();
  document.getElementById('outputText').value = outputText;
}

function convertToCamelCase() {
  const inputText = document.getElementById('inputText').value;
  const words = inputText.split(' ');
  const camelCaseText = words.map((word, index) => {
    if (index === 0) {
      return word.toLowerCase();
    }
    return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
  }).join('');
  document.getElementById('outputText').value = camelCaseText;
}

function convertToSnakeCase() {
  const inputText = document.getElementById('inputText').value;
  const snakeCaseText = inputText.toLowerCase().replace(/\s+/g, '_');
  document.getElementById('outputText').value = snakeCaseText;
}
