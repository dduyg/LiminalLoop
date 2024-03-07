function convertText(type) {
    let inputText = document.getElementById("inputText").value;
    let outputText = document.getElementById("outputText");
    switch (type) {
        case 'upper':
            outputText.value = inputText.toUpperCase();
            break;
        case 'lower':
            outputText.value = inputText.toLowerCase();
            break;
        case 'proper':
            outputText.value = inputText.toLowerCase().replace(/(^|\s)\S/g, function (char) {
                return char.toUpperCase();
            });
            break;
        case 'sentence':
            outputText.value = inputText.replace(/(^\w{1}|\.\s+\w{1})/g, function(char) {
                return char.toUpperCase();
            });
            break;
        case 'camel':
            outputText.value = inputText.replace(/\W+(.)/g, function(match, chr) {
                return chr.toUpperCase();
            });
            outputText.value = outputText.value.charAt(0).toLowerCase() + outputText.value.slice(1);
            break;
        case 'snake':
            outputText.value = inputText.toLowerCase().replace(/\s/g, '_');
            break;
        default:
            outputText.value = inputText;
            break;
    }
}
