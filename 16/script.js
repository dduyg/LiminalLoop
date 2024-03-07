function convertText(type) {
    let inputText = document.getElementById('inputText').value;
    let outputText = '';

    switch (type) {
        case 'uppercase':
            outputText = inputText.toUpperCase();
            break;
        case 'lowercase':
            outputText = inputText.toLowerCase();
            break;
        case 'propercase':
            outputText = inputText.toLowerCase().replace(/(^|\s)\S/g, function (char) {
                return char.toUpperCase();
            });
            break;
        case 'sentencecase':
            outputText = inputText.replace(/(^\w{1}|\.\s*\w{1})/gi, function (char) {
                return char.toUpperCase();
            });
            break;
        case 'camelcase':
            outputText = inputText.replace(/(?:^\w|[A-Z]|\b\w)/g, function (char, index) {
                return index === 0 ? char.toLowerCase() : char.toUpperCase();
            }).replace(/\s+/g, '');
            break;
        case 'snakecase':
            outputText = inputText.replace(/\s+/g, '_').toLowerCase();
            break;
        default:
            outputText = inputText;
    }

    document.getElementById('outputText').value = outputText;
}
