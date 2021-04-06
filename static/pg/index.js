var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})

document.getElementById("main-input").addEventListener("keydown", function (e) {
  if (e.key == "Tab") {
    e.preventDefault();
    var start = this.selectionStart;
    var end = this.selectionEnd;
    // set textarea value to: text before caret + tab + text after caret
    this.value =
      this.value.substring(0, start) + `\t` + this.value.substring(end);

    // put caret at right position again
    this.selectionStart = this.selectionEnd = start + 1;
  }
});


const api_url = 'http://localhost:5000';
const stdout_text = '/ts$ ';

const runCode = async () => {
  let code = document.getElementById('main-input').value;
  let res = await runInterpreter(code);

  let output_area = document.getElementById('output');

  if (res.success) {
    let result = res.int_result;
    
    if (result.exception) {
      let exception = result.exception;
      let line = '<p style="color: rgb(207, 62, 62);">Exception rasied: ' + exception + '</p>';
      output_area.innerHTML += line; 
    }
    else if (result.final_result === 'success') {
      // Code was valid and everything ran successfully
      
      let output = result.output;
      for (let i = 0; i <= output.length - 1; i++) {
        let line = '<p>' + stdout_text + output[i] + '</p>'
        output_area.innerHTML += line;
      }


    }
  } else {
    console.log('Something went wrong');
  }

}

const runInterpreter = async (code) => {
  const response = await fetch(api_url + '/api/runcode', {
    headers: {
      'Content-Type': 'application/json'
    },
    method: "POST",
    body: JSON.stringify({ 'code': code })
  });
  const json = await response.json();
  return json
}

const clearOutput = () => {
  let output = document.getElementById('output');
  output.innerHTML = '';
}