document.addEventListener("DOMContentLoaded", () => {
  // Handle clicks on num1 buttons
  const num1Buttons = document.querySelectorAll(".num1Button");
  num1Buttons.forEach((button) => {
    button.addEventListener("click", () => handleNum1Click(button.dataset.num));
  });

  // Handle clicks on operation buttons
  const operationButtons = document.querySelectorAll(".operationButton");
  operationButtons.forEach((button) => {
    button.addEventListener("click", () =>
      handleOperationClick(button.dataset.op)
    );
  });

  // Handle clicks on num2 buttons
  const num2Buttons = document.querySelectorAll(".num2Button");
  num2Buttons.forEach((button) => {
    button.addEventListener("click", () => handleNum2Click(button.dataset.num));
  });

  // Handle click on reset button
  document.getElementById("reset").addEventListener("click", () => {
    location.reload(); // Reload page to reset everything
  });
});

let selectedNum1, selectedOperation;

function handleNum1Click(num1) {
  selectedNum1 = parseInt(num1); // Parse as integer
  updateCalculationDisplay(num1);
  document.getElementById("num1Buttons").classList.add("hidden");

  fetch(`/zero-pair?num1=${num1}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        alert(data.error); // Display error to user
      } else {
        console.log("Received servo angles:", data.servo_angles_num1);
        document.getElementById("operationButtons").classList.remove("hidden");
        disableInvalidNum2Buttons(num1); // Disable invalid num2 buttons
      }
    })
    .catch((error) => {
      console.error("Fetch error:", error);
      alert("An error occurred while fetching data.");
    });
}

function handleOperationClick(operation) {
  selectedOperation = operation;
  document.getElementById("operationButtons").classList.add("hidden");
  updateCalculationDisplay(selectedNum1 + " " + decodeURIComponent(operation));
  document.getElementById("num2Buttons").classList.remove("hidden");
  disableInvalidNum2Buttons(selectedNum1); // Disable invalid num2 buttons
}

function handleNum2Click(num2) {
  updateCalculationDisplay(
    `${selectedNum1} ${decodeURIComponent(selectedOperation)} ${num2}`
  );
  document.getElementById("num2Buttons").classList.add("hidden");

  fetch(
    `/zero-pair?num1=${selectedNum1}&num2=${num2}&operation=${selectedOperation}`
  )
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        alert(data.error); // Display error to user
      } else {
        console.log("Final Result:", data.result);
        document.getElementById("resetButton").classList.remove("hidden");
      }
    })
    .catch((error) => {
      console.error("Fetch error:", error);
      alert("An error occurred while fetching data.");
    });
}

function updateCalculationDisplay(text) {
  document.getElementById("calculationDisplay").innerText = text;
}

function disableInvalidNum2Buttons(num1) {
  const num2Buttons = document.querySelectorAll(".num2Button");
  num2Buttons.forEach((button) => {
    const buttonText = button.innerHTML.trim();
    if (!isNaN(buttonText)) {
      const num2 = parseInt(buttonText);

      // Calculate potential result based on the selected operation
      let potentialResult;
      if (decodeURIComponent(selectedOperation) === "+") {
        potentialResult = num1 + num2;
      } else if (selectedOperation === "-") {
        potentialResult = num1 - num2;
      } else {
        console.error("Invalid operation:", selectedOperation);
        return; // Exit the function if operation is not valid
      }

      console.log("Potential result:", potentialResult);

      if (potentialResult > 8 || potentialResult < -8) {
        button.disabled = true;
        console.log("Disabling button:", buttonText);
      } else {
        button.disabled = false;
        console.log("Enabling button:", buttonText);
      }
    } else {
      console.log("Ignoring non-numeric button:", buttonText);
    }
  });
}
