// mywebscript.js
let RunSentimentAnalysis = ()=>{
    let textToAnalyze = document.getElementById("textToAnalyze").value;
    let xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        if (this.readyState !== 4) return;

        const display = document.getElementById("system_response");

        display.innerText = xhttp.responseText;

        if (this.status !== 200) { display.style.color = "red"}

    };
    xhttp.open("GET", "sentimentAnalyzer?textToAnalyze"+"="+textToAnalyze, true);
    xhttp.send();
}
