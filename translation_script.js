const fs = require('fs');

const htmlContent = fs.readFileSync('index.html', 'utf8');

// We will inject the large translations object and update the HTML.
// But first, let's write out the translation dictionary!
console.log("Translation script prep done.");
