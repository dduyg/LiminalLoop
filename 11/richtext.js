function convertText(caseType) {
    var inputText = document.getElementById("inputText").value;
    var outputText = document.getElementById("outputText");

    switch(caseType) {
        case 'uppercase':
            outputText.textContent = inputText.toUpperCase();
            break;
        case 'lowercase':
            outputText.textContent = inputText.toLowerCase();
            break;
        case 'titlecase':
            outputText.textContent = inputText.toLowerCase().replace(/(?:^|\s)\S/g, function(a) { return a.toUpperCase(); });
            break;
        case 'sentencecase':
            outputText.textContent = inputText.toLowerCase().replace(/(^\s*\w|[\.\!\?]\s*\w)/g,function(c){return c.toUpperCase()});
            break;
        case 'spacetohyphen':
            outputText.textContent = inputText.replace(/\s+/g, '-');
            break;
        case 'hyphentospace':
            outputText.textContent = inputText.replace(/-/g, ' ');
            break;
    }
}

function copyToClipboard() {
    var text = document.getElementById("outputText").textContent;
    navigator.clipboard.writeText(text).then(function() {
        alert("Text copied to clipboard!");
    }, function(err) {
        console.error('Error copying text: ', err);
    });
}
