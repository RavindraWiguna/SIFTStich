function squareNumber() {
    // Retrieve the user's input
    const numberInput = document.getElementById('numberInput').value;
  
    // Send the input to the server using fetch
    fetch('/square', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ number: numberInput }),
    })
      .then(response => response.json())
      .then(data => {
        // Update the result on the web page
        document.getElementById('result').innerText = `The square is: ${data.square}`;
      });
}


function test() {  
    // Send the input to the server using fetch
    fetch('/test', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 'something': 42 }),
    })
      .then(response => response.json())
      .then(data => {
        // Update the result on the web page
        let imgPlace = document.getElementById('result');
        imgPlace.innerHTML += `<img src="${data.src}" alt="">`
        

        // add button la
      });
}



  
  